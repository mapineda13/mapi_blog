from .default import *
SECRET_KEY = 'mapi_Keyword'
APP_ENV = APP_ENV_PRODUCTION

# Configuracion de DB
USER_DB = 'postgres'
PASS_DB = 'an63m0n13'
URL_DB = 'localhost'
NAME_DB = 'mapi_blog'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'
SQLALCHEMY_DATABASE_URI = FULL_URL_DB