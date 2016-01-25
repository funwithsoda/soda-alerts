# soda-alerts
This is a REST API for creating and managing alerts of new results for queries to Socrata datasets. The supported method for getting alerts is email. Future methods include SMS, webhooks, websockets, and Twitter. 

To make this lightweight I decided against using a real database and CRON.

## Install

1. Copy config_example.json to configuration.json and fill in the details
2. Run `pip install -r requirements.txt`
3. Run `python app.py` and `python get_data.py`

## Usage

Send a get request to `/add_alert/` with email address and the Socrata API url. You need to encode the URL if it has parameters like  `https://data.seattle.gov/resource/grwu-wqtk.json?type=Aid Response` E.g. `https%3A//data.seattle.gov/resource/grwu-wqtk.json%3Ftype%3DAid%20Response`

## Examples

### Alert of any new Seattle Fire Department response incidents

```
import requests
requests.get('http://localhost:5000/add_alert/?email=tim@insideyourgovernment.com&url=https://data.seattle.gov/resource/grwu-wqtk.json')
```

### Alert of any new Seattle Fire Department fire calls 
