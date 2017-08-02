aiopg_sqlite
============


Drop-in replacement for aiopg, using SQLITE database, retaining (some)
its functionality.

Useful (maybe) for testing without running test postgresql server.

Usage:

```
    async with aiopg_sqlite.create_engine(
            'sqlite:///:memory:',
            loop=loop,
            echo=True) as engine:
        async with engine.acquire() as conn:
            await conn.execute('create table t1 (c1 integer)')
            inserted = list()
            for i in range(10):
                await conn.execute('insert into t1 select %s' % i)
                inserted.append(i)
            async for row in conn.execute('select * from t1'):
                assert row.c1 in inserted
```
