from functools import wraps

from flask import request
from marshmallow import ValidationError


def apply_endpoint_params(schema, **schema_params):
    """
    Decorator gets endpoint parameters and apply marshmallow schema to them

    :param schema: Marshmallow schema
    :param schema_params: any marshmallow schema params
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url_kwargs = request.view_args
            for kwarg in url_kwargs:
                kwargs.pop(kwarg, None)

            # Apply schema
            try:
                url_kwargs = schema(**schema_params).load(url_kwargs)
            except ValidationError as exc:
                return {'errors': exc.messages}, 400
            kwargs.update(url_kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_params(schema, pop=None, as_field=None, **schema_params):
    """
    Getting request parameters

    :param schema: Marshmallow schema
    :param pop: fields to move from params to kwargs, list or comma-separated string
    :param schema_params: exclude=[], only=[], partial=True/False, unknown='exclude'
    :return: request params
    """
    if isinstance(pop, str):
        pop = [i.strip() for i in pop.split(',')]
    elif not pop:
        pop = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = None
            if request.method == 'GET':
                data = request.args
            elif request.method in ['POST', 'PUT', 'DELETE']:
                if not request.is_json:
                    return {'errors': {"common": "Cannot parse json"}}, 400
                data = request.json

            # Load params
            try:
                params = schema(**schema_params).load(data)
            except ValidationError as exc:
                return {'errors': exc.messages}, 400

            for field in pop:
                kwargs[field] = params.pop(field, None)
            if as_field:
                kwargs[as_field] = params
            else:
                args = list(args)
                args.append(params)

            return func(*args, **kwargs)

        return wrapper

    return decorator
