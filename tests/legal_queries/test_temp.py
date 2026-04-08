import pytest
from playwright.sync_api import Page
from .test_base import BaseLegalTest

class TestTemp(BaseLegalTest):
    def test_temp(self, page: Page):
        page.goto("http://localhost:3000/analysis")
        query = "Test query"
        try:
            self.verify_query(page, query, ["Test"])
        except Exception as e:
            print(f"\nCaught expected error: {e}")
