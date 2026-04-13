

"""Main application - orchestrates backend and frontend with event bus"""

import time
import threading
from productivity_app.infrastructure.events import EventBus
from productivity_app.interface.frontend import FrontEnd
from productivity_app.services.app_service import BackEnd


class Main:
    def __init__(self):
        self.event_bus = EventBus()
        self.backend = BackEnd(self.event_bus)
        self.frontend = FrontEnd(self.event_bus)
        self.running = True

    def main(self):
        """Start the application with backend on separate thread"""
        print("[Main] Starting application")

        backend_thread = threading.Thread(target=self._run_backend, daemon=True)
        backend_thread.start()

        self.frontend.step()

    def _run_backend(self):
        """Background loop for backend"""
        print("[Main] Backend thread started")
        while self.running:
            self.backend.step()
            time.sleep(1)


def run():
    """Entry point for console script (pyproject.toml)"""
    main = Main()
    main.main()


if __name__ == "__main__":
    run()
