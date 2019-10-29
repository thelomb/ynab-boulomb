from application.exceptions import (YnabException, YnabConnectionError)
import requests

_endpoints = {
    "base_url": {
        "url": "https://api.youneedabudget.com/v1"
    },
    "budgets": {
        "path": "/budgets/{budget_id}"
    },
    "accounts": {
        "path": "/budgets/{budget_id}/accounts/{account_id}"
    },
    "budgetmonths": {
        "path": "/budgets/{budget_id}/months/{month}"
    },
    "categories": {
        "path": "/budgets/{budget_id}/categories/{category_id}"
    },
    "payees": {
        "path": "/budgets/{budget_id}/payees/{payee_id}"
    },
    "transactions": {
        "path": "/budgets/{budget_id}/transactions/{transaction_id}"
    }
}


class Client():
    def __init__(self, token):
        self.headers = {"Accept": "application/json"}

        if token:
            self._token = token
            self._auth_header = {"Authorization": f"Bearer {self._token}"}
        else:
            raise YnabException("No token specified")

        self.headers.update(self._auth_header)
        self.url = _endpoints["base_url"]["url"]

    def _get_object(self, endpoint, headers=None):
        try:
            api_call = requests.get(f"{self.url}{endpoint}",
                                    headers=self.headers)
        except ConnectionError as e:
            return ConnectionError('Connection Error: {}'.format(e))

        if api_call.status_code != 200:
            return YnabConnectionError("Unable to call API endpoint: {}".
                                       format(api_call.status_code))
        output = api_call.json()['data']
        return output

    def get_budget(self, budget_id="last-used"):
        return self._get_object(_endpoints["budgets"]["path"].
                                format(budget_id=budget_id))
