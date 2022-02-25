# Marshmallow advanced Python library

## Extra fields

### Active field

Converts `active` field to `state` and back.

```python
>>> from marshmallow_extended import Schema
>>> from marshmallow_extended.fields import Active

>>> class SimpleSchema(Schema):
...     active = Active()

>>> SimpleSchema().dump({'state': 'active'})
{'active': True})
>>> SimpleSchema().dump({'state': 'inactive'})
{'active': False}

>>> SimpleSchema().load({'active': True})
{'state': 'active'}
>>> SimpleSchema().load({'active': False})
{'state': 'inactive'}
```

Filter by query parameter:

```python
>>> class SimpleFilterSchema(Schema):
...     active = Active(as_filter=True)

>>> SimpleFilterSchema().load({'active': 'true'})
{'state': 'active'}
>>> SimpleFilterSchema().load({'active': 'false'})
{'state': 'inactive'}
>>> SimpleFilterSchema().load({})
{'state__ne': 'deleted'}
```

For experienced usage try `positives`, `negatives`, `positive_filter`, 
`negative_filter`, `missing_filter` parameters. You can see behaviour for this parameters in tests.  

### Email field

Extended `marshmallow.field.Email` field: lowering case.

```python
>>> from marshmallow_extended import Schema
>>> from marshmallow_extended.fields import Email

>>> class SimpleSchema(Schema):
...     email = Email()

>>> SimpleSchema().load({'email': 'Test@email.com'})
{'email': 'test@email.com'}
```

### Instance field

Marshmallow field allowing to convert field to an ORM instance.

```python
>>> from marshmallow_extended import Schema
>>> from marshmallow_extended.fields import Instance
>>> from app.models import Restaurant

>>> class SimpleSchema(Schema):
...     restaurant = Instance(Restaurant)

>>> SimpleSchema().load({'restaurant': 1})
{'restaurant': <Restaurant 1>}
```

To return certain field of instance use `return_field` argument:

```python
>>> class SimpleSchema(Schema):
...     restaurant = Instance(Restaurant, return_field='name')

>>> SimpleSchema().load({'restaurant': 1})
{'restaurant': 'First restaurant'}
```

## Changelog

### 1.3.1 (2022-02-25)

- Added `return_field` argument to `Instance` marshmallow field (to SQL implementation).

### 1.3.1 (2021-06-10)

- Added `Enum` and `IContains` fields.
- Added `get_params` and `apply_endpoint_params` decorators.

### 1.3.0 (2021-06-10)

- Added `Email` field.