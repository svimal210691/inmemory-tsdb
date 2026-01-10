"""
Data point representation for time series database
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Any


@dataclass
class Point:
    """
    Represents a single data point in the time series database.
    Similar to InfluxDB's point structure with measurement, tags, fields, and timestamp.
    """
    measurement: str
    fields: Dict[str, Any]
    tags: Optional[Dict[str, str]] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values"""
        if self.tags is None:
            self.tags = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def get_series_key(self) -> str:
        """
        Generate a unique series key from measurement and tags.
        This is used to group points that belong to the same series.
        """
        if not self.tags:
            return self.measurement
        
        # Sort tags for consistent key generation
        sorted_tags = sorted(self.tags.items())
        tag_str = ','.join(f"{k}={v}" for k, v in sorted_tags)
        return f"{self.measurement},{tag_str}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert point to dictionary representation"""
        return {
            'measurement': self.measurement,
            'tags': self.tags,
            'fields': self.fields,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

