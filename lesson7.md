Homework (OOP): Система рассылки писем
🎯 Цель

Спроектировать и реализовать объектно-ориентированную систему рассылки писем.
Покрыть все функции из изначального ДЗ за счёт методов и утилитных классов.
Письмо должно менять статус из Status при вызове send().

Часть A. Модель, утилиты и валидация
1) Статусы письма (Enum)

Перечислите статусы, которыми может обладать письмо в процессе обработки/отправки.

from enum import StrEnum

class Status(StrEnum):
    DRAFT   = "draft"    # создано, но ещё не готово к отправке
    READY   = "ready"    # нормализовано и валидно; можно отправлять
    SENT    = "sent"     # отправлено успешно
    FAILED  = "failed"   # попытка отправки завершилась ошибкой
    INVALID = "invalid"  # письмо/адреса не прошли валидацию

2) Модель письма
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class Email:
    sender: str
    recipient: str
    subject: str
    body: str

    # вычисляемые/служебные поля:
    date: Optional[str] = None
    masked_sender: Optional[str] = None
    short_body: Optional[str] = None
    sent_text: Optional[str] = None
    status: Status = field(default=Status.DRAFT)

    # --- Методы «вместо функций» из версии на функциях ---

    def clean_body_text(self) -> "Email":
        """Заменяет табы/переводы строки на пробелы; возвращает self."""
        self.body = TextUtils.clean_body_text(self.body)
        return self

    def add_send_date(self) -> "Email":
        """Добавляет текущую дату YYYY-MM-DD; возвращает self."""
        self.date = date.today().isoformat()
        return self

    def add_short_body(self, n: int = 10) -> "Email":
        """Сохраняет короткую версию body в self.short_body; возвращает self."""
        self.short_body = f"{self.body[:n]}..." if len(self.body) > n else self.body
        return self

    def build_sent_text(self) -> "Email":
        """Формирует итоговый текст письма (как в изначальном ДЗ) в self.sent_text; возвращает self."""
        clean_body = TextUtils.clean_body_text(self.short_body or self.body)
        self.sent_text = (
            f"Кому: {self.recipient}, от {self.sender}\n"
            f"Тема: {self.subject}, дата {self.date}\n"
            f"{clean_body}"
        )
        return self

    def mask_sender(self) -> "Email":
        """Заполняет masked_sender на основе sender."""
        login, domain = AddressUtils.extract_login_domain(self.sender)
        self.masked_sender = AddressUtils.mask_sender_email(login, domain)
        return self

    def is_empty_fields(self) -> tuple[bool, bool]:
        """(is_subject_empty, is_body_empty)."""
        return (not self.subject.strip(), not self.body.strip())

    # --- Методы по заданию ---

    def repl(self, message: str) -> "Email":
        """
        Создаёт «ответ» (reply) на текущее письмо:
        меняем местами отправителя/получателя, добавляем 'Re: ' к теме, тело = message.
        Статус нового письма: DRAFT.
        """
        return Email(
            sender=self.recipient,
            recipient=self.sender,
            subject=f"Re: {self.subject}",
            body=message,
            status=Status.DRAFT,
        )

    def prepare(self) -> "Email":
        """
        Полная подготовка письма: нормализация адресов, очистка subject/body,
        короткое тело, дата. Если есть пустые поля/некорректные адреса — статус INVALID.
        """
        # нормализация адресов
        norm = AddressUtils.normalize_addresses({"sender": self.sender, "recipient": self.recipient})
        self.sender, self.recipient = norm["sender"], norm["recipient"]

        # валидация
        if not (EmailValidator.is_valid(self.sender) and EmailValidator.is_valid(self.recipient)):
            self.status = Status.INVALID
            return self

        # пустота темы/тела
        subj_empty, body_empty = self.is_empty_fields()
        if subj_empty or body_empty:
            self.status = Status.INVALID
            return self

        # очистка/дата/короткое/маска/текст
        self.subject = TextUtils.clean_body_text(self.subject)
        self.clean_body_text().add_send_date().add_short_body().mask_sender().build_sent_text()
        self.status = Status.READY
        return self

    def send(self) -> "Email":
        """
        Отправка письма. Если статус не READY — помечаем FAILED.
        При успехе — статус SENT.
        """
        if self.status is not Status.READY:
            self.status = Status.FAILED
            return self
        # тут могла бы быть реальная интеграция SMTP/HTTP
        self.status = Status.SENT
        return self

