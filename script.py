import requests # for making HTTP requests
import json # for working with JSON data
import datetime # for getting the current time
import boto3 # for interacting with S3
import os # for getting environment variables

# Create an S3 resource
s3 = boto3.resource('s3')
# Get the Grafana API key from an environment variable
keyenv = os.environ["GRAFANA_KEY"]
key = f"Bearer {keyenv}"
# Get the current time in UTC in the format "YYYY-MM-DDTHH"
time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H")
# Get the Grafana URL from an environment variable
url = os.environ["GRAFANA_URL"]
# Get the name of the S3 bucket from an environment variable
bucket = os.environ["S3_BUCKET"]

print("Getting list")

# Get a list of dashboards from the Grafana API
folders = requests.get(f"{url}/api/search?type=dash-db", headers = {"Authorization": key}).json()

# Get the UIDs of the dashboards
uids = [ sub["uid"] for sub in folders ]

# Iterate over the dashboard UIDs
for i in uids:
    print(f"Getting {i} ...")
    
    # Get the JSON from the Grafana API
    dashboard = requests.get(f"{url}/api/dashboards/uid/{i}", headers = {"Authorization": key}).json()
    
    # Get the acual JSON part, due to the API adding on a meta block
    thejson = json.dumps(dashboard["dashboard"])
    
    # Upload the JSON data to S3
    print(f"Uploading {time}/{i}.json ...")
    s3.Bucket(bucket).put_object(Key=f"{time}/{i}.json", Body=thejson)