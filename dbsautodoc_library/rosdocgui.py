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

import datetime
import os
import glob
import subprocess
import sys
from pathlib import Path

from PySide2 import QtCore, QtGui, QtWidgets

WINDOW_HEIGHT = 350
WINDOW_WIDTH = 700


class ROSDocGUI(QtWidgets.QWidget):
    """
    The ROSDocGUI class is a PySide2 Graphical User Interface (GUI) window
    that allows user to set Project Name, Authors, Version number and
    Source Files.
    Once the settings are configured, users can generate the
    Read-The-Docs Sphinx
    documentation based on Doxygen comment blocks.
    """
    def __init__(self):
        super().__init__()

        self.debug = False
        self.session_config_lines = [None] * 10
        self.input_dir_array = []
        if not os.path.exists('./session_config.txt'):
            print("session_config.txt does not exist. Defaulting.")
            self.session_config_lines[0] = 'default_project_name'
            self.project_name = 'default_project_name'
            self.session_config_lines[1] = 'default_author_name'
            self.author_name = 'default_author_name'
            self.session_config_lines[2] = '0.0.0'
            self.version_no = '0.0.0'
        else:
            self.session_config_lines = [line.rstrip('\n') for
                                         line in open('./session_config.txt')]

            if len(self.session_config_lines) <= 3:
                print("session_config.txt is invalid. Defaulting.")
                self.session_config_lines.clear()
                self.session_config_lines = [None] * 10
                self.session_config_lines[0] = 'default_project_name'
                self.project_name = 'default_project_name'
                self.session_config_lines[1] = 'default_author_name'
                self.author_name = 'default_author_name'
                self.session_config_lines[2] = '0.0.0'
                self.version_no = '0.0.0'
            else:
                self.project_name = self.session_config_lines[0]
                self.author_name = self.session_config_lines[1]
                self.version_no = self.session_config_lines[2]
                for i in range(3, len(self.session_config_lines)):
                    if self.session_config_lines[i] != 'None':
                        self.input_dir_array.append(
                            self.session_config_lines[i])
        print(self.input_dir_array)

        self.setWindowTitle('dbs_autodoc')
        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.setWindowIcon(QtGui.QIcon("img/dbs_autodoc_logo.png"))

        self.setButtons()

    def setButtons(self):
        self.quit_button = QtWidgets.QPushButton('Quit', self)
        self.quit_button.setIcon(QtGui.QIcon('img/icons8/quit.png'))
        self.quit_button.setIconSize(QtCore.QSize(50, 50))
        self.quit_button.setGeometry(0, 300, WINDOW_WIDTH/2, 50)

        self.name_button = QtWidgets.QPushButton('Set Project Name', self)
        self.name_button.setGeometry(0, 0, WINDOW_WIDTH/2, 50)

        self.author_button = QtWidgets.QPushButton('Set Author', self)
        self.author_button.setGeometry(0, 50, WINDOW_WIDTH/2, 50)

        self.version_button = QtWidgets.QPushButton('Set Version', self)
        self.version_button.setGeometry(0, 100, WINDOW_WIDTH/2, 50)

        self.select_source_button = QtWidgets.QPushButton(
            'Select Source Files',
            self)
        self.select_source_button.setGeometry(0, 150, WINDOW_WIDTH/4, 50)

        self.clear_source_button = QtWidgets.QPushButton('Clear Source Files',
                                                         self)
        self.clear_source_button.setGeometry(WINDOW_WIDTH/4,
                                             150,
                                             WINDOW_WIDTH/4,
                                             50)

        self.generate_button = QtWidgets.QPushButton('Generate', self)
        self.generate_button.setGeometry(0, 200, WINDOW_WIDTH/4, 50)

        self.view_button = QtWidgets.QPushButton('View Docs', self)
        self.view_button.setGeometry(WINDOW_WIDTH/4, 200, WINDOW_WIDTH/4, 50)

        self.clear_button = QtWidgets.QPushButton('Clear Docs', self)
        self.clear_button.setIcon(QtGui.QIcon('img/icons8/clean.png'))
        self.clear_button.setIconSize(QtCore.QSize(50, 50))
        self.clear_button.setGeometry(0, 250, WINDOW_WIDTH/2, 50)

        self.status_window = QtWidgets.QTextEdit(self)
        self.status_window.setGeometry(WINDOW_WIDTH/2,
                                       0,
                                       WINDOW_WIDTH/2,
                                       WINDOW_HEIGHT)
        self.updateStatusWindow()

        self.name_button.clicked.connect(self.setProjectName)
        self.select_source_button.clicked.connect(self.selectSourceFiles)
        self.clear_source_button.clicked.connect(self.clearSourceFiles)
        self.generate_button.clicked.connect(self.generateDocs)
        self.view_button.clicked.connect(self.viewDocs)
        self.author_button.clicked.connect(self.setAuthor)
        self.version_button.clicked.connect(self.setVersion)
        self.quit_button.clicked.connect(self.closeWindow)
        self.clear_button.clicked.connect(self.clearDocs)

    def updateStatusWindow(self):
        self.status_window.clear()
        for i in range(0, len(self.session_config_lines)):

            if self.session_config_lines[i] is None:
                continue

            if i == 0:
                self.status_window.append('Project Name : ' +
                                          self.session_config_lines[i] + '\n')
            elif i == 1:
                self.status_window.append('Author Name : ' +
                                          self.session_config_lines[i] + '\n')
            elif i == 2:
                self.status_window.append('Version No. : ' +
                                          self.session_config_lines[i] + '\n')
            elif i == 3:
                self.status_window.append('Source Files : \n')
                self.status_window.append(str(i - 2) +
                                          ' : ' +
                                          self.session_config_lines[i])
            else:
                self.status_window.append(str(i - 2) +
                                          ' : ' +
                                          self.session_config_lines[i])

    def clearDocs(self):
        if self.debug is False:
            msgbox = QtWidgets.QMessageBox(
                QtWidgets.QMessageBox.Question,
                'Confirm clean',
                'Are you sure?')
            msgbox.addButton(QtWidgets.QMessageBox.Yes)
            msgbox.addButton(QtWidgets.QMessageBox.No)
            msgbox.setDefaultButton(QtWidgets.QMessageBox.No)

            reply = msgbox.exec()

            if reply != QtWidgets.QMessageBox.Yes:
                return

        if os.path.exists('output_docs'):
            p1 = subprocess.Popen(['rm', '-r',
                                   '_build', 'docs_sphinx',
                                   'Doxyfile.in', 'output_docs'])
            p1.communicate()

        print('DOCS cleaned.')

    def setVersion(self):
        if self.debug is False:
            self.version_no, ok = QtWidgets.QInputDialog.getText(
                self,
                'Version No.',
                'Enter Version No.',
                text=self.version_no)

            if not ok:
                print('No Version No. given. Setting to default -  0.0.0')
            else:
                print('Version No. set to: ', self.version_no)
        else:
            self.version_no = '0.0.0'

        self.session_config_lines[2] = self.version_no
        self.updateStatusWindow()

    def setProjectName(self):
        if self.debug is False:
            self.project_name, ok = QtWidgets.QInputDialog.getText(
                self,
                'text',
                'Enter project name',
                text=self.project_name)

            if not ok:
                print('No Project Name given. '
                      'Setting to default -  ROS package')
                self.project_name = 'default_project_name'
            else:
                print('Project Name set to: ', self.project_name)
        else:
            self.project_name = 'default_project_name'

        self.session_config_lines[0] = self.project_name
        self.updateStatusWindow()

    def setAuthor(self):
        if self.debug is False:
            input_author_name, ok = QtWidgets.QInputDialog.getText(
                self,
                'text',
                'Enter author\'s name',
                text=self.author_name)

            if not ok:
                print('No Project Name given. Setting to default')
                self.author_name = 'default_author_name'
            else:
                print('Author Name set to: ', input_author_name)
                self.author_name = input_author_name
        else:
            self.author_name = 'default_author_name'

        self.session_config_lines[1] = self.author_name
        self.updateStatusWindow()

    def selectSourceFiles(self):
        if self.debug is False:
            input_dirs, ok = (
                QtWidgets.QFileDialog.getOpenFileNames(
                    self,
                    'Select the source files:',
                    os.path.abspath('./'),
                    'Source Files (*.py *.hpp *.cpp *.h)'))

            if ok:
                for dir in input_dirs:
                    self.input_dir_array.append(dir)
                    self.session_config_lines.append(dir)
        else:
            cpp_files = []
            python_files = []
            file_dir = './test'

            temp_cpp_files = glob.glob(file_dir + "/**/*.cpp",
                                       recursive=True)
            if len(temp_cpp_files) != 0:
                for file in temp_cpp_files:
                    abs_path_to_file = os.path.abspath(file)
                    cpp_files.append(abs_path_to_file)
            # Adding all .hpp files under cpp_files
            temp_hpp_files = glob.glob(file_dir + "/**/*.hpp",
                                       recursive=True)
            if len(temp_hpp_files) != 0:
                for file in temp_hpp_files:
                    abs_path_to_file = os.path.abspath(file)
                    cpp_files.append(abs_path_to_file)
            # Adding all .py files under python_files
            temp_python_files = glob.glob(file_dir + "/**/*.py",
                                          recursive=True)
            if len(temp_python_files) != 0:
                for file in temp_python_files:
                    abs_path_to_file = os.path.abspath(file)
                    python_files.append(abs_path_to_file)
            input_dirs = cpp_files + python_files
            for dir in input_dirs:
                self.input_dir_array.append(dir)
                self.session_config_lines.append(dir)

        self.updateStatusWindow()

    def clearSourceFiles(self):
        msgbox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Question,
            'Confirm clean',
            'Are you sure?')
        msgbox.addButton(QtWidgets.QMessageBox.Yes)
        msgbox.addButton(QtWidgets.QMessageBox.No)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.No)

        reply = msgbox.exec()

        if reply != QtWidgets.QMessageBox.Yes:
            return

        self.input_dir_array.clear()
        self.session_config_lines = self.session_config_lines[:3]

        self.updateStatusWindow()

    def generateDocs(self):
        self.createDoxyFile()
        self.createSphinxConf()
        self.createSphinxTemplate()

        p1 = subprocess.Popen(['make', 'html', '-C', 'docs_sphinx'])
        p1.communicate()
        if not os.path.exists('output_docs/'):
            p2 = subprocess.Popen(['cp', '-r',
                                   'docs_sphinx/_build/html/', 'output_docs/'])
            p2.communicate()
        else:
            p2 = subprocess.Popen(['rm', '-r', 'output_docs/'])
            p2.communicate()
            p3 = subprocess.Popen(['cp', '-r',
                                   'docs_sphinx/_build/html/', 'output_docs/'])
            p3.communicate()

    def viewDocs(self):
        p1 = subprocess.Popen(['firefox', 'output_docs/index.html'])
        p1.communicate()

    def createDoxyFile(self):
        if not os.path.exists('Doxyfile.in'):
            p1 = subprocess.Popen(['doxygen', '-g'])
            p1.communicate()
            p2 = subprocess.Popen(['mv', 'Doxyfile', 'Doxyfile.in'])
            p2.communicate()
        else:
            print('Doxyfile.in already exists. '
                  'Please delete it if you wish to start anew.')

        # Modify configurations.
        a_file = open('Doxyfile.in', 'r')

        pointer_array = []

        config_lines = a_file.readlines()
        for i in range(0, len(config_lines)):
            if 'GENERATE_LATEX         =' in config_lines[i]:
                pointer_array.insert(0, i)
            if 'GENERATE_XML           =' in config_lines[i]:
                pointer_array.insert(1, i)
            if 'VERBATIM_HEADERS       =' in config_lines[i]:
                pointer_array.insert(2, i)
            if 'RECURSIVE              =' in config_lines[i]:
                pointer_array.insert(3, i)
            if 'PROJECT_NAME           =' in config_lines[i]:
                pointer_array.insert(4, i)
            if 'INPUT                  =' in config_lines[i]:
                pointer_array.insert(5, i)
            if 'OUTPUT_DIRECTORY       =' in config_lines[i]:
                pointer_array.insert(6, i)

        # Compress all source files path to one line for writing.
        all_in_1 = ''
        for dir in self.input_dir_array:
            if dir is not None:
                all_in_1 = all_in_1 + '\"'
                all_in_1 = all_in_1 + dir
                all_in_1 = all_in_1 + '\" '
        print(all_in_1)

        config_lines[pointer_array[0]] = 'GENERATE_LATEX         = NO\n'
        config_lines[pointer_array[1]] = 'GENERATE_XML           = YES\n'
        config_lines[pointer_array[2]] = 'VERBATIM_HEADERS       = NO\n'
        config_lines[pointer_array[3]] = 'RECURSIVE              = YES\n'
        config_lines[pointer_array[4]] = ('PROJECT_NAME           = \
                                          "{name}\"\n'.format(
                                          name=self.project_name))
        config_lines[pointer_array[5]] = ('INPUT                  = \
                                          {source_files}\n'.format(
                                          source_files=all_in_1))
        config_lines[pointer_array[6]] = 'OUTPUT_DIRECTORY       = "_build"\n'

        a_file = open('Doxyfile.in', 'w')
        a_file.writelines(config_lines)
        a_file.close()

        p1 = subprocess.Popen(['doxygen', 'Doxyfile.in'])
        p1.communicate()

    def closeWindow(self):

        # print('len = ', len(self.session_config_lines))
        # for line in self.session_config_lines:
        #     print(line)

        if self.session_config_lines[0] is not None:
            print('Saving to session_config.txt.')
            a_file = open('session_config.txt', 'w')
            for line in self.session_config_lines:
                if 'None' not in str(line):
                    print(line)
                    a_file.writelines(str(line) + '\n')
            a_file.close()

        self.close()

    def createSphinxConf(self):
        a_file = open('dbsautodoc_library/conf.py', 'r')

        pointer_array = [999, 999, 999, 999, 999]

        config_lines = a_file.readlines()

        for i in range(0, len(config_lines)):
            # Additional safeguard to avoid confusion with
            # breathe_default_project.
            if 'project =' in config_lines[i]:
                if 'breath' not in config_lines[i]:
                    pointer_array[0] = i
            if 'copyright =' in config_lines[i]:
                pointer_array[1] = i
            if 'author =' in config_lines[i]:
                pointer_array[2] = i
            if '../_build/xml/' in config_lines[i]:
                pointer_array[3] = i
            if 'breathe_default_project =' in config_lines[i]:
                pointer_array[4] = i

        year = datetime.datetime.now().year

        config_lines[pointer_array[0]] = ('project = \
                                          \'{project_name}\'\n'.format(
                                          project_name=self.project_name))
        config_lines[pointer_array[1]] = ('copyright = \'{this_year}, \
                                          {author}\'\n'.format(
                                          this_year=year,
                                          author=self.author_name))
        config_lines[pointer_array[2]] = ('author = \'{author}\'\n'.format(
                                          author=self.author_name))
        config_lines[pointer_array[3]] = ('	\"{project_name}\": \
                                          "../_build/xml/\"\n'.format(
                                          project_name=self.project_name))
        config_lines[pointer_array[4]] = ('breathe_default_project = \
                                          "{project_name}\"\n'.format(
                                          project_name=self.project_name))

        a_file = open('ros_conf.py', 'w')
        a_file.writelines(config_lines)
        a_file.close()

    def createSphinxTemplate(self):
        if not os.path.exists('docs_sphinx'):
            p1 = subprocess.Popen(['sphinx-quickstart',
                                   'docs_sphinx',
                                   '-q',
                                   '--project=' + self.project_name,
                                   '--author=' + self.author_name,
                                   '-v=' + self.version_no])
            p1.communicate()
        else:
            p1 = subprocess.Popen(['rm', '-r', 'docs_sphinx'])
            p1.communicate()
            p2 = subprocess.Popen(['sphinx-quickstart',
                                   'docs_sphinx',
                                   '-q',
                                   '--project=' + self.project_name,
                                   '--author=' + self.author_name,
                                   '-v=' + self.version_no])
            p2.communicate()

        p2 = subprocess.Popen(['cp', 'ros_conf.py', 'docs_sphinx/conf.py'])

        a_file = open('docs_sphinx/index.rst', 'a')
        a_file.write('\n')
        a_file.write('Table of Contents\n')
        a_file.write('^^^^^^^^^^^^^^^^^\n')
        a_file.write('\n')
        a_file.write('.. toctree::\n')
        a_file.write('    :maxdepth: 2\n')
        a_file.write('\n')
        a_file.write('    self\n')
        a_file.write('\n')

        for dir in self.input_dir_array:
            a_file.write('    api/{filename}\n'.format(
                         filename=Path(dir).stem))

        # If already exists, remove it.
        if os.path.exists('docs_sphinx/api'):
            p1 = subprocess.Popen(['rm', '-r', 'docs_sphinx/api'])
            p1.communicate()
        p2 = subprocess.Popen(['mkdir', '-p', 'docs_sphinx/api'])
        p2.communicate()

        for dir in self.input_dir_array:
            p3 = subprocess.Popen(['touch',
                                   'docs_sphinx/api/{filename}.rst'.format(
                                    filename=Path(dir).stem)])
            p3.communicate()
            a_file = open('docs_sphinx/api/{filename}.rst'.format(
                          filename=Path(dir).stem), 'w')
            a_file.write('.. _api_{filename}:\n'.format(
                         filename=Path(dir).stem))
            a_file.write('\n')
            a_file.write('{title}\n'.format(title=Path(dir).stem))
            underline = ''
            for i in range(0, len(Path(dir).stem)):
                underline = underline + '='
            a_file.write(underline + '\n')
            a_file.write('\n')
            a_file.write('.. doxygenfile:: {filename_with_extension}\n'.format(
                         filename_with_extension=os.path.basename(dir)))
            a_file.write('   :project: {project_name}\n'.format(
                         project_name=self.project_name))
            a_file.close()
