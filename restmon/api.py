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
api.add_resource(frontPage, "/")
api.add_resource(getMemory, "/memory")
api.add_resource(getCPU, "/cpu")
api.add_resource(getCPUPercent, "/cpupercent")
api.add_resource(getStorage, "/storage")
api.add_resource(getPlatform, "/platform")
