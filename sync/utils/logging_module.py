import logging
import boto3
import os

from sync.handlers.config_handler import ConfigHandler

class Logger:
    def __init__(self, cloudwatch_group=None, cloudwatch_stream=None, log_file_name="application.log"):
        # Load the log directory from the configuration file
        config = ConfigHandler()
        log_directory = config.get_value('LOGGING', 'LOG_DIR')

        # Convert the path to an absolute directory and create it if it doesn't exist
        absolute_log_directory = os.path.abspath(log_directory)
        if not os.path.exists(absolute_log_directory):
            os.makedirs(absolute_log_directory)

        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # File handler
        log_file_path = os.path.join(absolute_log_directory, log_file_name)
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.INFO)

        # Formatter setup
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # Adding handlers to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

        # CloudWatch setup if given
        self.cloudwatch_group = cloudwatch_group
        self.cloudwatch_stream = cloudwatch_stream
        self.cloudwatch_client = None

        if self.cloudwatch_group and self.cloudwatch_stream:
            self.cloudwatch_client = boto3.client('logs')

    def log(self, level, message):
        self.logger.log(level, message)
        if self.cloudwatch_client:
            self._send_to_cloudwatch(level, message)

    def _send_to_cloudwatch(self, level, message):
        # Convert logging level to CloudWatch terminology
        level_map = {
            logging.CRITICAL: 'CRITICAL',
            logging.ERROR: 'ERROR',
            logging.WARNING: 'WARNING',
            logging.INFO: 'INFO',
            logging.DEBUG: 'DEBUG',
            logging.NOTSET: 'NOTSET'
        }
        cw_level = level_map.get(level, 'NOTSET')

        try:
            response = self.cloudwatch_client.create_log_stream(
                logGroupName=self.cloudwatch_group,
                logStreamName=self.cloudwatch_stream
            )

            log_event = {
                'timestamp': int(response['ResponseMetadata']['HTTPHeaders']['date']),
                'message': f'[{cw_level}] {message}'
            }

            response = self.cloudwatch_client.put_log_events(
                logGroupName=self.cloudwatch_group,
                logStreamName=self.cloudwatch_stream,
                logEvents=[log_event]
            )

        except Exception as e:
            self.logger.error(f"Error sending log to CloudWatch: {str(e)}")
