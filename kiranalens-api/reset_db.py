"""Drop all leftover types and tables, then let alembic start fresh."""
import asyncio, asyncpg

async def reset():
    conn = await asyncpg.connect(
        host='db.vieblvxktxyribpsrxdg.supabase.co',
        port=5432, user='postgres',
        password='KiranaLens@123', database='postgres', timeout=10
    )

    # Drop tables in dependency order
    for tbl in ['geo_features', 'visual_features', 'assessments', 'users', 'alembic_version']:
        await conn.execute(f'DROP TABLE IF EXISTS {tbl} CASCADE')
        print(f'Dropped table: {tbl}')

    # Drop all custom enum types
    for typ in ['assessmentstatus', 'inventoryvalueband', 'refillsignal', 'userrole', 'userrole_old']:
        await conn.execute(f'DROP TYPE IF EXISTS {typ} CASCADE')
        print(f'Dropped type: {typ}')

    await conn.close()
    print('\nDatabase cleaned. Ready for fresh migration.')

asyncio.run(reset())
