from flask import Flask
from flask_restful import Resource, Api

import restmon.resources
import restmon.os_platform
import restmon.os

app = Flask(__name__)
api = Api(app)

#For Memory status
api.add_resource(resources.getMemory,'/memory')
#For CPU times
api.add_resource(resources.getCPU,'/cpu')
#CPU utilization in percent
api.add_resource(resources.getCPUPercent,'/cpupercent')
#Root partition status
api.add_resource(resources.getStorage,'/storage')
#Front Page		
api.add_resource(resources.frontPage,'/')
#Platform Details
api.add_resource(os_platform.getPlatform,'/platform')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=int(os.getenv('PORT', 9090)),debug=True)