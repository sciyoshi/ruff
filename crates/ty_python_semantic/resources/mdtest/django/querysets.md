# Django QuerySet Lookups

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## Filter keyword lookups are checked against model fields

`filter()`, `exclude()`, and `get()` accept dynamic `**kwargs` in Django's stubs, but Django lookup
keywords still correspond to model fields.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model
from django.db.models.fields import CharField, FloatField, IntegerField

_M = TypeVar("_M", bound=Model)

class QuerySet(Generic[_M]):
    def filter(self, **kwargs: object) -> "QuerySet[_M]": ...
    def exclude(self, **kwargs: object) -> "QuerySet[_M]": ...
    def get(self, **kwargs: object) -> _M: ...
    async def aget(self, **kwargs: object) -> _M: ...
    def order_by(self, *field_names: str) -> "QuerySet[_M]": ...
    def select_related(self, *fields: str) -> "QuerySet[_M]": ...

class Manager(Generic[_M]):
    def filter(self, **kwargs: object) -> QuerySet[_M]: ...
    def exclude(self, **kwargs: object) -> QuerySet[_M]: ...
    def get(self, **kwargs: object) -> _M: ...
    async def aget(self, **kwargs: object) -> _M: ...
    def order_by(self, *field_names: str) -> QuerySet[_M]: ...
    def select_related(self, *fields: str) -> QuerySet[_M]: ...
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
from typing import ClassVar
from django.db.models.options import Options

class Model:
    _meta: ClassVar[Options]
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
from typing import Generic, TypeVar, overload

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")

class Field(Generic[_ST, _GT]):
    @overload
    def __get__(self, instance: None, owner: type) -> "Field[_ST, _GT]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _GT: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance: object, value: _ST) -> None: ...

class CharField(Field[str, str]):
    def __init__(self, *, max_length: int = 255, null: bool = False): ...

class IntegerField(Field[int, int]):
    def __init__(self, *, null: bool = False): ...
```

```py
from django.db.models import Model, CharField, IntegerField

class User(Model):
    name = CharField(max_length=100)
    age = IntegerField()

reveal_type(User.objects.filter(name="Ada"))  # revealed: QuerySet[User]
reveal_type(User.objects.exclude(age__gte=30))  # revealed: QuerySet[User]
reveal_type(User.objects.get(id=1))  # revealed: User
reveal_type(User.objects.get(id="1"))  # revealed: User

User.objects.filter(age=object())  # error: [invalid-argument-type]
User.objects.filter(missing=1)  # error: [unknown-argument]
User.objects.filter(age__isnull=False)
User.objects.filter(name__icontains="a")
User.objects.order_by("name", "-age", "?")
User.objects.order_by("missing")  # error: [unknown-argument]

async def check_async_get() -> None:
    await User.objects.aget(age=object())  # error: [invalid-argument-type]
    await User.objects.aget(missing=1)  # error: [unknown-argument]
```

## Relation lookup paths are checked

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model
from django.db.models.fields import CharField, FloatField, IntegerField
from django.db.models.fields.related import ForeignKey, OneToOneField

_M = TypeVar("_M", bound=Model)

class QuerySet(Generic[_M]):
    def filter(self, **kwargs: object) -> "QuerySet[_M]": ...
    def select_related(self, *fields: str) -> "QuerySet[_M]": ...

class Manager(Generic[_M]):
    def filter(self, **kwargs: object) -> QuerySet[_M]: ...
    def select_related(self, *fields: str) -> QuerySet[_M]: ...
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
from typing import Generic, TypeVar, overload

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")

class Field(Generic[_ST, _GT]):
    @overload
    def __get__(self, instance: None, owner: type) -> "Field[_ST, _GT]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _GT: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance: object, value: _ST) -> None: ...

class CharField(Field[str, str]):
    def __init__(self, *, max_length: int = 255, primary_key: bool = False): ...

class IntegerField(Field[int, int]):
    def __init__(self, *, primary_key: bool = False): ...
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
from typing import Generic, TypeVar, overload

_To = TypeVar("_To")

class ForeignKey(Generic[_To]):
    @overload
    def __get__(self, instance: None, owner: type) -> "ForeignKey[_To]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _To: ...
    def __get__(self, instance, owner): ...
    def __init__(self, to: type, *, on_delete, null: bool = False, related_name: str = "", related_query_name: str = ""): ...

class OneToOneField(ForeignKey[_To]):
    pass
```

