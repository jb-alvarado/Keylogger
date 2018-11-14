#!/usr/bin/env python3

import os

from datetime import datetime
from pathlib import Path
from subprocess import Popen
from threading import Thread


class Keylog(Thread):
    def __init__(self, output):
        Thread.__init__(self)
        self._output = output
        self.proc = None
        self.stop_requested = False

    def run(self):
        cmd = ['keylogger', self._output]
        self.proc = Popen(cmd)

    def stop(self):
        if self.proc is not None:
            self.proc.terminate()


def set_output():
    home = str(Path.home())

    return os.path.join(
        home, 'keylogger_' + datetime.now().strftime('%Y-%m-%d') + '.log')


def main():
    output = set_output()

    logging = Keylog(output)
    logging.start()


if __name__ == "__main__":
    main()
