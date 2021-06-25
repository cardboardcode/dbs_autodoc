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

import errno
import os
import subprocess
import sys

import pytest

from dbsautodoc_library.rosdoccmd import ROSDocCMD

test_cpp_filepath = './test/example_cpp.hpp'
test_py_filepath = './test/example_python.py'
test_cpp_filepath_abs = ''
test_py_filepath_abs = ''
test_file_dir = './test'
# Check if the example_cpp.hpp and example_python files is present
# If it is, get absolute paths to the files.
if os.path.isfile(test_cpp_filepath) is True:
    test_cpp_filepath_abs = os.path.abspath(test_cpp_filepath)
else:
    raise FileNotFoundError(
        errno.ENOENT, os.strerror(errno.ENOENT), test_cpp_filepath)
    sys.exit(1)
if os.path.isfile(test_py_filepath) is True:
    test_py_filepath_abs = os.path.abspath(test_py_filepath)
else:
    raise FileNotFoundError(
        errno.ENOENT, os.strerror(errno.ENOENT), test_py_filepath)
    sys.exit(1)


def test_rosdoccmd_printhelp(capsys):
    args = ['run_app.py', '--help']

    with pytest.raises(SystemExit):
        doc_generator = ROSDocCMD(args[1:])  # noqa
    out, err = capsys.readouterr()
    assert err == ''


def test_rosdoccmd_argparse_withPreviousSessionConfig(monkeypatch):

    global test_cpp_filepath_abs, test_py_filepath_abs

    # Ensure that there is no session_config.txt.
    if os.path.isfile('./session_config.txt') is True:
        remove_process = subprocess.Popen(['rm', 'session_config.txt'])
        remove_process.communicate()

    session_config_lines = ['Not Book of Gary',
                            'Anti-Gary',
                            '1.0.0',
                            test_cpp_filepath_abs,
                            test_py_filepath_abs]

    if session_config_lines[0] is not None:
        print('Saving to session_config.txt.')
        a_file = open('session_config.txt', 'w')
        for line in session_config_lines:
            if 'None' not in str(line):
                print(line)
                a_file.writelines(str(line) + '\n')
        a_file.close()

    args = ['run_app.py',
            '--name',
            'Book of Gary',
            '--author',
            'Gary',
            '--version',
            '0.0.0',
            './test']

    monkeypatch.setattr('builtins.input', lambda _: 'N')

    doc_generator = ROSDocCMD(args[1:])
    assert doc_generator.project_name == 'Not Book of Gary'
    assert doc_generator.author_name == 'Anti-Gary'
    assert doc_generator.version_no == '1.0.0'


def test_rosdoccmd_argparse_withoutSessionConfig():

    # Ensure that there is no session_config.txt.
    if os.path.isfile('./session_config.txt') is True:
        remove_process = subprocess.Popen(['rm', 'session_config.txt'])
        remove_process.communicate()

    args = ['run_app.py',
            '--name',
            'Book of Gary',
            '--author',
            'Gary',
            '--version',
            '0.0.0',
            './test']

    doc_generator = ROSDocCMD(args[1:])
    assert doc_generator.project_name == 'Book of Gary'
    assert doc_generator.author_name == 'Gary'
    assert doc_generator.version_no == '0.0.0'


def test_rosdoccmd_argpase_withFaultySessionConfig(monkeypatch):

    # Ensure that there is no session_config.txt.
    if os.path.isfile('./session_config.txt') is True:
        remove_process = subprocess.Popen(['rm', 'session_config.txt'])
        remove_process.communicate()

    # Create faulty session_config.txt
    session_config_lines = ['this', 'is', 'faulty']

    if session_config_lines[0] is not None:
        print('Saving to session_config.txt.')
        a_file = open('session_config.txt', 'w')
        for line in session_config_lines:
            if 'None' not in str(line):
                print(line)
                a_file.writelines(str(line) + '\n')
        a_file.close()

    args = ['run_app.py',
            '--name',
            'Book of Gary',
            '--author',
            'Gary',
            '--version',
            '0.0.1',
            './test']

    monkeypatch.setattr('builtins.input', lambda _: 'N')

    doc_generator = ROSDocCMD(args[1:])
    assert doc_generator.project_name == 'default_project_name'
    assert doc_generator.author_name == 'default_author_name'
    assert doc_generator.version_no == '0.0.0'