```py
from typing import Self
from django.db.models import Model, CharField, ForeignKey, OneToOneField

class Account(Model):
    slug = CharField(max_length=100, primary_key=True)

class User(Model):
    account = ForeignKey(Account, on_delete=None)

class AccessToken(Model):
    user = ForeignKey(User, on_delete=None)

class Profile(Model):
    user = OneToOneField(User, on_delete=None, related_name="profile")
    account = ForeignKey(Account, on_delete=None)

class Badge(Model):
    code = CharField(max_length=100)
    user = OneToOneField(User, on_delete=None, related_name="badge", related_query_name="badge_lookup")

class Post(Model):
    title = CharField(max_length=100)
    author = ForeignKey(User, on_delete=None, related_name="posts", related_query_name="authored_post")

class UserWithMethod(User):
    def has_token(self: Self) -> bool:
        AccessToken.objects.filter(user=self)
        return True

class UserWithImplicitSelf(User):
    def has_token(self) -> bool:
        AccessToken.objects.filter(user=self)
        return True

User.objects.filter(account="team")
User.objects.filter(account_id="team")
User.objects.filter(account_pk="team")
User.objects.filter(account=None)
User.objects.filter(account_id=None)
User.objects.filter(account__slug="team")
AccessToken.objects.filter(user__account_id="team")
AccessToken.objects.filter(user__account_pk="team")
AccessToken.objects.filter(user__account__pk="team")
AccessToken.objects.filter(user__account__slug=1)  # error: [invalid-argument-type]
User.objects.filter(account__isnull=False)
User.objects.filter(account__in=object())
User.objects.filter(authored_post__title="hello")
User.objects.filter(posts__title="hello")  # error: [unknown-argument]
User.objects.filter(badge_lookup__code="staff")
User.objects.filter(pk="1")
User.objects.select_related("account")
User.objects.select_related("profile")
User.objects.select_related("profile__account")
User.objects.select_related("badge_lookup")
User.objects.select_related("profile__account__slug")  # error: [invalid-argument-type]
User.objects.select_related("account__slug")  # error: [invalid-argument-type]
User.objects.select_related("missing")  # error: [unknown-argument]
User.objects.filter(account__slug=1)  # error: [invalid-argument-type]
User.objects.filter(account__missing=1)  # error: [unknown-argument]
```

## Lookup exact types follow Django field descriptor metadata

Some field classes accept a broader exact lookup type than the value returned from model instance
attribute access.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model
from django.db.models.fields import DecimalField, IntegerField

_M = TypeVar("_M", bound=Model)

class QuerySet(Generic[_M]):
    def filter(self, **kwargs: object) -> "QuerySet[_M]": ...

class Manager(Generic[_M]):
    def filter(self, **kwargs: object) -> QuerySet[_M]: ...
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
from decimal import Decimal
from typing import Generic, TypeVar, overload

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")

class Field(Generic[_ST, _GT]):
    @overload
    def __get__(self, instance: None, owner: type) -> "Field[_ST, _GT]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _GT: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance: object, value: _ST) -> None: ...

class DecimalField(Field[Decimal, Decimal]):
    def __init__(self, *, max_digits: int, decimal_places: int): ...

class FloatField(Field[float, float]):
    def __init__(self): ...

class IntegerField(Field[int, int]):
    def __init__(self): ...

class FloatField(Field[float, float]):
    def __init__(self): ...
```

```py
from decimal import Decimal
from django.db.models import Model, DecimalField, IntegerField

class Measurement(Model):
    amount = DecimalField(max_digits=8, decimal_places=2)
    count = IntegerField()

