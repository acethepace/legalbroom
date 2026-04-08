import os
import httpx
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class Citation(BaseModel):
    id: str
    title: str
    court: str
    date_filed: str
    snippet: str
    url: str

class CourtListenerService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COURTLISTENER_API_KEY")
        self.base_url = "https://www.courtlistener.com/api/rest/v4/search/"
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Token {self.api_key}"} if self.api_key else {}
        )

    async def search(self, query: str, limit: int = 5) -> List[Citation]:
        params = {
            "q": query,
            "page_size": limit,
        }
        
        try:
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            citations = []
            
            for i, res in enumerate(results):
                print(f"DEBUG: CourtListener Raw Result: {res}")
                # Map CourtListener response to Citation schema
                case_name = res.get("caseName") or res.get("absolute_url", "Unknown Case")
                court = res.get("court", "Unknown Court")
                date_filed = res.get("dateFiled") or res.get("date_filed", "Unknown Date")
                opinions = res.get("opinions", []); snippet = opinions[0].get("snippet", "") if opinions else res.get("snippet", "")
                
                # Construct absolute URL
                relative_url = res.get("absolute_url", "")
                url = f"https://www.courtlistener.com{relative_url}" if relative_url else ""
                
                citations.append(Citation(
                    id=f"Source {i + 1}",
                    title=case_name,
                    court=court,
                    date_filed=date_filed,
                    snippet=snippet,
                    url=url
                ))
                
            return citations
            
        except httpx.HTTPStatusError as e:
            # Log error or handle it appropriately
            print(f"HTTP error occurred: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
