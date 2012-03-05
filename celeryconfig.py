# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

# List of modules to import when celery starts.
CELERY_IMPORTS = ("opendylan.celery.tasks", )

## Result store settings.
CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0

## Broker settings.
BROKER_URL = "redis://localhost:6379/0"

## Worker settings
## If you're doing mostly I/O you can have more processes,
## but if mostly spending CPU, try to keep it close to the
## number of CPUs on your machine. If not set, the number of CPUs/cores
## available will be used.
CELERYD_CONCURRENCY = 10

CELERY_ENABLE_UTC = True
