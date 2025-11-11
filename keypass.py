import argparse
import cryptography
import json

args = argparse.ArgumentParser(
    description="KeyPass Password Manager"
)
args.add_argument(
    "init",
    type=str,
    help="initialize a new password vault"
)
args.add_argument(
    "get",
    type=str,
    help="retrieve passwords from a vault"
)
args.add_argument(
    "set",
    type=str,
    help="add password to a vault"
)






