from flask import Flask
from routes.user import form_bp
import config

app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = config.SECRET_KEY
app.register_blueprint(form_bp)

app.run(debug=True)
