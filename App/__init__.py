from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'palavra-secreta'



from App import routes