import pytest
from playwright.sync_api import Page
from .test_base import BaseLegalTest

class TestCriminalProcedure(BaseLegalTest):
    """
    Test suite for Criminal Procedure queries.
    """

    def test_miranda_rights_custody(self, chat_client: Page):
        """
        Test Miranda Rights (custody) query.
        """
        query = "What is the holding in Miranda v. Arizona regarding police interrogation?"
        expected_keywords = ["Miranda", "interrogation", "Fifth Amendment"]
        self.verify_query(chat_client, query, expected_keywords)

    def test_sixth_amendment_speedy_trial_covid(self, chat_client: Page):
        """
        Test Sixth Amendment (speedy trial COVID) query.
        """
        query = "How have courts addressed Sixth Amendment speedy trial claims in the context of COVID-19 related delays?"
        expected_keywords = ["Sixth Amendment", "speedy trial", "COVID", "delay"]
        self.verify_query(chat_client, query, expected_keywords)
