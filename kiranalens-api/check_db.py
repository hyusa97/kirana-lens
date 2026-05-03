import asyncio, asyncpg

async def check():
    conn = await asyncpg.connect(
        host='db.vieblvxktxyribpsrxdg.supabase.co',
        port=5432, user='postgres',
        password='KiranaLens@123', database='postgres', timeout=10
    )
    tables = await conn.fetch(
        "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename"
    )
    print('Tables:', [r['tablename'] for r in tables])

    try:
        ver = await conn.fetch('SELECT version_num FROM alembic_version')
        print('Alembic version:', [r['version_num'] for r in ver])
    except Exception as e:
        print('No alembic_version table:', e)

    await conn.close()

asyncio.run(check())
