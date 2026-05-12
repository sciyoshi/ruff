# Django Reverse Relationships

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## ForeignKey reverse related_name returns source manager

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
from django.db.models.fields.related import ForeignKey
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
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, CharField, ForeignKey

class Author(Model):
    name = CharField(max_length=100)

class Book(Model):
    author = ForeignKey(Author, on_delete=None, related_name="books")

a = Author()
reveal_type(a.books)  # revealed: Manager[Book]
reveal_type(a.books.get())  # revealed: Book
```

## Reverse members are discovered across project packages

Django registers models from all installed apps, so a reverse relation may be declared in a
different top-level package from the target model.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def first(self) -> _T | None: ...
```

`/src/apps/__init__.py`:

```py
```

`/src/apps/identity/__init__.py`:

```py
```

`/src/apps/identity/models.py`:

```py
from django.db.models import Model

class Account(Model):
    pass

class User(Model):
    pass
```

`/src/server/__init__.py`:

```py
```

`/src/server/slack/__init__.py`:

```py
```

`/src/server/slack/models.py`:

```py
from django.conf import settings
from django.db.models import Model, ForeignKey
from apps.identity.models import Account

class AccountSlack(Model):
    account = ForeignKey(Account, on_delete=None, related_name="slack_accounts")

class UserSlack(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=None, related_name="slack_users")
```

`/.venv/<path-to-site-packages>/django/conf/__init__.py`:

```py
class Settings:
    AUTH_USER_MODEL: str

settings = Settings()
```

```py
from apps.identity.models import Account, User

account = Account()
reveal_type(account.slack_accounts)  # revealed: Manager[AccountSlack]
reveal_type(account.slack_accounts.first())  # revealed: AccountSlack | None
user = User()
reveal_type(user.slack_users)  # revealed: Manager[UserSlack]
reveal_type(user.slack_users.first())  # revealed: UserSlack | None
```

## Reverse members are discovered from imported third-party model modules

Some Django packages define models in site-packages that point at `settings.AUTH_USER_MODEL`. If the
custom user model imports that package model, ty can use that explicit import to discover the
reverse accessor without scanning every installed package.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/conf/__init__.py`:

```py
class Settings:
    AUTH_USER_MODEL: str

settings = Settings()
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

class User(Model):
    pass
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None, null: bool = False): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def filter(self, **kwargs) -> "Manager[_T]": ...
    def first(self) -> _T | None: ...
```

`/.venv/<path-to-site-packages>/user_sessions/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/user_sessions/models.py`:

```py
from django.conf import settings
from django.db import models

class Session(models.Model):
    user = models.ForeignKey(getattr(settings, "AUTH_USER_MODEL", "auth.User"), null=True, on_delete=None)
```

`/src/apps/__init__.py`:

```py
```

`/src/apps/identity/__init__.py`:

```py
```

`/src/apps/identity/models.py`:

```py
from django.db.models import Model
from user_sessions.models import Session

class User(Model):
    pass
```

`/src/server/__init__.py`:

```py
```

`/src/project/__init__.py`:

```py
```

`/src/project/settings/__init__.py`:

```py
```

`/src/project/settings/main.py`:

```py
AUTH_USER_MODEL = "identity.user"
```

```py
from apps.identity.models import User

user = User()
reveal_type(user.session_set)  # revealed: Manager[Session]
reveal_type(user.session_set.filter(user=user).first())  # revealed: Session | None
```

## Multiple reverse targets share models-module discovery

Reverse relationship discovery is cached for the Django models module, while each target model still
receives only its own reverse members.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

`/src/shop/__init__.py`:

```py
```

`/src/shop/models.py`:

```py
from django.db.models import Model, ForeignKey

class Author(Model):
    pass

class Store(Model):
    pass

class Book(Model):
    author = ForeignKey(Author, on_delete=None, related_name="books")
    store = ForeignKey(Store, on_delete=None, related_name="books")
```

```py
from shop.models import Author, Store

author = Author()
store = Store()
reveal_type(author.books)  # revealed: Manager[Book]
reveal_type(store.books)  # revealed: Manager[Book]
author.store_set  # error: [unresolved-attribute]
store.author_set  # error: [unresolved-attribute]
```

## Reverse relation across app packages is synthesized

Reverse relationships across app packages are discovered from Django model modules under the same
first-party search path.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

`/src/accounts/__init__.py`:

```py
```

`/src/accounts/models.py`:

```py
from django.db.models import Model

class User(Model):
    pass
```

`/src/library/__init__.py`:

```py
```

`/src/library/models.py`:

```py
from django.db.models import Model, ForeignKey
from accounts.models import User

class Book(Model):
    owner = ForeignKey(User, on_delete=None, related_name="owned_books")
```

```py
from accounts.models import User

u = User()
reveal_type(u.owned_books)  # revealed: Manager[Book]
reveal_type(u.owned_books.get())  # revealed: Book
```

## ForeignKey default reverse accessor returns source manager

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, ForeignKey

class Category(Model):
    pass

class Blog(Model):
    category = ForeignKey(Category, on_delete=None)

c = Category()
reveal_type(c.blog_set)  # revealed: Manager[Blog]
reveal_type(c.blog_set.get())  # revealed: Blog
```

## OneToOne reverse accessor returns source model

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import OneToOneField
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class OneToOneField:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

```py
from django.db.models import Model, OneToOneField

class User(Model):
    pass

class Profile(Model):
    user = OneToOneField(User, on_delete=None, related_name="profile")

u = User()
reveal_type(u.profile)  # revealed: Profile
```

## ManyToMany reverse related_name returns source manager

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

class Book(Model):
    pass

class Author(Model):
    books = ManyToManyField(Book, related_name="authors")

