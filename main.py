import os
import logger
import urllib2
import subprocess


class PythonBuild(object):
    """
    Class abstracting a Python 
    build.
    """
    def __init__(self, version, target=os.path.join(os.path.expanduser('~'), 'python'), host='localhost'):
        """
        """
        self.version = version
        self.target = target
        self.package_url = 'https://www.python.org/ftp/python/%s/Python-%s.tgz' % (self.version, self.version)
        self.tempoary_directory = '/tmp'
        self.package_path = os.path.join(self.tempoary_directory, os.path.basename(self.package_url))

    def getPackage(self):
        """
        """
        download = urllib2.urlopen(self.package_url)
        with open(self.package_path,'wb') as f:
            f.write(download.read())

    def extractPackage(self):
        """
        """
        with open(self.package_path) as f:
            pass  # TODO: Extract package.

    def compilePackage(self):
        """
        """
        configure_proc = suprocess.Popen(['./configure', '--prefix=%s' % self.target])
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
