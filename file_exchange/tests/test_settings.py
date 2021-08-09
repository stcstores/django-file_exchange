import os

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

INSTALLED_APPS = ["file_exchange", "file_exchange.tests.testapp"]


SECRET_KEY = "iufoj=mibkpdz*%bob952x(%49rqgv8gg45k36kjcg76&-y5=!"
