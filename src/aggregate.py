"""
Module for getting aggregate data from a list of Points
"""
from typing import List, Dict, Optional, Any
from .point import Point

class Aggregate:

    def __init__(self):
        pass

    @staticmethod
    def sum(points: List[Point], field: str) -> Point:
        """Calculate the sum of a specific field across all points"""
        total = 0.0
        for point in points:
            if field in point.fields and isinstance(point.fields[field], (int, float)):
                total += point.fields[field]
        return Point(
            measurement=points[0].measurement if points else "sum",
            fields={"sum": total},
            tags= points[0].tags if points else {},
            timestamp=points[0].timestamp if points else None
        )

    @staticmethod
    def average(points: List[Point], field: str) -> Point:
        """Calculate the average of a specific field across all points"""
        total = 0.0
        count = 0
        for point in points:
            if field in point.fields and isinstance(point.fields[field], (int, float)):
                total += point.fields[field]
                count += 1
        avg = total / count if count > 0 else 0.0
        return Point(
            measurement=points[0].measurement if points else "average",
            fields={"average": avg},
            tags= points[0].tags if points else {},
            timestamp=points[0].timestamp if points else None
        )

    @staticmethod
    def min(points: List[Point], field: str) -> Point:
        """Calculate the minimum of a specific field across all points"""
        minimum = None
        for point in points:
            if field in point.fields and isinstance(point.fields[field], (int, float)):
                if minimum is None or point.fields[field] < minimum:
                    minimum = point.fields[field]
        return Point(
            measurement=points[0].measurement if points else "min",
            fields={"min": minimum} if minimum is not None else {"min": 0.0},
            tags= points[0].tags if points else {},
            timestamp=points[0].timestamp if points else None
        )

    @staticmethod
    def max(points: List[Point], field: str) -> Point:
        """Calculate the maximum of a specific field across all points"""
        maximum = None
        for point in points:
            if field in point.fields and isinstance(point.fields[field], (int, float)):
                if maximum is None or point.fields[field] > maximum:
                    maximum = point.fields[field]
        return Point(
            measurement=points[0].measurement if points else "max",
            fields={"max": maximum} if maximum is not None else {"max": 0.0},
            tags= points[0].tags if points else {},
            timestamp=points[0].timestamp if points else None
        )