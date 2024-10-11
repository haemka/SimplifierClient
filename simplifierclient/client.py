import logging
import hashlib
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SimplifierClient:
    def __init__(self, username, password):
        self.base_url = "https://packages.simplifier.net"
        self.session =  requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

    def get_all_package_data(self, package):
        result = self.session.get(urljoin(self.base_url, package))
        return result.json()

    def get_package_data(self, package, version=None):
        if version == 'latest' or version is None:
            if version is None:
                logger.warning("No version given, assuming latest.")
            version = self.get_latest_package_version(package)
            logger.info(f"Latest version is {version}.")
        return self.get_all_package_data(package)['versions'][version]

    def get_package_distribution(self, package, version=None):
        return self.get_package_data(package, version)['dist']

    def get_latest_package_data(self, package):
        latest_version = self.get_latest_package_version(package)
        return self.get_all_package_data(package)['versions'][latest_version]

    def get_all_package_versions(self, package):
        all_package_data = self.get_all_package_data(package)
        return list(all_package_data['versions'].keys())

    def get_latest_package_version(self, package):
        return self.get_all_package_data(package)['dist-tags']['latest']

    def download_package(self, package, version=None):
        dist = self.get_package_distribution(package, version)
        data = self.session.get(dist['tarball'])
        if version == 'latest' or version is None:
            version = self.get_latest_package_version(package)
        if self.verify_checksum(data.content, dist['shasum']):
            filename = f'{package}-{version}.tgz'
            logger.info(f'Checksum verified. Saving package to {filename}.')
            with open(filename, 'wb') as f:
                f.write(data.content)
        else:
            logger.error(f"Download failed due to checksum mismatch." )

    @staticmethod
    def verify_checksum(data, expected_checksum):
        sha1 = hashlib.sha1()
        sha1.update(data)
        result = expected_checksum == sha1.hexdigest()
        return result
