import requests

# This is called cache, pussies
def get_iam_token(iam_token_cache={"token": None}):
    """Fetch IAM token if not cached, otherwise return cached token."""
    if iam_token_cache['token'] is None:
        url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
        headers = {"Metadata-Flavor": "Google"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        iam_token_cache['token'] = response.json().get("access_token")
    return iam_token_cache['token']

def fetch_secret(secret_id):
    """Fetch secret value from Yandex Lockbox given a secret ID."""
    iam_token = get_iam_token()
    url = f"https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/{secret_id}/payload"
    headers = {"Authorization": f"Bearer {iam_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    secret_data = response.json()
    return secret_data["entries"][0]["textValue"] if "entries" in secret_data else None


get_iam_token()