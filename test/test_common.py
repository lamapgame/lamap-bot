import pytest
from app.common import logger

class TestLogger:
    def setup_method(self):
        self.logger = logger.Logger()

    def test_admin(self):
        # self.logger.admin(...)
        assert False