Measurement.objects.filter(amount=Decimal("1.5"))
Measurement.objects.filter(amount=1)
Measurement.objects.filter(amount="1.5")
Measurement.objects.filter(count=1)
Measurement.objects.filter(count="1")
Measurement.objects.filter(count=object())  # error: [invalid-argument-type]
```

## get_or_create defaults are checked

Literal `defaults=` dictionaries are validated against model fields when the keys are statically
known.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model
from django.db.models.fields import CharField, FloatField, IntegerField

_M = TypeVar("_M", bound=Model)

class Manager(Generic[_M]):
    def create(self, **kwargs: object) -> _M: ...
    def acreate(self, **kwargs: object) -> _M: ...
    def filter(self, **kwargs: object) -> object: ...
    def get_or_create(self, defaults: dict[str, object] | None = None, **kwargs: object) -> tuple[_M, bool]: ...
    async def aget_or_create(self, defaults: dict[str, object] | None = None, **kwargs: object) -> tuple[_M, bool]: ...
    def update_or_create(
        self,
        defaults: dict[str, object] | None = None,
        create_defaults: dict[str, object] | None = None,
        **kwargs: object,
    ) -> tuple[_M, bool]: ...
    async def aupdate_or_create(
        self,
        defaults: dict[str, object] | None = None,
        create_defaults: dict[str, object] | None = None,
        **kwargs: object,
    ) -> tuple[_M, bool]: ...
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
from typing import Generic, TypeVar, overload

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")

class Field(Generic[_ST, _GT]):
    @overload
    def __get__(self, instance: None, owner: type) -> "Field[_ST, _GT]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _GT: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance: object, value: _ST) -> None: ...

class CharField(Field[str, str]):
    def __init__(self, *, max_length: int = 255): ...

class IntegerField(Field[int, int]):
    def __init__(self): ...

class FloatField(Field[float, float]):
    def __init__(self): ...
```

```py
from django.db.models import Model, CharField, FloatField, IntegerField

class User(Model):
    name = CharField(max_length=100)
    age = IntegerField()
    rating = FloatField()
    external_id: int

    @property
    def token(self) -> str:
        return self.name

    @token.setter
    def token(self, value: str) -> None:
        self.name = value

User.objects.create(name="Ada", age=30)
User.objects.create(rating=1)
User.objects.create(rating=1.5)
User.objects.create(rating=object())  # error: [invalid-argument-type]
User.objects.create(name=object())  # error: [invalid-argument-type]
User.objects.create(missing=1)  # error: [unknown-argument]
User.objects.create(name__exact="Ada")  # error: [unknown-argument]
User.objects.create(token="secret")
User.objects.create(token=object())  # error: [invalid-argument-type]
User.objects.create(external_id=1)
User.objects.acreate(name="Ada", age=30)
User.objects.acreate(missing=1)  # error: [unknown-argument]
User(name="Ada", age=30, rating=1)
User(name="Ada", rating=1.5)
User(external_id=1)
User(name=object())  # error: [invalid-argument-type]
User(missing=1)  # error: [unknown-argument]
User("Ada", 30)
User("Ada", object())  # error: [invalid-argument-type]
User("Ada", 30, 1, "extra")  # error: [invalid-argument-type]

def build_user(*args: object, **kwargs: object) -> User:
    return User(*args, **kwargs)

User.objects.get_or_create(name="Ada", defaults={"age": 30})
User.objects.get_or_create(name="Ada", defaults={"rating": 1})
User.objects.get_or_create(name="Ada", defaults={"rating": 1.5})
User.objects.get_or_create(name="Ada", defaults={"external_id": int})
User.objects.get_or_create(name="Ada", defaults={"age": lambda: 30})
User.objects.get_or_create(name="Ada", defaults={"age": object()})  # error: [invalid-argument-type]
User.objects.get_or_create(name="Ada", defaults={"token": "secret"})
User.objects.get_or_create(name="Ada", defaults={"token": object()})  # error: [invalid-argument-type]
User.objects.filter(external_id=1)
User.objects.update_or_create(name="Ada", create_defaults={"missing": 1})  # error: [unknown-argument]

async def check_async_defaults() -> None:
    await User.objects.aget_or_create(name=object())  # error: [invalid-argument-type]
    await User.objects.aget_or_create(name="Ada", defaults={"age": object()})  # error: [invalid-argument-type]
    await User.objects.aupdate_or_create(name="Ada", create_defaults={"missing": 1})  # error: [unknown-argument]
```

## values and values_list field lookups

`values()` and `values_list()` accept field lookup strings. `values_list(flat=True)` preserves the
selected field type as the queryset row type when the queryset stubs expose a second row type
parameter.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model
from django.db.models.fields import BooleanField, CharField, FloatField, IntegerField, TextField
from django.db.models.fields.related import ManyToManyField

_M = TypeVar("_M", bound=Model)
_R = TypeVar("_R")

class Expression: ...

