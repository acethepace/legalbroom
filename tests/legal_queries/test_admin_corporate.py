import pytest
from playwright.sync_api import Page
from .test_base import BaseLegalTest

class TestAdminCorporateLaw(BaseLegalTest):
    """
    Test suite for Administrative and Corporate Law queries.
    """

    def test_chevron_doctrine_challenges(self, chat_client: Page):
        """
        Test Chevron Doctrine (challenges) query.
        """
        query = "What are the current legal challenges to the Chevron doctrine in administrative law?"
        expected_keywords = ["Chevron", "defer", "administrative"]
        self.verify_query(chat_client, query, expected_keywords)

    def test_sec_crypto_investment_contracts(self, chat_client: Page):
        """
        Test SEC/Crypto (investment contracts) query.
        """
        query = "How does the SEC apply the Howey test to determine if a cryptocurrency is an investment contract?"
        expected_keywords = ["SEC", "Howey", "cryptocurrency", "investment contract"]
        self.verify_query(chat_client, query, expected_keywords)
