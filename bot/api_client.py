import aiohttp
import asyncio
import logging
from typing import Any, Dict, List, Optional

# For debugging and observability
logger = logging.getLogger("api_client")
logger.setLevel(logging.INFO)

# For local debugging
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class APIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        """Safely close the session."""
        if self.session and not self.session.closed:
            await self.session.close()

    # Generic request handler
    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        """
        Handles HTTP requests with centralized error management and logging.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with APIClient(...)'.")

        try:
            async with self.session.request(method, url, **kwargs) as response:
                # Log and handle non-2xx status codes
                if response.status >= 400:
                    text = await response.text()
                    logger.error(f"HTTP {response.status} on {url}: {text}")
                    return None

                # Return parsed JSON
                try:
                    return await response.json()
                except aiohttp.ContentTypeError:
                    logger.warning(f"Non-JSON response from {url}")
                    return None

        except aiohttp.ClientError as e:
            logger.error(f"Network error while calling {url}: {e}")
            return None
        except asyncio.TimeoutError:
            logger.error(f"Request to {url} timed out.")
            return None

    # Event CRUD
    async def get_events(self) -> List[Dict[str, Any]]:
        """Fetch all events."""
        return await self._request("GET", "/events") or []

    async def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific event by ID."""
        return await self._request("GET", f"/events/{event_id}")

    async def create_event(self, event_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new event."""
        return await self._request("POST", "/events", json=event_data)

    async def update_event(self, event_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing event."""
        return await self._request("PUT", f"/events/{event_id}", json=update_data)

    async def delete_event(self, event_id: str) -> bool:
        """Delete an event by ID."""
        resp = await self._request("DELETE", f"/events/{event_id}")
        return bool(resp)

    # Cyber Fact CRUD
    async def get_facts(self) -> List[Dict[str, Any]]:
        """Fetch all cybersecurity facts."""
        return await self._request("GET", "/facts") or []

    async def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific fact by ID."""
        return await self._request("GET", f"/facts/{fact_id}")

    async def create_fact(self, fact_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new cybersecurity fact."""
        return await self._request("POST", "/facts", json=fact_data)

    async def update_fact(self, fact_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a cybersecurity fact."""
        return await self._request("PUT", f"/facts/{fact_id}", json=update_data)

    async def delete_fact(self, fact_id: str) -> bool:
        """Delete a cybersecurity fact."""
        resp = await self._request("DELETE", f"/facts/{fact_id}")
        return bool(resp)

    # Cyber Joke CRUD
    async def get_jokes(self) -> List[Dict[str, Any]]:
        """Fetch all cybersecurity jokes."""
        return await self._request("GET", "/jokes") or []

    async def get_joke(self, joke_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific joke by ID."""
        return await self._request("GET", f"/jokes/{joke_id}")

    async def create_joke(self, joke_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new cybersecurity joke."""
        return await self._request("POST", "/jokes/", json=joke_data)

    async def update_joke(self, joke_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a cybersecurity joke."""
        return await self._request("PUT", f"/jokes/{joke_id}", json=update_data)

    async def delete_joke(self, joke_id: str) -> bool:
        """Delete a cybersecurity joke."""
        resp = await self._request("DELETE", f"/jokes/{joke_id}")
        return bool(resp)

    # Quiz CRUD
    async def get_quizzes(self):
        """Fetch all quizzes."""
        return await self._request("GET", "/quiz") or []

    async def get_quiz(self, quiz_id: str):
        """Fetch a quiz by ID."""
        return await self._request("GET", f"/quiz/{quiz_id}")

    async def create_quiz(self, quiz_data: dict):
        """Create a new quiz."""
        return await self._request("POST", "/quiz", json=quiz_data)

    async def delete_quiz(self, quiz_id: str):
        """Delete a quiz."""
        return await self._request("DELETE", f"/quiz/{quiz_id}")

    # About CRUD
    async def get_about(self) -> Optional[Dict[str, Any]]:
        """Fetch about-us information."""
        return await self._request("GET", "/about")

    # Quote CRUD
    async def get_quotes(self) -> List[Dict[str, Any]]:
        """Fetch all cybersecurity quotes."""
        return await self._request("GET", "/quotes") or []
    
    async def get_quote(self, quote_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a specific quote by ID."""
        return await self._request("GET", f"/quotes/{quote_id}")

    async def create_quote(self, quote_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new cybersecurity quote."""
        return await self._request("POST", "/quotes/", json=quote_data)

    async def update_quote(self, quote_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a cybersecurity quote."""
        return await self._request("PUT", f"/quotes/{quote_id}", json=update_data)

    async def delete_quote(self, quote_id: str) -> bool:
        """Delete a cybersecurity quote."""
        resp = await self._request("DELETE", f"/quotes/{quote_id}")
        return bool(resp)
