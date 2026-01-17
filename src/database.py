"""
Main database class for in-memory time series database
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from collections import defaultdict
from .point import Point
from .series import Series
from .query import Query


class InMemoryTSDB:
    """
    In-memory time series database with InfluxDB-like API.
    
    Features:
    - Store time-stamped data points with measurements, tags, and fields
    - Query by measurement, tags, time range, and field values
    - Efficient time-range queries using sorted data structures
    - Support for multiple series (measurement + tags combinations)
    """
    
    def __init__(self):
        """Initialize the database"""
        # Map from series key (measurement + tags) to Series object
        self._series: Dict[str, Series] = {}
        # Map from measurement name to set of series keys
        self._measurements: Dict[str, set] = defaultdict(set)
    
    def write(self, measurement: str, fields: Dict[str, Any], 
              tags: Optional[Dict[str, str]] = None, 
              timestamp: Optional[datetime] = None) -> None:
        """
        Write a data point to the database.
        
        Args:
            measurement: The measurement name (e.g., 'cpu', 'temperature')
            fields: Dictionary of field name-value pairs (the actual data)
            tags: Optional dictionary of tag name-value pairs (metadata for filtering)
            timestamp: Optional timestamp (defaults to current time)
        """
        point = Point(
            measurement=measurement,
            fields=fields,
            tags=tags or {},
            timestamp=timestamp or datetime.now()
        )
        
        series_key = point.get_series_key()
        
        # Create series if it doesn't exist
        if series_key not in self._series:
            series = Series(measurement, point.tags)
            self._series[series_key] = series
            self._measurements[measurement].add(series_key)
        
        # Add point to series
        self._series[series_key].add_point(point)
    
    def write_points(self, points: List[Point]) -> None:
        """Write multiple points at once"""
        for point in points:
            series_key = point.get_series_key()
            
            if series_key not in self._series:
                series = Series(point.measurement, point.tags)
                self._series[series_key] = series
                self._measurements[point.measurement].add(series_key)
            
            self._series[series_key].add_point(point)
    
    def query(self, measurement: Optional[str] = None,
              tags: Optional[Dict[str, str]] = None,
              start: Optional[datetime] = None,
              end: Optional[datetime] = None,
              limit: Optional[int] = None) -> List[Point]:
        """
        Query the database.
        
        Args:
            measurement: Filter by measurement name
            tags: Filter by tag key-value pairs
            start: Start time for range query
            end: End time for range query
            limit: Maximum number of results to return
            
        Returns:
            List of matching Point objects
        """
        query = Query()
        
        if measurement:
            query.from_measurement(measurement)
        
        if tags:
            query.where_tags(**tags)
        
        if start or end:
            query.time_range(start, end)
        
        if limit:
            query.limit(limit)
        
        return query.execute(self._series)
    
    def create_query(self) -> Query:
        """Create a new query builder"""
        return Query()
    
    def execute_query(self, query: Query) -> List[Point]:
        """Execute a query builder and return results"""
        return query.execute(self._series)
    
    def get_measurements(self) -> List[str]:
        """Get list of all measurement names"""
        return list(self._measurements.keys())
    
    def get_series_count(self) -> int:
        """Get the total number of series"""
        return len(self._series)

    def get_all_series_keys(self) -> List[str]:
        """Get all time series registered in DB"""
        keys = []
        for key, value in self._series.items():
            keys.append(key)
        return keys
    
    def get_point_count(self) -> int:
        """Get the total number of points across all series"""
        return sum(series.count() for series in self._series.values())
    
    def delete_measurement(self, measurement: str) -> int:
        """
        Delete all series for a given measurement.
        Returns the number of series deleted.
        """
        if measurement not in self._measurements:
            return 0
        
        series_keys = self._measurements[measurement].copy()
        deleted_count = 0
        
        for series_key in series_keys:
            if series_key in self._series:
                del self._series[series_key]
                deleted_count += 1
        
        del self._measurements[measurement]
        return deleted_count
    
    def delete_series(self, measurement: str, tags: Dict[str, str]) -> bool:
        """
        Delete a specific series identified by measurement and tags.
        Returns True if series was deleted, False if it didn't exist.
        """
        # Create a temporary point to generate the series key
        temp_point = Point(measurement=measurement, fields={}, tags=tags)
        series_key = temp_point.get_series_key()
        
        if series_key in self._series:
            del self._series[series_key]
            self._measurements[measurement].discard(series_key)
            if not self._measurements[measurement]:
                del self._measurements[measurement]
            return True
        
        return False
    
    def clear(self):
        """Clear all data from the database"""
        self._series.clear()
        self._measurements.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        total_points = self.get_point_count()
        series_count = self.get_series_count()
        measurement_count = len(self._measurements)
        
        return {
            'total_points': total_points,
            'series_count': series_count,
            'measurement_count': measurement_count,
            'measurements': list(self._measurements.keys())
        }

