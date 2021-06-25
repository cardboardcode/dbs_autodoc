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
import subprocess
import sys
import getopt
import os.path
import glob
from pathlib import Path


class ROSDocCMD():

    def __init__(self, args):

        self.session_config_lines = [None] * 10
        self.input_dir_array = []

        self.project_name = 'My Docs'
        self.author_name = 'Anonymous'
        self.version_no = '0.0.0'
        self.saveLastSessionConfig = False
        self._skipParseSessionConfig = False

        self.parse_args(args)

        # If session_config.txt exists, ask user whether user wishes to
        # overwrite previous session configurations.
        # Otherwise, directly use input arguments to populate class attributes.
        if os.path.exists('./session_config.txt'):
            confirmation = input('A previous session configuration exits.'
                                 ' Would you like to overwrite that? (Y/N)')
            # If user wishes to overwrite, assign boolean and
            # just parse the input arguments.
            # Otherwise, proceed to read session_config.txt for
            # pre-existing configuration details.
            if confirmation == 'Y' or confirmation == 'y':
                self._skipParseSessionConfig = True
                return
            else:
                self.session_config_lines = [line.rstrip('\n') for
                                             line in
                                             open('./session_config.txt')]

                # Verify if the session_config.txt is not corrupted.
                # If it is true, then assign default values.
                # Otherwise, read it accordingly and populate class attributes.
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
                return
        else:
            self._skipParseSessionConfig = True
            return

    def print_help(self):
        '''
        The print_help function.
        Outputs how a user can configure use of dbs_autodoc to generate the
        documentation from Doxygen-formatted commented C++ and Python code.
        '''
        print('python3 run_app.py [--name My Docs] '
              '[--author Chad] [--version 0.0.0]'
              '[--input_dir] <file directory to the '
              'codebase you wish to document.> ...')
        print()
        print('Converts Doxygen code comments into '
              'Sphinx-formatted documentations.')
        print()
        print('-h      Displays this help.')
        print('--name (-n) Sets project name.')
        print('        If no project name (-n) is given' +
              ' \'My Docs\' is used')
        print('--author (-a) Sets author/authors\' names.')
        print('        If no author name (-a) is given' +
              ' \'Anonymous\' is used')
        print('--version (-v) Sets documentation version no..')
        print('        If no version no. (-v) is given' +
              ' \'0.0.0\' is used')

    def parse_args(self, args):

        opts, opt_files = getopt.getopt(args, 'hsn:a:v:',
                                        ['name=',
                                         'author=',
                                         'version=',
                                         'help',
                                         'purge',
                                         'save'])

        print("opts = ", opts)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.print_help()
                sys.exit(0)
            elif opt in ('-n', '--name'):
                self.setProjectName(arg)
                print("project_name = ", self.project_name)
            elif opt in ('-a', '--author'):
                self.setAuthor(arg)
                print("author_name = ", self.author_name)
            elif opt in ('-v', '--version'):
                self.setVersion(arg)
                print("version_no = ", self.version_no)
            elif opt in ('--purge'):
                confirmation = input('Removing output_docs folder and '
                                     'session_config.txt file. '
                                     'Are you sure? (Y/N)')
                if confirmation == 'Y' or confirmation == 'y':
                    if os.path.exists('output_docs'):
                        p1 = subprocess.Popen(['rm', '-r',
                                               '_build', 'docs_sphinx',
                                               'Doxyfile.in', 'output_docs'])
                        p1.communicate()
                    print('DOCS cleaned.')
                    sys.exit(0)
            elif opt in ('--save'):
                self.saveLastSessionConfig = True

        # Check if directory is invalid
        # Otherwise, list out all cpp and python source file in the directory.
        cpp_files = []
        python_files = []

        for file_dir in opt_files:
            if os.path.isdir(file_dir) is True:
                # Adding all .cpp files under cpp_files
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

        self.setSourceFiles(cpp_files + python_files)

    def setVersion(self, version_no):

        self.version_no = version_no
        self.session_config_lines[2] = self.version_no

    def setProjectName(self, project_name):

        self.project_name = project_name
        self.session_config_lines[0] = self.project_name

    def setAuthor(self, author_name):

        self.author_name = author_name
        self.session_config_lines[1] = self.author_name

    def setSourceFiles(self, input_dirs):
        # print("input_dir_array = ")
        for dir in input_dirs:
            # print(dir)
            self.input_dir_array.append(dir)
            self.session_config_lines.append(dir)

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
        # print(pointer_array)
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

    def saveSessionConfig(self):

        if self.session_config_lines[0] is not None:
            print('Saving to session_config.txt.')
            a_file = open('session_config.txt', 'w')
            for line in self.session_config_lines:
                if 'None' not in str(line):
                    print(line)
                    a_file.writelines(str(line) + '\n')
            a_file.close()

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

        print("pointer_array = ", pointer_array)
        print("len(pointer_array) = ", len(pointer_array))
        print("len(config_lines) = ", len(config_lines))
        print("config_lines[pointer_array[4]] = ", pointer_array[4])
        print("config_lines[pointer_array[1]] = ",
              config_lines[pointer_array[1]])

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
                                   '--project="' + self.project_name + '"',
                                   '--author="' + self.author_name + '"',
                                   '-v="' + self.version_no + '"'])
            p1.communicate()
        else:
            p1 = subprocess.Popen(['rm', '-r', 'docs_sphinx'])
            p1.communicate()
            p2 = subprocess.Popen(['sphinx-quickstart',
                                   'docs_sphinx',
                                   '-q',
                                   '--project="' + self.project_name + '"',
                                   '--author="' + self.author_name + '"',
                                   '-v="' + self.version_no + '"'])
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
