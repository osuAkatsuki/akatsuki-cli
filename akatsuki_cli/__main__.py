#!/usr/bin/env python3
import argparse
from akatsuki_cli.commands import vault

parser: argparse.ArgumentParser


def handle_vault_command(args: argparse.Namespace) -> int:
    if args.subcommand == "get":
        response = vault.get(args.service, args.environment, args.key)
        print("vault get")
    elif args.subcommand == "get-all":
        print("vault get-all")
    elif args.subcommand == "delete":
        print("vault delete")
    else:
        parser.print_help()

    return 0


def handle_command(args: argparse.Namespace) -> int:
    if args.command == "vault":
        return handle_vault_command(args)
    else:
        parser.print_help()

    return 0


def main() -> int:
    global parser
    parser = argparse.ArgumentParser("akatsuki")

    parser.add_argument("--version", action="version", version="0.0.1")

    subparsers = parser.add_subparsers(dest="command")

    # $ akatsuki vault
    vault_parser = subparsers.add_parser("vault")
    vault_subparsers = vault_parser.add_subparsers(dest="subcommand")

    # $ akatsuki vault get <service> <environment> <key>
    vault_get_parser = vault_subparsers.add_parser("get")
    vault_get_parser.add_argument("service")
    vault_get_parser.add_argument("environment")
    vault_get_parser.add_argument("key")

    # $ akatsuki vault get-all <service> <environment> -o <output_file>
    vault_get_all_parser = vault_subparsers.add_parser("get-all")
    vault_get_all_parser.add_argument("service")
    vault_get_all_parser.add_argument("environment")
    vault_get_all_parser.add_argument("-o", "--output-file")

    # TODO: what other vault subcommands would be useful? search? unseal?

    args = parser.parse_args()
    if not args:
        parser.print_help()
        return 0

    return handle_command(args)


if __name__ == "__main__":
    exit(main())
