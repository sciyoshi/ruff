# Django Request

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## Immutable QueryDict methods are reported

`django-stubs` models mutating methods on immutable `QueryDict` values as returning `Never`. The
plugin turns those calls into a Django-specific diagnostic.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/http/__init__.py`:

```py
from django.http.request import QueryDict
```

`/.venv/<path-to-site-packages>/django/http/request.py`:

```py
from typing import Never, overload

class QueryDict:
    def __init__(self, *, mutable: bool = False): ...
    @overload
    def update(self, other: dict[str, str], /) -> Never: ...
    @overload
    def update(self, other: None = None, /) -> None: ...
    def update(self, other=None, /): ...
```

```py
from django.http import QueryDict

query = QueryDict()
query.update({"page": "1"})  # error: [invalid-argument-type] "This QueryDict is immutable."
query.update()
```
