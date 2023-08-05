# AuthAPI

A Simple Python API for Authenticated Operations.

![landing_img](./docs/img/landing.png)

## Quickstart:

Let's assume you want to interact with Google Ads API.

1. Create a `app_secret.json` with the following information:

```json
{
    "client_id": "...",
    "client_secret": "..."
}
```

2. Upload `app_secret.json` to your Secret Manager. Let's assume it's Google Cloud's Secret Manager.

3. Create a `main.py` script and paste the following content.

```python
from authapi import AuthAPI, AuthData

class JsonSecret:
    def __init__(self, path: str):
        self.path = path

    def pull(self) -> dict:
        with open(self.path, "r") as f:
            return json.load(f)

    def push(self, payload: dict) -> None:
        with open(self.path, "w") as f:
            json.dump(payload, f)

app_secret = JsonSecret("your_secret.json")
app_token = JsonSecret("your_token.json")

auth_data = AuthData(**app_secret.pull())

app = AuthAPI(
    name="Auth API: My Auth API",
    auth_data=auth_data,
    token_secret=app_token,
)

app.debug = True


@app.route("/run", methods=["GET", "POST"])
def run():
    token = app.get_token()
    # Do your stuff here
    return "Done!"


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
```

You must fill the details in `your_secret.json` as follows:

```json
{
    "client_id": "",
    "client_secret": "",
    "authorize_url": "",
    "access_token_url": "",
    "scopes": []
}

```

4. Visit [https://127.0.0.1:5000/](https://127.0.0.1:5000/) to start the authentication process.

