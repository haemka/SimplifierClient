# SimplifierClient

A simple client library for the [Simplifier package registry](https://simplifier.net) API.

## CLI

The library features a CLI interface via the command `fhirpackage`.

```
usage: fhirpackage [-h] [-u USERNAME] [-p PASSWORD] {list,download} package

A simple FHIR package client for Simplifier.

positional arguments:
  {list,download}       The command to execute.
  package               The package

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Simplifier username
  -p PASSWORD, --password PASSWORD
                        Simplifier password

The 'list' command lists all available package versions. The 'download'
command downloads the specified package. The desired package version can be
appended to the package name separated by a colon (i.e.
hl7.fhir.r4.core:4.0.1). 'latest' can be used as an alias for the latest
version. If the version is omitted tthe latest version is assumed.
```

## Installation

```
python3 -m pip install git+https://github.com/haemka/SimplifierClient
```