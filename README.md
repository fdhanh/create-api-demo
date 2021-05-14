# Gatekeeper API: Stream Processing of Database User Activity
## Case
In a company, the back end will build a system that can capture all database user activity data. 
As a data engineer we will transport the data in real time and then put it in some database (BigQuery) so that later the business team will be able to create the reports they need. 
Unfortunately, the backend will not allow us to tap their databases since accessing production data directly will potentially harm the database performance. The backend team will send the user activity in JSON format so we have to prepare our API (Application Programming Interface) called Gatekeeper.

## API
An API is a set of programming code that enables data transmission between one software product and another. It also contains the terms of this data exchange.

## Installation
Use git to clone this repository
```git clone https://github.com/fdhanh/create-api-demo.git```

## Prerequisite
- Make sure you have python 3.6 installed on your machine
```python --version```
- Enabled Cloud Pub/Sub API 
- Create service account as an owner (Save json file to app folder)
- Activate Cloud SDK on your local device
- Install postman to your browser for post json

To run the script in this repository, you need to install the prerequisite library from requirements.txt
```pip install -r requirements.txt```

## Usage
Make sure that you have:

Run `bash pubsub.sh` to create pubsub topic, subscription, and create BigQuery dataset.

Run `python app\main.py`
![alt text](https://github.com/fdhanh/gatekeeper-api/blob/master/img/main-terminal.JPG?raw=true)

Run `python app\subscriber.py` 

After API and subscriber is activated, go to postman (request URL: http://localhost/api/v1) and post something to check. For an example:
```
{"activities": [
	{
		"operation": "insert",
		"table": "t1",
		"col_names": ["a", "b"],
		"col_types": ["integer", "string"],
		"col_values": [20, "duapuluh"]
	},
	{
		"operation": "insert",
		"table": "t1",
		"col_names": ["a", "c"],
		"col_types": ["integer", "string"],
		"col_values": [1, "check alter column"]
	},
	{
		"operation": "insert",
		"table": "t2",
		"col_names": ["id", "notes"],
		"col_types": ["integer", "string"],
		"col_values": [1, "insert row1"]
	},
	{
		"operation": "insert",
		"table": "t2",
		"col_names": ["id", "notes"],
		"col_types": ["integer", "string"],
		"col_values": [2, "insert row2 to delete"]
	},
	{
		"operation": "delete",
		"table": "t2",
		"col_names": ["id", "notes"],
		"col_types": ["integer", "string"],
		"col_values": [2, "insert row2 to delete"]
	}]
}
```

Remember that operation, table, col_names, col_values, col_types need to be added.<br>
Operation which is allowed are: insert and delete. Outside of that, it will return error. <br>
Col_types which is allowed are: string, bytes, integer, float, numeric, bignumeric, boolean, timestamp, date, time, datetime, geography, record.

