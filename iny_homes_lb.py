import requests
import time
import json
from datetime import datetime
import random
from collections import deque

# Define all available servers
SERVERS = [
    "http://35.200.185.69:8000/v1/autocomplete",
    "http://35.200.185.69:8000/v2/autocomplete",
    "http://35.200.185.69:8000/v3/autocomplete",
]

REQUEST_COUNT = 0

TIMEOUT = 10  # Request timeout in seconds
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Track requests per server for stats
SERVER_REQUESTS = {url: 0 for url in SERVERS}
SERVER_FAILURES = {url: 0 for url in SERVERS}

# Server queue for round-robin load balancing
SERVER_QUEUE = deque(SERVERS)

def get_next_server():
    """Get the next server using round-robin approach."""
    # Rotate the queue and return the first element
    SERVER_QUEUE.rotate(-1)
    return SERVER_QUEUE[0]

def make_request(query: str):
    """Make a load-balanced request across multiple servers."""
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    
    # Try each server until we get a successful response
    for _ in range(len(SERVERS)):
        server_url = get_next_server()
        SERVER_REQUESTS[server_url] += 1
        
        try:
            start_time = time.time()
            response = requests.get(server_url, params={"query": query}, headers=HEADERS, timeout=TIMEOUT)
            elapsed_time = time.time() - start_time
            
            if response.status_code == 429:
                # This server is rate limited, try another one
                SERVER_FAILURES[server_url] += 1
                print(f"Rate limited on {server_url.split('/')[-2]}. Trying next server...")
                continue
                
            # Print response for debugging
            print(f"\nQuery: '{query}' | Server: {server_url.split('/')[-2]} | Status: {response.status_code} | Time: {elapsed_time:.3f}s")
            print(f"Response: {response.text[:100]}..." if len(response.text) > 100 else f"Response: {response.text}")
            
            if response.status_code == 200:
                return response.json()
            else:
                # This server returned an error, try another one
                SERVER_FAILURES[server_url] += 1
                print(f"Error from {server_url.split('/')[-2]}, trying next server...")
                
        except requests.exceptions.RequestException as e:
            SERVER_FAILURES[server_url] += 1
            print(f"Request error for '{query}' on {server_url.split('/')[-2]}: {e}")
    
    # If we've tried all servers and none worked
    print(f"All servers failed for query: '{query}'")
    return None

def extract_names():
    """
    Extract all possible names from the API using recursive exploration.
    For each name found, the function will query that name to find additional connected names
    until no new names are discovered.
    """
    
    to_process = set()  # Queue of names to process
    names_found = []
    # Start with a-z prefixes
    from datetime import datetime

    # Initialize with single-letter prefixes (a to z)
    prefixes = {chr(i) for i in range(ord('a'), ord('z') + 1)}
    to_process = set(prefixes)  # Separate queue to track elements to process

    print("\nStarting recursive name extraction from API...")
    start_time = datetime.now()

    # Process names dynamically
    while to_process:
        current_prefix = to_process.pop()  # Remove and process one element at a time
        names_found.append(current_prefix)

        result = make_request(current_prefix)
        if result and isinstance(result, dict) and "results" in result:
            names = set(result["results"])  # Extract names
            new_names = names - prefixes  # Filter out already seen names

            if new_names:
                prefixes.update(new_names)  # Add to master set
                to_process.update(new_names)  # Queue new names for processing
                print(f"Prefix '{current_prefix}': Found {len(names)} names, {len(new_names)} are new")
            else:
                print(f"Prefix '{current_prefix}': No new names added")
        else:
            print(f"Prefix '{current_prefix}': No result returned")

    
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    print(f"\nExtraction complete!")
    print(f"Total unique names found: {len(names_found)}")
    print(f"Total API requests made: {REQUEST_COUNT}")
    print(f"Total time elapsed: {elapsed:.2f} seconds")
  
    # Print server stats
    print("\nServer Statistics:")
    for server_url in SERVERS:
        server_name = server_url.split('/')[-2]
        success_rate = ((SERVER_REQUESTS[server_url] - SERVER_FAILURES[server_url]) / SERVER_REQUESTS[server_url] * 100) if SERVER_REQUESTS[server_url] > 0 else 0
        print(f"  {server_name}: {SERVER_REQUESTS[server_url]} requests, {SERVER_FAILURES[server_url]} failures, {success_rate:.1f}% success rate")
    
    return {
        "names": sorted(names_found),
        "total_time": elapsed,
        "request_count": REQUEST_COUNT,
        "server_stats": {url.split('/')[-2]: {"requests": SERVER_REQUESTS[url], "failures": SERVER_FAILURES[url]} for url in SERVERS}
    }

if __name__ == "__main__":
    # Test each server with a basic query
    print("Testing all servers with a simple query...")
    for server in SERVERS:
        server_name = server.split('/')[-2]
        # Use direct call to test each server individually
        try:
            response = requests.get(server, params={"query": "a"}, headers=HEADERS, timeout=TIMEOUT)
            print(f"Server {server_name}: Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Server {server_name}: Error - {e}")
    
    # Extract all names with load balancing
    results = extract_names()

    # Print summary
    print("\nFinal Summary:")
    print(f"Total unique names found: {len(results['names'])}")
    print(f"Total requests made: {results['request_count']}")
    print(f"Total time taken: {results['total_time']:.2f}s")
    
    # Save results to file
    output_file = f"all_names_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_file}")