import requests
import time
import json
import sendgrid
import re

with open('configuration.json', 'r') as f:
    configuration = json.loads(f.read())

def remove_dollar_component(url, component):
    if '&' in url:
        m = re.search('(?P<select>\$%s=.*&)' % (component), url)
    else:
        m = re.search('(?P<select>\$%s=.*)' % (component), url)
    if m:
        what_to_replace = m.group('select')
        url = url.replace(what_to_replace, '')
    return url

def get_last_created_at(url):
    # remove $select, $limit, and $order
    for component in ['select', 'limit', 'order']:
        url = remove_dollar_component(url, component)
    return requests.get('%s&$limit=1&$select=:created_at&$order=:created_at%%20DESC&$$app_token=%s' % (url, configuration['socrata_app_token'])).json()

def process_alert_job():
    if not 'last_created_at' in alert_job and alert_job['confirmed']:
        result = get_last_created_at(alert_job['url'])
        alert_job['last_created_at'] = result[0][':created_at']
    elif alert_job['confirmed']:
        the_data = requests.get('%s&$where=:created_at%%20>%%20"%s"&$$app_token=%s' % (alert_job["url"], alert_job['last_created_at'], configuration['socrata_app_token'])).json()
        result = get_last_created_at(alert_job['url'])
        alert_job['last_created_at'] = result[0][':created_at']
        if not the_data:
            continue
        html_of_data = """
        <style>
        td, th {
        border:1px solid #000;
        margin:5px;
        text-align:left;
        vertical-align:top;
        }
        
        </style>
        <table>"""
        keys = []
        for row in the_data[0]:
            for key in row.keys():
                if not key in keys:
                    keys.append(key)
        html_of_data += '<tr>'
        for key in keys:
            html_of_data += '<th>%s</th>' % (key)
        html_of_data += '</tr>'
        for row in the_data:
            html_of_data += '<tr>'
            print row
            for key in keys:
                value = ''
                if row.get(key):
                    value = row.get(key)
                html_of_data += '<td>%s</td>' % (value)
            html_of_data += '</tr>'
        html_of_data += '</table>'
        
        username = configuration['sendgrid_username']
        password = configuration['sendgrid_password']
        sg = sendgrid.SendGridClient(username, password)
    
        message = sendgrid.Mail()
        message.add_to(alert_job['email'])
        message.set_subject('Alert for '+alert_job['url'])
        message.set_html(html_of_data+'<a href="'+configuration['domain']+'/delete_alert/?id='+alert_job["id"]+'">Click here to delete alert</a>')
        message.set_from('Doe John <doe@email.com>')
        status, msg = sg.send(message)
    return alert_job

def process_alert_jobs():
    with open('data.json', 'r') as f:
        alert_jobs = json.loads(f.read())
    for alert_job in alert_jobs:
        alert_job.update(process_alert_job(alert_job))
    with open('data.json', 'w') as f:
        f.write(json.dumps(alert_jobs))

while True:
    process_alert_jobs()
    time.sleep(60*5)
