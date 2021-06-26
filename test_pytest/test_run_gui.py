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

from dbsautodoc_library.rosdocgui import ROSDocGUI
from PySide2 import QtWidgets, QtCore
import pytest
import os
import sys
import subprocess


def test_rosdocgui(qtbot):

    window = ROSDocGUI()
    qtbot.addWidget(window)

    window.show()

    assert window.isVisible() is True


# def test_rosdocgui_quitButton(qtbot):
#
#     window = ROSDocGUI()
#     qtbot.addWidget(window)
#
#     window.show()
#
#     qtbot.mouseClick(window.quit_button, QtCore.Qt.LeftButton)
#
#     assert window.isVisible() is False
#
#
# def test_rosdocgui_nameButton(qtbot):
#
#     window = ROSDocGUI()
#     qtbot.addWidget(window)
#
#     window.debug = True
#
#     qtbot.mouseClick(window.name_button, QtCore.Qt.LeftButton)
#
#     assert window.session_config_lines[0] == 'default_project_name'
#
#
# def test_rosdocgui_authorButton(qtbot):
#
#     window = ROSDocGUI()
#     qtbot.addWidget(window)
#
#     window.debug = True
#
#     qtbot.mouseClick(window.author_button, QtCore.Qt.LeftButton)
#
#     assert window.session_config_lines[1] == 'default_author_name'
#
#
# def test_rosdocgui_versionButton(qtbot):
#
#     window = ROSDocGUI()
#     qtbot.addWidget(window)
#
#     window.debug = True
#
#     qtbot.mouseClick(window.version_button, QtCore.Qt.LeftButton)
#
#     assert window.session_config_lines[2] == '0.0.0'
#
#
# def test_rosdocgui_selectSourceButton(qtbot):
#
#     window = ROSDocGUI()
#     qtbot.addWidget(window)
#
#     window.debug = True
#
#     qtbot.mouseClick(window.select_source_button, QtCore.Qt.LeftButton)
#
#     _, first_file = os.path.split(window.session_config_lines[-2])
#     _, second_file = os.path.split(window.session_config_lines[-1])
#     assert first_file == 'example_cpp.hpp'
#     assert second_file == 'example_python.py'
#
#
# def test_rosdocgui_generateButton(qtbot):
#
#     # Ensure that there is no session_config.txt.
#     if os.path.isfile('./session_config.txt') is True:
#         remove_process = subprocess.Popen(['rm', 'session_config.txt'])
#         remove_process.communicate()
#
#     session_config_lines = ['Book of Gary',
#                             'Gary',
#                             '1.0.0']
#
#     if session_config_lines[0] is not None:
#         print('Saving to session_config.txt.')
#         a_file = open('session_config.txt', 'w')
#         for line in session_config_lines:
#             if 'None' not in str(line):
#                 print(line)
#                 a_file.writelines(str(line) + '\n')
#         a_file.close()
#
#     window = ROSDocGUI()
#     qtbot.addWidget(window)
#
#     window.debug = True
#
#     qtbot.mouseClick(window.select_source_button, QtCore.Qt.LeftButton)
#
#     _, first_file = os.path.split(window.session_config_lines[-2])
#     _, second_file = os.path.split(window.session_config_lines[-1])
#     assert first_file == 'example_cpp.hpp'
#     assert second_file == 'example_python.py'
#
#     qtbot.mouseClick(window.generate_button, QtCore.Qt.LeftButton)
#
#     assert os.path.isdir('./output_docs') is True
#     assert os.path.isfile('./output_docs/index.html') is True
#
#
# def test_rosdocgui_clearButton(qtbot):
#
#     window = ROSDocGUI()
#     qtbot.addWidget(window)
#
#     window.debug = True
#
#     qtbot.mouseClick(window.clear_button, QtCore.Qt.LeftButton)
#
#     assert os.path.isdir('./output_docs') is False
#     assert os.path.isdir('./docs_sphinx') is False
#     assert os.path.isdir('./_build') is False
#     assert os.path.isfile('./Doxyfile.in') is False
