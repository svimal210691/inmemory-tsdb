"""
Query builder and executor for time series database
"""

from typing import List, Optional, Dict, Callable, Any
from datetime import datetime
from .point import Point
from .series import Series


class Query:
    """
    Query builder for time series database queries.
    Supports filtering by measurement, tags, time range, and field values.
    """
    
    def __init__(self):
        self._measurement: Optional[str] = None
        self._tags: Optional[Dict[str, str]] = None
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None
        self._field_filters: List[Callable[[Point], bool]] = []
        self._limit: Optional[int] = None
    
    def from_measurement(self, measurement: str) -> 'Query':
        """Filter by measurement name"""
        self._measurement = measurement
        return self
    
    def where_tags(self, **tags: str) -> 'Query':
        """Filter by tag key-value pairs"""
        if self._tags is None:
            self._tags = {}
        self._tags.update(tags)
        return self
    
    def time_range(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> 'Query':
        """Filter by time range"""
        self._start_time = start
        self._end_time = end
        return self
    
    def where_field(self, field_name: str, operator: str, value: Any) -> 'Query':
        """
        Filter by field value.
        Operators: '=', '!=', '>', '<', '>=', '<='
        """
        def filter_func(point: Point) -> bool:
            if field_name not in point.fields:
                return False
            
            field_value = point.fields[field_name]
            
            if operator == '=':
                return field_value == value
            elif operator == '!=':
                return field_value != value
            elif operator == '>':
                return field_value > value
            elif operator == '<':
                return field_value < value
            elif operator == '>=':
                return field_value >= value
            elif operator == '<=':
                return field_value <= value
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        
        self._field_filters.append(filter_func)
        return self
    
    def limit(self, n: int) -> 'Query':
        """Limit the number of results"""
        self._limit = n
        return self
    
    def matches_tags(self, point_tags: Dict[str, str]) -> bool:
        """Check if point tags match query tags"""
        if self._tags is None:
            return True
        
        for key, value in self._tags.items():
            if key not in point_tags or point_tags[key] != value:
                return False
        return True
    
    def matches_measurement(self, measurement: str) -> bool:
        """Check if measurement matches query"""
        if self._measurement is None:
            return True
        return self._measurement == measurement
    
    def matches_time_range(self, timestamp: datetime) -> bool:
        """Check if timestamp is within query time range"""
        if self._start_time and timestamp < self._start_time:
            return False
        if self._end_time and timestamp > self._end_time:
            return False
        return True
    
    def matches_field_filters(self, point: Point) -> bool:
        """Check if point matches all field filters"""
        return all(filter_func(point) for filter_func in self._field_filters)
    
    def matches(self, point: Point) -> bool:
        """Check if a point matches all query criteria"""
        if not self.matches_measurement(point.measurement):
            return False
        if not self.matches_tags(point.tags):
            return False
        if not self.matches_time_range(point.timestamp):
            return False
        if not self.matches_field_filters(point):
            return False
        return True
    
    def execute(self, series_dict: Dict[str, Series]) -> List[Point]:
        """
        Execute the query against a dictionary of series.
        Returns a list of matching points.
        """
        results: List[Point] = []
        
        for series_key, series in series_dict.items():
            # Check if measurement matches
            if not self.matches_measurement(series.measurement):
                continue
            
            # Check if tags match
            if not self.matches_tags(series.tags):
                continue
            
            # Get points in time range
            points = series.query_range(self._start_time, self._end_time)
            
            # Apply field filters
            for point in points:
                if self.matches_field_filters(point):
                    results.append(point)
        
        # Apply limit
        if self._limit is not None:
            results = results[:self._limit]
        
        return results

