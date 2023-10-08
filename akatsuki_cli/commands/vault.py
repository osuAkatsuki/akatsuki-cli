import hvac

import os

vault_client = hvac.Client(
    url="https://vault.akatsuki.gg",
    token=os.environ["VAULT_TOKEN"],
)


def get(service: str, environment: str, key: str) -> None:
    path = f"secrets/{environment}/{service}/{key}"
    response = vault_client.secrets.kv.v2.read_secret(path)
    breakpoint()
