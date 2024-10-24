import argparse
import os.path
import sys
from pathlib import Path

from simplifierclient.client import SimplifierClient


def cli():
    """CLI function for the SimplifierClient library

    :return:
    """
    parser = argparse.ArgumentParser(
        description="A simple FHIR package client for Simplifier.",
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
        "Versions for 'search' command can also be given in parts (i.e. hl7:4)."
        "Package names and versions for 'search' command can also be given in parts"
        " (i.e. hl7.fhir:4). An additional filter for the FHIR version can be added"
        " delimited by another colon (i.e. hl7.fhir.r4.core:4.0.1:R4) for the"
        " 'search' command. To search for pre-release Versions, prepend the version"
        " number with an exclamation mark (i.e. hl7.fhir.r4.core:!4).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "command",
        choices=["search", "list", "download"],
        help="The command to execute. ",
    )
    parser.add_argument("package", nargs=1, help="The package")
    parser.add_argument("-u", "--username", help="Simplifier username")
    parser.add_argument("-p", "--password", help="Simplifier password")
    parser.add_argument("-d", "--debug", action='store_true', help="Enable Debug messages")
    args = parser.parse_args()

    if args.username and args.password:
        username = args.username
        password = args.password
    elif os.path.exists(os.path.join(Path.home(), ".simplifierrc")):
        with open(os.path.join(Path.home(), ".simplifierrc"), "r") as f:
            for line in f.readlines():
                if line.startswith("username"):
                    username = line.split("=", 1)[1]
                if line.startswith("password"):
                    password = line.split("=", 1)[1]
    else:
        print("No username or password provided.")
        sys.exit(1)

    c = SimplifierClient(username, password, args.debug)

    package, version, fhir_version = (args.package[0].split(":", 2) + [None] * 3)[:3]

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
        if version and version.startswith('!'):
            version = version.split('!')[1]
            include_prereleases = True
        else:
            include_prereleases = False
        results = c.search_package(package, version, fhir_version, include_prereleases)
        if results:
            text = f"\033[1mSearch results for {package}"
            text += f" with version {version}" if version else ""
            text += f" for FHIR version {fhir_version}" if fhir_version else ""
            text += f" including pre-releases" if include_prereleases else ""
            text += ":\033[0m"
            print(text)
            for package in results:
                print(f"- \033[1m{package['Name']}\033[0m\n"
                      f"  Description: {package['Description']}\n"
                      f"  FHIR Version: {package['FhirVersion']}"
                )
        else:
            print("No package found.")
    else:
        parser.print_usage()

    sys.exit(0)