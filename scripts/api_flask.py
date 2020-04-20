from flask import Flask
from Service.compare_image_v2 import CompareImageV2

app = Flask(__name__)

@app.route('/similares/<id>')
def similares(id):
    return CompareImageV2().get_similares(id)