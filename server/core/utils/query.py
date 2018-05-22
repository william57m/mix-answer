import re
import sqlalchemy

from sqlalchemy import and_
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.sql import sqltypes

from urllib.parse import parse_qsl
from urllib.parse import unquote

from core.utils.exceptions import BadRequestError


def order_query(request, query):
    """ Order query by fields

    :param request: request where we extract the values
    :param query: SQLAlchemy query object

    :return: query with order_by clause

    """

    sort = request.get_argument('sort', False)

    if sort:
        for value in sort.split(','):
            sign = value[:1]
            field = value[1:]

            # Check sign
            if sign not in ['+', '-']:
                raise BadRequestError('Invalid sign sort.')

            # Check field
            if hasattr(query.column_descriptions[0]['entity'], field):
                field = getattr(query.column_descriptions[0]['entity'], field)
                query = query.order_by(asc(field)) if sign == '+' else query.order_by(desc(field))

    return query


def extract_metadata(query):
    """ Extract metadata

        :param query: SQLAlchemy query object

        :return: metadata dictionnary

    """

    count = query.count()

    metadata = {
        'count': count,
        'total': count,
        'limit': 0,
        'offset': 0,
    }

    return metadata


def limit_offset_query(request, query, metadata=None):
    """ Add limit offset to query

        :param request: request where we extract the values
        :param query: SQLAlchemy query object

        :return: query with limit offset clauses

    """

    limit = request.get_argument('limit', False)
    if limit:
        query = query.limit(limit)

    offset = request.get_argument('offset', False)
    if offset:
        query = query.offset(offset)

    if metadata:
        metadata['count'] = query.count()
        metadata['limit'] = int(limit)
        metadata['offset'] = int(offset)

    return query


def add_condition(conditions, clause, model_class, key, value):
    if isinstance(getattr(model_class, key).type, sqltypes.Integer):
        try:
            conditions = clause(conditions, getattr(model_class, key) == int(value))
        except ValueError:
            pass
    else:
        conditions = clause(conditions, sqlalchemy.func.upper(
            getattr(model_class, key)
        ).contains(
            sqlalchemy.func.upper(value)
        ))
    return conditions


def filter_query(request, query, model_class, authorized_fields=None, metadata=None):
    """ Add search to query

        :param request: request where we extract the values
        :param query: SQLAlchemy query object
        :param model_class: class of the query
        :param metadata: query metadata (necessary to update the total count)

        :return: query with search clause

    """

    authorized_fields = authorized_fields if authorized_fields else []
    search_encoded = request.get_argument('search', False)
    string_query = request.get_argument('string_query', False)

    if string_query:
        conditions = or_()
        value = string_query
        for key in authorized_fields:
            conditions = add_condition(conditions, or_, model_class, key, value)
        query = query.filter(conditions)
    elif search_encoded:
        search = dict(parse_qsl(unquote(search_encoded)))
        conditions = and_()
        for key in search:
            if key in authorized_fields:
                value = search[key].replace('%', '\%').replace('_', '\_')
                conditions = add_condition(conditions, and_, model_class, key, value)
        query = query.filter(conditions)

    if metadata and (string_query or search_encoded):
        metadata['total'] = query.count()

    return query


def check_param(data, name, type_param, required):
    if name not in data:
        if required:
            raise BadRequestError(f'Param {name} is missing')
        else:
            return None

    param = data[name]

    if type_param == 'integer':
        try:
            param = int(param)
        except ValueError:
            raise BadRequestError(f'Param {name} must be an integer')
    elif type_param == 'boolean':
        if param in [True, 'True', 'true', '1', 1]:
            return True
        elif param in [False, 'False', 'false', '0', 0]:
            return False
        else:
            raise BadRequestError(f'Param {name} must be a boolean')
    elif type_param == 'list':
        if type(param) is not list:
            raise BadRequestError(f'Param {name} must be an array')
    elif type_param == 'email':
        if not re.match(r'[^@]+@[^@]+\.[^@]+', param):
            raise BadRequestError(f'{param} is not a valid email')

    return param


def update_by_property_list(property_list, request_data, object_to_update):
    """ Update given keys of an object

    :param property_list: string list of properties to update
    :param request_data: data received in the request
    :param object_to_update: SQLAlchemy object to update

    """

    for key in property_list:

        if key in request_data:
            _type = object_to_update.__mapper__.columns[key].type.__class__.__name__

            # Update property according to the type
            if _type in ['String', 'Text', 'UnicodeText', 'JSON', 'JSONB']:
                setattr(object_to_update, key, request_data[key])
            elif _type == 'Boolean':
                setattr(object_to_update, key, str(request_data[key]).lower() == 'true')
