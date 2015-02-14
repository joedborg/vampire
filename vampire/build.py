import os
import shutil
import tarfile
import logging
import subprocess
from urllib.request import urlopen

logger = logging.getLogger('vampire')


class Directory(object):
    """
    Change directory.
    """
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.origin = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.origin)


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
        self.nice_version = '.'.join(list(self.version))
        self.target = target
        self.host = host
        self.temporary_directory = '/tmp'
        self.package_url = 'https://www.python.org/ftp/python/%s/Python-%s.tar.xz' % (
            self.nice_version, self.nice_version
        )
        self.package_name_zipped = os.path.basename(self.package_url)
        self.package_name = os.path.splitext(os.path.splitext(self.package_name_zipped)[0])[0]
        self.package_path = os.path.join(self.temporary_directory, self.package_name_zipped)

        self.is_three = int(self.version.replace('.', '')) > 300

    def __call__(self):
        """
        Run the methods.
        """
        self.get()
        self.extract()
        self.compile()
        self.cleanup()

    def get(self):
        """
        Download the Python build.
        """
        logger.info('Downloading...')
        download = urlopen(self.package_url)
        with open(self.package_path, 'wb') as f:
            f.write(download.read())
        logger.info('...done.')

    def extract(self):
        """
        Extract the build.
        """
        logger.info('Extracting...')
        with tarfile.open(self.package_path) as f:
            f.extractall(self.temporary_directory)
        logger.info('...done.')

    def compile(self):
        """
        Compile the build.
        """
        logger.info('Installing...')
        with Directory(os.path.join(self.temporary_directory, self.package_name)):
            configure_process = subprocess.Popen(['./configure', '--prefix=%s' % self.target])
            configure_process.wait()
            if configure_process.returncode != 0:
                configure_process.communicate()
                raise RuntimeError('Configure exited with status %s' % configure_process.returncode)
            make_process = subprocess.Popen(['make'])
            make_process.wait()
            if make_process.returncode != 0:
                make_process.communicate()
                raise RuntimeError('Make exited with status %s' % make_process.returncode)
            install_process = subprocess.Popen(['make', 'install'])
            install_process.wait()
            if install_process.returncode != 0:
                install_process.communicate()
                raise RuntimeError('Make install exited with status %s' % install_process.returncode)
        logger.info('...done.')

    def cleanup(self):
        """
        Cleanup the source
        files.
        """
        logger.info('Cleaning up...')
        os.remove(self.package_path)
        shutil.rmtree(os.path.join(self.temporary_directory, self.package_name))
        logger.info('...done.')