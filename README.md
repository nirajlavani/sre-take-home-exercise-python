# Endpoint Availability Monitor
This is a simple Python script that monitors the availability of HTTP endpoints with a given YAML config file. The script with check the endpoint's status every 15 seconds by default and logs the cumulative availability as a percentage. This script is a take home assessment provided by Fetch.

## Features
- Accepts a YAML config file of endpoints
- Sends 'GET' or 'POST' requests
- Considers an endpoint as "UP" if...
  - Status is 2XX
  - Response Body is valid JSON
  - Response completes within 500ms
- Tracks availability per domain while ignoring ports
- Resistant to timeouts and invalid responses
- Prints logs every 15 seconds by default

## Install
Ensure [Python 3.6+](https://realpython.com/installing-python/) is installed.

Install `pyyaml` and `requests` with:
```bash
pip3 install -r requirements.txt
```

## Usage
Run the following command:
```bash
python3 main.py sample.yaml
```
Expected format to run the script (if you want to use your own yaml configuration files):
```bash
python3 main.py <path-to-yaml-file>
```
## Example Output
```
UP: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body
 - Status: 200

UP: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/
 - Status: 200

DOWN: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body
 - Status: 422
 - Response: Failed to deserialize the JSON body into the target type: missing field `foo` at line 1 column 2

DOWN: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/error
 - Error: Request timed out (over 500ms)

dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com has 50% availability percentage
---
```

## Code Changes
A good bit of changes were made to the original script.
### Identifying Issues
There were many issues at first glance.
- Little to no exception handling
- No logging
- Missing functionality

I first started with fixing the Entry Point of the script then working on each function call in order of execution. Once I got the script running, I wrote in some safeguards for any potential pitfalls (invalid JSON body, timeout exceptions, invalid yaml path, etc.). One of the final steps was to ensure readability (write comments, make sure the character count per line doesn't surpass 80, etc.) Below is a summary of the changes made. 

### Major Changes
- Error handling in `load_config()` to ensure the user-provided yaml file was found and parsed successfully.
- In `monitor_endpoints()`, isolated the domain name from the port by appending `.split(":")[0]`. This could also be done "cleaner" with `urlparse(endpoint["url"]).hostname` but requires an additional import. 
- Exception handling in `check_health()` like `requests.Timeout` and `requests.RequestException`.
- Parsed the body if it's a JSON string.

### Minor Changes
- Specified the request within `check_health()` to timeout after 500ms.
- Moved the `import sys` statement to the top of the file.
- Added print statements to log errors, responses, and status of a response in `check_health()`.
- Made the time frequency (in seconds) a default parameter of the monitor_endpoints() function for better readability.
- Cleaner shutdown with `sys.exit(0)` when the user performs a keyboard interrupt... technically not needed.
- Added more comments for better readability.
- Added a generic exception block in the entry point to catch and log any unforseen errors.

## Contact
Email me at `1907niraj@gmail.com` for further assistance!
