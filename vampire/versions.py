
from urllib.request import urlopen
from html.parser import HTMLParser
from collections import defaultdict
import requests

class PythonIndexParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.versions = list()

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        for attr in attrs:
            if 'href' in attr and len(attr) > 1:
                version = attr[1].rstrip('/')
                if version[:1].isdigit():
                    self.versions.append(version)

    def get_versions(self):
        return self.versions

def available_versions(recent=False):
    """ Acquire list of available python versions
    :param recent: Only show versions updated in last few years
    """
    package_url = "https://www.python.org/ftp/python/"

    download = urlopen(package_url)
    parser = PythonIndexParser()
    foo = download.read()
    parser.feed(str(foo))

    versions = sorted(parser.get_versions())

    # alphas and release candidates get their own directory, but add to the 
    # numeric version numbers found in the directories.
    # We only care about these in the most recently two or three directories
    check_versions = list(versions[-3:])
    for version in check_versions:
        url = 'https://www.python.org/ftp/python/{0}/Python-{0}.tar.xz'.format(version)
        header_info = requests.head(url)
        if header_info.status_code != 200:
            versions.remove(version)

    # --listall was used, return all values
    if recent is False:
        return versions

    """
    Produce a list of the highest available MICRO version for each
    MAJOR.MINOR group. Standard max check, indexed by MAJOR.MINOR
    """
    version_filter = defaultdict(int)
    for version in versions:
        vsplit = version.split('.')
        # assumpion: there will always be a major and minor version, based
        # on existence of '2.0'
        majorminor = "{}.{}".format(vsplit[0], vsplit[1])
        if len(vsplit) < 3:
            micro = 0
        else:
            micro = int(vsplit[2])
        if version_filter[majorminor] < micro:
            version_filter[majorminor] = micro

    versions = list()
    for version in version_filter:
        # 0 wasn't in the original, so don't put it back
        if version_filter[version] == 0:
            versions.append(version)
        else:
            versions.append("{}.{}".format(version, version_filter[version]))

    return sorted(versions)

if __name__ == '__main__':
    print(available_versions(recent=True))
