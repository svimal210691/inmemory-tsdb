# In-Memory Time Series Database

An in-memory implementation of a time series database similar to InfluxDB, written in Python.

## Features

- **Time-stamped data points**: Store data with measurements, tags, and fields
- **Efficient queries**: Fast time-range queries using sorted data structures
- **Tag-based filtering**: Filter data by metadata tags
- **Field filtering**: Query by field values with various operators
- **Multiple series**: Automatically groups points by measurement and tags
- **In-memory storage**: Fast access with no disk I/O overhead
- **Aggregation functions**: Simple aggregation functions like sum, mean, min, max on time series data 

## Installation

No external dependencies required - uses only Python standard library.

```bash
cd /Users/vsharma3/work/repos/inmemory-tsdb
# Python 3.7+ required
```

## Quick Start

```python
from src.database import InMemoryTSDB
from src.point import Point
from datetime import datetime, timedelta

# Create database instance
db = InMemoryTSDB()

# Write a data point
db.write(
    measurement='cpu',
    fields={'usage': 45.2, 'temperature': 65.0},
    tags={'host': 'server1', 'region': 'us-east'},
    timestamp=datetime.now()
)

# Write multiple points
for i in range(10):
    db.write(
        measurement='temperature',
        fields={'value': 20 + i},
        tags={'sensor': 'sensor1'},
        timestamp=datetime.now() - timedelta(minutes=i)
    )

# Query data
points = db.query(
    measurement='cpu',
    tags={'host': 'server1'},
    start=datetime.now() - timedelta(hours=1)
)

# Using query builder
query = db.create_query()
results = (query
    .from_measurement('temperature')
    .where_tags(sensor='sensor1')
    .time_range(start=datetime.now() - timedelta(hours=1))
    .where_field('value', '>', 25)
    .limit(10)
    .execute(db._series))

# Get statistics
stats = db.get_stats()
print(f"Total points: {stats['total_points']}")
print(f"Series count: {stats['series_count']}")
print(f"Measurements: {stats['measurements']}")
```

## API Reference

### InMemoryTSDB

Main database class.

#### Methods

- `write(measurement, fields, tags=None, timestamp=None)`: Write a single data point
- `write_points(points)`: Write multiple points at once
- `query(measurement=None, tags=None, start=None, end=None, limit=None)`: Query the database
- `create_query()`: Create a query builder
- `get_measurements()`: Get list of all measurement names
- `get_series_count()`: Get total number of series
- `get_point_count()`: Get total number of points
- `delete_measurement(measurement)`: Delete all series for a measurement
- `delete_series(measurement, tags)`: Delete a specific series
- `clear()`: Clear all data
- `get_stats()`: Get database statistics

### Point

Represents a single data point.

#### Attributes

- `measurement`: Measurement name (string)
- `fields`: Dictionary of field name-value pairs
- `tags`: Dictionary of tag name-value pairs (optional)
- `timestamp`: Datetime object (optional, defaults to now)

### Query

Query builder for complex queries.

#### Methods

- `from_measurement(measurement)`: Filter by measurement
- `where_tags(**tags)`: Filter by tag key-value pairs
- `time_range(start, end)`: Filter by time range
- `where_field(field_name, operator, value)`: Filter by field value
  - Operators: `=`, `!=`, `>`, `<`, `>=`, `<=`
- `limit(n)`: Limit number of results
- `execute(series_dict)`: Execute query and return results

## Examples

### Example 1: CPU Monitoring

```python
from src.database import InMemoryTSDB
from datetime import datetime, timedelta

db = InMemoryTSDB()

# Simulate CPU monitoring data
for i in range(100):
    db.write(
        measurement='cpu',
        fields={'usage': 50 + (i % 30), 'load': 1.5 + (i % 10) * 0.1},
        tags={'host': f'server{i % 5}', 'region': 'us-east'},
        timestamp=datetime.now() - timedelta(minutes=100-i)
    )

# Query recent high CPU usage
high_cpu = db.query(
    measurement='cpu',
    start=datetime.now() - timedelta(hours=1)
)

# Filter by field value
query = db.create_query()
high_usage = (query
    .from_measurement('cpu')
    .where_field('usage', '>', 70)
    .limit(20)
    .execute(db._series))
```

### Example 2: Sensor Data

```python
def example_search_platform():
    """Example 5: Searching platform information"""
    print("\n Add some CPU metrics for FDS service in different regions and worker groups")
    print("\n Then query data points in a time range")
    print("\n And then demo some aggregation functions on time series data")x

    db = InMemoryTSDB()
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
```

## Performance Considerations

- Points are stored sorted by timestamp for efficient range queries
- Series are indexed by measurement and tags for fast lookups
- All data is stored in memory - suitable for moderate data volumes
- For very large datasets, consider implementing data retention policies

## Limitations

- Data is not persisted (in-memory only)
- No replication or clustering
- No authentication or authorization
- Single-threaded (not thread-safe)

## Future Enhancements

Potential improvements:
- Data persistence (JSON, CSV, or binary format)
- Thread-safe operations
- Data retention policies
