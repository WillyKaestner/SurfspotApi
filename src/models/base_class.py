# Construct a base class for declarative class definitions.
# The new base class will be given a metaclass that produces appropriate Table objects
# Sqlalchemy 2.0: https://docs.sqlalchemy.org/en/14/changelog/migration_20.html#migration-orm-configuration
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
