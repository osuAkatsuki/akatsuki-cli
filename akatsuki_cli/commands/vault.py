from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import pprint

import hvac

import os

vault_client = hvac.Client(
    url=os.environ["VAULT_ADDR"],
    token=os.environ["VAULT_TOKEN"],
)


class OutputFormatter(ABC):
    @staticmethod
    @abstractmethod
    def format(data: Dict[str, Any]) -> str:
        ...


class PrettyPrintFormatter(OutputFormatter):
    @staticmethod
    def format(data: Dict[str, Any]) -> str:
        return pprint.pformat(data)


class EnvFileFormatter(OutputFormatter):
    @staticmethod
    def format(data: Dict[str, Any]) -> str:
        return "\n".join([f'{key.upper()}="{value}"' for key, value in data.items()])


def get(service: str, environment: str, output_file: Optional[str] = None) -> None:
    response = vault_client.secrets.kv.v2.read_secret(
        path=f"{environment}/{service}",
        mount_point="secrets",
    )

    formatter = EnvFileFormatter() if output_file else PrettyPrintFormatter()
    formatted_data = formatter.format(response["data"]["data"])

    if output_file:
        with open(output_file, "w") as f:
            f.write(formatted_data)
    else:
        print(formatted_data)

    return None
