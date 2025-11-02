# tests/mocks/api_client.py

from unittest.mock import MagicMock


# noinspection PyUnusedLocal
class MockCrossRefClient:
    """
    A mock client that simulates the CrossRefClient for testing purposes.
    It now includes a mock session to handle DOI resolution checks.
    """

    def __init__(self, email: str):
        self.email = email
        self.doi_map = {
            "Attention Is All You Need": "10.1234/attention.doi"
        }

        # --- NEW: Create a mock session object ---
        self.session = MagicMock()
        # Configure the 'head' method of the mock session to call our helper
        self.session.head.side_effect = self._mock_head_request

    @staticmethod
    def _mock_head_request(url, **kwargs):
        """Simulates the response from a HEAD request to doi.org."""
        mock_response = MagicMock()

        # We'll pretend that the DOI for the "Attention" paper is the only valid one.
        if "10.1234/attention.doi" in url:
            mock_response.status_code = 302  # Simulate a successful redirect
        else:
            mock_response.status_code = 404  # Simulate Not Found for any other DOI

        return mock_response

    def get_doi_for_entry(self, entry: dict) -> str or None:
        """Simulates finding a DOI based on the entry's title."""
        title = entry.get("title")
        return self.doi_map.get(title)

    @staticmethod
    def get_metadata_by_doi(doi: str, original_entry: dict) -> dict or None:
        """Simulates returning canonical metadata for a known DOI."""
        if doi == "10.1234/attention.doi":
            return {
                "title": ["Attention Is All You Need (Canonical)"],
                "author": [{"family": "Vaswani", "given": "Ashish"}],
                "year": "2017"
            }
        return None
