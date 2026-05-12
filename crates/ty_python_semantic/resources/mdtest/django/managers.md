# Django Model Managers

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## Default objects manager is specialized to model

Django adds an `objects` manager to model classes that do not define their own manager.

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

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
class CharField:
    def __init__(self, *, max_length: int = 255): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, CharField

class Article(Model):
    title = CharField(max_length=100)

reveal_type(Article.objects)  # revealed: Manager[Article]
reveal_type(Article.objects.get())  # revealed: Article
reveal_type(Article._default_manager)  # revealed: Manager[Article]
reveal_type(Article._default_manager.get())  # revealed: Article
```

## Default and base manager attributes are specialized to model

Django also exposes `_default_manager` and `_base_manager` on model classes.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
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

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model

class Article(Model):
    pass

reveal_type(Article._default_manager)  # revealed: Manager[Article]
reveal_type(Article._default_manager.get())  # revealed: Article
reveal_type(Article._base_manager)  # revealed: Manager[Article]
reveal_type(Article._base_manager.get())  # revealed: Article
```

## Default manager uses first declared manager

When a model declares a manager under a custom attribute, Django uses it as `_default_manager`.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
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

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, Manager

class ArticleManager(Manager["Article"]):
    def published(self) -> "Article":
        return self.get()

class Article(Model):
    published_objects = ArticleManager()

reveal_type(Article.published_objects)  # revealed: ArticleManager
reveal_type(Article._default_manager)  # revealed: ArticleManager
reveal_type(Article._default_manager.get())  # revealed: Article
reveal_type(Article._default_manager.published())  # revealed: Article
```

## Bare explicit manager is specialized to model

Django binds an explicitly declared `Manager()` to the model that owns it.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
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

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, Manager

class Article(Model):
    objects = Manager()

reveal_type(Article.objects)  # revealed: Manager[Article]
reveal_type(Article.objects.get())  # revealed: Article
```

## Generic custom manager is specialized to model

A generic custom manager instantiated without explicit type arguments is bound to the owning model.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
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

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from typing import Generic, TypeVar
from django.db.models import Model, Manager

_T = TypeVar("_T")

class ArticleManager(Manager[_T], Generic[_T]):
    def published(self) -> _T:
        return self.get()

class Article(Model):
    objects = ArticleManager()

reveal_type(Article.objects)  # revealed: ArticleManager[Article]
reveal_type(Article.objects.get())  # revealed: Article
reveal_type(Article.objects.published())  # revealed: Article
reveal_type(Article._default_manager)  # revealed: ArticleManager[Article]
reveal_type(Article._default_manager.published())  # revealed: Article
```

## Non-generic custom manager keeps custom methods and model type

A custom manager that subclasses `Manager` without type parameters still has inherited manager
methods bound to the owning model.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
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

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, Manager

class ArticleManager(Manager):
    def custom(self) -> int:
        return 1

class Article(Model):
    objects = ArticleManager()

reveal_type(Article.objects.custom())  # revealed: int
reveal_type(Article._default_manager.custom())  # revealed: int
```

## Inherited explicit manager is specialized to child model

When a model inherits a declared manager from a parent model, Django binds the manager to the child
model.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
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

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, Manager

class Parent(Model):
    objects = Manager()

class Child(Parent):
    pass

reveal_type(Parent.objects)  # revealed: Manager[Parent]
reveal_type(Parent.objects.get())  # revealed: Parent
reveal_type(Child.objects)  # revealed: Manager[Child]
reveal_type(Child.objects.get())  # revealed: Child
reveal_type(Child._default_manager)  # revealed: Manager[Child]
reveal_type(Child._default_manager.get())  # revealed: Child
```

## Managers inherited from abstract models are specialized to child model

Django copies managers inherited from abstract bases onto the concrete child model.

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

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
class CharField:
    def __init__(self, *, max_length: int = 255): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from typing import Generic, TypeVar
from django.db.models import Model, CharField, Manager

_T = TypeVar("_T")

class NameManager(Manager[_T], Generic[_T]):
    def named(self) -> _T:
        return self.get()

class ValueManager(Manager[_T], Generic[_T]):
    def valued(self) -> _T:
        return self.get()

class AbstractName(Model):
    class Meta:
        abstract = True

    name = CharField(max_length=50)
    names = NameManager()

class AbstractValue(Model):
    class Meta:
        abstract = True

    value = CharField(max_length=50)
    values = ValueManager()

class Concrete(AbstractName, AbstractValue):
    pass

reveal_type(AbstractName.names)  # revealed: NameManager[AbstractName]
reveal_type(AbstractName.names.named())  # revealed: AbstractName
reveal_type(AbstractValue.values)  # revealed: ValueManager[AbstractValue]
reveal_type(AbstractValue.values.valued())  # revealed: AbstractValue
reveal_type(Concrete.names)  # revealed: NameManager[Concrete]
reveal_type(Concrete.names.named())  # revealed: Concrete
reveal_type(Concrete.values)  # revealed: ValueManager[Concrete]
reveal_type(Concrete.values.valued())  # revealed: Concrete
reveal_type(Concrete._default_manager)  # revealed: NameManager[Concrete]
reveal_type(Concrete._default_manager.named())  # revealed: Concrete
```

