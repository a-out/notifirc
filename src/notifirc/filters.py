import re
from functools import partial

def contains(msg, arg):
    reg = re.compile(r'\s*' + re.escape(arg) + r'[^a-z]', re.IGNORECASE)
    return reg.search(msg) is not None

def starts_with(msg, arg):
    reg = re.compile(r'^' + re.escape(arg), re.IGNORECASE)
    return reg.match(msg) is not None

FILTERS = {
    'contains': contains,
    'starts_with': starts_with
}

def create_filter(f_id, f_type, arg):
    return {
        'id': f_id,
        'func': partial(FILTERS[f_type], arg=arg)
    }

def initialize_filters(pg_conn):
    filters = []
    with pg_conn.cursor() as cursor:
        cursor.execute("SELECT * from filters")

        for f in cursor:
            filters.append(create_filter(f[0], f[1], f[2]))
    return filters