3) Текстовые утилиты (clean_body_text и др.)
class TextUtils:
    @staticmethod
    def clean_body_text(body: str) -> str:
        """Заменяет табы и переводы строк на пробелы и нормализует пробелы по краям."""
        return body.replace("\t", " ").replace("\n", " ").strip()

4) Работа с адресами (normalize, extract, mask)
class AddressUtils:
    @staticmethod
    def normalize_addresses(email: dict) -> dict:
        """
        Приводит sender/recipient к нижнему регистру и обрезает пробелы по краям.
        Возвращает НОВЫЙ dict {'sender': ..., 'recipient': ...}.
        """
        return {
            "sender": (email.get("sender") or "").strip().lower(),
            "recipient": (email.get("recipient") or "").strip().lower(),
        }

    @staticmethod
    def extract_login_domain(address: str) -> tuple[str, str]:
        """
        'user@mail.ru' -> ('user', 'mail.ru'); примитивная разбивка.
        """
        address = (address or "").strip()
        if "@" not in address:
            return ("", "")
        login, domain = address.split("@", 1)
        return login, domain

    @staticmethod
    def mask_sender_email(login: str, domain: str) -> str:
        """
        Маска email: первые 2 символа логина + '***@' + домен.
        """
        head = (login or "")[:2]
        return f"{head}***@{domain}"

5) Валидация адресов (is_valid, get_correct_email)
class EmailValidator:
    ALLOWED_SUFFIXES = (".com", ".ru", ".net")

    @staticmethod
    def is_valid(address: str) -> bool:
        """
        Адрес корректен, если содержит '@' и оканчивается на .com/.ru/.net (регистр не важен).
        """
        if not isinstance(address, str):
            return False
        addr = address.strip()
        if "@" not in addr or not addr:
            return False
        low = addr.lower()
        return low.endswith(EmailValidator.ALLOWED_SUFFIXES)

    @staticmethod
    def get_correct_email(email_list: list[str]) -> list[str]:
        """Возвращает список корректных email (нормализованных)."""
        res: list[str] = []
        for raw in email_list:
            addr = (raw or "").strip().lower()
            if EmailValidator.is_valid(addr):
                res.append(addr)
        return res


Тестовые данные для проверки get_correct_email:

test_emails = [
    "user@gmail.com",
    "admin@company.ru",
    "test_123@service.net",
    "Example.User@domain.com",
    "default@study.com",
    " hello@corp.ru  ",
    "user@site.NET",
    "user@domain.coM",
    "user.name@domain.ru",
    "usergmail.com",
    "user@domain",
    "user@domain.org",
    "@mail.ru",
    "name@.com",
    "name@domain.comm",
    "",
    "   ",
]

6) Фабрика писем
class EmailFactory:
    @staticmethod
    def create_email(sender: str, recipient: str, subject: str, body: str) -> Email:
        """
        Создаёт Email-модель с базовыми полями; статус DRAFT.
        """
        return Email(sender=sender, recipient=recipient, subject=subject, body=body)

Часть B. Сервис отправки

Создайте сервис, который повторяет логику прежней функции sender_email(...), но в ООП-стиле.

