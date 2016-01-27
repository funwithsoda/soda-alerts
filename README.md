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

### Health

Examples provided by Mark Silverberg (to-do: turn these into SODA queries)
- Alert me when a hospital near me has updated data or their score for a measure is below the national average: https://data.medicare.gov/Hospital-Compare/Complications-Hospital/632h-zaca
- Alert me when a new hospital/facility is added to this dataset: https://data.medicare.gov/Hospital-Compare/Hospital-General-Information/xubh-q36u , http://www.opendatanetwork.com/search?q=hospitals
- Alert me when deaths in my city for the most recent week exceed X or are 1.5X the number for last year: https://data.cdc.gov/NNDSS/TABLE-III-Deaths-in-122-U-S-cities/rpjd-ejph
- Alert me when an establishment in my zip code gets a failed rating: https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5

### Public Safety

#### Alert of any new Seattle Fire Department response incidents

```
import requests
requests.get('http://localhost:5000/add_alert/?email=tim@insideyourgovernment.com&url=https://data.seattle.gov/resource/grwu-wqtk.json')
```

#### Alert of any new Seattle Fire Department fire calls 
