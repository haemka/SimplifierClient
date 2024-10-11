import argparse
import os.path
import sys
from pathlib import Path

from simplifierclient.client import SimplifierClient


def cli():
    parser = argparse.ArgumentParser(description="A simple FHIR package client for Simplifier.",
                                     epilog="Commands:\n"
                                            "- search: Searches for packages. The 'package' parameter is used as search"
                                            " term for this command. The search term is matched to any part of the"
                                            " package name.\n"
                                            "- list: Lists all available versions of the specified package.\n"
                                            "- download: Downloads the specified package.\n"
                                            "\n"
                                            "Package names and versions:\n"
                                            "A package version can be appended to the package name separated by a colon"
                                            " (i.e. hl7.fhir.r4.core:4.0.1).\n"
                                            "'latest' can be used as an alias for the latest version. If the version is"
                                            " omitted the latest version is assumed.\n"
                                            "Versions for 'search' command can also be given in parts (i.e. hl7:4).",
                                     formatter_class=argparse.RawTextHelpFormatter
                                     )
    parser.add_argument("command", choices=["search", "list", "download"], help="The command to execute. ")
    parser.add_argument("package", nargs=1, help="The package")
    parser.add_argument("-u", "--username", help="Simplifier username")
    parser.add_argument("-p", "--password", help="Simplifier password")
    args = parser.parse_args()

    if args.username and args.password:
        username = args.username
        password = args.password
    elif os.path.exists(os.path.join(Path.home(), ".simplifierrc")):
        with open(os.path.join(Path.home(), ".simplifierrc"), "r") as f:
            for line in f.readlines():
                if line.startswith("username"):
                    username = line.split('=', 1)[1]
                if line.startswith("password"):
                    password = line.split('=', 1)[1]
    else:
        print("No username or password provided.")
        sys.exit(1)

    c = SimplifierClient(username, password)

    if ':' in args.package[0]:
        package, version = args.package[0].split(':')
    else:
        package, version = args.package[0], None

    if args.command == "download":
        c.download_package(package, version)
    elif args.command == "list":
        print(f"\033[1mAvailable versions for package {package}:\033[0m")
        latest_version = c.get_latest_package_version(package)
        for version in c.get_all_package_versions(package):
            if version == latest_version:
                v = f"\033[93m{version} (latest)\033[0m"
            else:
                v = version
            print(f"- {v}")
    elif args.command == "search":
        if version:
            print(f"\033[1mSearch results for {package} with version {version}:\033[0m")
        else:
            print(f"\033[1mSearch results for {package}:\033[0m")
        for package in c.search_package(package, version):
            print(f"- \033[1m{package['Name']}\033[0m\n  Description: {package['Description']}\n  FHIR Version: {package['FhirVersion']}")
    else:
        parser.print_usage()
