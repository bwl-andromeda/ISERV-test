import logging
import unittest
from unittest.mock import patch
from logstash_async.handler import AsynchronousLogstashHandler
from opentelemetry.trace import set_tracer_provider
from pytracelog.base import (
    PyTraceLog, LOGSTASH_HOST, LOGSTASH_PORT, OTEL_EXPORTER_JAEGER_AGENT_HOST
)
from pytracelog.logging.handlers import (
    StdoutHandler, StderrHandler, TracerHandler
)


class TestPyTraceLog(unittest.TestCase):

    def test_init_root_logger(self):
        PyTraceLog.init_root_logger(level=logging.INFO)
        self.assertEqual(logging.root.level, logging.INFO)
        stdout_handler_found = any(isinstance(h, StdoutHandler)
                                   for h in logging.root.handlers)
        stderr_handler_found = any(isinstance(h, StderrHandler)
                                   for h in logging.root.handlers)
        self.assertTrue(stdout_handler_found,
                        "StdoutHandler не найден в корневом логгере")
        self.assertTrue(stderr_handler_found,
                        "StderrHandler не найден в корневом логгере")
        PyTraceLog.init_root_logger(level=logging.INFO)
        stdout_handler_count = sum(isinstance(h, StdoutHandler)
                                   for h in logging.root.handlers)
        stderr_handler_count = sum(isinstance(h, StderrHandler)
                                   for h in logging.root.handlers)
        self.assertEqual(stdout_handler_count, 1, "Дублирование StdoutHandler")
        self.assertEqual(stderr_handler_count, 1, "Дублирование StderrHandler")

    def test_init_tracer_logger(self):
        PyTraceLog.init_tracer_logger(level=logging.INFO)
        tracer_handler_found = any(isinstance(h, TracerHandler)
                                   for h in PyTraceLog._handlers)
        self.assertTrue(tracer_handler_found)
        PyTraceLog.init_tracer_logger(level=logging.INFO)
        tracer_handler_count = sum(isinstance(h, TracerHandler)
                                   for h in PyTraceLog._handlers)
        self.assertEqual(tracer_handler_count, 1)

    def test_reset(self):
        PyTraceLog.init_root_logger(level=logging.INFO)
        PyTraceLog.init_logstash_logger(level=logging.INFO)
        PyTraceLog.init_tracer_logger(level=logging.INFO)

        PyTraceLog.reset()
        self.assertEqual(logging.root.level, logging.WARNING)
        self.assertIsNone(PyTraceLog._old_factory)
        self.assertEqual(len(logging.root.handlers), 0)
        self.assertEqual(len(PyTraceLog._handlers), 0)


if __name__ == '__main__':
    unittest.main()
