# SimplifierClient

A simple client library for the [Simplifier package registry](https://simplifier.net) API.

## Installation

```
python -m pip install --user git+https://github.com/haemka/SimplifierClient.git
```

## CLI

The library features a CLI interface via the command `fhirpackage`.

```
usage: fhirpackage [-h] [-u USERNAME] [-p PASSWORD]
                   {search,list,download} package

A simple FHIR package client for Simplifier.

positional arguments:
  {search,list,download}
                        The command to execute. 
  package               The package

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Simplifier username
  -p PASSWORD, --password PASSWORD
                        Simplifier password
  -t, --terse           Terse output mode
  -d, --debug           Enable Debug messages

Commands:
- search: Searches for packages. The 'package' parameter is used as search term for this command. The search term is matched to any part of the package name.
- list: Lists all available versions of the specified package.
- download: Downloads the specified package.

Package names and versions:
A package version can be appended to the package name separated by a colon (i.e. hl7.fhir.r4.core:4.0.1).
'latest' can be used as an alias for the latest version. If the version is omitted the latest version is assumed.
Versions for 'search' command can also be given in parts (i.e. hl7:4).Package names and versions for 'search' command can also be given in parts (i.e. hl7.fhir:4). An additional filter for the FHIR version can be added delimited by another colon (i.e. hl7.fhir.r4.core:4.0.1:R4) for the 'search' command. To search for pre-release Versions, prepend the version number with a tilde character (i.e. hl7.fhir.r4.core:~4).
```

Username and password may be stored inside a `.simplifierrc` file inside your home directory:
```
username=user@example.com
password=P455w0rd
```
