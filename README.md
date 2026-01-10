# In-Memory Time Series Database

An in-memory implementation of a time series database similar to InfluxDB, written in Python.

## Features

- **Time-stamped data points**: Store data with measurements, tags, and fields
- **Efficient queries**: Fast time-range queries using sorted data structures
- **Tag-based filtering**: Filter data by metadata tags
- **Field filtering**: Query by field values with various operators
- **Multiple series**: Automatically groups points by measurement and tags
- **In-memory storage**: Fast access with no disk I/O overhead

## Installation

No external dependencies required - uses only Python standard library.

```bash
cd /Users/vsharma3/work/repos/influxdb-inmemory
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
from src.database import InMemoryTSDB
from datetime import datetime, timedelta
import random

db = InMemoryTSDB()

# Simulate temperature sensor data
sensors = ['sensor1', 'sensor2', 'sensor3']
for sensor in sensors:
    for i in range(50):
        db.write(
            measurement='temperature',
            fields={'value': 20 + random.uniform(-5, 5)},
            tags={'sensor': sensor, 'location': 'warehouse'},
            timestamp=datetime.now() - timedelta(minutes=50-i)
        )

# Query specific sensor
sensor1_data = db.query(
    measurement='temperature',
    tags={'sensor': 'sensor1'},
    start=datetime.now() - timedelta(hours=1)
)

# Find anomalies
query = db.create_query()
anomalies = (query
    .from_measurement('temperature')
    .where_field('value', '>', 25)
    .execute(db._series))
```

### Example 3: Using Point Objects

```python
from src.database import InMemoryTSDB
from src.point import Point
from datetime import datetime

db = InMemoryTSDB()

# Create points explicitly
points = [
    Point(
        measurement='events',
        fields={'count': 10, 'duration': 1.5},
        tags={'type': 'api', 'status': 'success'},
        timestamp=datetime.now()
    ),
    Point(
        measurement='events',
        fields={'count': 5, 'duration': 0.8},
        tags={'type': 'api', 'status': 'error'},
        timestamp=datetime.now()
    )
]

db.write_points(points)

# Query all events
all_events = db.query(measurement='events')
```

## Performance Considerations

- Points are stored sorted by timestamp for efficient range queries
- Series are indexed by measurement and tags for fast lookups
- All data is stored in memory - suitable for moderate data volumes
- For very large datasets, consider implementing data retention policies

## Limitations

- Data is not persisted (in-memory only)
- No built-in aggregation functions (can be added in application layer)
- No replication or clustering
- No authentication or authorization
- Single-threaded (not thread-safe)

## Future Enhancements

Potential improvements:
- Data persistence (JSON, CSV, or binary format)
- Aggregation functions (mean, sum, max, min, etc.)
- Thread-safe operations
- Data retention policies
- Export/import functionality
- Query optimization

## License

This is a simple implementation for demonstration purposes.

