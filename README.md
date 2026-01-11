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
### Example 1: Find high CPU usage data points

```python
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
```

### Example 2: Compute aggregates on data points 

```python
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
