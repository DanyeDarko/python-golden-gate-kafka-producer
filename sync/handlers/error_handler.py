import logging

from sync.utils.logging_module import Logger

class ErrorHandler:
    def __init__(self):
        self.logger = Logger()

    def handle_parse_error(self, transaction_str, exception):
        """
        Handle XML parsing errors and log the malformed XML.
        """
        error_msg = f"Se detectó un XML malformado:\n{transaction_str} \n{exception}"
        self.logger.log(logging.ERROR, error_msg)

        with open("malformed_xml.txt", "a", encoding="utf-8") as file:
            file.write(transaction_str)

    def handle_generic_error(self, error_msg, exception):
        """
        Handle generic errors and log them.
        """
        full_msg = f"{error_msg} \n{exception}"
        self.logger.log(logging.ERROR, full_msg)