## Meta manager names select default and base managers

Django's `Meta.default_manager_name` and `Meta.base_manager_name` select manager attributes by name.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/db/models/__init__.py`:

```py
from django.db.models.base import Model
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

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, Manager

class PublicManager(Manager["Article"]):
    def visible(self) -> "Article":
        return self.get()

class AllManager(Manager["Article"]):
    def any_status(self) -> "Article":
        return self.get()

class Article(Model):
    public = PublicManager()
    all_objects = AllManager()

    class Meta:
        default_manager_name = "public"
        base_manager_name = "all_objects"

reveal_type(Article._default_manager)  # revealed: PublicManager
reveal_type(Article._default_manager.visible())  # revealed: Article
reveal_type(Article._base_manager)  # revealed: AllManager
reveal_type(Article._base_manager.any_status())  # revealed: Article
```

## Manager queryset methods preserve model type

Once ty synthesizes the default manager as `Manager[Model]`, queryset-returning methods declared by
Django stubs should preserve the concrete model type.

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
from django.db.models.query import QuerySet
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

`/.venv/<path-to-site-packages>/django/db/models/query.py`:

```py
from typing import Any, Generic, TypeVar

_T = TypeVar("_T")

class QuerySet(Generic[_T]):
    def filter(self, **kwargs: Any) -> "QuerySet[_T]": ...
    def first(self) -> _T | None: ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Any, Generic, TypeVar
from django.db.models.query import QuerySet

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def all(self) -> QuerySet[_T]: ...
    def filter(self, **kwargs: Any) -> QuerySet[_T]: ...
```

```py
from django.db.models import Model, CharField

class Article(Model):
    title = CharField(max_length=100)

reveal_type(Article.objects.all())  # revealed: QuerySet[Article]
reveal_type(Article.objects.filter(title="Django"))  # revealed: QuerySet[Article]
reveal_type(Article.objects.filter(title="Django").first())  # revealed: Article | None
```

## Explicit objects manager is preserved

When a model defines `objects` explicitly, ty should use the class-body declaration instead of
synthesizing the default manager.

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

`/.venv/<path-to-site-packages>/django/db/models/fields/__init__.py`:

```py
class CharField:
    def __init__(self, *, max_length: int = 255): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    pass
```

```py
from django.db.models import Model, CharField

class CustomManager:
    pass

class Article(Model):
    title = CharField(max_length=100)
    objects = CustomManager()

reveal_type(Article.objects)  # revealed: CustomManager
```

## Manager from_queryset exposes queryset methods

Django copies public queryset methods onto managers created with `Manager.from_queryset`.

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
from django.db.models.query import QuerySet
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

`/.venv/<path-to-site-packages>/django/db/models/query.py`:

```py
from typing import Any, Generic, TypeVar

_T = TypeVar("_T")

class QuerySet(Generic[_T]):
    def filter(self, **kwargs: Any) -> "QuerySet[_T]": ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")
_M = TypeVar("_M", bound="Manager")

class Manager(Generic[_T]):
    @classmethod
    def from_queryset(cls: type[_M], queryset_cls) -> type[_M]: ...
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, CharField, Manager, QuerySet

class CacheQuerySet(QuerySet[_T]):
    def nocache(self) -> "CacheQuerySet[_T]":
        raise NotImplementedError

class ArticleQuerySet(CacheQuerySet["Article"]):
    def visible(self) -> "ArticleQuerySet":
        raise NotImplementedError
    def get_visible(self) -> "Article | None":
        raise NotImplementedError

ArticleManager = Manager.from_queryset(ArticleQuerySet)

class Article(Model):
    title = CharField(max_length=100)
    objects = ArticleManager()

reveal_type(Article.objects.get())  # revealed: Article
reveal_type(Article.objects.visible())  # revealed: ArticleQuerySet
reveal_type(Article.objects.nocache())  # revealed: CacheQuerySet[_T@CacheQuerySet]
reveal_type(Article.objects.all())  # revealed: ArticleQuerySet
reveal_type(Article.objects.order_by("title"))  # revealed: ArticleQuerySet
Article.objects.filter(missing=1)  # error: [unknown-argument]
article = Article.objects.annotate(score=1).get_visible()
if article is not None:
    reveal_type(article.score)  # revealed: Literal[1]
```

