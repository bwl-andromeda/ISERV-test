import unittest
import logging
from unittest.mock import MagicMock, patch
from opentelemetry.trace import StatusCode, Status
from pytracelog.logging.handlers import StdoutHandler, StderrHandler, TracerHandler


class TestHandlers(unittest.TestCase):

    def test_stdout_handler(self):
        handler = StdoutHandler()
        record_info = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Info message",
            args=(),
            exc_info=None
        )
        record_error = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=20,
            msg="Error message",
            args=(),
            exc_info=None
        )
        self.assertTrue(handler.error_record_filter(record_info))
        self.assertFalse(handler.error_record_filter(record_error))


if __name__ == '__main__':
    unittest.main()
