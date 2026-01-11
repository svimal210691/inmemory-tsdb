"""
Module for getting aggregate data from a list of Points
"""
from typing import List, Dict, Optional, Any

from .aggregatemetric import AggregateMetric
from .point import Point

class Aggregate:

    def __init__(self):
        pass

    @staticmethod
    def sum(points: List[Point], field: str) -> AggregateMetric:
        """Calculate the sum of a specific field across all points"""
        total = 0.0
        for point in points:
            if field in point.fields and isinstance(point.fields[field], (int, float)):
                total += point.fields[field]
        return AggregateMetric(
            measurement=points[0].measurement if points else "sum",
            tags=points[0].tags if points else {},
            startTime=points[0].timestamp,
            endTime=points[-1].timestamp,
            value=total
        )

    @staticmethod
    def average(points: List[Point], field: str) -> AggregateMetric:
        """Calculate the average of a specific field across all points"""
        total = 0.0
        count = 0
        for point in points:
            if field in point.fields and isinstance(point.fields[field], (int, float)):
                total += point.fields[field]
                count += 1
        avg = total / count if count > 0 else 0.0
        return AggregateMetric(
            measurement=points[0].measurement if points else "avg",
            tags=points[0].tags if points else {},
            startTime=points[0].timestamp,
            endTime=points[-1].timestamp,
            value=avg
        )

    @staticmethod
    def min(points: List[Point], field: str) -> AggregateMetric:
        """Calculate the minimum of a specific field across all points"""
        minimum = None
        for point in points:
            if field in point.fields and isinstance(point.fields[field], (int, float)):
                if minimum is None or point.fields[field] < minimum:
                    minimum = point.fields[field]
        return AggregateMetric(
            measurement=points[0].measurement if points else "min",
            tags=points[0].tags if points else {},
            startTime=points[0].timestamp,
            endTime=points[-1].timestamp,
            value=minimum
        )

    @staticmethod
    def max(points: List[Point], field: str) -> AggregateMetric:
        """Calculate the maximum of a specific field across all points"""
        maximum = None
        for point in points:
            if field in point.fields and isinstance(point.fields[field], (int, float)):
                if maximum is None or point.fields[field] > maximum:
                    maximum = point.fields[field]
        return AggregateMetric(
            measurement=points[0].measurement if points else "max",
            tags=points[0].tags if points else {},
            startTime=points[0].timestamp,
            endTime=points[-1].timestamp,
            value=maximum
        )