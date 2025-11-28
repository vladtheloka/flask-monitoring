from flask import Flask, jsonify
from restmon.resources import SystemResources

app = Flask(__name__)

@app.get("/system_info")
def system_info():
	return jsonify({
		"os_details": SystemResources.get_os_details(),
		"cpu_usage": SystemResources.get_cpu_usage(),
		"memory_usage": SystemResources.get_memory_usage(),
		"storage_usage": SystemResources.get_storage_usage(),
		"network_usage": SystemResources.get_network_usage(),
        "system_uptime": SystemResources.get_system_uptime(),
	})