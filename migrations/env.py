from logging.config import fileConfig

from flask import current_app
from alembic import context
from sqlalchemy import engine_from_config, pool

from app.extensions import db

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = db.metadata


def get_engine():
    return current_app.extensions["migrate"].db.engine


def get_engine_url():
    return str(get_engine().url).replace("%", "%%")


def run_migrations_offline():
    url = get_engine_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(
        config.config_ini_section
    )

    configuration["sqlalchemy.url"] = get_engine_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()