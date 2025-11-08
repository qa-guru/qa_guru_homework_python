from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from typing import Optional, List, Tuple


# =========================
# 1) Статусы письма (Enum)
# =========================
class Status(StrEnum):
    DRAFT   = "draft"
    READY   = "ready"
    SENT    = "sent"
    FAILED  = "failed"
    INVALID = "invalid"


# =========================
# 2) Вспомогательные функции
# =========================
def clean_text(text: str) -> str:
    """Заменяет \t и \n на пробелы, лишние пробелы обрезает."""
    return (text or "").replace("\t", " ").replace("\n", " ").strip()

def mask_sender_email(login: str, domain: str) -> str:
    """Первые 2 символа логина + '***@' + домен."""
    return f"{(login or '')[:2]}***@{domain}" if domain else "***"


# =========================================
# 3) Модель EmailAddress с инкапсуляцией
# =========================================
class EmailAddress:
    """Инкапсулирует адрес и операции над ним. Хранит только корректные адреса."""
    ALLOWED_SUFFIXES = (".com", ".ru", ".net")

    def __init__(self, address: str):
        normalized = self._normalize(address)
        self._address: str = normalized  # приватное поле
        # Валидация: храним только корректный адрес
        if not self.check_correct_email():
            raise ValueError(f"Invalid email: {address!r}")

    # --- свойства ---
    @property
    def value(self) -> str:
        """Нормализованный адрес (read-only)."""
        return self._address

    @property
    def masked(self) -> str:
        """Маскированный вид адреса."""
        login, domain = self.extract_login_domain()
        return mask_sender_email(login, domain)

    def __str__(self) -> str:
        return self._address

    # --- публичные методы ---
    def normalize_addresses(self) -> None:
        """
        Приводит адрес к lower().strip().
        (В конструкторе уже нормализуется, метод оставлен для совместимости с требованиями.)
        """
        self._address = self._normalize(self._address)

    def mask_email(self) -> str:
        """Возвращает маску адреса (не меняет состояние)."""
        return self.masked

    def check_correct_email(self) -> bool:
        """Корректен, если содержит '@' и оканчивается на .com/.ru/.net (регистр не важен)."""
        a = self._address
        return "@" in a and a.endswith(self.ALLOWED_SUFFIXES)

    # --- приватные помощники ---
    @staticmethod
    def _normalize(addr: str) -> str:
        return (addr or "").strip().lower()

    def extract_login_domain(self) -> Tuple[str, str]:
        """'user@mail.ru' -> ('user', 'mail.ru'), при отсутствии '@' -> ('','')."""
        addr = self._address.strip().lower()
        if "@" not in addr:
            return "", ""
        return addr.split("@", 1)[0], addr.split("@", 1)[1]


