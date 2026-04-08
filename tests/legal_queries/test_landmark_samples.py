import pytest
from playwright.sync_api import Page
from .test_base import BaseLegalTest

class TestLandmarkSamples(BaseLegalTest):
    """
    Landmark Sample Test Suite to verify retrieval relevance for key legal scenarios.
    """

    def test_constitutional_law_terry(self, chat_client: Page):
        """
        Test Constitutional Law (Vehicle Search/Terry).
        """
        query = (
            "A police officer stopped a vehicle for a minor traffic violation. During the stop, "
            "the officer noticed the driver was acting nervous and proceeded to search the glove "
            "compartment without a warrant or the driver's consent, finding a concealed weapon. "
            "The driver was not under arrest at the time of the search. I need an analysis of "
            "whether this search exceeds the scope of a Terry stop and relevant precedents "
            "regarding warrantless vehicle searches in the absence of probable cause."
        )
        expected_keywords = [r"(Fourth Amendment|Terry v\. Ohio)", r"warrantless search"]
        self.verify_query(chat_client, query, expected_keywords)

    def test_employment_law_bdo_seidman(self, chat_client: Page):
        """
        Test Employment Law (Non-Compete/BDO Seidman).
        """
        query = (
            "My client is a senior marketing executive who signed a non-compete agreement with a "
            "former employer in New York. The agreement prohibits the executive from working for "
            "any 'competitor' in the 'North American continent' for a period of 24 months. My "
            "client has been offered a role at a smaller firm that operates in a slightly different "
            "niche. I need to find cases where New York courts have found geographic and temporal "
            "restrictions of this magnitude to be 'unreasonable' or 'overbroad.' Specifically, "
            "look for the BDO Seidman standard."
        )
        expected_keywords = [r"non-compete", r"BDO Seidman", r"reasonable"]
        self.verify_query(chat_client, query, expected_keywords)

    def test_corporate_law_netjets(self, chat_client: Page):
        """
        Test Corporate Law (Piercing the Veil/NetJets).
        """
        query = (
            "A creditor is attempting to collect a $500,000 judgment against a defunct LLC. The "
            "sole member of the LLC frequently used the company's business account to pay for "
            "personal mortgage payments and luxury travel. There were no corporate minutes ever "
            "recorded, and the company was consistently undercapitalized. I am looking for recent "
            "cases in Delaware regarding the 'alter ego' theory and specific factors that led "
            "courts to pierce the corporate veil in single-member LLCs. Mention NetJets Aviation if relevant."
        )
        expected_keywords = [r"corporate veil", r"alter ego", r"(NetJets|Delaware)"]
        self.verify_query(chat_client, query, expected_keywords)

    def test_administrative_law_howey(self, chat_client: Page):
        """
        Test Administrative Law (SEC/Crypto/Howey).
        """
        query = (
            "My client is launching a new utility token for a decentralized storage network. "
            "The SEC has recently been aggressive in classifying such tokens as securities. "
            "I need an analysis of how the Howey test is currently being applied to 'utility tokens' "
            "in the crypto space, specifically looking for cases where the 'expectation of profit' "
            "prong was successfully challenged because the token had a primary consumptive use."
        )
        expected_keywords = [r"Howey test", r"(investment contract|expectation of profit)"]
        self.verify_query(chat_client, query, expected_keywords)
