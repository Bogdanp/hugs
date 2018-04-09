import functools
import sqlite3

from .repository import Repository

try:
    from psycopg2.extras import DictRow, RealDictRow

    ROW_CLASSES = (dict, sqlite3.Row, DictRow, RealDictRow)
except ImportError:  # pragma: no cover
    ROW_CLASSES = (dict, sqlite3.Row)


class Manager:
    """Managers extend repositories with the ability to iterate over
    queries and convert result rows to concrete data types.
    """

    def __init__(self, value_factory=dict, *, repository=None):
        self.repository = repository or Repository()
        self.load_queries = self.repository.load_queries
        self.value_factory = value_factory

    def __getattr__(self, name):
        fn = getattr(self.repository, name)
        if getattr(fn, "is_command", False):
            return command_runner(fn)
        return query_iterator(fn, self.value_factory)


def command_runner(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)

        # Grab the cursor late so that if the user forgets to provide
        # it the TypeError they get will refer to the query function,
        # not wrapper() itself.
        cursor = args[0]
        if cursor.description:
            result = cursor.fetchone()
            if isinstance(result, ROW_CLASSES):
                return result

            return {col[0]: val for col, val in zip(cursor.description, result)}
        return None
    return wrapper


def query_iterator(fn, value_factory):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)

        # Grab the cursor late so that if the user forgets to provide
        # it the TypeError they get will refer to the query function,
        # not wrapper() itself.
        cursor = args[0]
        while True:
            results = cursor.fetchmany()
            if not results:
                break

            for result in results:
                if not isinstance(result, ROW_CLASSES):
                    result = {col[0]: val for col, val in zip(cursor.description, result)}

                yield value_factory(**result)

    return wrapper
