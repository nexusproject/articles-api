#
#

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pprint import pprint as p

engine = create_async_engine(
    "mysql+aiomysql://root:@localhost/articles",
    echo=False, pool_size=10, max_overflow=5, pool_pre_ping=True, 
)

def async_session():
    return AsyncSession(engine, expire_on_commit=False)

async def check_connection():
    #async with engine.begin():
    #    pass
    pass


