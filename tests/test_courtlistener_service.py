import asyncio
import httpx
from unittest.mock import AsyncMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.services.courtlistener import CourtListenerService, Citation

async def test_search_mapping():
    print("Running test_search_mapping...")
    # Mock response data
    mock_response_data = {
        "results": [
            {
                "caseName": "Test Case 1",
                "court": "Test Court 1",
                "date_filed": "2024-01-01",
                "snippet": "Snippet 1",
                "absolute_url": "/opinion/1/"
            },
            {
                "caseName": None,
                "court": "Test Court 2",
                "date_filed": "2024-02-02",
                "snippet": "Snippet 2",
                "absolute_url": "/opinion/2/"
            }
        ]
    }

    # Initialize service
    service = CourtListenerService(api_key="test_key")
    
    # Mock httpx.AsyncClient.get
    with patch.object(httpx.AsyncClient, 'get', new_callable=AsyncMock) as mock_get:
        mock_request = httpx.Request("GET", "https://www.courtlistener.com/api/rest/v3/search/")
        mock_get.return_value = httpx.Response(200, json=mock_response_data, request=mock_request)
        
        results = await service.search("test query", limit=2)
        
        assert len(results) == 2
        
        # Verify first result
        assert results[0].id == "Source 1"
        assert results[0].title == "Test Case 1"
        assert results[0].court == "Test Court 1"
        assert results[0].date_filed == "2024-01-01"
        assert results[0].snippet == "Snippet 1"
        assert results[0].url == "https://www.courtlistener.com/opinion/1/"
        
        # Verify second result (fallback for title)
        assert results[1].id == "Source 2"
        assert results[1].title == "/opinion/2/"
        assert results[1].court == "Test Court 2"
        assert results[1].date_filed == "2024-02-02"
        assert results[1].snippet == "Snippet 2"
        assert results[1].url == "https://www.courtlistener.com/opinion/2/"
    print("test_search_mapping passed!")

async def test_search_error_handling():
    print("Running test_search_error_handling...")
    service = CourtListenerService(api_key="test_key")
    
    with patch.object(httpx.AsyncClient, 'get', new_callable=AsyncMock) as mock_get:
        # Create a mock response for the error
        mock_response = httpx.Response(500, request=httpx.Request("GET", "https://test.com"))
        mock_get.side_effect = httpx.HTTPStatusError("Error", request=mock_response.request, response=mock_response)
        
        results = await service.search("test query")
        assert results == []
    print("test_search_error_handling passed!")

async def main():
    try:
        await test_search_mapping()
        await test_search_error_handling()
        print("\nAll tests passed successfully!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
