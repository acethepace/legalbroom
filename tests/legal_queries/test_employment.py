import pytest
from playwright.sync_api import Page
from .test_base import BaseLegalTest

class TestEmploymentLaw(BaseLegalTest):
    """
    Test suite for Employment Law queries.
    """

    def test_constructive_dismissal_ny(self, chat_client: Page):
        """
        Test Constructive Dismissal (NY) query.
        """
        query = "What are the requirements for a constructive dismissal claim in New York?"
        expected_keywords = ["constructive dismissal", "New York", "resignation", "intolerable"]
        self.verify_query(chat_client, query, expected_keywords)

    def test_non_compete_overbreadth(self, chat_client: Page):
        """
        Test Non-competes (overbreadth) query.
        """
        query = "How do courts evaluate the overbreadth of geographic restrictions in non-compete agreements?"
        expected_keywords = ["non-compete", "geographic", "overbreadth"]
        self.verify_query(chat_client, query, expected_keywords)
