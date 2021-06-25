#!/usr/bin/env python3

# Copyright 2021 ROS-Industrial Consortium Asia Pacific
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import signal
from dbsautodoc_library.rosdoccmd import ROSDocCMD
from dbsautodoc_library.rosdocgui import ROSDocGUI
import getopt

from PySide2 import QtWidgets


def main_gui():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    myapp = QtWidgets.QApplication(sys.argv)

    window = ROSDocGUI()
    window.show()

    myapp.exec_()
    sys.exit()


def main_cmd(args=None):
    try:
        doc_generator = ROSDocCMD(args[1:])
    except getopt.GetoptError:
        doc_generator.print_help()
        sys.exit(2)

    doc_generator.generateDocs()

    if doc_generator.saveLastSessionConfig is True:
        doc_generator.saveSessionConfig()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        main_gui()
    else:
        main_cmd(sys.argv)
