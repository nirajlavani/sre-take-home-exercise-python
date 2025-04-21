import yaml
import requests
import sys
import time
from collections import defaultdict


# Function to load configuration from the YAML file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML format: {e}")

# Function to perform health checks
def check_health(endpoint):
    url = endpoint.get("url")
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        start = time.time()
        response = requests.request(method, url, headers=headers, json=body)
        duration = (time.time() - start) * 1000

        if duration <= 500 and 200 <= response.status_code < 300:
            return "UP"
        else:
            print(f"DOWN: {url}")
            print(f" - Status: {response.status_code}")
            print(f" - Time: {int(duration)}ms")
            return "DOWN"
    except requests.RequestException:
        print(f"DOWN: {url}")
        print(f" - Error: {e}")
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path, frequency):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            result = check_health(endpoint)

            domain = endpoint["url"].split("//")[-1].split("/")[0].split(":")[0]
            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(frequency)

# Entry point of the program
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)
    try:
        config_file = sys.argv[1]
        monitor_endpoints(config_file, 15)

    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error has occurred: {e}")