class QuerySet(Generic[_M, _R]):
    def annotate(self, *args: object, **kwargs: object) -> "QuerySet[_M, _R]": ...
    def alias(self, *args: object, **kwargs: object) -> "QuerySet[_M, _R]": ...
    def aggregate(self, *args: object, **kwargs: object) -> dict[str, object]: ...
    async def aaggregate(self, *args: object, **kwargs: object) -> dict[str, object]: ...
    def exclude(self, **kwargs: object) -> "QuerySet[_M, _R]": ...
    def filter(self, **kwargs: object) -> "QuerySet[_M, _R]": ...
    def get(self) -> _R: ...
    def order_by(self, *fields: str) -> "QuerySet[_M, _R]": ...
    def prefetch_related(self, *lookups: object) -> "QuerySet[_M, _R]": ...
    def select_related(self, *fields: str) -> "QuerySet[_M, _R]": ...
    def values(self, *fields: str, **expressions: object) -> "QuerySet[_M, dict[str, object]]": ...
    def values_list(self, *fields: str, flat: bool = False, named: bool = False) -> "QuerySet[_M, _R]": ...

class Manager(Generic[_M]):
    def annotate(self, *args: object, **kwargs: object) -> QuerySet[_M, _M]: ...
    def alias(self, *args: object, **kwargs: object) -> QuerySet[_M, _M]: ...
    def aggregate(self, *args: object, **kwargs: object) -> dict[str, object]: ...
    async def aaggregate(self, *args: object, **kwargs: object) -> dict[str, object]: ...
    def filter(self, **kwargs: object) -> QuerySet[_M, _M]: ...
    def order_by(self, *fields: str) -> QuerySet[_M, _M]: ...
    def prefetch_related(self, *lookups: object) -> QuerySet[_M, _M]: ...
    def select_related(self, *fields: str) -> QuerySet[_M, _M]: ...
    def values(self, *fields: str, **expressions: object) -> QuerySet[_M, dict[str, object]]: ...
    def values_list(self, *fields: str, flat: bool = False, named: bool = False) -> QuerySet[_M, _M]: ...

class Prefetch:
    def __init__(self, lookup: str, queryset: object = ..., *, to_attr: str | None = None): ...

class GenericPrefetch(Prefetch): ...

class F(Expression):
    def __init__(self, name: str): ...

class Value(Expression):
    def __init__(self, value: object): ...

class When:
    def __init__(self, **kwargs: object): ...

class Case(Expression):
    def __init__(self, *cases: When, default: object = ..., output_field: object = ...): ...

class Func(Expression):
    def __init__(self, *expressions: object, output_field: object = ...): ...

class RawSQL(Expression):
    def __init__(self, sql: str, params: object, output_field: object = ...): ...

class Subquery(Expression):
    def __init__(self, queryset: object, output_field: object = ...): ...

class Aggregate(Expression): ...

class Count(Aggregate):
    def __init__(self, expression: str): ...

class Max(Aggregate):
    def __init__(self, expression: str): ...
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
from typing import Generic, TypeVar, overload

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")

class Field(Generic[_ST, _GT]):
    @overload
    def __get__(self, instance: None, owner: type) -> "Field[_ST, _GT]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _GT: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance: object, value: _ST) -> None: ...

class BooleanField(Field[bool, bool]):
    def __init__(self): ...

class CharField(Field[str, str]):
    def __init__(self, *, max_length: int = 255): ...

class IntegerField(Field[int, int]):
    def __init__(self): ...

class FloatField(Field[float, float]):
    def __init__(self): ...

class TextField(Field[str, str]):
    def __init__(self): ...
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
from typing import Generic, TypeVar, overload

_To = TypeVar("_To")

class ManyToManyField(Generic[_To]):
    @overload
    def __get__(self, instance: None, owner: type) -> "ManyToManyField[_To]": ...
    @overload
    def __get__(self, instance: object, owner: type): ...
    def __get__(self, instance, owner): ...
    def __init__(self, to: type | str, *, related_name: str = ""): ...

class ForeignKey(Generic[_To]):
    @overload
    def __get__(self, instance: None, owner: type) -> "ForeignKey[_To]": ...
    @overload
    def __get__(self, instance: object, owner: type): ...
    def __get__(self, instance, owner): ...
    def __init__(self, to: type | str): ...
```

`/.venv/<path-to-site-packages>/django/db/models/options.py`:

```py
from typing import Any
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.fields import Field
from django.db.models.fields.reverse_related import ForeignObjectRel

class Options:
    def get_field(self, field_name: str) -> Field[Any, Any] | ForeignObjectRel | GenericForeignKey: ...
