# Installation
Use git to clone this repository
`git clone https://github.com/fdhanh/create-api-demo.git`

# Prerequisite
Make sure you have python 3.6 installed on your machine
`python --version`

To run the script in this repository, you need to install the prerequisite library from requirements.txt
`pip install -r requirements.txt`

# Usage
Make sure that you have:
- Enabled Cloud Pub/Sub API 
- Create service account as an owner (Save json file to app folder)
- Activate Cloud SDK on your local device
- Install postman to your browser for post json.

Run `bash pubsub.sh` to create pubsub topic, subscription, and create BigQuery dataset

Run `python app\main.py`
Run `python app\subscriber.py` 
After API and subscriber is activated, go to postman (request URL: http://localhost/api/v1) and post something to check. For an example:
```
{"activities": [
	{
		"operation": "insert",
		"table": "table1",
		"col_names": ["a", "b"],
		"col_types": ["integer", "string"],
		"col_values": [20, "duapuluh"]
	},
	{
		"operation": "insert",
		"table": "table1",
		"col_names": ["c", "b"],
		"col_types": ["integer", "string"],
		"col_values": [21, "duasatu"]
	},
	{
		"operation": "insert",
		"table": "table1",
		"col_names": ["c", "b"],
		"col_types": ["integer", "string"],
		"col_values": [21, "duasatu"]
	}
	]
}
```

Remember that operation, table, col_names, col_values, col_types need to be added.<br>
Operation which is allowed are: insert and delete. Outside of that, it will return error.
Col_types which is allowed are: string, bytes, integer, float, numeric, bignumeric, boolean, timestamp, date, time, datetime, geography, record

