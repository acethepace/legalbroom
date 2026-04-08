import pytest
import re
from playwright.sync_api import Page, expect

def test_case_analysis_e2e(page: Page):
    # 1. Navigate to http://localhost:3000/analysis
    print("Navigating to http://localhost:3000/analysis...")
    page.goto("http://localhost:3000/analysis")
    
    # 2. Fill the case details text area with a sample legal scenario
    scenario = "A police officer stopped a vehicle for a minor traffic violation. During the stop, the officer noticed a suspicious package in the back seat and searched the vehicle without a warrant, finding illegal substances. The defendant claims this was an unreasonable search and seizure under the Fourth Amendment."
    print(f"Typing scenario: {scenario}")
    
    # The textarea can be found by placeholder
    textarea = page.get_by_placeholder("Describe the case details")
    expect(textarea).to_be_enabled(timeout=10000)
    textarea.fill(scenario)
    
    # 3. Submit the form
    submit_button = page.get_by_role("button", name="Submit for Analysis")
    expect(submit_button).to_be_enabled(timeout=5000)
    submit_button.click()
    
    # 4. Assert that the "Grading case relevance..." status appears
    print("Waiting for 'Grading case relevance...' status...")
    status_msg = page.locator("div.animate-pulse").filter(has_text="Grading case relevance...")
    
    try:
        expect(status_msg).to_be_visible(timeout=30000)
        print("Status message 'Grading case relevance...' appeared.")
    except Exception as e:
        print(f"Status message did not appear. Current page content: {page.content()[:1000]}...")
        raise e
        
    # 5. Assert that the final summary cites the relevant cases using [Source N]
    print("Waiting for response and citations...")
    
    # The assistant's response is in the last .markdown-content div
    content_locator = page.locator(".markdown-content").last
    
    # Wait for the response to start appearing
    expect(content_locator).to_be_visible(timeout=90000)
    
    # Wait for the status message to disappear, indicating the response is complete
    last_message = page.locator(".markdown-content").last.locator("..")
    expect(last_message.locator("div.animate-pulse")).not_to_be_visible(timeout=90000)
    
    # Wait for at least one citation button or [Source N] marker to appear
    try:
        # The frontend renders [1] as a button with just the number
        citation_button = last_message.locator("button").filter(has_text=re.compile(r"^\d+$")).first
        expect(citation_button).to_be_visible(timeout=60000)
        print("Citation button found!")
    except Exception:
        # Fallback: check if it's rendered as text
        expect(content_locator).to_contain_text(re.compile(r"\[Source \d+\]"), timeout=60000)
        print("[Source N] text found!")
    
    # Get the full text of the response
    full_text = content_locator.inner_text()
    print(f"Final response text: {full_text[:200]}...")
    
    # Assert [Source N] markers
    source_markers = re.findall(r"\[Source \d+\]", full_text)
    if not source_markers:
        # Fallback: check if it's rendered as a button with just the number
        citation_buttons = last_message.locator("button").filter(has_text=re.compile(r"^\d+$"))
        if citation_buttons.count() > 0:
            print(f"Found {citation_buttons.count()} citation buttons instead of [Source N] text.")
        else:
            assert False, f"Expected [Source N] markers, found none. Full text: {full_text}"
    else:
        print(f"Found source markers: {source_markers}")
        assert len(source_markers) > 0, "Expected at least one [Source N] marker."

if __name__ == "__main__":
    import subprocess
    subprocess.run(["pytest", "-s", __file__])
