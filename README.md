# ivy_homes
# Autocomplete API Extractor

A Python script for extracting names from multiple autocomplete API servers with load balancing capabilities.

## Overview

This tool connects to multiple autocomplete API servers to retrieve all possible name suggestions by using recursive exploration. It implements a round-robin load balancing strategy to distribute requests across available servers and provides detailed statistics about the extraction process.

## Features

- **Multi-server support**: Connects to multiple API endpoints (v1, v2, v3)
- **Load balancing**: Uses a round-robin approach to distribute requests across servers
- **Automatic failover**: Tries alternative servers when one fails or is rate-limited
- **Recursive exploration**: Discovers all possible autocomplete suggestions by exploring responses
- **Detailed statistics**: Tracks request counts, success rates, and performance metrics
- **Results export**: Saves extracted names to a timestamped JSON file

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone this repository or download the script
2. Install required dependencies:

```bash
pip install requests
```

## Usage

Simply run the script:

```bash
python autocomplete_extractor.py
```

The script will:
1. Test each server with a basic query
2. Begin recursive name extraction starting with single-letter prefixes (a-z)
3. Process each autocomplete suggestion to find additional connected names
4. Display real-time progress and statistics
5. Save all discovered names to a JSON file

## How It Works

1. The script initializes with a set of single-letter prefixes (a-z)
2. For each prefix, it queries the autocomplete API
3. New names found in responses are added to the processing queue
4. The process continues until no new names are discovered
5. Load balancing ensures requests are distributed across all available servers
6. If a server fails or returns an error, the script automatically tries the next server

## Configuration

You can modify these variables at the top of the script:

- `SERVERS`: List of API endpoint URLs
- `TIMEOUT`: Request timeout in seconds (default: 10)
- `HEADERS`: HTTP headers for requests

## Output

The script generates:
1. Real-time console output showing extraction progress
2. A summary of statistics upon completion 
3. A JSON file containing all extracted names and detailed metrics

The JSON file is named `all_names_YYYYMMDD_HHMMSS.json` with the following structure:

```json
{
  "names": ["name1", "name2", ...],
  "total_time": 123.45,
  "request_count": 500,
  "server_stats": {
    "v1": {"requests": 170, "failures": 2},
    "v2": {"requests": 165, "failures": 1},
    "v3": {"requests": 165, "failures": 3}
  }
}
```
