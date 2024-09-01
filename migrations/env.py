from pathlib import Path
from dotenv import load_dotenv
import os
import logging

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.libs.sql_alchemy_lib import Base

# Load environment variables from .env file
load_dotenv()

"""
##################################################################################
#########Import all Your model Here so Alembic will know the model is exists######
##################################################################################
"""
from app.user.user_model import UserModel
from app.health_check.health_check_model import HealthCheckModel
from app.business_category.business_category_model import BusinessCategory
from app.business.business_model import Business
from app.rating.rating_model import Rating
from app.user_need.user_need_model import UserNeeds
from app.article.article_model import Article
"""
##################################################################################
#########Import all Your model Here so Alembic will know the model is exists######
##################################################################################
"""

# Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData object for 'autogenerate' support
target_metadata = Base.metadata

# Get database URL from environment variable
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL is not set in environment variables.")

# Set the SQLAlchemy URL configuration
config.set_main_option("sqlalchemy.url", database_url)

# Logging
logger = logging.getLogger('alembic')
logger.info(f"Using database URL: {database_url}")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
