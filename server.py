from flask import Flask
from flask import jsonify
app = Flask(__name__)

from air_quality_monitor import AirQualityMonitor

@app.route('/air_quality')
def measure():
    air_quality = air_quality_monitor.measure()
    return jsonify(air_quality)

if __name__ == '__main__':
    air_quality_monitor = AirQualityMonitor()
    app.run(host='0.0.0.0')

