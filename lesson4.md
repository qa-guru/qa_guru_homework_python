## Homework

```python
email1 = {
    "subject": "  Quarterly Report  ",
    "from": "  Alice.Cooper@Company.ru ",
    "to": "   bob_smith@Gmail.com   ",
    "body": "Hello Bob,\n\tHere is the quarterly report.\n\tPlease review and let me know your feedback.\n\nBest,\nAlice"
}

email2 = {
    "subject": " Weekend plans ",
    "from": "  katya_yan@yandex.ru ",
    "to": "  friend@mail.ru ",
    "body": "\tHey!\nLet's go hiking this weekend.\nBring snacks!\n"
}

email3 = {
    "subject": "Reminder: Meeting",
    "from": "  ceo@corporation.com ",
    "to": " team_lead@outlook.com ",
    "body": "   "
}

email4 = {
    "subject": "   ",
    "from": "   alex@business.net ",
    "to": "   hr@company.ru ",
    "body": "Hi HR,\nPlease find attached my updated CV.\nThanks!"
}

email5 = {
    "subject": "Project collaboration",
    "from": " partner@organization.org ",
    "to": "  lead_dev@icloud.com ",
    "body": "Hello,\nWe are interested in a partnership.\tPlease reply soon.\nRegards,\nTeam"
}
```

1. **Создайте словарь `email`**, который содержит поля:  
   `"subject"` (тема письма), `"from"` (адрес отправителя), `"to"` (адрес получателя), `"body"` (текст письма).

2. **Добавьте дату отправки**: создайте переменную `send_date` как текущую дату в формате `YYYY-MM-DD` и запишите её в
   `email["date"]`.  
   https://www.w3schools.com/python/python_datetime.asp
3. **Нормализуйте e-mail адреса** отправителя и получателя: приведите к нижнему регистру и уберите пробелы по краям.  
   Запишите обратно в `email["from"]` и `email["to"]`.

4. **Извлеките логин и домен отправителя** в две переменные `login` и `domain`.

5. **Создайте сокращённую версию текста**: возьмите первые 10 символов `email["body"]` и добавьте многоточие `"..."`.  
   Сохраните в новый ключ словаря: `email["short_body"]`.

6. **Списки доменов**: создайте список личных доменов  
   `['gmail.com','list.ru', 'yahoo.com','outlook.com','hotmail.com','icloud.com','yandex.ru','mail.ru','list.ru','bk.ru','inbox.ru']`  
   и список корпоративных доменов  
   `['company.ru','corporation.com','university.edu','organization.org','company.ru', 'business.net']`.
   с учетом того что там должны быть только уникальные значение
7. **Проверьте что в списке личных и корпоративных доменов нет пересечений**: ни один домен не должен входить в оба
   списка одновременно.
8. **Проверьте «корпоративность» отправителя**: создайте булеву переменную `is_corporate`, равную результату проверки
   вхождения домена отправителя в список корпоративных доменов.

9. **Соберите «чистый» текст сообщения** без табов и переводов строк: замените `"\t"` и `"\n"` на пробел.  
   Сохраните в `email["clean_body"]`.

10. **Сформируйте текст отправленного письма** многострочной f-строкой и сохраните в `email["sent_text"]`:

`Кому: {получатель}, от {отправитель}
Тема: {тема письма}, дата {дата}
{чистый текст сообщения}`

11. **Рассчитайте количество страниц печати** для `email["sent_text"]`, если на 1 страницу помещается 500 символов.  
    Сохраните результат в переменную `pages`. Значение должно быть округленно в большую сторону

12. **Проверьте пустоту темы и тела письма**: создайте переменные  `is_subject_empty, is_body_empty ` в котором будет
    хранится что тема письма содержит данные


13. **Создайте «маску» e-mail отправителя**: первые 2 символа логина + `"***@"` + домен.  
    Запишите в `email["masked_from"]`.

14. **Удалите из списка личных доменов** значения `"list.ru"` и `"bk.ru"`.

----------

### Подсказки:

- `datetime.now().strftime("%Y-%m-%d")`.
- `.strip().lower()`.
- `split("@")[0]` и `split("@")[1]`.   _(Считаем, что адрес корректный и содержит `@`.)_
- `.replace("\t", " ").replace("\n", " ")`.
- Подсказка (без дополнительных библиотек): «потолок» целочисленно — `(len(text) + 499) // 500`.
- `is_subject_empty = not email["subject"]` и `is_body_empty = not email["body"]`.
- `login[:2]`.
- `personal_domains.remove("list.ru")` и `personal_domains.remove("bk.ru")`.
- `domain in corporate_domains`
        
