"""
Data point representation for aggregate metric of a field
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Any

@dataclass
class AggregateMetric:
    measurement: str
    value: float
    tags: Optional[Dict[str, str]] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None


    def __post_init__(self):
        """Initialize default values"""
        if self.tags is None:
            self.tags = {}
        if self.startTime is None:
            self.startTime = datetime.now()
        if self.endTime is None:
            self.endTime = datetime.now()