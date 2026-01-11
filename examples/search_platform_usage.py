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



def example_metric_aggregates():
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

def example_high_cpu_usage():
    """Example: Add some CPU usage data points for few minutes and find high cpu usage data points"""
    db = InMemoryTSDB()
    add_data_points(db)
    now = datetime.now()

    # Query all events
    all_events = db.query(measurement='cpu')
    print(f"\nTotal events: {len(all_events)}")

    # Use query builder - find high CPU usage
    query = db.create_query()
    results = (query
               .from_measurement('cpu')
               .where_tags(region='us-east')
               .time_range(start=now - timedelta(minutes=5))
               .where_field('value', '>', 70)
               .limit(5))
    results = db.execute_query(results)

    print(f"\nFound {len(results)} points with CPU usage > 70%")
    if results:
        for point in results:
            print_point(point)
    else:
        # Show some data to demonstrate query works
        all_cpu = db.query(measurement='cpu', limit=5)
        print("  (No points > 70%, showing sample data instead:)")
        for point in all_cpu[:3]:
            print(f"  Worker: {point.tags['worker']}, Usage: {point.fields['value']}%")


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
    #example_metric_aggregates()
    example_high_cpu_usage()
