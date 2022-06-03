#
#

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_async_engine(
    "mysql+aiomysql://root:@localhost/articles",
    echo=False, pool_size=10, max_overflow=5, pool_pre_ping=True
)

def async_session():
    return sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
