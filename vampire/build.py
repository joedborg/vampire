import os
import logging
import urllib2
import subprocess

logger = logging.getLogger('vampire')


class PythonBuild(object):
    """
    Class abstracting a Python 
    build.
    """
    def __init__(self, version, target, host):
        """
        Set the constants.
        """
        logger.debug('Version: %s' % version)
        logger.debug('Target: %s' % target)
        logger.debug('Host: %s' % host)
        self.version = version
        self.target = target
        self.host = host
        self.package_url = 'https://www.python.org/ftp/python/%s/Python-%s.tgz' % (self.version, self.version)
        self.temporary_directory = '/tmp'
        self.package_path = os.path.join(self.temporary_directory, os.path.basename(self.package_url))

    def getPackage(self):
        """
        Download the python build.
        """
        download = urllib2.urlopen(self.package_url)
        with open(self.package_path,'wb') as f:
            f.write(download.read())

    def extractPackage(self):
        """
        Extract the build.
        """
        with open(self.package_path) as f:
            pass  # TODO: Extract package.

    def compilePackage(self):
        """
        Compile the build.
        """
        configure_proc = subprocess.Popen(['./configure', '--prefix=%s' % self.target])
        configure_proc.wait()
        if configure_proc.returncode != 0:
            configure_proc.communicate()
            raise RuntimeError('Configure exited with status %s' % configure_proc.returncode)
        make_proc = subprocess.Popen(['make'])
        make_proc.wait()
        if make_proc.returncode != 0:
            make_proc.communicate()
            raise RuntimeError('Make exited with status %s')
        install_proc = subprocess.Popen(['make', 'install'])
        install_proc.wait()
        if install_proc.returncode != 0:
            install_proc.communicate()
            raise RuntimeError('Make install exited with status %s' % install_proc.returncode)
