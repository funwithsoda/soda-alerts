from flask import Flask
app = Flask(__name__)
import json
import uuid
import os
from flask import request, jsonify
if not 'data.json' in os.listdir('.'):
    with open('data.json', 'w') as f:
        f.write(json.dumps([]))
@app.route("/add_alert/")
def add_alert():
    random_id = str(uuid.uuid4())
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
    if '?' in request.args.get('url'):
        url = request.args.get('url')
    else:
        url = request.args.get('url') + '?'
    data.append({"id": random_id, "email": request.args.get('email'), "url": url, "confirmed": False})
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))
    import sendgrid
    with open('configuration.json', 'r') as f:
        configuration = json.loads(f.read())
        username = configuration['sendgrid_username']
        password = configuration['sendgrid_password']
    sg = sendgrid.SendGridClient(username, password)
    
    message = sendgrid.Mail()
    message.add_to(request.args.get('email'))
    message.set_subject('Example')
    message.set_html('<a href="'+configuration['domain']+'/confirm_alert/?id='+random_id+'">Click here to confirm</a>')
    message.set_from('Doe John <doe@email.com>')
    status, msg = sg.send(message)
    return jsonify(success=True)        
    
    
@app.route("/confirm_alert/")
def confirm_alert():
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
        for row in data:
            if row['id'] == request.args.get('id'):
                row['confirmed'] = True
                break
    with open('data.json', 'w') as f:
        f.write(json.dumps(f.read()))
    return jsonify(success=True)     
    
@app.route("/delete_alert/")
def delete_alert():
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
        for i, row in enumerate(data):
            if row['id'] == request.args.get('id'):
                del data[i]
                break
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))
    return jsonify(success=True)     

if __name__ == "__main__":
    app.run(debug=True)
