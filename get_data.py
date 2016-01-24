import requests
for alert_job in []:
    if not 'last_created_at' in alert_job and alert_job['confirmed']:
        result = requests.get('%s&$limit=1&$select=:created_at&$order=:created_at DESC&$$app_token=%s' % (alert_job[url], configuration['socrata_app_token'])).json()
        alert_job['last_created_at'] = result[':created_at']
    elif alert_job['confirmed']:
        the_data = requests.get('%s&$app_token=%s' % (alert_job[url], configuration['socrata_app_token'])).json()
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
        sg = sendgrid.SendGridClient(username=username, password=password)
    
        message = sendgrid.Mail()
        message.add_to(alert_job['email'])
        message.set_subject('Alert for '+alert_job['url'])
        message.set_html(html_of_data+'<a href="'+configuration['domain']+'/delete_alert/?id='+random_id+'">Click here to delete alert</a>')
        message.set_from('Doe John <doe@email.com>')
        status, msg = sg.send(message)
