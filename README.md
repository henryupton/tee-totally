# Tee Totally - Golf Tee Time Manager

A Python CLI tool for finding and monitoring golf tee times at New Zealand golf courses.

## Features

- **Find Available Tee Times**: Search for available slots with flexible filtering
- **Monitor Changes**: Track tee time availability changes over time
- **Advanced Filtering**: Filter by time periods, day of week, number of players, and more
- **Club Management**: List and manage golf club information
- **Data Comparison**: Compare tee time states between different time periods

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tee-totally
```

2. Install dependencies:
```bash
pip install pendulum click beautifulsoup4 requests selenium
```

3. Install ChromeDriver (for club data updates):
```bash
# macOS
brew install chromedriver

# Or download from https://chromedriver.chromium.org/
```

## Quick Start

### Find Available Tee Times

```bash
# Basic search for next 7 days
python3 cli.py get --club-id 341

# Find specific tee times with filters
python3 cli.py find --club-id 341 \
  --from "2025-08-27 00:00:00" \
  --to "2025-08-30 23:59:59" \
  --period morning \
  --free-slots 2
```

### List Available Clubs

```bash
# Show all clubs
python3 cli.py list

# Show specific fields
python3 cli.py list --fields name club_id url
```

## CLI Commands

### `find` - Advanced Tee Time Search

The most powerful command for finding tee times with comprehensive filtering options.

**Required Options:**
- `--club-id` - Golf club ID to search
- `--from` - Start timestamp (YYYY-MM-DD HH:MM:SS)
- `--to` - End timestamp (YYYY-MM-DD HH:MM:SS)

**Filtering Options:**
- `--time-range` - Time range filter (HH:MM-HH:MM, e.g., 08:00-12:00)
- `--period` - Predefined periods: dawn, morning, noon, afternoon, evening
- `--free-slots` - Minimum free slots required (default: 1)
- `--playing-partners` - Minimum booked slots by other players
- `--day-of-week` - Filter by specific days (can specify multiple)

**Examples:**

```bash
# Find morning tee times on weekends
python3 cli.py find --club-id 341 \
  --from "2025-08-27 00:00:00" \
  --to "2025-09-02 23:59:59" \
  --period morning \
  --day-of-week saturday \
  --day-of-week sunday

# Find tee times with existing partners (2+ players already booked)
python3 cli.py find --club-id 341 \
  --from "2025-08-27 00:00:00" \
  --to "2025-08-27 23:59:59" \
  --playing-partners 2 \
  --free-slots 1

# Custom time range on specific days
python3 cli.py find --club-id 341 \
  --from "2025-08-27 00:00:00" \
  --to "2025-09-02 23:59:59" \
  --time-range "14:00-17:00" \
  --day-of-week wednesday \
  --day-of-week friday
```

### `get` - Fetch and Monitor Tee Times

```bash
# Get tee times for next 7 days (default)
python3 cli.py get --club-id 341

# Get tee times for specific date range
python3 cli.py get --club-id 341 \
  --booking-date "2025-08-27" \
  --look-forward-days 14
```

### `list` - Show Available Clubs

```bash
# Show all club information
python3 cli.py list

# Show specific fields only
python3 cli.py list --fields name club_id booking_url
```

### `compare` - Compare Tee Time States

```bash
# Compare two tee time files
python3 cli.py compare \
  --file-a clubs/341/2025-08-27/tee_times_123.json \
  --file-b clubs/341/2025-08-27/tee_times_456.json

# Save comparison to file
python3 cli.py compare \
  --file-a file1.json \
  --file-b file2.json \
  --output-path comparison.json
```

## Time Period Reference

When using `--period`, the following time ranges apply:

| Period    | Time Range |
|-----------|------------|
| `dawn`    | 05:00-07:00 |
| `morning` | 07:00-12:00 |
| `noon`    | 11:00-14:00 |
| `afternoon` | 12:00-18:00 |
| `evening` | 17:00-21:00 |

## Data Storage

- Tee time data is stored in `clubs/{club_id}/{date}/tee_times_{timestamp}.json`
- Club information is stored in `clubs/manifests/manifest_{timestamp}.json`
- The system automatically tracks changes between runs

## Filtering Logic

### Free Slots vs Playing Partners

- `--free-slots N`: Requires at least N available slots
- `--playing-partners N`: Requires at least N already booked slots
- **Constraint**: `free-slots + playing-partners ≤ 4` (golf foursome limit)

### Multiple Day Selection

```bash
# Multiple days can be specified
--day-of-week monday --day-of-week wednesday --day-of-week friday
```

### Time Filtering Priority

1. `--time-range` takes precedence over `--period` if both specified
2. Day-of-week filtering happens before API calls (efficient)
3. All other filters are applied to results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions, please create an issue in the repository.