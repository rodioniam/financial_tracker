from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
import asyncio

from alembic import context

from database import Base
# этот импорт нужен чтобы Base.metadata работал как надо
from models import User, Transaction, Category
import os
from dotenv import load_dotenv

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = f"postgresql+asyncpg://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@localhost:5432/{os.environ['DB_NAME']}"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# def run_migrations_online() -> None:
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_async_engine(
        f"postgresql+asyncpg://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@localhost:5432/{os.environ['DB_NAME']}"
    )

    def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)  # noqa
        with context.begin_transaction():
            context.run_migrations()

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