class EmailService:
    DEFAULT_SENDER = "default@study.com"

    def sender_email(
        self,
        recipient_list: list[str],
        subject: str,
        message: str,
        *,
        sender: str = DEFAULT_SENDER,
    ) -> list[Email]:
        """
        Возвращает список готовых Email (с заполненными полями и статусами).
        Порядок действий строго соответствует исходному ДЗ, но на классах.
        """
        # 1. список получателей не пуст
        if not recipient_list:
            return []

        # 2. валидируем отправителя и получателей
        sender_norm = AddressUtils.normalize_addresses({"sender": sender, "recipient": ""})["sender"]
        if not EmailValidator.is_valid(sender_norm):
            return []  # неверный отправитель

        recipients_norm = [AddressUtils.normalize_addresses({"sender": "", "recipient": r})["recipient"]
                           for r in recipient_list]
        recipients_ok = EmailValidator.get_correct_email(recipients_norm)
        if not recipients_ok:
            return []

        # 3. проверка пустоты темы/тела (до создания множества писем)
        subj_empty = not (subject or "").strip()
        body_empty = not (message or "").strip()
        if subj_empty or body_empty:
            return []

        # 4. исключить отправку самому себе
        recipients_ok = [r for r in recipients_ok if r != sender_norm]
        if not recipients_ok:
            return []

        # 5. нормализация контента
        subject_clean = TextUtils.clean_body_text(subject)
        message_clean = TextUtils.clean_body_text(message)

        # 6-11. создаём, готовим, маскируем, формируем текст, отправляем
        out: list[Email] = []
        for to in recipients_ok:
            mail = (
                EmailFactory.create_email(sender_norm, to, subject_clean, message_clean)
                .prepare()             # -> READY/INVALID
            )
            if mail.status is Status.READY:
                mail.send()           # -> SENT
            out.append(mail)
        return out

Часть C. Примеры использования
# 1) Простая отправка
svc = EmailService()
result = svc.sender_email(
    recipient_list=[" admin@company.ru ", "default@study.com"],  # второй удалится (сам себе)
    subject="Hello!",
    message="Привет,\nколлега!\tРады видеть.",
    sender="DEFAULT@STUDY.com",
)

for e in result:
    print(e.status, e.sent_text)
    # Пример ожидаемого:
    # Status.SENT Кому: admin@company.ru, от default@study.com
    # Тема: Hello!, дата 2025-11-07
    # Привет, коллега! Рады видеть.

# 2) Ответ (repl)
first = result[0]
reply = first.repl("Спасибо, принято!").prepare().send()
print("REPLY:", reply.status, reply.sent_text)

Чек-лист соответствия исходным функциям

normalize_addresses → AddressUtils.normalize_addresses()

add_short_body → Email.add_short_body()

clean_body_text → TextUtils.clean_body_text()

build_sent_text → Email.build_sent_text()

check_empty_fields → Email.is_empty_fields()

mask_sender_email → AddressUtils.mask_sender_email()

get_correct_email → EmailValidator.get_correct_email() (+ is_valid)

create_email → EmailFactory.create_email()

add_send_date → Email.add_send_date()

extract_login_domain → AddressUtils.extract_login_domain()

sender_email(...) → EmailService.sender_email(...)

Новое: Email.repl() и Email.send() с изменением status (Status Enum)

🎒 Результат/Вывод

Выведите готовый список писем в виде:

for e in result:
    print(f"""
Кому: {e.recipient}, от {e.sender}
Тема: {e.subject}, дата {e.date}
{e.short_body or e.body}
    """.strip())




# Homework (OOP): Система рассылки писем

**Цель**
Спроектировать и реализовать объектно-ориентированную систему рассылки писем.

## Статусы письма (Enum)
Перечислите статусы, которыми может обладать письмо в процессе обработки/отправки с помощью StrEnum

    DRAFT = "draft"
    READY = "ready"
    SENT = "sent"
    FAILED = "failed"
    INVALID = "invalid"

## Модель EmailAdress
Класс инкапсулирует строковый email и операции над ним.
-   Приватное поле `_address: str`.
-   Конструктор сохраняет только корректные адреса.  Если адрес невалидный — выбрасывает ValueError..
    
-   Свойства:
    -   `value -> str` — возвращает нормализованный адрес.
    -   `masked -> str` — маска вида `первые_2_символа + "***@" + домен`.
        
