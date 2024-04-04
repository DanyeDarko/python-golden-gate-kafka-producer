
import logging
from watchdog.events import FileSystemEventHandler
import sys

# sys.path.append('/home/danielbrito/Develop/2024/MADO/data-lake/app/sync')

from sync.handlers.file_buffer_handler import FileBufferHandler
from sync.handlers.error_handler import ErrorHandler
from sync.handlers.config_handler import ConfigHandler
from sync.utils.logging_module import Logger
from sync.database.data_module import Database


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

        self.config = ConfigHandler()
        self.buffer_handler = FileBufferHandler()
        self.error_handler = ErrorHandler()
        self.database = Database()
        self.logger = Logger()

    def _update_buffer(self, file):
        last_position = self.database.get_last_position(file)
        print(f"Last position: {last_position}")
        self.buffer_handler.update(file, last_position)

        # Guardamos la posición actual del archivo después de procesarlo
        current_position = self.buffer_handler.get_current_position(file)
        print(f"Current position: {current_position}")
        self.database.set_last_position(file, current_position)

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            self.logger.log(logging.INFO, f"Archivo modificado: {file_path}")
            if not self.buffer_handler.has_buffer(file_path):
                self.logger.log(logging.INFO, f"Init Buffer to file: {file_path}")
                self.buffer_handler.init_buffer(file_path)

            self._update_buffer(file_path)
