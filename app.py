from flask import Flask
app = Flask(__name__)

@app.route("/add_alert/")
def add_alert():
    return "Hello World!"
    
@app.route("/confirm_alert/")
def confirm_alert():
    return "Hello World!"
    
@app.route("/delete_alert/")
def delete_alert():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
