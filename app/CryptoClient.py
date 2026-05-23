import os
from dotenv import load_dotenv
import requests


class CryptoClientError(Exception):
    pass

class CryptoClient:
    _BASE_URL_COINGECKO = "https://api.coingecko.com/api/v3"
    _BASE_URL_ALTERNATIVE = "https://api.alternative.me"
    _BASE_URL_COINSTATS = "https://openapiv1.coinstats.app"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        load_dotenv()
        self._api_key = os.environ.get("COINSTATS_API_KEY")
        
    
    def _get(self, base_url, endpoint, params=None, headers=None):
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.Timeout:
            raise CryptoClientError(f"Request timed out after {self.timeout}s.")
        except requests.ConnectionError:
            raise CryptoClientError("Could not connect to the API.")
        except requests.RequestException as e:
            raise CryptoClientError(f"Request failed: {e}")

        if response.status_code == 429:
            raise CryptoClientError("Rate limit exceeded. Please slow down requests.")
        if not response.ok:
            raise CryptoClientError(f"HTTP {response.status_code}: {response.text}")

        try:
            return response.json()
        except ValueError:
            raise CryptoClientError("API returned invalid JSON.")

    def _coinstats_headers(self):
        if not self._api_key:
            raise CryptoClientError(
                "COINSTATS_API_KEY environment variable is not set."
            )
        return {"X-API-KEY": self._api_key}

    def get_coins(self, coin_ids):
        params = {
            "ids": ",".join(coin_ids),
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "precision": "full",
        }
        
        return self._get(
            base_url=self._BASE_URL_COINGECKO,
            endpoint="/simple/price",
            params=params,
        )

    def get_trending_coins(self):
        response = self._get(
            base_url=self._BASE_URL_COINGECKO,
            endpoint="/search/trending",
            params={"precision": "full"},
        )
        return [
            {
                "id": coin["item"]["id"],
                "name": coin["item"]["name"],
                "symbol": coin["item"]["symbol"],
                "market_cap_rank": coin["item"]["market_cap_rank"],
                "market_cap_usd": coin["item"]["data"]["market_cap"][1:],
                "price_usd": coin["item"]["data"]["price"],
                "price_change_percentage_24h": (
                    coin["item"]["data"]["price_change_percentage_24h"]["usd"]
                ),
            }
            for coin in response["coins"]
        ]

    def get_global_market_data(self):
        response = self._get(
            base_url=self._BASE_URL_COINGECKO,
            endpoint="/global",
        )
        return response.get("data", {})

    def get_fear_and_greed_index(self):
        response = self._get(
            base_url=self._BASE_URL_ALTERNATIVE,
            endpoint="/fng/",
            params={"limit": 1},
        )
        return response.get("data", [{}])[0]

    def get_wallet_balances(self, wallets, blockchains):
        
        block_chain_address = [f"{blockchain}:{wallet}" for blockchain in blockchains for wallet in wallets]
        
        params = {
            "wallets": ",".join(block_chain_address)
        }
        return self._get(
            base_url=self._BASE_URL_COINSTATS,
            endpoint="/wallet/balance/many",
            params=params,
            headers=self._coinstats_headers(),
        )

    def get_blockchains(self):
        response = self._get(
            base_url=self._BASE_URL_COINSTATS,
            endpoint="/wallet/blockchains",
            headers=self._coinstats_headers(),
        )
        
        if isinstance(response, list):
            return response
        return response.get("data", response)
    
    def is_valid_wallet_address(self, address, blockchain):
        url = f"{self._BASE_URL_COINSTATS}/wallet/status"
        params = {"address": address, "connectionId": blockchain}
 
        try:
            response = requests.get(
                url,
                params=params,
                headers=self._coinstats_headers(),
                timeout=self.timeout,
            )
        except requests.Timeout:
            raise CryptoClientError(f"Request timed out after {self.timeout}s.")
        except requests.ConnectionError:
            raise CryptoClientError("Could not connect to the API.")
        except requests.RequestException as e:
            raise CryptoClientError(f"Request failed: {e}")
 
        if response.status_code == 429:
            raise CryptoClientError("Rate limit exceeded. Please slow down requests.")

        if response.status_code in (400, 404, 422):
            return False

        if not response.ok:
            raise CryptoClientError(
                f"HTTP {response.status_code}: {response.text}"
            )
 
        return True