```

`/.venv/<path-to-site-packages>/django/db/models/fields/reverse_related.py`:

```py
class ForeignObjectRel: ...
```

`/.venv/<path-to-site-packages>/django/contrib/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/contrib/contenttypes/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/contrib/contenttypes/fields.py`:

```py
class GenericForeignKey: ...
```

```py
from typing import Any
from django.db.models import (
    Model,
    BooleanField,
    Case,
    CharField,
    Count,
    F,
    FloatField,
    Func,
    GenericPrefetch,
    IntegerField,
    Max,
    Prefetch,
    RawSQL,
    Subquery,
    TextField,
    Value,
    When,
    QuerySet,
)
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields import Field
from django.contrib.contenttypes.fields import GenericForeignKey

def accepts_field(field: Field[Any, Any]) -> None: ...

class User(Model):
    name = CharField(max_length=100)
    age = IntegerField()
    rating = FloatField()
    accounts = ManyToManyField("Account")

class Account(Model):
    handle = CharField(max_length=100)

class Activity(Model):
    accounts = ManyToManyField(Account, related_name="activities")
    content_object = GenericForeignKey()

class Login(Model):
    user = ForeignKey(User)

class UserQuerySet(QuerySet[User, User]):
    def annotate(self, *args: object, **kwargs: object) -> "UserQuerySet":
        return self
    def filter(self, **kwargs: object) -> "UserQuerySet":
        return self

accepts_field(User._meta.get_field("name"))
reveal_type(User._meta.get_field("name"))  # revealed: CharField
reveal_type(User._meta.get_field(field_name="age"))  # revealed: IntegerField
reveal_type(User._meta.get_field("accounts"))  # revealed: ManyToManyField[Unknown]
reveal_type(Login._meta.get_field("user"))  # revealed: ForeignKey[Unknown]
reveal_type(Login._meta.get_field("user_id"))  # revealed: ForeignKey[Unknown]
reveal_type(Account._meta.get_field("activities"))  # revealed: ForeignObjectRel
reveal_type(Activity._meta.get_field("content_object"))  # revealed: GenericForeignKey
User._meta.get_field("missing")  # error: [unknown-argument]
User._meta.get_field(field_name="missing")  # error: [unknown-argument]
User.objects.values("name", "age")
User.objects.values("missing")  # error: [unknown-argument]
User.objects.values_list("missing", flat=True)  # error: [unknown-argument]
User.objects.values_list("name", "age", flat=True)  # error: [invalid-argument-type]
User.objects.values_list("name", flat=True, named=True)  # error: [invalid-argument-type]
User.objects.filter(accounts=Account())
User.objects.filter(accounts=1)
User.objects.filter(accounts=None)
User.objects.filter(accounts=object())  # error: [invalid-argument-type]
User.objects.filter(accounts__handle="ada")
User.objects.filter(accounts__isnull=True)
Account.objects.filter(activities__in=[Activity()])
Account.objects.filter(activities__isnull=True)
User.objects.filter(rating__lte=1)
User.objects.filter(rating__lte=1.5)
User.objects.filter(rating__lte=object())  # error: [invalid-argument-type]
User.objects.prefetch_related("missing")  # error: [unknown-argument]
User.objects.prefetch_related("name")  # error: [invalid-argument-type]
User.objects.prefetch_related("login_set")
User.objects.prefetch_related(Prefetch("missing", to_attr="bad"))  # error: [unknown-argument]
Activity.objects.prefetch_related(GenericPrefetch("content_object"))
Activity.objects.prefetch_related(GenericPrefetch("accounts"))  # error: [invalid-argument-type]
Activity.objects.prefetch_related(GenericPrefetch("missing"))  # error: [unknown-argument]
User.objects.prefetch_related(Prefetch("accounts", to_attr="name"))  # error: [invalid-argument-type]
User.objects.values("name").prefetch_related(Prefetch("accounts", to_attr="name"))  # error: [invalid-argument-type]
User.objects.values("name").prefetch_related(Prefetch("accounts", to_attr="age"))
# fmt: off
User.objects.annotate(display_name=Value("Ada")).prefetch_related(Prefetch("accounts", to_attr="display_name"))  # error: [invalid-argument-type]
User.objects.prefetch_related(Prefetch("accounts", to_attr="cached_accounts"), Prefetch("accounts", to_attr="cached_accounts"))  # error: [invalid-argument-type]
# fmt: on
reveal_type(User.objects.values("name"))  # revealed: QuerySet[User, <TypedDict with items 'name'>]
reveal_type(User.objects.values("name", "age"))  # revealed: QuerySet[User, <TypedDict with items 'age', 'name'>]
reveal_type(User.objects.values())  # revealed: QuerySet[User, <TypedDict with items 'age', 'id', 'name', 'rating'>]
reveal_type(User.objects.values(display_name="Ada"))  # revealed: QuerySet[User, <TypedDict with items 'display_name'>]
User.objects.values(display_name="Ada").order_by("display_name")
User.objects.values("name").order_by("display_name")  # error: [unknown-argument]
reveal_type(User.objects.values("name", display_age=1))  # revealed: QuerySet[User, <TypedDict with items 'display_age', 'name'>]
reveal_type(User.objects.values_list("name"))  # revealed: QuerySet[User, tuple[str]]
reveal_type(User.objects.values_list("name", "age"))  # revealed: QuerySet[User, tuple[str, str | int]]
reveal_type(User.objects.values_list("name", "age", named=True))  # revealed: QuerySet[User, Row]
reveal_type(User.objects.values_list(flat=True))  # revealed: QuerySet[User, str | int]
reveal_type(User.objects.values_list())  # revealed: QuerySet[User, tuple[str | int, str, str | int, float]]
reveal_type(User.objects.values_list(named=True))  # revealed: QuerySet[User, Row]
reveal_type(User.objects.values_list("name", flat=True))  # revealed: QuerySet[User, str]
reveal_type(User.objects.values_list("age", flat=True))  # revealed: QuerySet[User, str | int]
reveal_type(User.objects.annotate(display_name="Ada").get().display_name)  # revealed: Literal["Ada"]
reveal_type(User.objects.alias(score=1).get().score)  # revealed: Literal[1]
User.objects.annotate(display_name="Ada").filter(display_name="Ada")
dynamic_annotations: dict[str, object] = {}
User.objects.annotate(**{"display_name": Value("Ada")}).filter(display_name="Ada")
User.objects.annotate(**dynamic_annotations, display_name=Value("Ada")).filter(display_name="Ada")
User.objects.annotate(display_name=Value("Ada")).select_related("display_name")

