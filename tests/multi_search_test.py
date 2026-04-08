import pytest
import re
import time
from playwright.sync_api import Page, expect

def test_multi_search_refinement_e2e(page: Page):
    """
    Verify the iterative search logic in the Case Analysis flow.
    1. Navigates to http://localhost:3000/analysis.
    2. Enters a legal scenario that requires refined search.
    3. Asserts that the "Refining search..." status message appears.
    4. Asserts that citations are returned.
    """
    # 1. Navigate to http://localhost:3000/analysis
    print("Navigating to http://localhost:3000/analysis...")
    page.goto("http://localhost:3000/analysis")
    
    # 2. Enter a legal scenario that is likely to require refined search
    # We use a query that asks for a comprehensive list and multiple iterations.
    scenario = "I am researching AI copyright precedents in the Second Circuit. I need a very comprehensive list. Please perform an initial search, and then refine it at least once to find more specific cases from 2023 and 2024. I specifically want you to be thorough and search multiple times."
    print(f"Typing scenario: {scenario}")
    
    # The placeholder in AnalysisForm.tsx is long, so we use a substring match
    textarea = page.get_by_placeholder("Describe the case details", exact=False)
    expect(textarea).to_be_enabled(timeout=10000)
    textarea.fill(scenario)
    
    # 3. Submit the form
    submit_button = page.get_by_role("button", name="Submit for Analysis")
    expect(submit_button).to_be_enabled(timeout=5000)
    submit_button.click()
    
    # 4. Assert that the "Refining search..." status message appears
    print("Waiting for status messages...")
    
    status_messages = []
    refining_found = False
    
    # Monitor status messages for up to 5 minutes (LLM calls can be slow)
    start_time = time.time()
    while time.time() - start_time < 300:
        # Status messages are in divs with animate-pulse in Chat.tsx
        status_locator = page.locator("div.animate-pulse")
        count = status_locator.count()
        for i in range(count):
            try:
                text = status_locator.nth(i).inner_text().strip()
                if text and text not in status_messages:
                    status_messages.append(text)
                    print(f"Status: {text}")
                if "Refining search..." in text:
                    refining_found = True
            except:
                pass
        
        if refining_found:
            break
            
        # Check if we've already reached synthesis without finding "Refining search..."
        # If we see "Synthesizing answer..." it means we are past the search phase
        if any("Synthesizing answer..." in msg for msg in status_messages) and not refining_found:
            # Wait a few more seconds just in case the status message was missed
            page.wait_for_timeout(2000)
            # Re-check
            status_locator = page.locator("div.animate-pulse")
            for i in range(status_locator.count()):
                if "Refining search..." in status_locator.nth(i).inner_text():
                    refining_found = True
                    break
            if not refining_found:
                print("Reached synthesis without seeing 'Refining search...'.")
                break

        # Check for error
        error_locator = page.locator("text=Error")
        if error_locator.count() > 0:
            print(f"Detected error: {error_locator.first.inner_text()}")
            break

        page.wait_for_timeout(500)

    assert refining_found, f"Expected 'Refining search...' status, but only saw: {status_messages}"
    print("Status message 'Refining search...' appeared!")

    # 5. Assert that citations are returned
    print("Waiting for final synthesis and citations...")
    
    # Citations should appear in the SourcesPanel on the right
    # SourcesPanel.tsx renders citations in a list
    sources_panel = page.locator("aside, div.w-96").filter(has_text="Sources")
    
    # Wait for at least one citation to appear in the SourcesPanel
    # Citations are rendered as buttons or list items in SourcesPanel
    citation_item = page.locator("div.w-96 button").first
    expect(citation_item).to_be_visible(timeout=180000)
    
    print("Citations found in SourcesPanel!")

if __name__ == "__main__":
    import subprocess
    import sys
    # Run pytest on this file
    result = subprocess.run(["pytest", "-s", __file__])
    sys.exit(result.returncode)
