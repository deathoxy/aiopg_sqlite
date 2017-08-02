__version__ = '0.0.1a'

import sqlalchemy


def create_engine(uri, loop, *args, **kwargs):
    return Engine(uri, loop, *args, **kwargs)


class WrapIter():
    def __init__(self, value):
        self.value = value

    def __next__(self):
        exc = StopIteration()
        exc.value = self.value
        raise exc


class Engine():
    def __init__(self, uri, loop, *args, **kwargs):
        self.engine = sqlalchemy.create_engine(uri, *args, **kwargs)
        self.loop = loop

    def acquire(self):
        self.connection = Connection(self.loop, self.engine)
        return self.connection

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        self.close()

    async def wait_closed(self):
        pass  # pragma: no cover

    def close(self):
        pass

    def __await__(self):
        return WrapIter(self)  # pragma: no cover


class _Stop(Exception):
    pass


class Connection():
    def __init__(self, loop, engine):
        self.loop = loop
        self.engine = engine
        self.data = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        pass

    def execute(self, *args, **kwargs):
        return Executor(self.engine, *args, **kwargs)


class Executor():
    def __init__(self, engine, *args, **kwargs):
        self.engine = engine
        self.args = args
        self.kwargs = kwargs
        self.connection = None

    async def __aiter__(self):
        self.connection = self.engine.connect()
        self.iter = iter(self.connection.execute(*self.args, **self.kwargs))
        return self

    async def __anext__(self):
        def masked_next():
            try:
                result = self.iter.__next__()
            except StopIteration:
                raise _Stop
            return result
        try:
            return masked_next()
        except _Stop:
            self.iter.close()
            self.connection.close()
            raise StopAsyncIteration()

    def __await__(self):
        self.connection = self.engine.connect()
        result = self.connection.execute(*self.args, **self.kwargs)
        self.connection.close()
        return WrapIter(result)
