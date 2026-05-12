# Django Auth

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## get_user_model resolves project User model

`django.contrib.auth.get_user_model()` returns the configured concrete user model. Without runtime
settings, ty falls back to the unique `User` model in the first-party project.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields import CharField
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
class CharField:
    def __init__(self, *, max_length: int = 255): ...
```

`/.venv/<path-to-site-packages>/django/contrib/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/contrib/auth/__init__.py`:

```py
def get_user_model(): ...
```

`/src/accounts/models.py`:

```py
from django.db.models import Model, CharField

class User(Model):
    email = CharField(max_length=255)
```

`/src/accounts/__init__.py`:

```py
```

`/src/accounts/views.py`:

```py
from django.contrib.auth import get_user_model

user = get_user_model()
reveal_type(user)  # revealed: User
reveal_type(user.email)  # revealed: str
```

## Auth user boolean attributes are bool

`django-stubs` models auth boolean attributes as `bool` even when the underlying stubs are loose.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/contrib/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/contrib/auth/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/contrib/auth/models.py`:

```py
from django.db.models import Model

class PermissionMixin:
    is_superuser: object

class AbstractUser(Model, PermissionMixin):
    is_staff: object
    is_active: object
```

```py
from django.contrib.auth.models import AbstractUser, PermissionMixin
from django.db.models import Model

class User(AbstractUser):
    pass

class TokenUser(Model, PermissionMixin):
    pass

user = User()
reveal_type(user.is_staff)  # revealed: bool
reveal_type(user.is_active)  # revealed: bool
reveal_type(user.is_superuser)  # revealed: bool

token_user = TokenUser()
reveal_type(token_user.is_superuser)  # revealed: bool
```
