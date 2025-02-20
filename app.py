from flask import Flask
from place.api import place_bp
from weather.api import weather_bp
app = Flask(__name__)

app.register_blueprint(place_bp, url_prefix='/api')
app.register_blueprint(weather_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)