## QuerySet as_manager exposes queryset methods

Django also creates a manager from queryset methods via `QuerySet.as_manager()`.

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
from django.db.models.query import QuerySet
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

`/.venv/<path-to-site-packages>/django/db/models/query.py`:

```py
from typing import Any, Generic, TypeVar

_T = TypeVar("_T")

class QuerySet(Generic[_T]):
    def filter(self, **kwargs: Any) -> "QuerySet[_T]": ...
    @classmethod
    def as_manager(cls): ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    def get(self) -> _T: ...
```

```py
from django.db.models import Model, CharField, QuerySet

class ArticleQuerySet(QuerySet):
    def visible(self) -> "ArticleQuerySet":
        raise NotImplementedError

ArticleManager = ArticleQuerySet.as_manager()

class Article(Model):
    title = CharField(max_length=100)
    objects = ArticleManager

class DirectArticle(Model):
    title = CharField(max_length=100)
    objects = ArticleQuerySet.as_manager()

reveal_type(Article.objects.visible())  # revealed: ArticleQuerySet
reveal_type(Article.objects.order_by("title"))  # revealed: ArticleQuerySet
reveal_type(DirectArticle.objects.visible())  # revealed: ArticleQuerySet
reveal_type(DirectArticle.objects.order_by("title"))  # revealed: ArticleQuerySet
```

## Manager from_queryset preserves manager methods

Managers created with `Manager.from_queryset` keep methods declared on the manager class as well as
methods copied from the queryset class.

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
from django.db.models.query import QuerySet
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

`/.venv/<path-to-site-packages>/django/db/models/query.py`:

```py
from typing import Any, Generic, TypeVar

_T = TypeVar("_T")

class QuerySet(Generic[_T]):
    def filter(self, **kwargs: Any) -> "QuerySet[_T]": ...
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

```py
from django.db.models import Model, CharField, Manager, QuerySet

class ArticleQuerySet(QuerySet["Article"]):
    def visible(self) -> "ArticleQuerySet":
        raise NotImplementedError

class _ArticleManager(Manager["Article"]):
    def by_slug(self, slug: str) -> "ArticleQuerySet":
        raise NotImplementedError

ArticleManager = _ArticleManager.from_queryset(ArticleQuerySet)

class ArticleManager(ArticleManager):
    pass

class Article(Model):
    title = CharField(max_length=100)
    objects = ArticleManager()

reveal_type(ArticleManager().by_slug("django"))  # revealed: ArticleQuerySet
reveal_type(Article.objects.visible())  # revealed: ArticleQuerySet
reveal_type(Article.objects.by_slug("django"))  # revealed: ArticleQuerySet
```

## Cacheops hint decorator adds queryset methods

Some projects use a small mypy plugin to model methods monkey-patched by `django-cacheops`. When the
plugin marker decorator is present, the queryset should expose those methods without requiring
project-specific queryset class names.

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
from django.db.models.query import QuerySet
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

`/.venv/<path-to-site-packages>/django/db/models/query.py`:

```py
from typing import Any, Generic, TypeVar

_T = TypeVar("_T")

class QuerySet(Generic[_T]):
    def all(self) -> "QuerySet[_T]": ...
```

`/.venv/<path-to-site-packages>/django/db/models/manager.py`:

```py
from typing import Generic, TypeVar

_T = TypeVar("_T")

class Manager(Generic[_T]):
    @classmethod
    def from_queryset(cls, queryset_cls): ...
    def all(self): ...
```

`/src/utils/typing.py`:

```py
from typing import TypeVar

T = TypeVar("T")

def cacheops_hint(cls: type[T]) -> type[T]:
    return cls
```

```py
from django.db.models import Model, CharField, Manager, QuerySet
from utils.typing import cacheops_hint

@cacheops_hint
class CacheopsArticleQuerySet(QuerySet["Article"]):
    pass

class ArticleQuerySet(CacheopsArticleQuerySet):
    pass

ArticleManager = Manager.from_queryset(ArticleQuerySet)

class Article(Model):
    title = CharField(max_length=100)
    objects = ArticleManager()

reveal_type(Article.objects.all().nocache())  # revealed: ArticleQuerySet
reveal_type(Article.objects.all().cache())  # revealed: ArticleQuerySet
reveal_type(Article.objects.all().invalidated_update(title="new"))  # revealed: int
Article.objects.nocache().all()
Article.objects.cache().all()
reveal_type(Article.objects.invalidated_update(title="new"))  # revealed: int
```
