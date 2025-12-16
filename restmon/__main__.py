import os
import signal
from restmon.api import create_app
from restmon.state import set_not_ready


def handle_sigterm(signum, frame): # type: ignore
    print("SIGTERM received, switching to not_ready")
    set_not_ready()


signal.signal(signal.SIGTERM, handle_sigterm) # type: ignore

if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
    )