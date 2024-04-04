import sys

sys.path.append('/home/danielbrito/Develop/2024/MADO/data-lake/app/')

from watchdog.observers import Observer
from handlers.file_change_handler import FileChangeHandler
from handlers.config_handler import ConfigHandler


if __name__ == "__main__":
    config_handler = ConfigHandler()
    DIR_PATH = config_handler.get_value('DEFAULT', 'DIR_PATH')
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, DIR_PATH, recursive=True)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