def local_annotation_dict() -> None:
    annotations = {"display_name": Value("Ada")}
    User.objects.annotate(**annotations).filter(display_name="Ada")
    User.objects.annotate(**annotations).values("display_name")
    reveal_type(User.objects.annotate(**annotations).get().display_name)  # revealed: Literal["Ada"]

UserQuerySet().annotate(display_name=Value("Ada")).filter(display_name="Ada")
UserQuerySet().annotate(display_name=Value("Ada")).values("display_name")
UserQuerySet().annotate(score=Value(1)).order_by("score")
# fmt: off
reveal_type(User.objects.annotate(display_name="Ada").values("display_name"))  # revealed: QuerySet[User & <Protocol with members 'display_name'>, <TypedDict with items 'display_name'>]
# fmt: on
User.objects.annotate(name=Value("Ada"))  # error: [invalid-argument-type]
User.objects.annotate(display_name=Value("Ada")).annotate(display_name=Value("Grace"))  # error: [invalid-argument-type]
User.objects.values("age").annotate(age=Value(1))  # error: [invalid-argument-type]
# fmt: off
reveal_type(User.objects.values("name").annotate(age=Value(1)).values("age"))  # revealed: QuerySet[User, <TypedDict with items 'age'>]
User.objects.values_list("age").annotate(age=Value(1))  # error: [invalid-argument-type]
reveal_type(User.objects.values_list("name").annotate(age=Value(1)).values("age"))  # revealed: QuerySet[User, <TypedDict with items 'age'>]
reveal_type(User.objects.values_list("name", flat=True).annotate(age=Value(1)).values("age"))  # revealed: QuerySet[User, <TypedDict with items 'age'>]
User.objects.values_list("age", named=True).annotate(age=Value(1))  # error: [invalid-argument-type]
reveal_type(User.objects.values_list("name", named=True).annotate(age=Value(1)).values("age"))  # revealed: QuerySet[User, <TypedDict with items 'age'>]
# fmt: on
reveal_type(User.objects.annotate(display_name=F("name")).get().display_name)  # revealed: str
User.objects.annotate(display_name=F("name")).filter(display_name="Ada")
User.objects.annotate(display_name=F("name")).filter(display_name__icontains="a")
User.objects.annotate(display_name=F("name")).filter(display_name__icontains=1)  # error: [invalid-argument-type]
reveal_type(User.objects.annotate(display_name=Value("Ada")).get().display_name)  # revealed: Literal["Ada"]
User.objects.annotate(display_name=Value("Ada")).filter(display_name="Ada")
bucket = (
    User.objects.annotate(bucket=Case(When(age=1, then=Value("one")), default=Value(""), output_field=TextField())).get().bucket
)
reveal_type(bucket)  # revealed: str
User.objects.annotate(bucket=Case(When(age=1, then=Value("one")), default=Value(""), output_field=TextField())).exclude(bucket="")
# fmt: off
reveal_type(User.objects.annotate(display_name=Case(When(age=1, then="name"), default="name")).get().display_name)  # revealed: str
User.objects.annotate(display_name=Case(When(age=1, then="name"), default="name")).filter(display_name="Ada")
User.objects.annotate(display_name=Case(When(age=1, then="name"), default="name")).filter(display_name__icontains=1)  # error: [invalid-argument-type]
# fmt: on
score = User.objects.annotate(score=Subquery(User.objects.values("age"), output_field=IntegerField())).get().score
reveal_type(score)  # revealed: int
User.objects.annotate(score=Subquery(User.objects.values("age"), output_field=IntegerField())).filter(score__gt=0)
reveal_type(User.objects.annotate(flag=RawSQL("1 = 1", [], output_field=BooleanField())).get().flag)  # revealed: bool
User.objects.annotate(flag=RawSQL("1 = 1", [], output_field=BooleanField())).filter(flag=True)
User.objects.annotate(flag=RawSQL("1 = 1", [])).filter(flag=True)
reveal_type(User.objects.annotate(rank=Func(F("age"), output_field=IntegerField())).get().rank)  # revealed: int
User.objects.annotate(rank=Func(F("age"), output_field=IntegerField())).filter(rank__gte=1)
User.objects.annotate(rank=Func(F("age"))).filter(rank__gte=1)
reveal_type(User.objects.annotate(total=Count("age")).get().total)  # revealed: int
User.objects.annotate(total=Count("age")).filter(total=1)
User.objects.annotate(total=Count("age")).filter(total__gte=1)
User.objects.annotate(total=Count("age")).filter(total__gte="one")  # error: [invalid-argument-type]
User.objects.annotate(total=Count("age")).filter(total__isnull=False)
User.objects.annotate(total=Count("age")).order_by("total__gte")
reveal_type(User.objects.annotate(Count("age")).get().age__count)  # revealed: int
User.objects.annotate(Count("age")).filter(age__count=1)
User.objects.annotate(Count("age")).filter(age__count__gt=1)
User.objects.annotate(Count("age")).values("age__count")
User.objects.annotate(Count("age")).order_by("age__count")
User.objects.annotate(Count("age")).filter(age__count__gt="one")  # error: [invalid-argument-type]
# fmt: off
reveal_type(User.objects.annotate(total=Count("age")).values("total"))  # revealed: QuerySet[User & <Protocol with members 'total'>, <TypedDict with items 'total'>]
# fmt: on
reveal_type(User.objects.aggregate(total=Count("age")))  # revealed: <TypedDict with items 'total'>
reveal_type(User.objects.aggregate(total=Count("age"))["total"])  # revealed: int
reveal_type(User.objects.aggregate(Count("age")))  # revealed: <TypedDict with items 'age__count'>
reveal_type(User.objects.aggregate(Count("age"))["age__count"])  # revealed: int
reveal_type(User.objects.aggregate(Max("name"))["name__max"])  # revealed: str

