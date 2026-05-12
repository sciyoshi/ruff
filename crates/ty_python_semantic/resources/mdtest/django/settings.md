# Django Settings

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## settings attributes use project and global settings

`django-stubs` resolves `django.conf.settings.NAME` from the configured project settings module,
falling back to Django's global settings.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/conf/__init__.py`:

```py
class LazySettings:
    pass

settings = LazySettings()
```

`/.venv/<path-to-site-packages>/django/conf/global_settings.py`:

```py
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

`/src/project/__init__.py`:

```py
```

`/src/project/settings.py`:

```py
SECRET_KEY = "secret"
INSTALLED_APPS = ["accounts"]
DEBUG = False
```

`/src/app.py`:

```py
import project.settings
from django.conf import settings

reveal_type(settings.SECRET_KEY)  # revealed: Literal["secret"]
reveal_type(settings.INSTALLED_APPS)  # revealed: list[str]
reveal_type(settings.DEBUG)  # revealed: Literal[False]
reveal_type(settings.USE_TZ)  # revealed: Literal[True]
reveal_type(settings.DEFAULT_AUTO_FIELD)  # revealed: Literal["django.db.models.BigAutoField"]
settings.MISSING  # error: [unresolved-attribute]
```
