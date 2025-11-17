import subprocess
from flask_restful import Resource


def run(cmd):
    return subprocess.check_output(cmd).strip()


class GetPlatform(Resource):
    def get(self):
        return {
            'kernelversion': run(['uname', '-r']),
            'hostname': run(['uname', '-n']),
            'architecture': run(['uname', '-m']),
            'operatingsystem': run(['uname', '-o']),
        }
