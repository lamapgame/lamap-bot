import pytest
from common import logger

class TestLogger:
    def setup_method(self):
        self.logger = logger.Logger("Tester")

    def test_admin(self):
        # self.logger.admin(...)
        assert False
