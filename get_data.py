import requests
import time
import json
with open('configuration.json', 'r') as f:
    configuration = json.loads(f.read())
while True:
    with open('data.json', 'r') as f:
        alert_jobs = json.loads(f.read())
    for alert_job in alert_jobs:
        if not 'last_created_at' in alert_job and alert_job['confirmed']:
            result = requests.get('%s&$limit=1&$select=:created_at&$order=:created_at DESC&$$app_token=%s' % (alert_job["url"], configuration['socrata_app_token'])).json()
            alert_job['last_created_at'] = result[':created_at']
        elif alert_job['confirmed']:
            the_data = requests.get('%s&$where=:created_at%%20>%%20"%s"&$app_token=%s' % (alert_job["url"], alert_job['last_created_at'], configuration['socrata_app_token'])).json()
            result = requests.get('%s&$limit=1&$select=:created_at&$order=:created_at DESC&$$app_token=%s' % (alert_job["url"], configuration['socrata_app_token'])).json()
            alert_job['last_created_at'] = result[':created_at']
            if not the_data:
                continue
            html_of_data = '<table>'
            keys = sorted(the_data.keys())
            html_of_data += '<tr>'
            for key in keys:
                html_of_data += '<th>%s</th>' % (key)
            html_of_data += '</tr>'
            for row in the_data:
                html_of_data += '<tr>'
                for key in keys:
                    html_of_data += '<td>%s</td>' % (row[key])
                html_of_data += '</tr>'
            html_of_data += '</table>'
            
            username = configuration['sendgrid_username']
            password = configuration['sendgrid_password']
            sg = sendgrid.SendGridClient(username, password)
        
            message = sendgrid.Mail()
            message.add_to(alert_job['email'])
            message.set_subject('Alert for '+alert_job['url'])
            message.set_html(html_of_data+'<a href="'+configuration['domain']+'/delete_alert/?id='+random_id+'">Click here to delete alert</a>')
            message.set_from('Doe John <doe@email.com>')
            status, msg = sg.send(message)
    with open('data.json', 'w') as f:
        f.write(json.dumps(alert_jobs))
    time.sleep(60*5)
