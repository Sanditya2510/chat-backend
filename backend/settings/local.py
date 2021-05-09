import os

CACHES = {
   'default': {
      'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
      'LOCATION': '127.0.0.1:11211',
   }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_LOCAL_DB', 'sas_chat'),
        'USER': os.getenv('DB_LOCAL_USER', 'admin'),
        'PASSWORD': os.getenv('DB_LOCAL_PASSWORD', 'admin123'),
        'HOST': os.getenv('DB_LOCAL_HOST', 'localhost'),
        'PORT': '5432',
    }
}
