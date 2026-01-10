"""
In-Memory Time Series Database - InfluxDB-like implementation
"""

from .database import InMemoryTSDB
from .point import Point
from .query import Query

__all__ = ['InMemoryTSDB', 'Point', 'Query']
__version__ = '0.1.0'

