# soda-alerts
Allows one to get email alerts using the Socrata Open Data API. Other hooks to consider adding are Twitter Bots and Web Hooks and Websockets.

To make this lightweight I decided against using a real database and CRON.

Install:

1. Copy configuration_example.json to configuration.json and fill in the details
2. Run app.py and get_data.py

Example:

```
import requests
requests.get('http://localhost:5000/add_alert/?email=tim@insideyourgovernment.com&url=https://data.seattle.gov/resource/grwu-wqtk.json')
```
