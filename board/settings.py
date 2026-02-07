from pathlib import Path

# =========================
# БАЗОВЫЕ ПУТИ ПРОЕКТА
# =========================
# BASE_DIR — корень проекта (где лежит manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# БЕЗОПАСНОСТЬ И РЕЖИМ РАБОТЫ
# =========================
# Секретный ключ проекта (никому не показывать в продакшене)
SECRET_KEY = "django-insecure-y^!fx8_e_#-319x2w084hb9=@plgtiw_9r87$^)b&r3p%cfy3a"

# DEBUG=True — режим разработки (в продакшене должен быть False)
DEBUG = True

# Какие домены имеют право открывать сайт (на PythonAnywhere — твой домен)
ALLOWED_HOSTS = ["52p.pythonanywhere.com"]


# =========================
# ПРИЛОЖЕНИЯ (APPS)
# =========================
INSTALLED_APPS = [
    # --- встроенные приложения Django ---
    "django.contrib.admin",          # админка
    "django.contrib.auth",           # пользователи/логин/пароли
    "django.contrib.contenttypes",   # служебное (типы моделей)
    "django.contrib.sessions",       # сессии (логин держится)
    "django.contrib.messages",       # сообщения (messages framework)
    "django.contrib.staticfiles",    # статические файлы (CSS/JS)

    # --- твои приложения проекта ---
    "board.ads",  # приложение объявлений
    # ВАЖНО: 'board' сюда НЕ добавляем — это пакет проекта, а не app
]


# =========================
# MIDDLEWARE (ПРОСЛОЙКИ)
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",            # базовая безопасность
    "django.contrib.sessions.middleware.SessionMiddleware",     # сессии
    "django.middleware.common.CommonMiddleware",                # общие настройки
    "django.middleware.csrf.CsrfViewMiddleware",                # защита CSRF (формы)
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # авторизация
    "django.contrib.messages.middleware.MessageMiddleware",     # сообщения
    "django.middleware.clickjacking.XFrameOptionsMiddleware",   # защита от iframe атак
]


# =========================
# URLS / WSGI
# =========================
ROOT_URLCONF = "board.urls"          # главный файл маршрутов urls.py
WSGI_APPLICATION = "board.wsgi.application"  # вход для сервера (PythonAnywhere)


# =========================
# ШАБЛОНЫ (HTML)
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Здесь Django ищет шаблоны (ты используешь board/templates)
        "DIRS": [BASE_DIR / "board" / "templates"],
        "APP_DIRS": True,  # искать templates внутри приложений (ads/templates и т.д.)
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
        "ENGINE": "django.db.backends.sqlite3",   # пока sqlite (норм для обучения)
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================
# ПРОВЕРКА ПАРОЛЕЙ
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =========================
# ЯЗЫК И ВРЕМЯ
# =========================
LANGUAGE_CODE = "ru"   # язык интерфейса Django
TIME_ZONE = "UTC"      # можно позже поменять на "Europe/Moscow"

USE_I18N = True        # интернационализация
USE_TZ = True          # хранить даты в UTC


# =========================
# СТАТИКА И МЕДИА (PythonAnywhere)
# =========================
# STATIC_URL — URL для статики (как в браузере)
STATIC_URL = "/static/"

# STATIC_ROOT — куда собирать статику на сервере (collectstatic)
STATIC_ROOT = "/home/52p/board/static"

# MEDIA — куда загружать файлы (картинки объявлений и т.д.)
MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/52p/board/media"


# =========================
# ПЕРЕХОДЫ ПОСЛЕ ВХОДА/ВЫХОДА
# =========================
LOGIN_REDIRECT_URL = "/"   # куда перекинуть после логина
LOGOUT_REDIRECT_URL = "/"  # куда перекинуть после логаута


# =========================
# ПРОЧЕЕ
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # тип PK по умолчанию
