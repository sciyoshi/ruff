# Django Third-Party Model Integrations

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## django-mptt runtime tree fields are available on model instances

`django-mptt` contributes concrete tree fields at model construction time. Projects often use those
fields directly even though older stubs only expose methods like `get_level()`.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField
from django.db.models.manager import Manager
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

class IntegerField:
    def __init__(self): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def filter(self, **kwargs) -> "Manager[_T]": ...
```

`/.venv/<path-to-site-packages>/mptt/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/mptt/models.py`:

```py
from django.db.models import Model, Manager

class MPTTModel(Model):
    objects: Manager
    def get_level(self) -> int: ...
```

```py
from django.db.models import CharField
from mptt.models import MPTTModel

class Node(MPTTModel):
    title = CharField(max_length=100)

node = Node()
reveal_type(node.level)  # revealed: int
reveal_type(node.lft)  # revealed: int
reveal_type(node.rght)  # revealed: int
reveal_type(node.tree_id)  # revealed: int
Node.objects.filter(level=1)
Node.objects.filter(lft__gte=1)
Node.objects.filter(rght__lt=10)
Node.objects.filter(tree_id__in=[1])
Node.objects.filter(level=object())  # error: [invalid-argument-type]
```
