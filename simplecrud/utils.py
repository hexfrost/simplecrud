import asyncio
from functools import wraps


def async_to_sync(func):
    """Decorator to convert async function to sync"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(func(*args, **kwargs))
        return result

    return wrapper


def inject_connection(func):
    """Decorator to inject database connection to function"""

    @wraps(func)
    def inner(*args, **kwargs):
        from simplecrud.settings import session
        if not kwargs.get('conn'):
            kwargs['conn'] = session()
        result = func(*args, **kwargs)
        try:
            kwargs['conn'].close()
        except:
            pass
        return result

    return inner
