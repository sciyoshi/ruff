# Django Many-to-Many Relationships

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## ManyToManyField returns related model manager

Accessing a many-to-many field on a model instance returns a manager over the related model.

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
from django.db.models.fields.related import ManyToManyField
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
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ManyToManyField:
    def __init__(self, to, *, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, CharField, ManyToManyField

class Author(Model):
    name = CharField(max_length=100)

class Book(Model):
    title = CharField(max_length=100)
    authors = ManyToManyField(Author, related_name="books")

b = Book()
reveal_type(b.authors)  # revealed: Manager[Author]
reveal_type(b.authors.get())  # revealed: Author
```

## String self-reference resolves to current model manager

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ManyToManyField
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ManyToManyField:
    def __init__(self, to, *, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, ManyToManyField

class Person(Model):
    friends = ManyToManyField("self")

p = Person()
reveal_type(p.friends)  # revealed: Manager[Person]
reveal_type(p.friends.get())  # revealed: Person
```

## ManyToManyField uses many-related manager when available

django-stubs models many-to-many access as `ManyRelatedManager`, which exposes mutation methods like
`add` and `set`.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ManyToManyField
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ManyToManyField:
    def __init__(self, to, *, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related_descriptors.py`:

```py
from typing import Generic, TypeVar
from django.db.models.manager import Manager

_T = TypeVar("_T")
_Through = TypeVar("_Through")

class ManyRelatedManager(Manager[_T], Generic[_T, _Through]):
    def add(self, *objs: _T | int) -> None: ...
    def set(self, objs) -> None: ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    @classmethod
    def from_queryset(cls, queryset_cls): ...
    def get(self) -> _T: ...
```

`/.venv/<path-to-site-packages>/django/db/models/query.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class QuerySet(Generic[_T]):
    pass
```

```py
from django.db.models import Model, ManyToManyField, Manager, QuerySet

class AuthorQuerySet(QuerySet["Author"]):
    def nocache(self) -> "AuthorQuerySet":
        return self

    def first(self) -> "Author | None":
        return None

AuthorManager = Manager.from_queryset(AuthorQuerySet)

class Author(Model):
    objects = AuthorManager()

class Book(Model):
    authors = ManyToManyField(Author)

book = Book()
author = Author()
reveal_type(book.authors.get())  # revealed: Author
reveal_type(book.authors.nocache().first())  # revealed: Author | None
book.authors.add(author)
book.authors.set([author])
```