async def aggregate_async() -> None:
    reveal_type(User.objects.aaggregate(total=Count("age")))  # revealed: CoroutineType[Any, Any, <TypedDict with items 'total'>]
    reveal_type((await User.objects.aaggregate(total=Count("age")))["total"])  # revealed: int

# fmt: off
reveal_type(User.objects.prefetch_related(Prefetch("accounts", queryset=Account.objects.filter(), to_attr="cached_accounts")).get().cached_accounts)  # revealed: list[Account]
reveal_type(User.objects.prefetch_related(Prefetch("accounts", to_attr="lookup_accounts")).get().lookup_accounts)  # revealed: list[Account]
reveal_type(User.objects.prefetch_related(Prefetch("login_set", to_attr="cached_logins")).get().cached_logins)  # revealed: list[Login]
# fmt: on
```

## queryset field-name methods validate literal fields

`defer()`, `only()`, `earliest()`, and `latest()` also take field names and should report unknown
literal field names.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField

_M = TypeVar("_M", bound=Model)

class QuerySet(Generic[_M]):
    def defer(self, *fields: str) -> "QuerySet[_M]": ...
    def only(self, *fields: str) -> "QuerySet[_M]": ...

class Manager(Generic[_M]):
    def defer(self, *fields: str) -> QuerySet[_M]: ...
    def only(self, *fields: str) -> QuerySet[_M]: ...
    def order_by(self, *fields: str) -> QuerySet[_M]: ...
    def earliest(self, *fields: str) -> _M: ...
    def latest(self, *fields: str) -> _M: ...
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
from typing import Generic, TypeVar, overload

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")

class Field(Generic[_ST, _GT]):
    @overload
    def __get__(self, instance: None, owner: type) -> "Field[_ST, _GT]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _GT: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance: object, value: _ST) -> None: ...

class CharField(Field[str, str]):
    def __init__(self, *, max_length: int = 255): ...

class IntegerField(Field[int, int]):
    def __init__(self): ...
```

