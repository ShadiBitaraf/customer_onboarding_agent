# app/services/saas_api_client.py
import aiohttp
from app.dependencies import settings

class SaaSAPIClient:
    def __init__(self):
        self.base_url = settings.SAAS_API_URL
        self.api_key = settings.API_KEY

    async def onboard_customer(self, customer_data: dict):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}{settings.MOCK_SAAS_API_SUCCESS}"
            async with session.post(url, json=customer_data, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_url = f"{self.base_url}{settings.MOCK_SAAS_API_ERROR}"
                    async with session.get(error_url) as error_response:
                        return await error_response.json()

saas_api_client = SaaSAPIClient()