b = Book()
reveal_type(b.authors)  # revealed: Manager[Author]
reveal_type(b.authors.get())  # revealed: Author
```

## related_name plus disables reverse accessor

Django treats `related_name="+"` as an instruction not to create a reverse relation.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

```py
from django.db.models import Model, ForeignKey

class Author(Model):
    pass

class Book(Model):
    author = ForeignKey(Author, on_delete=None, related_name="+")

a = Author()
a.book_set  # error: [unresolved-attribute]
```

## related_name placeholders are expanded

Django expands `%(class)s`, `%(model_name)s`, and `%(app_label)s` placeholders in `related_name`.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

`/src/library/__init__.py`:

```py
```

`/src/library/models.py`:

```py
from django.db.models import Model, ForeignKey

class Author(Model):
    pass

class Book(Model):
    author = ForeignKey(Author, on_delete=None, related_name="%(app_label)s_%(class)s_items")
```

```py
from library.models import Author

a = Author()
reveal_type(a.library_book_items)  # revealed: Manager[Book]
reveal_type(a.library_book_items.get())  # revealed: Book
```

## Inherited app-label reverse name placeholders are expanded from concrete subclasses

An abstract base model can define `related_name="%(app_label)s"` once, while concrete subclasses in
other apps receive reverse accessors named after their concrete app labels.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import OneToOneField
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class OneToOneField:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/src/apps/__init__.py`:

```py
```

`/src/apps/identity/__init__.py`:

```py
```

`/src/apps/identity/models.py`:

```py
from django.db.models import Model

class User(Model):
    pass
```

`/src/apps/integrations/__init__.py`:

```py
```

`/src/apps/integrations/models.py`:

```py
from django.db.models import Model, OneToOneField
from apps.identity.models import User

class IntegrationUser(Model):
    class Meta:
        abstract = True

    user = OneToOneField(User, on_delete=None, related_name="%(app_label)s")
```

`/src/apps/integrations/google/__init__.py`:

```py
```

`/src/apps/integrations/google/models.py`:

```py
from apps.integrations.models import IntegrationUser

class GoogleUser(IntegrationUser):
    pass
```

```py
from apps.identity.models import User

user = User()
reveal_type(user.google)  # revealed: GoogleUser
```

## Reverse relation across modules in the same app

Models in the same `models/` package can define reverse relationships from different modules.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

`/src/library/__init__.py`:

```py
```

`/src/library/models/__init__.py`:

```py
```

`/src/library/models/authors.py`:

```py
from django.db.models import Model

class Author(Model):
    pass
```

`/src/library/models/books.py`:

```py
from django.db.models import Model, ForeignKey
from library.models.authors import Author

class Book(Model):
    author = ForeignKey(Author, on_delete=None, related_name="books")
```

```py
from library.models.authors import Author

a = Author()
reveal_type(a.books)  # revealed: Manager[Book]
reveal_type(a.books.get())  # revealed: Book
```

## settings.AUTH_USER_MODEL reverse relation

`settings.AUTH_USER_MODEL` resolves to the unique `User` model in the same first-party package.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/conf/__init__.py`:

```py
class _Settings:
    AUTH_USER_MODEL: object

settings = _Settings()
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

`/src/apps/__init__.py`:

```py
```

`/src/apps/identity/__init__.py`:

```py
```

`/src/apps/identity/models.py`:

```py
from django.db.models import Model

class User(Model):
    pass
```

`/src/apps/invitations/__init__.py`:

```py
```

`/src/apps/invitations/models.py`:

```py
from django.conf import settings
from django.db.models import Model, ForeignKey

class Invite(Model):
    recipient = ForeignKey(settings.AUTH_USER_MODEL, on_delete=None, related_name="received_invites")
```

```py
from apps.identity.models import User

user = User()
reveal_type(user.received_invites)  # revealed: Manager[Invite]
reveal_type(user.received_invites.get())  # revealed: Invite
```

## Reverse manager uses related model default manager queryset

Reverse related managers are subclasses of both Django's related manager and the related model's
default manager, so queryset-returning manager methods preserve `from_queryset` subclasses.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
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
class ForeignKey:
    def __init__(self, to, *, on_delete, related_name: str | None = None): ...
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related_descriptors.py`:

```py
from typing import Generic, TypeVar
from django.db.models.manager import Manager

_T = TypeVar("_T")

class RelatedManager(Manager[_T], Generic[_T]):
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar
from django.db.models.query import QuerySet

_T = TypeVar("_T")

class Manager(Generic[_T]):
    @classmethod
    def from_queryset(cls, queryset_cls): ...
    def all(self) -> QuerySet[_T]: ...
    def order_by(self, *field_names: str) -> QuerySet[_T]: ...
```

`/.venv/<path-to-site-packages>/django/db/models/query.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class QuerySet(Generic[_T]):
    def order_by(self, *field_names: str) -> "QuerySet[_T]": ...
```

```py
from django.db.models import Model, ForeignKey, Manager, QuerySet

class BookQuerySet(QuerySet["Book"]):
    def sortable(self) -> "BookQuerySet":
        return self

BookManager = Manager.from_queryset(BookQuerySet)

class Author(Model):
    pass

class Book(Model):
    objects = BookManager()
    author = ForeignKey(Author, on_delete=None, related_name="books")

a = Author()
reveal_type(a.books.all())  # revealed: BookQuerySet
reveal_type(a.books.all().order_by("id"))  # revealed: BookQuerySet
reveal_type(a.books.sortable())  # revealed: BookQuerySet

maybe_author: Author | None = Author()
if maybe_author:
    reveal_type(maybe_author.books.all())  # revealed: BookQuerySet
    reveal_type(maybe_author.books.all().order_by("id"))  # revealed: BookQuerySet
    reveal_type(maybe_author.books.sortable())  # revealed: BookQuerySet
```
