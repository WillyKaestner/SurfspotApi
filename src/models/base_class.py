# Construct a base class for declarative class definitions.
# The new base class will be given a metaclass that produces appropriate Table objects
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