def test_rosdoccmd_generateDocs(monkeypatch):
    args = ['run_app.py',
            '--name',
            'Book of Gary',
            '--author',
            'Gary',
            '--version',
            '0.0.0',
            './test']

    monkeypatch.setattr('builtins.input', lambda _: 'Y')

    doc_generator = ROSDocCMD(args[1:])
    assert doc_generator.project_name == 'Book of Gary'
    assert doc_generator.author_name == 'Gary'
    assert doc_generator.version_no == '0.0.0'

    doc_generator.generateDocs()

    assert os.path.isdir('./output_docs') is True


def test_rosdoccmd_saveSessionConfig(monkeypatch):
    args = ['run_app.py',
            '--name',
            'Book of Gary',
            '--author',
            'Gary',
            '--version',
            '0.0.0',
            '--save',
            './test']

    monkeypatch.setattr('builtins.input', lambda _: 'Y')

    doc_generator = ROSDocCMD(args[1:])
    assert doc_generator.project_name == 'Book of Gary'
    assert doc_generator.author_name == 'Gary'
    assert doc_generator.version_no == '0.0.0'

    assert doc_generator.saveLastSessionConfig is True

    if doc_generator.saveLastSessionConfig is True:
        doc_generator.saveSessionConfig()

    isSessionConfigGenerated = os.path.isfile('./session_config.txt')

    assert isSessionConfigGenerated is True


def test_rosdoccmd_argpase_purge(capsys, monkeypatch):
    args = ['run_app.py', '--purge']

    monkeypatch.setattr('builtins.input', lambda _: 'Y')

    with pytest.raises(SystemExit):
        doc_generator = ROSDocCMD(args[1:])  # noqa
    out, err = capsys.readouterr()
    assert err == ''

    # Check if output_docs has been deleted.
    isOutPutDocsDeleted = os.path.isdir('./output_docs')

    assert isOutPutDocsDeleted is False


def test_rosdoccmd_cleanSlate(monkeypatch):

    global test_cpp_filepath_abs, test_py_filepath_abs

    # Ensure that there is no session_config.txt.
    if os.path.isfile('./session_config.txt') is True:
        remove_process = subprocess.Popen(['rm', 'session_config.txt'])
        remove_process.communicate()
    if os.path.isdir('./docs_sphinx') is True:
        remove_process = subprocess.Popen(['rm', '-r', './docs_sphinx'])
        remove_process.communicate()

    session_config_lines = ['Not Book of Gary',
                            'Anti-Gary',
                            '1.0.0',
                            test_cpp_filepath_abs,
                            test_py_filepath_abs]

    if session_config_lines[0] is not None:
        print('Saving to session_config.txt.')
        a_file = open('session_config.txt', 'w')
        for line in session_config_lines:
            if 'None' not in str(line):
                print(line)
                a_file.writelines(str(line) + '\n')
        a_file.close()

    args = ['run_app.py',
            '--name',
            'Book of Gary',
            '--author',
            'Gary',
            '--version',
            '0.0.0',
            './test']

    monkeypatch.setattr('builtins.input', lambda _: 'N')

    doc_generator = ROSDocCMD(args[1:])
    assert doc_generator.project_name == 'Not Book of Gary'
    assert doc_generator.author_name == 'Anti-Gary'
    assert doc_generator.version_no == '1.0.0'


def test_rosdoccmd_existingSlate(monkeypatch):

    global test_cpp_filepath_abs, test_py_filepath_abs

    # Ensure that there is no session_config.txt.
    if os.path.isfile('./session_config.txt') is True:
        remove_process = subprocess.Popen(['rm', 'session_config.txt'])
        remove_process.communicate()

    session_config_lines = ['Not Book of Gary',
                            'Anti-Gary',
                            '1.0.0',
                            test_cpp_filepath_abs,
                            test_py_filepath_abs]

    if session_config_lines[0] is not None:
        print('Saving to session_config.txt.')
        a_file = open('session_config.txt', 'w')
        for line in session_config_lines:
            if 'None' not in str(line):
                print(line)
                a_file.writelines(str(line) + '\n')
        a_file.close()

    args = ['run_app.py',
            '--name',
            'Book of Gary',
            '--author',
            'Gary',
            '--version',
            '0.0.0',
            './test']

    monkeypatch.setattr('builtins.input', lambda _: 'Y')

    doc_generator = ROSDocCMD(args[1:])
    assert doc_generator.project_name == 'Book of Gary'
    assert doc_generator.author_name == 'Gary'
    assert doc_generator.version_no == '0.0.0'
