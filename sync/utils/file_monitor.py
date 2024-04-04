import logging

from watchdog.observers import Observer
from sync.handlers.config_handler import ConfigHandler
from sync.utils.logging_module import Logger

class FileMonitor:
    def __init__(self, dir_path=None, event_handler_class=None):
        # If no dir_path provided, fetch from config
        self.config = ConfigHandler()
        self.logger = Logger()

        if not dir_path:
            dir_path = self.config.get_value('DEFAULT', 'DIR_PATH')

        if not event_handler_class:
            self.logger.log(logging.ERROR, "No event handler class provided.")
            raise ValueError("An event handler class must be provided.")

        self.dir_path = dir_path
        self.event_handler = event_handler_class()
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self.event_handler, path=self.dir_path, recursive=False)
        self.observer.start()
        self.logger.log(logging.INFO, f"File monitor started for directory: {self.dir_path}")

        try:
            self.observer.join()
        except KeyboardInterrupt:
            self.logger.log(logging.INFO, "File monitor interrupted.")
            self.stop()

    def stop(self):
        self.observer.stop()
        self.logger.log(logging.INFO, "File monitor stopped.")
