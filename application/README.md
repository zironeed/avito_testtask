# zadanie-6105

Задание выполнено на стеке: Python + Django REST Framework

---

## Подготовка к тестированию

### Настройка проекта
Необходимо ввести несколько команд:
```
pip install -r requirements.txt
```
```
python manage.py prepare_for_test
```

Переменные окружения просто копируйте из файла .env-sample
Здесь вам потребуются лишь следующие переменные:
* `POSTGRES_USERNAME` - имя пользователя
* `POSTGRES_PASSWORD` - пароль
* `POSTGRES_HOST` - хост (по умолчанию стоит db, если хотите запустить без докера - вводите localhost)
* `POSTGRES_PORT` - порт
* `POSTGRES_DATABASE` - имя БД

### Запуск
* Docker - просто запустите Dockerfile
* Non-docker - python manage.py runserver 0.0.0.0:8080

---

## Urls

### Важные

* `admin/` - административная панель
* `swagger/` - документация

### Полезные для тестов

* `token/` - для получения JWT-токенов
* `refresh/` - для обновления токенов (оно вам вряд-ли потребуется)

#### _Для urls, начинающихся на /api, прописаны docstrings. Они отображаются в swagger_

---

### Дополнительно
Описана конфигурация линтера. Описание лежит в файле .pylintrc

`pylint --rcfile=.pylintrc ./application` - для запуска линтера

---

## Спасибо за внимание!

На этом у меня все, надеюсь, что ничего не упустил)

---