import argparse
import cryptography
import json

args = argparse.ArgumentParser(
    description="KeyPass Password Manager"
)
args.add_argument(
    "mode",
    choices=["init", "add", "list", "search", "del"],
    type=str,
    help="init/add/list/search/del :: create new vault, add new passwords, retrieve passwords, search passwords, or delete passwords"
)

userargs = args.parse_args()




