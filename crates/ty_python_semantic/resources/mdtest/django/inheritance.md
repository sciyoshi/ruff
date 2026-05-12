# Django Model Inheritance

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## Fields declared on a parent model are visible on the child

When a concrete model inherits from another model, all fields declared on the parent are accessible
on instances of the child class, with the same types as on the parent.

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
    def __init__(self, *, max_length: int = 255, null: bool = False, blank: bool = False, default=None): ...
```

```py
from django.db.models import Model, CharField

class TimestampedModel(Model):
    created_at = CharField(max_length=50)

class Post(TimestampedModel):
    title = CharField(max_length=200)

p = Post()
reveal_type(p.title)  # revealed: str
reveal_type(p.created_at)  # revealed: str
```

## Child model can override a parent field

A child model can redeclare a field that exists on a parent. The child's declaration takes
precedence.

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
    def __init__(self, *, max_length: int = 255, null: bool = False, blank: bool = False, default=None): ...

class IntegerField(Field[int, int]):
    def __init__(self, *, null: bool = False, blank: bool = False, default=None): ...
```

```py
from django.db.models import Model, CharField, IntegerField

class Base(Model):
    value = CharField(max_length=50)

class Child(Base):
    value = IntegerField()

c = Child()
reveal_type(c.value)  # revealed: int
```

## Multi-level inheritance propagates fields correctly

Fields are visible through multiple levels of model inheritance.

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
    def __init__(self, *, max_length: int = 255, null: bool = False, blank: bool = False, default=None): ...

class IntegerField(Field[int, int]):
    def __init__(self, *, null: bool = False, blank: bool = False, default=None): ...
```

```py
from django.db.models import Model, CharField, IntegerField

class GrandParent(Model):
    gp_field = CharField(max_length=10)

class Parent(GrandParent):
    p_field = IntegerField()

class Child(Parent):
    c_field = CharField(max_length=20)

c = Child()
reveal_type(c.c_field)  # revealed: str
reveal_type(c.p_field)  # revealed: int
reveal_type(c.gp_field)  # revealed: str
```

## Multi-table inheritance synthesizes parent links

Concrete Django model inheritance adds an implicit `OneToOneField` from the child table to the
parent table. The generated `<parent>_ptr` and `<parent>_ptr_id` names are accepted anywhere normal
model fields are accepted.

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
from django.db.models.fields import AutoField, CharField
from django.db.models.manager import Manager

_M = TypeVar("_M", bound=Model)
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    def __init__(self, **kwargs): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model

_M = TypeVar("_M", bound=Model)

class QuerySet(Generic[_M]):
    def filter(self, **kwargs: object) -> "QuerySet[_M]": ...

class Manager(Generic[_M]):
    def create(self, **kwargs: object) -> _M: ...
    def filter(self, **kwargs: object) -> QuerySet[_M]: ...
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
class AutoField:
    def __init__(self, *, primary_key: bool = False): ...

class CharField:
    def __init__(self, *, max_length: int = 255): ...
```

```py
from django.db.models import Model, AutoField, CharField

class Notification(Model):
    id = AutoField(primary_key=True)
    verb = CharField(max_length=100)

class UserNotification(Notification):
    extra = CharField(max_length=100)

notification = Notification()
user_notification = UserNotification(notification_ptr=notification)
reveal_type(user_notification.notification_ptr)  # revealed: Notification
reveal_type(user_notification.notification_ptr_id)  # revealed: int
UserNotification.objects.create(notification_ptr=notification)
UserNotification.objects.create(notification_ptr_id=1)
UserNotification.objects.filter(notification_ptr=notification)
UserNotification.objects.filter(notification_ptr_id=1)
UserNotification.objects.filter(notification_ptr=object())  # error: [invalid-argument-type]

DjangoNotification = Notification

class AliasedUserNotification(DjangoNotification):
    extra = CharField(max_length=100)

aliased = AliasedUserNotification(notification_ptr=notification)
reveal_type(aliased.notification_ptr)  # revealed: Notification
AliasedUserNotification.objects.create(notification_ptr=notification)
```

## Abstract model bases do not synthesize parent links

Abstract Django models contribute their fields to concrete subclasses, but they do not have their
own database table. A concrete subclass of abstract models should not get `<abstract>_ptr` parent
links, and an explicit primary key on the concrete model remains the `pk` lookup type.

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
from django.db.models.fields import AutoField, CharField

_M = TypeVar("_M", bound=Model)

class QuerySet(Generic[_M]):
    def filter(self, **kwargs: object) -> "QuerySet[_M]": ...

class Manager(Generic[_M]):
    def filter(self, **kwargs: object) -> QuerySet[_M]: ...
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    def __init__(self, **kwargs): ...
```

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
class AutoField:
    def __init__(self, *, primary_key: bool = False): ...

class CharField:
    def __init__(self, *, max_length: int = 255): ...
```

```py
from django.db.models import Model, AutoField, CharField

class AbstractBaseUser(Model):
    password = CharField(max_length=128)

    class Meta:
        abstract = True

class PermissionsMixin(Model):
    marker = CharField(max_length=128)

    class Meta:
        abstract = True

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    email = CharField(max_length=150)

    class Meta:
        abstract = True

class User(AbstractUser):
    id = AutoField(primary_key=True)

user = User()
reveal_type(user.pk)  # revealed: int
reveal_type(user.password)  # revealed: str
User.objects.filter(pk=1)
User.objects.filter(abstractbaseuser_ptr=AbstractBaseUser())  # error: [unknown-argument]
User.objects.filter(permissionsmixin_ptr=PermissionsMixin())  # error: [unknown-argument]
```

## Diamond inheritance uses MRO to resolve conflicting field names

When two parent models declare a field with the same name, Python's C3 linearization (MRO)
determines which definition wins. The first class in the MRO that defines the field takes
precedence, so the order of bases in the subclass declaration matters.

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
    def __init__(self, *, max_length: int = 255, null: bool = False, blank: bool = False, default=None): ...

class IntegerField(Field[int, int]):
    def __init__(self, *, null: bool = False, blank: bool = False, default=None): ...
```

```py
from django.db.models import Model, CharField, IntegerField

class MixinA(Model):
    value = CharField(max_length=50)

class MixinB(Model):
    value = IntegerField()

class Concrete(MixinA, MixinB):
    pass

c = Concrete()
reveal_type(c.value)  # revealed: str
```
