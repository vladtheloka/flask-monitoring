from flask import Flask
from flask_restful import Api

from .resources import (
    getMemory,
    getCPU,
    getCPUPercent,
    getStorage,
    frontPage,
)

from .os_platform import getPlatform

app = Flask(__name__)
api = Api(app)

# Routes
# register function-based view handlers directly to avoid passing unknown types to flask-restful's typing
app.add_url_rule("/", "frontPage", frontPage)
app.add_url_rule("/memory", "getMemory", getMemory)
app.add_url_rule("/cpu", "getCPU", getCPU)
app.add_url_rule("/cpupercent", "getCPUPercent", getCPUPercent)
app.add_url_rule("/storage", "getStorage", getStorage)
app.add_url_rule("/platform", "getPlatform", getPlatform)
