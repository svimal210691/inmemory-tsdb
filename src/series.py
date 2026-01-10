"""
Series storage and management for time series data
"""

from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from bisect import bisect_left, bisect_right
from .point import Point


class Series:
    """
    Represents a time series - a collection of points with the same measurement and tags.
    Points are stored sorted by timestamp for efficient time-range queries.
    """
    
    def __init__(self, measurement: str, tags: Dict[str, str]):
        self.measurement = measurement
        self.tags = tags
        self._points: List[Point] = []
        self._timestamps: List[datetime] = []
    
    def add_point(self, point: Point):
        """Add a point to the series, maintaining sorted order by timestamp"""
        timestamp = point.timestamp
        
        # Find insertion point to maintain sorted order
        idx = bisect_left(self._timestamps, timestamp)
        self._timestamps.insert(idx, timestamp)
        self._points.insert(idx, point)
    
    def query_range(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> List[Point]:
        """
        Query points within a time range.
        Returns all points between start (inclusive) and end (inclusive).
        """
        if not self._points:
            return []
        
        if start is None:
            start_idx = 0
        else:
            start_idx = bisect_left(self._timestamps, start)
        
        if end is None:
            end_idx = len(self._points)
        else:
            # bisect_right to include end timestamp
            end_idx = bisect_right(self._timestamps, end)
        
        return self._points[start_idx:end_idx]
    
    def get_latest(self, n: int = 1) -> List[Point]:
        """Get the latest n points"""
        return self._points[-n:] if n > 0 else []
    
    def get_oldest(self, n: int = 1) -> List[Point]:
        """Get the oldest n points"""
        return self._points[:n] if n > 0 else []
    
    def count(self) -> int:
        """Get the total number of points in this series"""
        return len(self._points)
    
    def clear(self):
        """Remove all points from the series"""
        self._points.clear()
        self._timestamps.clear()
    
    def get_time_range(self) -> Tuple[Optional[datetime], Optional[datetime]]:
        """Get the time range of points in this series"""
        if not self._timestamps:
            return None, None
        return self._timestamps[0], self._timestamps[-1]