# ============================
# 4) Модель Email (dataclass)
# ============================
@dataclass
class Email:
    sender: EmailAddress
    recipient: EmailAddress
    subject: str
    body: str

    date: Optional[str] = None
    masked_sender: Optional[str] = None
    short_body: Optional[str] = None
    sent_text: Optional[str] = None
    status: Status = field(default=Status.DRAFT)

    # --- Методы письма ---
    def clean_data(self) -> "Email":
        """Очищает subject/body через clean_text; возвращает self."""
        self.subject = clean_text(self.subject)
        self.body = clean_text(self.body)
        return self

    def add_send_date(self) -> "Email":
        """Добавляет текущую дату YYYY-MM-DD; возвращает self."""
        self.date = date.today().isoformat()
        return self

    def add_short_body(self, n: int = 10) -> "Email":
        """Сохраняет короткую версию body в self.short_body; возвращает self."""
        self.short_body = (self.body[:n] + "...") if len(self.body) > n else self.body
        return self

    def is_empty_fields(self) -> bool:
        """
        Проверяет, что subject и body НЕ пустые.
        Если пустые — ставит статус INVALID и возвращает True (пусто).
        """
        empty = (self.subject.strip() == "" or self.body.strip() == "")
        if empty:
            self.status = Status.INVALID
        return empty

    def __repr__(self) -> str:
        """Красивый вывод письма (masked для отправителя, если есть)."""
        masked_from = self.masked_sender or self.sender.masked
        short = clean_text(self.short_body or self.body)
        return (
            f"Status: {self.status}\n"
            f"Кому: {self.recipient.value}, от {masked_from}\n"
            f"Тема: {self.subject}, дата {self.date}\n"
            f"{short}"
        )

    # --- Создание ответа ---
    def reply(self, message: str) -> "Email":
        """Меняет местами sender/recipient, префикс 'Re:', тело=message, статус=DRAFT."""
        return Email(
            sender=self.recipient,
            recipient=self.sender,
            subject=f"Re: {self.subject}",
            body=message,
            status=Status.DRAFT,
        )

    # --- Подготовка письма к отправке ---
    def prepare(self) -> "Email":
        """
        Полная подготовка:
        - нормализует адреса (lower+strip);
        - валидирует email;
        - проверяет subject/body на пустоту;
        - чистит subject/body;
        - проставляет дату, short_body, masked_sender;
        - собирает sent_text;
        - меняет статус на READY (или INVALID при ошибке).
        """
        # нормализация адресов
        self.sender.normalize_addresses()
        self.recipient.normalize_addresses()

        # валидация адресов (после нормализации)
        if not (self.sender.check_correct_email() and self.recipient.check_correct_email()):
            self.status = Status.INVALID
            return self

        # очистка текстов
        self.clean_data()

        # проверка пустоты
        if self.is_empty_fields():
            return self  # статус уже INVALID

        # дата, короткое тело
        self.add_send_date()
        self.add_short_body()

        # маска отправителя
        login, domain = self.sender.extract_login_domain()
        self.masked_sender = mask_sender_email(login, domain)

        # финальный текст
        self.sent_text = self.__repr__()

        # готово к отправке
        self.status = Status.READY
        return self


# ============================
# 5) Сервис отправки писем
# ============================
class EmailService:
    DEFAULT_SENDER = "default@study.com"

    def send_email(self, email: Email, recipient: Optional[str] = None) -> Email:
        """
        Отправляет письмо одному получателю.
        Если status=READY — SENT, иначе FAILED.
        Параметр recipient оставлен для совместимости сигнатуры (можно не использовать).
        """
        email.status = Status.SENT if email.status is Status.READY else Status.FAILED
        print(email)
        return email

    def send_to_many(
        self,
        email: Email,
        recipient_list: List[str],
        subject: str,
        message: str,
        *,
        sender: str = DEFAULT_SENDER,
    ) -> List[Email]:
        """
        Создаёт и отправляет письма всем валидным адресатам из списка:
        - проверяет, что список не пуст;
        - нормализует и валидирует sender/recipients;
        - исключает отправку самому себе (цикл for);
        - нормализует subject/body через clean_text;
        - для каждого получателя создаёт Email, prepare() и send_email();
        - возвращает список писем (SENT/FAILED/INVALID).
        """
        out: List[Email] = []

        # 1) список получателей не пуст
        if not recipient_list:
            return out

        # 2) валидируем отправителя (EmailAddress бросит ошибку при невалидном)
        try:
            sender_addr = EmailAddress(sender)
        except ValueError:
            return out

        # нормализуем получателей и оставляем только валидные
        normalized_recipients: List[str] = []
        for raw in recipient_list:
            try:
                ea = EmailAddress(raw)
                normalized_recipients.append(ea.value)
            except ValueError:
                # пропускаем невалидные адреса
                continue

        if not normalized_recipients:
            return out

        # 3) проверка пустоты темы/тела (нормализуем текст заранее)
        subject_clean = clean_text(subject)
        message_clean = clean_text(message)
        if subject_clean == "" or message_clean == "":
            return out

        # 4) исключить отправку самому себе (цикл for)
        filtered: List[str] = []
        for r in normalized_recipients:
            if r != sender_addr.value:
                filtered.append(r)
        if not filtered:
            return out

        # 5) создаём/готовим/отправляем
        for to in filtered:
            # новый Email на основе входных данных (не мутируем входной email)
            try:
                em = Email(
                    sender=EmailAddress(sender_addr.value),
                    recipient=EmailAddress(to),
                    subject=subject_clean,
                    body=message_clean,
                    status=Status.DRAFT,
                )
            except ValueError:
                # если вдруг на этом шаге получатель стал невалиден — пропустим
                continue

            em.prepare()           # -> READY/INVALID
            self.send_email(em)    # -> SENT/FAILED
            out.append(em)

        return out


