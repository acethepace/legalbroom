import pytest
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def chat_client(page: Page):
    """
    Fixture to navigate to the chat page and wait for the "LIVE" status.
    """
    # Navigate to the frontend
    page.goto("http://localhost:3000")
    
    # Wait for the connection to be established
    # Instead of just checking for "Live" text, wait for the chat input to be enabled 
    # and for its placeholder to contain "Inquire".
    # This is a more direct indicator that the WebSocket is open and the application is ready.
    chat_input = page.get_by_placeholder(re.compile(r"Inquire", re.IGNORECASE))
    expect(chat_input).to_be_enabled(timeout=30000)
    
    return page
