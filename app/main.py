from flask import Blueprint, jsonify
from .utils import get_cpu_usage, get_memory_usage 
from .utils import get_disk_usage, top_processes

main_bp = Blueprint('main', __name__)

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@main_bp.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        "cpu_percent": get_cpu_usage(),
        "memory_percent": get_memory_usage(),
        "disk_percent": get_disk_usage()
    })

@main_bp.route('/processes', methods=['GET'])
def processes():
    return jsonify({"top_processes": top_processes()})
