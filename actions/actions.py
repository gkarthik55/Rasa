import requests
import base64

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from oauth_config import oauth_config, CSOAuthConfiguration

class ActionSearchBug(Action):

    def name(self) -> Text:
        return "action_search_bug"

    def fetch_new_token(self, config: CSOAuthConfiguration) -> str:
        combined_credentials = f"{config.client_id}:{config.client_secret}"
        encoded_credentials = base64.b64encode(combined_credentials.encode()).decode("utf-8")

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }

        data = {
            "grant_type": config.grant_type,
            "scope": config.scope
        }

        try:
            response = requests.post(f"{config.endpoint}/oauth2/v1/token", data=data, headers=headers)
            response.raise_for_status()
            access_token = response.json().get("access_token")
            return access_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch token from external system: {str(e)}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            access_token = self.fetch_new_token(oauth_config)

            url = "https://lamp-dev.oraclecorp.com/commonservices/seekr/searchBugsByKeyword"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }

            request_body = {
                "query": {
                    "query_string": {
                        "fuzziness": "AUTO",
                        "query": "ESS",
                        "default_field": "keywords"
                    }
                }
            }

            response = requests.post(url, json=request_body, headers=headers)
            status_code = response.status_code
            json_response = response.json()

            dispatcher.utter_message(f"Status Code: {status_code}")
            dispatcher.utter_message(f"JSON Response: {json_response}")

        except Exception as e:
            dispatcher.utter_message(f"Error: {str(e)}")

        return []