-   Методы:
    
    -   `normalize_addresses() -> None` — приводит к `lower().strip()`. Применяется к самому объекту.
    -   `mask_email() -> str` — возвращает маску адреса (используйте `extract_login_domain()` из утилит).
    -   `check_correct_email() -> bool` — адрес корректен, если содержит `@` и оканчивается на `.com/.ru/.net`.

> Инкапсуляция: прямой записи `address` нет; изменяйте через методы.

## Функция очистки текста

``` python     
    def clean_text(text: str) -> str:
        """Заменяет \\t и \\n на пробелы, лишние пробелы обрезает."""
```

 
## Модель Email
**Модель письма**
Создать dataclass Email, c полями: 

    sender
    subject
    body
    date
    masked_sender
    short_body
    status
    
**Методы письма**

-   `clean_data(self) -> "Email"` — использует функцию clean_body_text и возвращает Email с очищенными `body` и `subject`
-   `add_send_date(self) -> "Email"` — добавляет Email текущую дату в формате `YYYY-MM-DD`.
-   `add_short_body(self, n) -> "Email"` — в `short_body` записывает первые `n` символов + `...` (если длиннее), n должно иметь дефолтное значение в 10 символов 
-   `is_empty_fields(self) -> bool` — проверяет заполнено ли поля subject и body, если хотя бы одно из них пустое, устанавливает статус INVALID и возвращает True.
- Описать `__repr__` для красивого текстового вывода письма. Если masked_sender заполнен — использовать его, иначе sender.value. Если short_body заполнен — использовать его, иначе body.
		
     Status: {status}
     Кому: {masked to}, от {masked from} 
     Тема: {subject}, дата {date} 
     {short_clean_body} ] 

**Добавьте метод, который создаёт «ответ» (reply) на текущее письмо**
Метод `reply(message: str) -> "Email"`:
-   меняет местами `sender` ⇄ `recipient`;
-   добавляет префикс `Re:` к теме;
-   тело = `message`;
-   статус DRAFT

**Добавьте метод, который подготавливает письмо для отправки:** - нормализует данные, проверяет заполнены ли данные  и меняет статус письма на READY
`prepare(self) -> "Email"`
-    eсли любой email невалиден → status = INVALID → return self
-   eсли subject/body после очистки пустые → status = INVALID → return self
Иначе:
  - add_send_date
  - add_short_body
  - masked_sender
  - собрать sent_text (через repr)
  - status = READY
 
## Сервис отправки EmailService

Реализуйте сервис, повторяющий логику прежней функции `sender_email(...)`, но в ООП-стиле, с методами: 
-   `send_email(self, email: Email, recipient) -> Email` — если `status=READY`, меняет на `SENT`, иначе на `FAILED`
-   `send_to_many(self, email: Email, recipient_list: list[str], subject: str, message: str, *, sender: str = "default@study.com") -> list[Email]` — создаёт и отправляет письма всем валидным значением из списка (если `status=READY`, меняет на `SENT`, иначе на `FAILED`)
	- если recipient_list пуст → вернуть []
	- нормализовать и проверить sender → если невалиден → вернуть []
	- из списка recipient_list исключить:
	    - невалидные адреса
	    - адрес отправителя (чтобы не отправлять самому себе)
	- если после фильтрации список пуст → вернуть []


**Метод, который подготавливает письмо для отправки**
Полная подготовка письма: нормализация адресов, очистка subject/body, короткое тело, добавления даты отправки. Если есть пустые поля/некорректные адреса — статус письма INVALID.
Метод `prepare() -> "Email"`:
  

**Пример ожидаемого результата по каждому письму **

    Status: SENT 
    Кому: admin@company.ru, от default@study.com
    Тема: Hello!, дата 2025-11-07
    Привет, коллега! Рады видеть.

  
### Дополнительное задание:
Создайте класс LoggingEmailService, который наследуется от EmailService,
и переопределяет метод send_email так, чтобы он:
- вызывал родительский send_email
- записывал информацию об отправке в файл `send.log`