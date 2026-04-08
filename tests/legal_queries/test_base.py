import re
from playwright.sync_api import Page, expect

class BaseLegalTest:
    """
    Base class for legal query tests providing common verification logic.
    """
    
    def verify_query(self, page: Page, query: str, expected_keywords: list[str], min_citations: int = 1):
        """
        Executes a legal query and verifies the response quality and structure.
        
        Args:
            page: The Playwright Page object.
            query: The legal query string to send.
            expected_keywords: List of keywords (regex) expected in the response.
            min_citations: Minimum number of [Source N] markers expected.
        """
        # 1. Type the query into the chat input
        chat_input = page.get_by_placeholder("Inquire about legal precedents...")
        expect(chat_input).to_be_enabled(timeout=5000)
        chat_input.fill(query)
        chat_input.press("Enter")

        # 2. Assert status transitions
        # The status message is in a div with animate-pulse
        status_msg = page.locator("div.animate-pulse")
        
        # Wait for the status message to indicate processing (any status)
        expect(status_msg).to_be_visible(timeout=20000)

        # 3. Assert response contains [Source N] markers
        # The assistant's response is in the last .markdown-content div
        content_locator = page.locator(".markdown-content").last
        
        # Wait for the response to start appearing
        expect(content_locator).to_be_visible(timeout=90000)
        
        # Wait for the status message to disappear, indicating the response is complete
        expect(status_msg).not_to_be_visible(timeout=60000)
        
        # Wait for at least one source marker to appear if min_citations > 0
        if min_citations > 0:
            expect(content_locator).to_contain_text(re.compile(r"\[Source \d+\]"), timeout=30000)

        # Get the full text of the response
        full_text = content_locator.inner_text()

        # Assert [Source N] markers
        # We use a regex to find them: [Source 1], [Source 2], etc.
        source_markers = re.findall(r"\[Source \d+\]", full_text)
        assert len(source_markers) >= min_citations, f"Expected at least {min_citations} [Source N] markers, found {len(source_markers)}. Full text: {full_text}"

        # 4. Assert expected_keywords are present in the final response
        for keyword in expected_keywords:
            assert re.search(keyword, full_text, re.IGNORECASE), f"Keyword '{keyword}' not found in response. Full text: {full_text}"
