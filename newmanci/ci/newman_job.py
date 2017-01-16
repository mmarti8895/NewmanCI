__author__ = 'martin'
from subprocess import CalledProcessError
from ci import settings
from os.path import join
from os import system

class NewmanJobList:

    def __init__(self):
        self.run_newman_source_list = settings.NEWMANCI_SOURCE_LIST

    def call_newman_jobs(self):
        for key, newman_source in self.run_newman_source_list.iteritems():
            try:
                outfile = key + '_output_$(date +"%Y%m%d%H%M%S")' +'.txt'
                system_output = system(
                                    'source ' + join(settings.NEWMANCI_BASE_DIR, newman_source) +
                                    ' | strip-ansi > '+ join(join(settings.NEWMANCI_LOG_DIR, key), outfile)
                                )
            except CalledProcessError:
                return 'Return Code: %s, Output: %s, CMD: %s' % (
                            CalledProcessError.returncode,
                            CalledProcessError.output,
                            CalledProcessError.cmd
                            )
        return system_output

if __name__ == '__main__':
    print NewmanJobList().call_newman_jobs()

