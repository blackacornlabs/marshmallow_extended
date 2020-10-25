# Marshmallow advanced Python library

## Extra fields

### Active field

Converts `active` field to `state` and back.

```python
>>> class SimpleSchema(Schema):
        active = Active()

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
        active = Active(as_filter=True)

>>> SimpleFilterSchema().load({'active': 'true'})
{'state': 'active'}
>>> SimpleFilterSchema().load({'active': 'false'})
{'state': 'inactive'}
>>> SimpleFilterSchema().load({})
{'state__ne': 'deleted'}
```

For experienced usage try `positives`, `negatives`, `positive_filter`, 
`negative_filter`, `missing_filter` parameters. You can see behaviour for this parameters in tests.  