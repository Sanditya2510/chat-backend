CACHES = {
   'default': {
      'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
      'LOCATION': '127.0.0.1:11211',
   }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sas_chat',
        'USER': 'admin',
        'PASSWORD': 'admin123',
        'HOST': 'localhost',
        'PORT': '',
    }
}
