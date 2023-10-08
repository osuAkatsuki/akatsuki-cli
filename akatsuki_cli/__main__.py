#!/usr/bin/env python3
import argparse
import logging

from akatsuki_cli.commands import vault

parser: argparse.ArgumentParser


def handle_vault_command(args: argparse.Namespace) -> None:
    if args.subcommand == "get":
        vault.get(args.service, args.environment, args.output_file)
    elif args.subcommand == "delete":
        print("vault delete")
    else:
        parser.print_help()

    return None


def handle_command(args: argparse.Namespace) -> int:
    try:
        if args.command == "vault":
            handle_vault_command(args)
        else:
            parser.print_help()
    except Exception:
        logging.exception(
            "Failed to execute command",
            extra={"args": args},
        )
        return 1
    else:
        return 0


def main() -> int:
    global parser
    parser = argparse.ArgumentParser("akatsuki")

    parser.add_argument("--version", action="version", version="0.0.1")

    subparsers = parser.add_subparsers(dest="command")

    # $ akatsuki vault
    vault_parser = subparsers.add_parser("vault")
    vault_subparsers = vault_parser.add_subparsers(dest="subcommand")

    # $ akatsuki vault get <service> <environment> [-o <output-file>]
    vault_get_parser = vault_subparsers.add_parser("get")
    vault_get_parser.add_argument("service")
    vault_get_parser.add_argument("environment")
    vault_get_parser.add_argument("-o", "--output-file")

    # TODO: what other vault subcommands would be useful? search? unseal?

    args = parser.parse_args()
    if not args:
        parser.print_help()
        return 0

    return handle_command(args)


if __name__ == "__main__":
    exit(main())
