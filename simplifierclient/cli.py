import argparse
from simplifierclient.client import SimplifierClient


def cli():
    parser = argparse.ArgumentParser(description="A simple FHIR package client for Simplifier.",
                                     epilog="The 'list' command lists all available package versions. The 'download' "
                                            "command downloads the specified package. The desired package version can "
                                            "be appended to the package name separated by a colon (i.e. "
                                            "hl7.fhir.r4.core:4.0.1). 'latest' can be used as an alias for the latest "
                                            "version. If the version is omitted tthe latest version is assumed."
                                     )
    parser.add_argument("command", choices=["list", "download"], help="The command to execute. ")
    parser.add_argument("package", nargs=1, help="The package")
    parser.add_argument("-u", "--username", help="Simplifier username")
    parser.add_argument("-p", "--password", help="Simplifier password")
    # parser.add_argument("-l", "--list", action="store_true", help="List all package versions")
    # parser.add_argument("-d", "--download", action="store_true", help="Download the package")
    args = parser.parse_args()

    c = SimplifierClient(args.username, args.password)

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
    else:
        parser.print_usage()
