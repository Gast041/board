from pathlib import Path

# =========================
# БАЗОВЫЕ ПУТИ ПРОЕКТА
# =========================
# BASE_DIR — корень проекта (рядом с manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# БЕЗОПАСНОСТЬ И РЕЖИМ РАБОТЫ
# =========================
# SECRET_KEY — секретный ключ Django (в проде нельзя светить)
SECRET_KEY = "django-insecure-y^!fx8_e_#-319x2w084hb9=@plgtiw_9r87$^)b&r3p%cfy3a"

# DEBUG=True — показывать подробные ошибки (пока оставляем True)
DEBUG = True

# Разрешённые домены (твой домен на PythonAnywhere)
ALLOWED_HOSTS = ["52p.pythonanywhere.com"]


# =========================
# ПРИЛОЖЕНИЯ (APPS)
# =========================
INSTALLED_APPS = [
    # --- встроенные приложения Django ---
    "django.contrib.admin",          # админка
    "django.contrib.auth",           # пользователи/логин/пароли
    "django.contrib.contenttypes",   # служебное (типы моделей)
    "django.contrib.sessions",       # сессии (держат логин)
    "django.contrib.messages",       # сообщения (messages)
    "django.contrib.staticfiles",    # статические файлы (CSS/JS)

    # --- твои приложения ---
    # ВАЖНО: "board" сюда НЕ надо, это пакет проекта, а не приложение
    "board.ads",                     # приложение объявлений (ads)
]


# =========================
# MIDDLEWARE (ПРОСЛОЙКИ)
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",            # базовая безопасность
    "django.contrib.sessions.middleware.SessionMiddleware",     # сессии
    "django.middleware.common.CommonMiddleware",                # общие настройки
    "django.middleware.csrf.CsrfViewMiddleware",                # CSRF защита
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # авторизация
    "django.contrib.messages.middleware.MessageMiddleware",     # сообщения
    "django.middleware.clickjacking.XFrameOptionsMiddleware",   # защита от iframe
]


# =========================
# URLS / WSGI
# =========================
ROOT_URLCONF = "board.urls"                 # главный файл маршрутов
WSGI_APPLICATION = "board.wsgi.application" # вход для сервера (PythonAnywhere)


# =========================
# ШАБЛОНЫ (HTML)
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Где искать шаблоны (ты используешь board/templates)
        "DIRS": [BASE_DIR / "board" / "templates"],
        # Разрешаем templates внутри apps (например board/ads/templates)
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",     # debug в шаблоне
                "django.template.context_processors.request",   # request в шаблоне
                "django.contrib.auth.context_processors.auth",  # user в шаблоне
                "django.contrib.messages.context_processors.messages",  # messages
            ],
        },
    },
]


# =========================
# БАЗА ДАННЫХ
# =========================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",   # sqlite (норм для старта)
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================
# ПРОВЕРКА ПАРОЛЕЙ
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  # похожесть на имя/логин
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},            # мин длина
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},           # простые пароли
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},          # только цифры
]


# =========================
# ЯЗЫК И ВРЕМЯ
# =========================
LANGUAGE_CODE = "ru"     # русский интерфейс Django
TIME_ZONE = "UTC"        # позже можно "Europe/Moscow"

USE_I18N = True          # включить переводы
USE_TZ = True            # хранить даты в UTC


# =========================
# СТАТИКА И МЕДИА (PythonAnywhere)
# =========================
STATIC_URL = "/static/"                 # URL для статики в браузере
STATIC_ROOT = "/home/52p/board/static"  # куда складывать статику на сервере

MEDIA_URL = "/media/"                   # URL для медиа
MEDIA_ROOT = "/home/52p/board/media"    # папка для загрузок


# =========================
# АВТОРИЗАЦИЯ / РЕДИРЕКТЫ
# =========================
# ✅ ВАЖНО: чтобы @login_required НЕ вёл на /accounts/login/
LOGIN_URL = "/login/"         # куда отправлять неавторизованных пользователей

LOGIN_REDIRECT_URL = "/"      # куда после успешного входа
LOGOUT_REDIRECT_URL = "/"     # куда после выхода


# =========================
# ПРОЧЕЕ
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # тип PK по умолчанию
