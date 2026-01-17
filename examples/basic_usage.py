#!/usr/bin/env python3
"""
Basic usage examples for the in-memory time series database
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import InMemoryTSDB
from src.point import Point
from src.aggregate import Aggregate
from src.compression import CompressionUtil


def example_basic_write_and_query():
    """Example 1: Basic write and query operations"""
    print("=" * 60)
    print("Example 1: Basic Write and Query")
    print("=" * 60)
    
    db = InMemoryTSDB()
    
    # Write some data points
    now = datetime.now()
    for i in range(10):
        db.write(
            measurement='temperature',
            fields={'value': 20 + i * 0.5},
            tags={'sensor': 'sensor1', 'location': 'room1'},
            timestamp=now - timedelta(minutes=i)
        )
    
    # Query all data
    all_points = db.query(measurement='temperature')
    print(f"\nTotal points written: {len(all_points)}")
    
    # Query with time range
    recent_points = db.query(
        measurement='temperature',
        start = now - timedelta(minutes=5)
    )
    print(f"Points in last 5 minutes: {len(recent_points)}")
    
    # Query with tags
    sensor1_points = db.query(
        measurement='temperature',
        tags={'sensor': 'sensor1'}
    )
    print(f"Points from sensor1: {len(sensor1_points)}")
    
    # Print stats
    stats = db.get_stats()
    print(f"\nDatabase stats:")
    print(f"  Total points: {stats['total_points']}")
    print(f"  Series count: {stats['series_count']}")
    print(f"  Measurements: {stats['measurements']}")


def example_query_builder():
    """Example 2: Using query builder for complex queries"""
    print("\n" + "=" * 60)
    print("Example 2: Query Builder")
    print("=" * 60)
    
    db = InMemoryTSDB()
    
    # Write CPU monitoring data
    now = datetime.now()
    for i in range(30):
        db.write(
            measurement='cpu',
            fields={'usage': 50 + (i % 40), 'load': 1.0 + (i % 10) * 0.2},
            tags={'host': f'server{i % 3}', 'region': 'us-east'},
            timestamp=now - timedelta(minutes=i%10)
        )
    
    # Use query builder - find high CPU usage
    query = db.create_query()
    results = (query
        .from_measurement('cpu')
        .where_tags(region='us-east')
        .time_range(start=now - timedelta(minutes=10))
        .where_field('usage', '>', 70)
        .limit(5))
    results = db.execute_query(results)
    
    print(f"\nFound {len(results)} points with CPU usage > 70%")
    if results:
        for point in results:
            print(f"  Host: {point.tags['host']}, Usage: {point.fields['usage']}%, "
                  f"Time: {point.timestamp.strftime('%H:%M:%S')}")
    else:
        # Show some data to demonstrate query works
        all_cpu = db.query(measurement='cpu', limit=5)
        print("  (No points > 70%, showing sample data instead:)")
        for point in all_cpu[:3]:
            print(f"  Host: {point.tags['host']}, Usage: {point.fields['usage']}%")


def example_multiple_series():
    """Example 3: Multiple series (different tags)"""
    print("\n" + "=" * 60)
    print("Example 3: Multiple Series")
    print("=" * 60)
    
    db = InMemoryTSDB()
    
    # Write data for multiple sensors
    sensors = ['sensor1', 'sensor2', 'sensor3']
    now = datetime.now()
    
    for sensor in sensors:
        for i in range(5):
            db.write(
                measurement='humidity',
                fields={'value': 50 + i * 2},
                tags={'sensor': sensor, 'location': 'warehouse'},
                timestamp=now - timedelta(minutes=i)
            )

    db.write(measurement='humidity',
                fields={'value': 50 + 2 * 2})
    db.write(measurement='humidity',
                fields={'value': 70},
                tags={'location': 'office'})
    
    stats = db.get_stats()
    print(f"\nDatabase stats:")
    print(f"  Total points: {stats['total_points']}")
    print(f"  Series count: {stats['series_count']}")  # Should be 3 (one per sensor)
    print(f"  Measurements: {stats['measurements']}")
    
    all_time_series = db.get_all_series_keys()
    print(f"All time series {all_time_series}")


def example_point_objects():
    """Example 4: Using Point objects directly"""
    print("\n" + "=" * 60)
    print("Example 4: Using Point Objects")
    print("=" * 60)
    
    db = InMemoryTSDB()
    
    # Create points explicitly
    points = [
        Point(
            measurement='events',
            fields={'count': 10, 'duration': 1.5},
            tags={'type': 'api', 'status': 'success'},
            timestamp=datetime.now() - timedelta(minutes=2)
        ),
        Point(
            measurement='events',
            fields={'count': 5, 'duration': 0.8},
            tags={'type': 'api', 'status': 'error'},
            timestamp=datetime.now() - timedelta(minutes=1)
        ),
        Point(
            measurement='events',
            fields={'count': 15, 'duration': 2.1},
            tags={'type': 'webhook', 'status': 'success'},
            timestamp=datetime.now()
        )
    ]
    
    db.write_points(points)
    
    # Query all events
    all_events = db.query(measurement='events')
    print(f"\nTotal events: {len(all_events)}")
    
    # Query successful events
    success_events = db.query(
        measurement='events',
        tags={'status': 'success'}
    )
    print(f"Successful events: {len(success_events)}")
    
    # Query with field filter
    query = db.create_query()
    long_events_query = (query
        .from_measurement('events')
        .where_field('duration', '>', 1.0))
    long_events = db.execute_query(long_events_query)
    print(f"Events with duration > 1.0s: {len(long_events)}")

def example_search_platform():
    """Example 5: Searching platform information"""
    print("\n Add some CPU metrics for FDS service in different regions and worker groups")
    print("\n Then query data points in a time range")
    print("\n And then demo some aggregation functions on time series data")

    db = InMemoryTSDB()
    # Create CPU usage measurements as Points explicitly
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

    # Query all events
    all_events = db.query(measurement='cpu')
    print(f"\nTotal events: {len(all_events)}")

    jira_events = db.query(
        measurement='cpu',
        tags={'worker': 'jira'}
    )
    print(f"Jira worker events: {len(jira_events)}")

    confluence_events = db.query(
        measurement='cpu',
        tags={'worker': 'confluence'}
    )
    print(f"Confluence worker events: {len(confluence_events)}")

    jira_east_events = db.query(
        measurement='cpu',
        tags={'worker': 'jira', 'region': 'us-east'}
    )

    jira_west_events = db.query(
        measurement='cpu',
        tags={'worker': 'jira', 'region': 'us-west'}
    )

    print("Jira worker aggregate metrics")
    sum_east = Aggregate.sum(jira_events, 'value')
    avg_east = Aggregate.average(jira_events, 'value')
    min_east = Aggregate.min(jira_events, 'value')
    max_east = Aggregate.max(jira_events, 'value')
    print_point(sum_east)
    print_point(avg_east)
    print_point(min_east)
    print_point(max_east)

    print("\n Jira worker us-east aggregate metrics")
    sum_jira_east = Aggregate.sum(jira_east_events, 'value')
    avg_jira_east = Aggregate.average(jira_east_events, 'value')
    min_jira_east = Aggregate.min(jira_east_events, 'value')
    max_jira_east = Aggregate.max(jira_east_events, 'value')
    print_point(sum_jira_east)
    print_point(avg_jira_east)
    print_point(min_jira_east)
    print_point(max_jira_east)

    print("\n Jira worker us-west aggregate metrics")
    sum_jira_west = Aggregate.sum(jira_west_events, 'value')
    avg_jira_west = Aggregate.average(jira_west_events, 'value')
    min_jira_west = Aggregate.min(jira_west_events, 'value')
    max_jira_west = Aggregate.max(jira_west_events, 'value')
    print_point(sum_jira_west)
    print_point(avg_jira_west)
    print_point(min_jira_west)
    print_point(max_jira_west)

def compression_example():
    cpu_usage_list = [random.randint(1, 100) for _ in range(1000000)]
    CompressionUtil.compress_simple(cpu_usage_list)
    CompressionUtil.compress_after_xor(cpu_usage_list)


def print_point(point: Point):
    """Helper function to print a Point object"""
    print(f"Measurement: {point.measurement}, Tags: {point.tags}, "
          f"Fields: {point.fields}, Timestamp: {point.timestamp}")

if __name__ == '__main__':
#     example_basic_write_and_query()
#     example_query_builder()
#     example_multiple_series()
#     example_point_objects()
#    example_search_platform()
    compression_example()

