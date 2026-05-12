# Django Custom Field Subclasses

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## Custom CharField subclass resolves to str

A user-defined field that inherits from `CharField` resolves to `str` on instance access.

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

class TrimmedCharField(CharField):
    pass

class Article(Model):
    slug = TrimmedCharField(max_length=50)

a = Article()
reveal_type(a.slug)  # revealed: str
```

## Custom IntegerField subclass resolves to int

A user-defined field inheriting from `IntegerField` resolves to `int` on instance access.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
from django.db.models.fields import IntegerField
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

class IntegerField(Field[int, int]):
    def __init__(self, *, null: bool = False, blank: bool = False, default=None): ...
```

```py
from django.db.models import Model, IntegerField

class BoundedIntegerField(IntegerField):
    pass

class Score(Model):
    value = BoundedIntegerField()

s = Score()
reveal_type(s.value)  # revealed: int
```

## Multi-level custom field chain resolves to base type

A field subclassed two levels deep still inherits the generic parameters from the root field class.

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
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model

_M = TypeVar("_M", bound=Model)

class Manager(Generic[_M]):
    def filter(self, **kwargs: object) -> object: ...
    def create(self, **kwargs: object) -> _M: ...
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

class BaseSlugField(CharField):
    pass

class AutoSlugField(BaseSlugField):
    pass

class Post(Model):
    slug = AutoSlugField(max_length=100)

p = Post()
reveal_type(p.slug)  # revealed: str
```

## Custom field imported from another module falls through to normal inference

When a custom field is referenced via a module attribute (`field_lib.TitleField(...)`) rather than
imported directly, it falls through to normal descriptor inference.

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

`field_lib.py`:

```py
from django.db.models.fields import CharField

class TitleField(CharField):
    pass
```

```py
import field_lib
from django.db.models import Model

class Article(Model):
    title = field_lib.TitleField(max_length=100)

a = Article()
reveal_type(a.title)  # revealed: str
```

## Custom OneToOneField subclass resolves by inheritance

A project-defined relation field should be recognized from its Django base class, not from a
project-specific class name.

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
from django.db.models.fields.related import OneToOneField
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
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
from typing import Generic, TypeVar, overload

_To = TypeVar("_To")

class OneToOneField(Generic[_To]):
    @overload
    def __get__(self, instance: None, owner: type) -> "OneToOneField[_To]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _To: ...
    def __get__(self, instance, owner): ...
    def __init__(self, to: type, *, on_delete, null: bool = False, related_name: str = ""): ...
```

```py
from django.db.models import Model, CharField, OneToOneField

class OptionalProfileLink(OneToOneField):
    pass

class User(Model):
    username = CharField(max_length=100)

class Profile(Model):
    user = OptionalProfileLink(User, on_delete=None, related_name="profile")

p = Profile()
reveal_type(p.user)  # revealed: User
reveal_type(p.user_id)  # revealed: int
u = User()
reveal_type(u.profile)  # revealed: Profile
```

## Custom OneToOneOrNoneField subclass is not special-cased

The classifier should recognize project-specific relation fields by following their Django base
class, even when the local class name comes from a real project.

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
from django.db.models.fields.related import OneToOneField
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
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
from typing import Generic, TypeVar, overload

_To = TypeVar("_To")

class OneToOneField(Generic[_To]):
    @overload
    def __get__(self, instance: None, owner: type) -> "OneToOneField[_To]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _To: ...
    def __get__(self, instance, owner): ...
    def __init__(self, to: type, *, on_delete, null: bool = False, related_name: str = ""): ...
```

```py
from django.db.models import Model, CharField, OneToOneField

class OneToOneOrNoneField(OneToOneField):
    pass

class User(Model):
    username = CharField(max_length=100)

class Profile(Model):
    user = OneToOneOrNoneField(User, on_delete=None, null=True)

p = Profile()
reveal_type(p.user)  # revealed: User | None
reveal_type(p.user_id)  # revealed: int | None
u = User()
reveal_type(u.profile)  # revealed: Profile
```

## Custom enum field value type from enum keyword

Some custom fields store primitive database values but expose enum instances on model objects. When
a recognized Django field is constructed with an `enum=` class argument, ty uses that enum class as
the model attribute type.

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
from django.db.models.manager import Manager
```

`/.venv/<path-to-site-packages>/django/db/models/base.py`:

```py
class Model:
    pass
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar
from django.db.models.base import Model

_M = TypeVar("_M", bound=Model)

class Manager(Generic[_M]):
    def filter(self, **kwargs: object) -> object: ...
    def create(self, **kwargs: object) -> _M: ...
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
    def __init__(self, *, max_length: int = 255, enum: type | None = None, null: bool = False): ...
```

`fields.py`:

```py
from django.db.models import CharField

class EnumBackedField(CharField):
    pass
```

```py
from enum import Enum
from fields import EnumBackedField
from django.db.models import Model

class Status(Enum):
    DONE = "done"
    OPEN = "open"

class Task(Model):
    status = EnumBackedField(enum=Status, null=True)

task = Task()
reveal_type(task.status)  # revealed: Status | None
task.status = Status.DONE
task.status = "done"  # error: [invalid-assignment]
Task.objects.filter(status="done")
Task.objects.filter(status=Status.DONE)
Task.objects.create(status=Status.OPEN)
Task.objects.create(status=object())  # error: [invalid-argument-type]

def filter_status(status: str | None) -> None:
    if status:
        Task.objects.filter(status=status)
```

## Custom relation field imported under an alias resolves by inheritance

The field classifier follows the imported class bound to the local name, so aliases do not need
project-specific special cases either.

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
from django.db.models.fields.related import OneToOneField
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
```

`/.venv/<path-to-site-packages>/django/db/models/fields/related.py`:

```py
from typing import Generic, TypeVar, overload

_To = TypeVar("_To")

class OneToOneField(Generic[_To]):
    @overload
    def __get__(self, instance: None, owner: type) -> "OneToOneField[_To]": ...
    @overload
    def __get__(self, instance: object, owner: type) -> _To: ...
    def __get__(self, instance, owner): ...
    def __init__(self, to: type, *, on_delete, null: bool = False, related_name: str = ""): ...
```

`fields.py`:

```py
from django.db.models import OneToOneField

class OptionalProfileLink(OneToOneField):
    pass
```

```py
from django.db.models import Model, CharField
from fields import OptionalProfileLink as ProfileLink

class User(Model):
    username = CharField(max_length=100)

class Profile(Model):
    user = ProfileLink(User, on_delete=None)

p = Profile()
reveal_type(p.user)  # revealed: User
reveal_type(p.user_id)  # revealed: int
```
