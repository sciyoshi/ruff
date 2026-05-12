# Django Forms

```toml
[environment]
python-version = "3.11"
python = "/.venv"
```

## Declared form fields are available through self.fields

Django's form metaclass copies declared form fields into `self.fields`. When the field name is a
string literal, ty resolves the concrete declared field type.

`/.venv/<path-to-site-packages>/django/__init__.py`:

```py
```

`/.venv/<path-to-site-packages>/django/forms/__init__.py`:

```py
from django.forms.fields import Field
from django.forms.forms import Form
from django.forms.models import ModelChoiceField
```

`/.venv/<path-to-site-packages>/django/forms/fields.py`:

```py
class Field:
    pass
```

`/.venv/<path-to-site-packages>/django/forms/forms.py`:

```py
from django.forms.fields import Field

class BaseForm:
    fields: dict[str, Field]

class Form(BaseForm):
    pass
```

`/.venv/<path-to-site-packages>/django/forms/models.py`:

```py
from django.forms.fields import Field

class ModelChoiceField(Field):
    queryset: object
    def __init__(self, *, queryset: object): ...
```

```py
from django import forms

class SendForm(forms.Form):
    def __init__(self) -> None:
        self.fields["user"].queryset = object()
        reveal_type(self.fields["user"])  # revealed: ModelChoiceField
        reveal_type(self.fields["missing"])  # revealed: Field

    user = forms.ModelChoiceField(queryset=object())
```
