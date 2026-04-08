import pytest
from playwright.sync_api import Page
from .test_base import BaseLegalTest

class TestConstitutionalLaw(BaseLegalTest):
    """
    Test suite for Constitutional Law queries.
    """

    def test_fourth_amendment_digital_privacy(self, chat_client: Page):
        """
        Test Fourth Amendment (digital privacy) query.
        """
        query = "What are the Fourth Amendment implications for digital privacy and cell phone searches?"
        expected_keywords = ["Fourth Amendment", "privacy", "search", "digital"]
        self.verify_query(chat_client, query, expected_keywords)

    def test_qualified_immunity_standard(self, chat_client: Page):
        """
        Test Qualified Immunity (standard) query.
        """
        query = "What is the current legal standard for qualified immunity for public officials?"
        expected_keywords = ["qualified immunity", "clearly established", "public official"]
        self.verify_query(chat_client, query, expected_keywords)