## Что сдавать

- Файл `email.py` с выполнением заданий по порядку.
- В конце файла сделайте `print(...)` ключевых результатов для быстрой проверки, например:  
  `print(email)` и `print(is_corporate, pages, is_subject_empty, is_body_empty)`.

## Критерии приемки

* Код читабелен и соответствует PEP 8(понятные имена, длина строки ≤ 100)
* На каждое домашнее задание создавайте отдельный PR
* Python 3.11+. В README укажите версию.
* requirements.txt обязателен (selenium, webdriver-manager, pytest, линтеры)
* Структура проекта корректна
* Отсутвуют мусорные файлы (.idea, venv и тд.)

## Полезные ссылки

* **Руководство по языку программирования Python** (
  Metanit) - [https://metanit.com/python/tutorial/](https://metanit.com/python/tutorial/)
* **Основы программирования** (Pythonworld) - [https://pythonworld.ru/osnovy](https://pythonworld.ru/osnovy)
* **Уроки по языку Python** (Devpractice) - [https://devpractice.ru/python/](https://devpractice.ru/python/)
* **Программирование на Python** (
  Stepik) - [https://stepik.org/course/67/syllabus](https://stepik.org/course/67/syllabus)
* **Python: основы и применение** (
  Stepik) - [https://stepik.org/course/512/syllabus](https://stepik.org/course/512/syllabus)
* **Интерактивный учебник Python** (Python
  Tutor) - [https://pythontutor.ru/visualizer/](https://pythontutor.ru/visualizer/)
* **Сборник задач по Python** (Itchief) - [https://itchief.ru/python](https://itchief.ru/python)
* **Задачи** (Python Tutor) - [https://ru.pythontutor.ru/problem/old/1](https://ru.pythontutor.ru/problem/old/1)
* **Документация по языку Python3** (docs-python.ru) - [https://docs-python.ru/](https://docs-python.ru/)
* **Встроенные типы данных** (
  docs.python.org) - [https://docs.python.org/3/library/stdtypes.html](https://docs.python.org/3/library/stdtypes.html)
* **Структурные типы данных** (
  docs.python.org) - [https://docs.python.org/3/tutorial/datastructures.html](https://docs.python.org/3/tutorial/datastructures.html)
* **Модуль с датой и временем** (`datetime`) (
  docs.python.org) - [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
* **Типизация** (`typing`) (
  docs.python.org) - [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html)
* **Статьи и тесты по Python** (Proglib) - [https://proglib.io/tag/Python](https://proglib.io/tag/Python)
* **Типы данных** - [https://realpython.com/python-data-types/](https://realpython.com/python-data-types/)
* **Строки (Strings)** - [https://realpython.com/python-strings/](https://realpython.com/python-strings/)
* **Списки и Кортежи (Lists, Tuples)
  ** - [https://realpython.com/python-lists-tuples/](https://realpython.com/python-lists-tuples/)
* **Словари (Dicts)** - [https://realpython.com/python-dicts/](https://realpython.com/python-dicts/)
* **Множества (Sets)** - [https://realpython.com/python-sets/](https://realpython.com/python-sets/)
* **Байты (Bytes)** - [https://realpython.com/python-bytes/](https://realpython.com/python-bytes/)
* **F-строки** - [https://realpython.com/python-f-strings/](https://realpython.com/python-f-strings/)
* **Проверка типов (Type Checking)
  ** - [https://realpython.com/python-type-checking/](https://realpython.com/python-type-checking/)
* **Переменные и типы данных
  ** - [https://programiz.com/python-programming/variables-datatypes](https://programiz.com/python-programming/variables-datatypes)
* **Строки** - [https://programiz.com/python-programming/string](https://programiz.com/python-programming/string)
* **Списки** - [https://programiz.com/python-programming/list](https://programiz.com/python-programming/list)
* **Кортежи** - [https://programiz.com/python-programming/tuple](https://programiz.com/python-programming/tuple)
* **Словари
  ** - [https://programiz.com/python-programming/dictionary](https://programiz.com/python-programming/dictionary)
* **Множества** - [https://programiz.com/python-programming/set](https://programiz.com/python-programming/set)
* **Типы данных
  ** - [https://w3schools.com/python/python_datatypes.asp](https://w3schools.com/python/python_datatypes.asp)
* **Дата и время
  ** - [https://w3schools.com/python/python_datetime.asp](https://w3schools.com/python/python_datetime.asp)
  
  
