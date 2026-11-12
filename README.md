# Лабораторная работа №6. Введение в FastAPI

**Студент:** Дума Данил КБ-241
**GitHub:** https://github.com/ScaleVVWizard/DumaDD

## Выполненные пункты

### №1. Подготовительный этап

Создана директория проекта, инициализирован git, добавлен `.gitignore` (шаблон для Python + строка `.env`):

![git init](screenshots/1-1.png)
![.gitignore](screenshots/1-2.png)

Проект инициализирован через `uv init`, создано и активировано виртуальное окружение, установлены `fastapi` и `uvicorn`:

![uv init и venv](screenshots/1-3.png)

Минимальное приложение в `main.py`, запуск через `uvicorn main:app --reload`:

![main.py](screenshots/1-12.png)

Корневой маршрут, Swagger (`/docs`) и ReDoc (`/redoc`):

![Главная страница](screenshots/1-13.png)
![Swagger](screenshots/1-14.png)
![ReDoc](screenshots/1-15.png)

Первый коммит:

![Коммит](screenshots/1-16.png)

### №2. Эндпоинт с параметрами пути и query

Добавлен эндпоинт `/items/{item_id}` с обязательным параметром пути `item_id` (int) и необязательным query-параметром `q`:

![main.py](screenshots/1-17.png)

Проверка в браузере по адресу `http://127.0.0.1:8000/items/42?q=test`:

![Браузер](screenshots/1-19.png)

Проверка в `/docs` через «Try it out»: без параметра `q` (возвращается `"q": null`) и с `q=test`:

![Docs без q](screenshots/1-20.png)
![Docs с q](screenshots/1-21.png)

Лог сервера со всеми запросами и коммит:

![Лог и коммит](screenshots/1-22.png)

### №3. Модель Pydantic и POST-запрос

Pydantic добавлен в зависимости явно (он уже был установлен как транзитивная зависимость FastAPI):

![uv add pydantic](screenshots/1-23.png)

В `main.py` определена модель `Item` и эндпоинт `POST /items/`, который возвращает полученный объект:

![main.py](screenshots/1-24.png)

В `/docs` появился новый эндпоинт `POST /items/` и схема `Item`:

![Docs](screenshots/1-25.png)

Проверка через «Try it out»: тело запроса и ответ сервера (код 200, объект возвращён без изменений):

![Тело запроса](screenshots/1-26.png)
![Ответ сервера](screenshots/1-27.png)

Коммит:

![Коммит](screenshots/1-28.png)

### №4. Вынос маршрутов в отдельные роутеры

Эндпоинты товаров перенесены в `app/routers/items.py` и объединены через `APIRouter` с префиксом `/items` и тегом `items`:

![items.py](screenshots/1-29.png)

В `main.py` роутер подключается через `include_router`:

![main.py](screenshots/1-30.png)

В `/docs` эндпоинты товаров теперь сгруппированы под тегом `items`, маршруты доступны по тем же адресам:

![Docs](screenshots/1-31.png)

Проверка `POST /items/` после рефакторинга: запрос и ответ сервера:

![Тело запроса](screenshots/1-32.png)
![Ответ сервера](screenshots/1-33.png)

Коммит:

![Коммит](screenshots/1-34.png)

### №5. Конфигурация через Pydantic Settings

Установлена библиотека `pydantic-settings`:

![uv add pydantic-settings](screenshots/1-35.png)

Класс настроек в `app/config.py`:

![config.py](screenshots/1-36.png)

Файл `.env` с настройками (в репозиторий не попадает, так как добавлен в `.gitignore`):

![.env](screenshots/1-37.png)

В `main.py` создан экземпляр настроек, `title` приложения берётся из конфигурации, добавлен эндпоинт `/info`:

![main.py](screenshots/1-38.png)

Проверка `/info`: значение `items_per_page` подхватилось из `.env` (20):

![/info](screenshots/1-39.png)

Коммит:

![Коммит](screenshots/1-40.png)

### №6. Обработка ошибок и улучшение документации

В `app/routers/items.py` добавлена заглушка базы данных `fake_db`, обработка ошибки 404 через `HTTPException`, описания параметров через `Path` и `Query`, а также описания и примеры полей модели `Item` через `Field`:

![items.py](screenshots/1-41.png)

В `main.py` указаны общие метаданные приложения: `description`, `version`, `contact`:

![main.py](screenshots/1-42.png)

Запрос существующего товара `/items/1`:

![Товар найден](screenshots/1-43.png)

Запрос несуществующего товара возвращает ошибку 404 с сообщением `Item not found`:

![Ошибка 404](screenshots/1-44.png)

В `/docs` отображаются название, описание, версия и контакт приложения:

![Docs](screenshots/1-46.png)


### №7. Самостоятельная работа: обновление товара и уникальность имени

Добавлен эндпоинт `PUT /items/{item_id}` с проверкой существования товара (404, если товар не найден). Добавлена функция `_name_exists`, которая проверяет уникальность имени без учёта регистра. При конфликте возвращается ошибка 400 `Item with this name already exists`. Проверка применяется и в `POST /items/`, и в `PUT` (при обновлении товар не конфликтует сам с собой благодаря параметру `exclude_id`). Чтобы было с чем сравнивать, `POST` теперь сохраняет новый товар в `fake_db`, а идентификаторы выдаются через счётчик `_next_id`:

![items.py](screenshots/1-47.png)

Новый эндпоинт `PUT /items/{item_id}` в `/docs`:

![Docs](screenshots/1-48.png)

Успешное обновление существующего товара (код 200):

![PUT 200](screenshots/1-49.png)

Обновление несуществующего товара (код 404):

![PUT 404](screenshots/1-50.png)

Попытка создать товар с уже занятым именем `Foo` (код 400):

![POST 400](screenshots/1-51.png)

Коммит:

![Коммит](screenshots/1-52.png)

### №8. Самостоятельная работа: логирование

Использована стандартная библиотека `logging`. В `main.py` настроен формат логов (время, уровень, имя логгера, сообщение) и добавлен middleware, который логирует каждый запрос: метод, путь, код ответа и время обработки. В роутере `app/routers/items.py` создан логгер `app.items`: успешные операции (создание и обновление товара) пишутся с уровнем INFO, нештатные ситуации (товар не найден, попытка создать дубликат) — с уровнем WARNING.

![main.py](screenshots/1-53.png)
![items.py](screenshots/1-54.png)

Вывод логов в консоли uvicorn: видны запросы с INFO и предупреждение WARNING при обращении к несуществующему товару `/items/999`:

![Логи](screenshots/1-55.png)

Коммит:

![Коммит](screenshots/1-55.png)
