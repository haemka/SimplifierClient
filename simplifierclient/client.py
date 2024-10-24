import logging
import hashlib
import re
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SimplifierClient:
    def __init__(self, username, password, debug=False):
        """Initializes a new simplifier client.

        :param username: The Simlifier username.
        :param password: The Simplier password.
        """
        self.base_url = "https://packages.simplifier.net"
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )
        if debug:
            logging.basicConfig(level=logging.DEBUG)

    def search_package(self, search_term, version=None, fhir_version=None, prerelease=False):
        """Searches for packages based on a search term.

        :param search_term: A search term.
        :param version: An optional version number to search for.
        :return:
        """
        params = f"name={search_term}"
        if version:
            if re.match(r'.*-[alpha,beta,ballot].*', version):
                logger.info("Pre-release keyword detected. Including pre-release packages in search.")
                prerelease=True
            params = f"{params}&version={version}"
        if fhir_version:
            params = f"{params}&fhirVersion={fhir_version}"
        if prerelease:
            params = f"{params}&prerelease={str(prerelease).lower()}"
        search_url = urljoin(self.base_url, f"catalog?{params}")
        logger.debug(f"Requesting {search_url}...")
        result = self.session.get(search_url)
        return result.json()

    def get_all_package_data(self, package):
        """Queries package data and returns data for all available versions of the package.

        :param package: The package to get data for.
        :return: The package data.
        """
        data_url = urljoin(self.base_url, package)
        logger.debug(f"Requesting {data_url}...")
        result = self.session.get(data_url)
        return result.json()

    def get_package_data(self, package, version=None):
        """Queries package data and returns data for a single version of the package.

        :param package: The package to get data for.
        :param version: An optional version of the package to get data for.
        :return: The package data.
        """
        if version == "latest" or version is None:
            if version is None:
                logger.warning("No version given, assuming latest.")
            version = self.get_latest_package_version(package)
            logger.info(f"Latest version is {version}.")
        return self.get_all_package_data(package)["versions"][version]

    def get_package_distribution(self, package, version=None):
        """Queries package data for available distributions of a package.

        :param package: The package to get distribution data for.
        :param version: An optional version of the package to get distribution data for.
        :return: The distribution data set for the package.
        """
        return self.get_package_data(package, version)["dist"]

    def get_latest_package_data(self, package):
        """Queries package data for the latest version of a package.

        :param package: The package to get data for.
        :return: The latest version of the package.
        """
        latest_version = self.get_latest_package_version(package)
        return self.get_all_package_data(package)["versions"][latest_version]

    def get_all_package_versions(self, package):
        """Queries package data for available versions of a package.

        :param package: The package to get data for.
        :return: A list of all available package versions.
        """
        all_package_data = self.get_all_package_data(package)
        return list(all_package_data["versions"].keys())

    def get_latest_package_version(self, package):
        """Queries package data for the latest available version.

        :param package: The package to get data for.
        :return: The latest version number of the package.
        """
        return self.get_all_package_data(package)["dist-tags"]["latest"]

    def download_package(self, package, version=None):
        """Downloads a package.

        :param package: The package to download.
        :param version: An optional version of the package to download.
        """
        dist = self.get_package_distribution(package, version)
        logger.info(f"Downloading {dist['tarball']}...")
        data = self.session.get(dist["tarball"])
        if version == "latest" or version is None:
            version = self.get_latest_package_version(package)
        if self.verify_checksum(data.content, dist["shasum"]):
            filename = f"{package}-{version}.tgz"
            logger.info(f"Checksum verified. Saving package to {filename}.")
            with open(filename, "wb") as f:
                f.write(data.content)
        else:
            logger.error(f"Download failed due to checksum mismatch.")

    @staticmethod
    def verify_checksum(data, expected_checksum):
        """verifies the checksum of data. Used for download verification.

        :param data: The data to verify.
        :param expected_checksum: The expected checksum of the data.
        :return: Boolean value indicating whether the checksum is correct.
        """
        sha1 = hashlib.sha1()
        sha1.update(data)
        result = expected_checksum == sha1.hexdigest()
        if result:
            logger.info("Checksum verified.")
        else:
            logger.warn("Checksum mismatch!")
        return result
