import os
import logging
import subprocess
from urllib.request import urlopen

logger = logging.getLogger('vampire')


class Umask(object):
    """
    Change umask.
    """
    def __init__(self, mask):
        self.mask = mask

    def __enter__(self):
        self.origin = os.umask(self.mask)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.umask(self.origin)


class PythonPackages(object):
    """
    Class abstracting Python
    packages.
    """
    def __init__(self, build, packages):
        """
        Set the constants.
        """
        self.build = build
        self.packages = packages

        self.python_executable = os.path.join(self.build.target, 'bin/python')

        if not self.build.is_three:
            self.ez_url = 'https://bootstrap.pypa.io/ez_setup.py'
            self.ez_path = os.path.join(self.build.temporary_directory, 'ez_setup.py')
            self.ez_executable = os.path.join(os.path.dirname(self.python_executable), 'easy_install')

        if self.build.is_three:
            self.pip_executable = os.path.join(os.path.dirname(self.python_executable), 'pip3')
        else:
            self.pip_executable = os.path.join(os.path.dirname(self.python_executable), 'pip')

    def __call__(self):
        """
        Run the methods.
        """
        if not self.build.is_three:
            self.pip()
        self.install()

    def pip(self):
        """
        Get and install pip.
        """
        logger.info('Installing pip...')
        download = urlopen(self.ez_url)
        with Umask(0o0077):
            with open(self.ez_path, 'wb') as f:
                f.write(download.read())

        ez_process = subprocess.Popen([self.python_executable, self.ez_path])
        ez_process.wait()
        if ez_process.returncode != 0:
            ez_process.communicate()
            raise RuntimeError('Easy install exited with status %s' % ez_process.returncode)

        pip_process = subprocess.Popen([self.ez_executable, 'pip'])
        pip_process.wait()
        if pip_process.returncode != 0:
            pip_process.communicate()
            raise RuntimeError('Pip install exited with status %s' % pip_process.returncode)

        os.remove(self.ez_path)
        logger.info('...done.')

    def install(self):
        """
        Pip install the packages.
        """
        for package in self.packages:
            logger.info('Installing %s...' % package)
            process = subprocess.Popen([self.pip_executable, 'install', package])
            process.wait()
            if process.returncode != 0:
                process.communicate()
                raise RuntimeError('Package install exited with status %s' % process.returncode)
            logger.info('...done.')
