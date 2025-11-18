from subprocess import Popen, PIPE
from flask_restful import Resource


def run_cmd(cmd):
    return (
        Popen(cmd, stdout=PIPE)
        .communicate()[0]
        .decode("utf-8")
        .strip()
    )


class getPlatform(Resource):
    def get(self):
        kernel = run_cmd(["uname", "-r"])
        hostname = run_cmd(["uname", "-n"])
        architecture = run_cmd(["uname", "-m"])
        os_name = run_cmd(["uname", "-o"])

        return {
            "kernelversion": kernel,
            "operatingsystem": os_name,
            "hostname": hostname,
            "architecture": architecture,
        }
