import os
env = os.environ.get

SECRET_KEY = 'qwerty'

# extract all APP_*** environment variables to settings
locals().update({k[4:].upper(): v for k, v in os.environ.items() if k.startswith("APP_")})

STORAGES = {
    'postgres': {
        'DBNAME':   env("POSTGRES_DBNAME", 'chat_app'),
        'USER':     env("POSTGRES_USER", 'docker'),
        'PASSWORD': env("POSTGRES_PASSWORD", 'secret'),
        'HOST':     env("POSTGRES_HOST", '172.19.0.2'),
        'PORT':     env("POSTGRES_PORT", 5432),
    },
}
