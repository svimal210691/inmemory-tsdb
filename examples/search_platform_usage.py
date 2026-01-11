#!/usr/bin/env python3
"""
Basic usage examples for the in-memory time series database
"""

import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import InMemoryTSDB
from src.point import Point
from src.aggregate import Aggregate
from src.aggregatemetric import AggregateMetric

def add_data_points(db:InMemoryTSDB):
    points = [
        Point(
            measurement='cpu',
            fields={'value': 85},
            tags={'region': 'us-east', 'worker': 'jira'},
            timestamp=datetime.now() - timedelta(minutes=2)
        ),
        Point(
            measurement='cpu',
            fields={'value': 75},
            tags={'region': 'us-east', 'worker': 'jira'},
            timestamp=datetime.now() - timedelta(minutes=1)
        ),
        Point(
            measurement='cpu',
            fields={'value': 55},
            tags={'region': 'us-east', 'worker': 'confluence'},
            timestamp=datetime.now() - timedelta(minutes=2)
        ),
        Point(
            measurement='cpu',
            fields={'value': 65},
            tags={'region': 'us-east', 'worker': 'confluence'},
            timestamp=datetime.now() - timedelta(minutes=1)
        ),
        Point(
            measurement='cpu',
            fields={'value': 45},
            tags={'region': 'us-west', 'worker': 'jira'},
            timestamp=datetime.now() - timedelta(minutes=2)
        ),
        Point(
            measurement='cpu',
            fields={'value': 55},
            tags={'region': 'us-west', 'worker': 'jira'},
            timestamp=datetime.now() - timedelta(minutes=1)
        ),
        Point(
            measurement='cpu',
            fields={'value': 80},
            tags={'region': 'us-west', 'worker': 'confluence'},
            timestamp=datetime.now() - timedelta(minutes=2)
        ),
        Point(
            measurement='cpu',
            fields={'value': 90},
            tags={'region': 'us-west', 'worker': 'confluence'},
            timestamp=datetime.now() - timedelta(minutes=1)
        )
    ]

    db.write_points(points)

def log_aggregates(db:InMemoryTSDB):
    jira_events = db.query(
        measurement='cpu',
        tags={'worker': 'jira'}
    )
    print(f"Jira worker events: {len(jira_events)}")


    jira_east_events = db.query(
        measurement='cpu',
        tags={'worker': 'jira', 'region': 'us-east'}
    )

    print("Jira worker aggregate metrics")
    sum_east = Aggregate.sum(jira_events, 'value')
    avg_east = Aggregate.average(jira_events, 'value')
    min_east = Aggregate.min(jira_events, 'value')
    max_east = Aggregate.max(jira_events, 'value')
    print_aggregate_metric(sum_east)
    print_aggregate_metric(avg_east)
    print_aggregate_metric(min_east)
    print_aggregate_metric(max_east)

    print("\n Jira worker us-east aggregate metrics")
    sum_jira_east = Aggregate.sum(jira_east_events, 'value')
    avg_jira_east = Aggregate.average(jira_east_events, 'value')
    min_jira_east = Aggregate.min(jira_east_events, 'value')
    max_jira_east = Aggregate.max(jira_east_events, 'value')
    print_aggregate_metric(sum_jira_east)
    print_aggregate_metric(avg_jira_east)
    print_aggregate_metric(min_jira_east)
    print_aggregate_metric(max_jira_east)



def example_search_platform():
    """Example 5: Searching platform information"""
    print("\n Add some CPU metrics for FDS service in different regions and worker groups")
    print("\n Then query data points in a time range")
    print("\n And then demo some aggregation functions on time series data")

    db = InMemoryTSDB()
    add_data_points(db)

    # Query all events
    all_events = db.query(measurement='cpu')
    print(f"\nTotal events: {len(all_events)}")

    log_aggregates(db)

def print_point(point: Point):
    """Helper function to print a Point object"""
    print(f"Measurement: {point.measurement}, Tags: {point.tags}, "
          f"Fields: {point.fields}, Timestamp: {point.timestamp}")

def print_aggregate_metric(aggregate: AggregateMetric):
    """Helper function to print a AggregateMetric object"""
    print(f"Measurement: {aggregate.measurement}, Tags: {aggregate.tags}, "
          f"Start Time: {aggregate.startTime}, End Time: {aggregate.endTime}, "
          f"Aggregate value: {aggregate.value}")

if __name__ == '__main__':
#     example_basic_write_and_query()
#     example_query_builder()
#     example_multiple_series()
#     example_point_objects()
    example_search_platform()
