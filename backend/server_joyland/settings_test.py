from decouple import config
from .settings import *  # import everything from your normal settings

# Override the database settings for test
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     "rentms_test",
        'USER':     config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST':     config('DB_HOST', default='localhost'),
        'PORT':     config('DB_PORT', default=5432, cast=int),
        "TEST": {
                "NAME": "rentms_test",   # 👈 force pytest to use this DB
                "MIRROR": None,
            },
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
LOGGING = {}