```py
from django.db.models import Model, CharField, IntegerField

class User(Model):
    name = CharField(max_length=100)
    age = IntegerField()

User.objects.defer("name").only("age")
User.objects.defer("missing")  # error: [unknown-argument]
User.objects.only("missing")  # error: [unknown-argument]
User.objects.earliest("name")
User.objects.latest("-age")
User.objects.order_by("age__year")
User.objects.order_by("name__exact")  # error: [invalid-argument-type]
User.objects.latest("name__contains")  # error: [invalid-argument-type]
User.objects.earliest("missing")  # error: [unknown-argument]
User.objects.latest("missing")  # error: [unknown-argument]
```

## bulk field collections validate literal fields

`bulk_update()` requires non-empty concrete non-primary-key field names. `bulk_create()` validates
literal `update_fields` and `unique_fields` collections, allowing `pk` only for `unique_fields`.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField
from django.db.models.fields.related import ManyToManyField

_M = TypeVar("_M", bound=Model)

class QuerySet(Generic[_M]):
    def bulk_update(self, objs: list[_M], fields: list[str]) -> None: ...

class Manager(Generic[_M]):
    def bulk_update(self, objs: list[_M], fields: list[str]) -> None: ...
    def bulk_create(
        self,
        objs: list[_M],
        batch_size: int | None = None,
        ignore_conflicts: bool = False,
        update_conflicts: bool = False,
        update_fields: list[str] | None = None,
        unique_fields: list[str] | None = None,
    ) -> None: ...
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
from typing import Generic, TypeVar, overload

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")

class Field(Generic[_ST, _GT]):
    @overload
    def __get__(self, instance: None, owner: type) -> "Field[_ST, _GT]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _GT: ...
    def __get__(self, instance, owner): ...
    def __set__(self, instance: object, value: _ST) -> None: ...

class CharField(Field[str, str]):
    def __init__(self, *, max_length: int = 255, primary_key: bool = False): ...

class IntegerField(Field[int, int]):
    def __init__(self): ...
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
class ManyToManyField:
    def __init__(self, to, *, related_name: str | None = None): ...
```

```py
from django.db.models import Model, CharField, IntegerField, ManyToManyField

class Tag(Model):
    label = CharField(max_length=100)

class Article(Model):
    slug = CharField(max_length=100, primary_key=True)
    title = CharField(max_length=100)
    views = IntegerField()
    tags = ManyToManyField(Tag)

Article.objects.bulk_update([], ["title", "views"])
Article.objects.bulk_update([], [])  # error: [invalid-argument-type]
Article.objects.bulk_update([], ["missing"])  # error: [unknown-argument]
Article.objects.bulk_update([], ["slug"])  # error: [invalid-argument-type]
Article.objects.bulk_update([], ["tags"])  # error: [invalid-argument-type]
Article.objects.bulk_create([], update_fields=["title"], unique_fields=["pk", "slug"])
Article.objects.bulk_create([], update_fields=["slug"])  # error: [invalid-argument-type]
Article.objects.bulk_create([], update_fields=["missing"])  # error: [unknown-argument]
Article.objects.bulk_create([], unique_fields=["missing"])  # error: [unknown-argument]
Article.objects.bulk_create([], None, False, True, ["title"], ["pk"])
Article.objects.bulk_create([], None, False, True, ["slug"])  # error: [invalid-argument-type]
Article.objects.bulk_create([], None, False, True, ["missing"])  # error: [unknown-argument]
Article.objects.bulk_create([], None, False, True, ["title"], ["tags"])  # error: [invalid-argument-type]
```
