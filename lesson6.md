# Homework: Система рассылки писем
---

## Часть A. Функции

Создайте набор функций для обработки информации о письме из HW4.
Каждая функция должна выполнять ровно одно действие и возвращать результат.
Аргументы и возвращаемые значения должны быть понятны по названию функции.

* Нормализация email адресов

``` python 
def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, в котором адрес приведен к нижнему регистру и очищен от пробелов по краям.
    """
``` 

* Сокращенная версия тела письма

``` python 
def add_short_body(email: dict) -> dict:
    """
    Возвращает email с новым ключом email["short_body"] — 
    первые 10 символов тела письма + "...".
    """
```

* Очистка текста письма

``` python 
def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
``` 

* Формирование итогового текста письма

``` python
def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {to}, от {from}
    Тема: {subject}, дата {date}
    {clean_body}
    """
```

* Проверка пустоты темы и тела

``` python
def check_empty_fields(subject: str, body:str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
``` 

* Маска email отправителя

``` python
def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
```

* Создать функцию которая проверит корректности email адресов. Адрес считается корректным, если:


- содержит символ @;
- оканчивается на один из доменов: .com, .ru, .net.

``` python
def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    """
```

Список emails для проверки работы функции

``` python
test_emails = [
    # Корректные адреса
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
```

* Создание словаря письма

``` python 
def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает словарь email с базовыми полями:
    'sender', 'recipient', 'subject', 'body'
    """
```

* Добавление даты отправки

``` 
from datetime import date

def add_send_date(email: dict) -> dict:
    """
    Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD.
    """
``` 

* Получение логина и домена

``` 
def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен отправителя.
    Пример: "user@mail.ru" -> ("user", "mail.ru")
    """
``` 

## Часть B. Отправка письма

Создать функцию отправки письма с базовой валидацией адресов и логикой выбора отправителя `recipient`

``` python
def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:
    pass
```

### 📝 Требования к функции

Функция `sender_email` принимает 3 позиционных аргумента `recipient_list` — emails получателя, `subject` — заголовок
письма, `message` — текст письма и
один обязательно именованный `sender="default@study.com"`.

```python
def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:
    pass
```

Внутри функции реализовать строго в указанном порядке:

- Проверить, что recipient_list не пустой.
- Проверить корректность email отправителя и получателей через get_correct_email().
- Проверить пустоту темы и тела письма через check_empty_fields().
  Если одно из них пустое — вернуть пустой список.
- Исключить отправку самому себе: пройти по каждому элементу recipient_list в цикле for,
  если адрес совпадает с sender, удалить его из списка.
- Нормализовать:
  subject и body → с помощью clean_body_text()
  recipient_list и sender → с помощью normalize_addresses()
- Создать письмо для каждого получателя функцией create_email().
- Добавить дату отправки с помощью add_send_date().
- Замаскировать email отправителя с помощью extract_login_domain() и mask_sender_email().
- Сохранить короткую версию в email["short_body"].
- Сформировать итоговый текст письма функцией build_sent_text().
- Вернуть итоговый список писем.


* **Пример готового dict email:**

```python
[
    {
        'recipient': 'admin@company.ru',
        'sender': 'default@study.com',
        'subject': 'Hello!',
        'date': '2025-11-04',
        'body': 'Привет, коллега!',
        'masked_sender': 'de***@study.com',
        'short_body': 'Привет, ко...',
        'sent_text': 'Кому: admin@company.ru, от default@study.com\nТема: Hello!, дата 2025-11-04\nПривет, ко...'
    },
    ...
]

```

* **Результат:** Вывод готово списка писем функцией

```python
"""
[
    Кому: {masked to}, от {masked from}
    Тема: {subject}, дата {date}
    {short_clean_body}
      ] ...
      
    
"""
```
