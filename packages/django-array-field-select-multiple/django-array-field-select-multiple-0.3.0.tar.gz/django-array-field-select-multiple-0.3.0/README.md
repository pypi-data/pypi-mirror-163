## Acknowledgement

This is a fork of the original code written by Silver Logic,
available [here](https://github.com/silverlogic/django-array-field-select/).

## About

A replacement for Django's ArrayField with a multiple select form field.

Please note that this selector makes sense only if the underlying base_field is using choices.

## Installation

```bash
pip install django-array-field-select-multiple
```

## How To Use

Replace all instances of your Django's `ArrayField` model field with the new
`ArrayField`. No functionality will be changed, except for the form field.

### Example

```python
from django.db import models
from array_field_select.fields import ArrayField


class Student(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
    years_in_school = ArrayField(
        models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    )
```