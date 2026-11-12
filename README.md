# Лабораторная работа №6. Введение в FastAPI

**Студент:** Дума Данил КБ-241
**GitHub:** https://github.com/ScaleVVWizard/DumaDD

## Выполненные пункты

### №1. Подготовительный этап

Создана директория проекта, инициализирован git, добавлен `.gitignore` (шаблон для Python + строка `.env`):

![git init](screenshots/1-1.PNG)
![.gitignore](screenshots/1-2.PNG)

Проект инициализирован через `uv init`, создано и активировано виртуальное окружение, установлены `fastapi` и `uvicorn`:

![uv init и venv](screenshots/1-3.PNG)

Минимальное приложение в `main.py`, запуск через `uvicorn main:app --reload`:

![main.py](screenshots/1-12.PNG)

Корневой маршрут, Swagger (`/docs`) и ReDoc (`/redoc`):

![Главная страница](screenshots/1-13.PNG)
![Swagger](screenshots/1-14.PNG)
![ReDoc](screenshots/1-15.PNG)

Первый коммит:

![Коммит](screenshots/1-16.PNG)

### №2. Эндпоинт с параметрами пути и query

Добавлен эндпоинт `/items/{item_id}` с обязательным параметром пути `item_id` (int) и необязательным query-параметром `q`:

![main.py](screenshots/1-17.PNG)

Проверка в браузере по адресу `http://127.0.0.1:8000/items/42?q=test`:

![Браузер](screenshots/1-19.PNG)

Проверка в `/docs` через «Try it out»: без параметра `q` (возвращается `"q": null`) и с `q=test`:

![Docs без q](screenshots/1-20.PNG)
![Docs с q](screenshots/1-21.PNG)

Лог сервера со всеми запросами и коммит:

![Лог и коммит](screenshots/1-22.PNG)

### №3. Модель Pydantic и POST-запрос

Pydantic добавлен в зависимости явно (он уже был установлен как транзитивная зависимость FastAPI):

![uv add pydantic](screenshots/1-23.PNG)

В `main.py` определена модель `Item` и эндпоинт `POST /items/`, который возвращает полученный объект:

![main.py](screenshots/1-24.PNG)

В `/docs` появился новый эндпоинт `POST /items/` и схема `Item`:

![Docs](screenshots/1-25.PNG)

Проверка через «Try it out»: тело запроса и ответ сервера (код 200, объект возвращён без изменений):

![Тело запроса](screenshots/1-26.PNG)
![Ответ сервера](screenshots/1-27.PNG)

Коммит:

![Коммит](screenshots/1-28.PNG)

### №4. Вынос маршрутов в отдельные роутеры

Эндпоинты товаров перенесены в `app/routers/items.py` и объединены через `APIRouter` с префиксом `/items` и тегом `items`:

![items.py](screenshots/1-29.PNG)

В `main.py` роутер подключается через `include_router`:

![main.py](screenshots/1-30.PNG)

В `/docs` эндпоинты товаров теперь сгруппированы под тегом `items`, маршруты доступны по тем же адресам:

![Docs](screenshots/1-31.PNG)

Проверка `POST /items/` после рефакторинга: запрос и ответ сервера:

![Тело запроса](screenshots/1-32.PNG)
![Ответ сервера](screenshots/1-33.PNG)

Коммит:

![Коммит](screenshots/1-34.PNG)

### №5. Конфигурация через Pydantic Settings

Установлена библиотека `pydantic-settings`:

![uv add pydantic-settings](screenshots/1-35.PNG)

Класс настроек в `app/config.py`:

![config.py](screenshots/1-36.PNG)

Файл `.env` с настройками (в репозиторий не попадает, так как добавлен в `.gitignore`):

![.env](screenshots/1-37.PNG)

В `main.py` создан экземпляр настроек, `title` приложения берётся из конфигурации, добавлен эндпоинт `/info`:

![main.py](screenshots/1-38.PNG)

Проверка `/info`: значение `items_per_page` подхватилось из `.env` (20):

![/info](screenshots/1-39.PNG)

Коммит:

![Коммит](screenshots/1-40.PNG)

### №6. Обработка ошибок и улучшение документации

В `app/routers/items.py` добавлена заглушка базы данных `fake_db`, обработка ошибки 404 через `HTTPException`, описания параметров через `Path` и `Query`, а также описания и примеры полей модели `Item` через `Field`:

![items.py](screenshots/1-41.PNG)

В `main.py` указаны общие метаданные приложения: `description`, `version`, `contact`:

![main.py](screenshots/1-42.PNG)

Запрос существующего товара `/items/1`:

![Товар найден](screenshots/1-43.PNG)

Запрос несуществующего товара возвращает ошибку 404 с сообщением `Item not found`:

![Ошибка 404](screenshots/1-44.PNG)

В `/docs` отображаются название, описание, версия и контакт приложения:

![Docs](screenshots/1-46.PNG)


### №7. Самостоятельная работа: обновление товара и уникальность имени

Добавлен эндпоинт `PUT /items/{item_id}` с проверкой существования товара (404, если товар не найден). Добавлена функция `_name_exists`, которая проверяет уникальность имени без учёта регистра. При конфликте возвращается ошибка 400 `Item with this name already exists`. Проверка применяется и в `POST /items/`, и в `PUT` (при обновлении товар не конфликтует сам с собой благодаря параметру `exclude_id`). Чтобы было с чем сравнивать, `POST` теперь сохраняет новый товар в `fake_db`, а идентификаторы выдаются через счётчик `_next_id`:

![items.py](screenshots/1-47.PNG)

Новый эндпоинт `PUT /items/{item_id}` в `/docs`:

![Docs](screenshots/1-48.PNG)

Успешное обновление существующего товара (код 200):

![PUT 200](screenshots/1-49.PNG)

Обновление несуществующего товара (код 404):

![PUT 404](screenshots/1-50.PNG)

Попытка создать товар с уже занятым именем `Foo` (код 400):

![POST 400](screenshots/1-51.PNG)

Коммит:

![Коммит](screenshots/1-52.PNG)

### №8. Самостоятельная работа: логирование

Использована стандартная библиотека `logging`. В `main.py` настроен формат логов (время, уровень, имя логгера, сообщение) и добавлен middleware, который логирует каждый запрос: метод, путь, код ответа и время обработки. В роутере `app/routers/items.py` создан логгер `app.items`: успешные операции (создание и обновление товара) пишутся с уровнем INFO, нештатные ситуации (товар не найден, попытка создать дубликат) — с уровнем WARNING.

![main.py](screenshots/1-53.PNG)
![items.py](screenshots/1-54.PNG)

Вывод логов в консоли uvicorn: видны запросы с INFO и предупреждение WARNING при обращении к несуществующему товару `/items/999`:

![Логи](screenshots/1-55.PNG)

Коммит:

![Коммит](screenshots/1-56.PNG)
