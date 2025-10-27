# Homework

1. Создать пользователя на GitHub
2. Создать новый проект на GitHub
3. Добавить необходимые зависимости
4. Исправить ошибки в коде (PEP8, PEP20)

```python
print("Hello, README!")
Text = "Lorem Ipsum - это текст-'рыба', часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной рыбой для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus PageMaker, в шаблонах которых используется Lorem Ipsum."


def add(a, b): return a + b


def greet(name): print("Привет," + name)


NUMS = [1, 2, 3, 4, 5]
greet("мир")
print(add(2, 2))
```

5. Переделать тест на открытие страницы python.org и проверки заголовка страницы

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def test_title():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=Options())
    driver.set_window_size(1440, 900)
    driver.get("https://www.selenium.dev")
    assert "Selenium" in driver.title
    driver.quit()
```

6. Код залить в репозиторий и прислать ссылку на PR

---

## Критерии приемки

* При создании пользователя и проекта, помните что в будущем это профиль будет вашей визитной карточкой
* Код читабелен и соответствует PEP 8(понятные имена, длина строки ≤ 100)
* На каждое домашнее задание создавайте отдельный PR
* Python 3.11+. В README укажите версию.
* requirements.txt обязателен (selenium, webdriver-manager, pytest, линтеры)
* Все тесты должны проходить: pytest -q → 0 failed
* Структура проекта корректна
* Отсутвуют мусорные файлы (.idea, venv и тд.)
* Каждое задание выполняется в отдельном файле

## Полезные ссылки

* [Pytest Documentation](https://docs.pytest.org/en/stable/)
* [Python Virtual Environments (venv)](https://docs.python.org/3/library/venv.html)
* [Pip freeze and requirements.txt](https://pip.pypa.io/en/stable/cli/pip_freeze/)
* [How to Run a Makefile in Windows](https://medium.com/@samsorrahman/how-to-run-a-makefile-in-windows-b4d115d7c516)
* [Makefile on MAC OS](https://wahyu-ehs.medium.com/makefile-on-mac-os-2ef0e67b0a15)
* [Оформляем README-файл профиля на GitHub](https://habr.com/ru/articles/649363/)
* [PEP-8 - Секрет чистого и профессионального кода! [Python - Первый шаг 014]](https://www.youtube.com/watch?v=_SYuxOC1pNU)
* [Дзен Python — философии программирования от Тима Петерса (PEP20)](https://pythonchik.ru/osnovy/dzen-python-pep20)
* [PEP 8 - руководство по написанию кода на Python](https://pythonworld.ru/osnovy/pep-8-rukovodstvo-po-napisaniyu-koda-na-python.html)
* [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
* [Ruff Documentation](https://docs.astral.sh/ruff/)
* [Black Documentation](https://black.readthedocs.io/en/stable/)
* [isort Documentation](https://pycqa.github.io/isort/)
* [Руководство по makefile для начинающих (Habr)](https://habr.com/ru/companies/ruvds/articles/484504/)

## Правила оформления Python-кода

| Раздел | Правило | Пример |
| --- | --- | --- |
| Отступы | 4 пробела на уровень вложенности | `if x: do_something()` |
| Длина строки | До 79 символов (или до 88 при использовании Black) | — |
| Пустые строки | Между функциями/классами верхнего уровня — 2 пустые строки | — |
| Кодировка | Всегда UTF-8 (по умолчанию в Python 3) | *(доп. шапка обычно не нужна)* |
| Импорты — расположение | Сразу после модульного docstring и перед константами | `"""Модуль..."""`<br><br>`import os`<br>`import sys`<br><br>`MAX_SIZE = 10` |
| Импорты — порядок | Группами с пустой строкой; алфавит внутри группы: stdlib → third-party → local | `import os`<br>`import sys`<br><br>`import requests`<br><br>`from . import utils` |
| Вокруг операторов | По одному пробелу с обеих сторон бинарных операторов | `total = a + b` |
| Аргументы/вызов | Без пробелов вокруг `=` у значений по умолчанию и keyword-аргументов | `def f(x=1, *, flag=True): ...`<br>`f(limit=10)` |
| Скобки | Без пробела сразу после `(` и перед `)` | `func(x, y)` |
| Срезы/индексы | Без пробела перед `[`; в простых срезах — без пробелов вокруг `:` | `a[i]`, `a[i:j]` |
| Точки/запятые | Нет пробела перед `, ; :` | `print(a, b)` |
| Имена функций/методов | `lower_snake_case` | `def process_item():` |
| Переменные | `lower_snake_case` | `user_count = 0` |
| Константы | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT = 5` |
| Классы/исключения | `CapWords` (PascalCase) | `class DataError(Exception): ...` |
| Модули/файлы | Короткие, строчные имена | `analytics.py`, `utils_io.py` |
| Защищённые члены | Префикс одного подчёркивания | `_internal_helper()` |
| «Магические» методы | Двойное подчёркивание спереди и сзади | `__init__`, `__repr__` |
| Сравнение с `None` | Использовать `is` / `is not` | `if value is None:` |
| Булевы значения | Полагаться на истинность/ложность объектов | `if items:` |
| Цепочки сравнений | Компактная запись | `if 0 < x < 10:` |
| Исключения | Всегда конкретный тип исключения | `except ValueError:` |
| Аннотации типов | Использовать PEP 484 для функций и переменных | `def add(a: int, b: int) -> int: ...`<br>`count: int = 0` |


