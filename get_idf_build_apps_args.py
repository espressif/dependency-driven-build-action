#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
import random
import string
import tempfile
import typing as t
import unittest
from unittest.mock import patch


def get_modified_components(modified_files: t.List[str], top_level_depth: int = 0) -> t.Set[str]:
    modified_components = set()
    excluded_dirs = [
        '.github',
        'test',
        'tests',
        'test_app',
        'test_apps',
        'managed_components',  # idf-component-manager
    ]
    for file in modified_files:
        toplevel_name = file.split(os.sep)[top_level_depth]
        toplevel_path = os.sep.join(file.split(os.sep)[: top_level_depth + 1])
        if toplevel_name in excluded_dirs:
            continue
        if not os.path.isdir(toplevel_path):
            continue
        modified_components.add(toplevel_name)

    return modified_components


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'modified_files_list', type=argparse.FileType('r'), help='Input file containing list of modified files'
    )
    parser.add_argument('output', type=argparse.FileType('w'), help='Output file containing idf-build-apps arguments')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument(
        '--top-level-depth',
        type=int,
        default=0,
        help='Depth of top-level directories to find the modified components. '
        'If the components are in the root directory, set this to 0. Default is 0.',
    )
    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()

    try:
        _main(args)
    finally:
        args.modified_files_list.close()
        args.output.close()


def _main(args: argparse.Namespace) -> None:
    if os.getenv('BUILD_AND_TEST_ALL_APPS', False):
        if args.verbose:
            print('BUILD_AND_TEST_ALL_APPS is set, building all apps')
        args.output.write('')
        return

    modified_files = args.modified_files_list.readlines()
    idf_build_apps_args = []
    if modified_files:
        idf_build_apps_args += ['--modified-files', '"' + ';'.join(modified_files) + '"']

    if args.verbose:
        print('Modified files:')
        for file in sorted(modified_files):
            print(f'  - {file}')

    modified_components = get_modified_components(modified_files, args.top_level_depth)
    if modified_components:
        idf_build_apps_args += ['--modified-components', '"' + ';'.join(modified_components) + '"']
    else:
        idf_build_apps_args += ['--modified-components', '";"']

    if args.verbose:
        print('Modified components:')
        if not modified_components:
            print('None')
        else:
            for component in sorted(modified_components):
                print(f'  - {component}')

    args.output.write(' '.join(idf_build_apps_args))


if __name__ == '__main__':
    main()


class TestGetModifiedComponents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workdir = os.curdir

    def setUp(self):
        tmp_path = os.path.join(tempfile.gettempdir(), ''.join(random.choice(string.ascii_letters) for _ in range(10)))
        os.makedirs(tmp_path, exist_ok=True)
        os.chdir(tmp_path)

    def tearDown(self):
        os.chdir(self.workdir)

    def test_no_modified_files(self):
        self.assertEqual(get_modified_components([]), set())

    def test_single_modified_file_in_root(self):
        os.mkdir('component')
        self.assertEqual(get_modified_components(['component/file.c']), {'component'})

    def test_multiple_modified_files_in_root(self):
        os.mkdir('component1')
        os.mkdir('component2')
        self.assertEqual(
            get_modified_components(['component1/file1.c', 'component2/file2.c']), {'component1', 'component2'}
        )

    def test_excluded_directories(self):
        os.mkdir('.github')
        os.mkdir('test')
        os.mkdir('tests')
        self.assertEqual(get_modified_components(['.github/file.c', 'test/file.c', 'tests/file.c']), set())

    def test_top_level_depth(self):
        os.mkdir('dir')
        os.mkdir(os.path.join('dir', 'component'))
        self.assertEqual(get_modified_components(['dir/component/file.c'], top_level_depth=1), {'component'})
        self.assertEqual(get_modified_components(['dir/component/file.c']), {'dir'})

    def test_non_existent_directories(self):
        self.assertEqual(get_modified_components(['nonexistent/file.c']), set())


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workdir = os.curdir
        cls.input = 'modified_files_list.txt'
        cls.output = 'output.txt'

    def setUp(self):
        tmp_path = os.path.join(tempfile.gettempdir(), ''.join(random.choice(string.ascii_letters) for _ in range(10)))
        os.makedirs(tmp_path, exist_ok=True)
        os.chdir(tmp_path)

    def tearDown(self):
        os.chdir(self.workdir)

    @patch.dict(os.environ, {'BUILD_AND_TEST_ALL_APPS': '1'})
    def test_build_all_apps(self):
        with open(self.input, 'w') as f:
            f.write('component/file.c\n')
        args = [
            self.input,
            self.output,
        ]
        with patch('sys.argv', ['', *args]):
            main()
        with open(self.output) as f:
            self.assertEqual(f.read(), '')

    def test_modified_files_argument(self):
        with open(self.input, 'w') as f:
            f.write('component/file.c\n')
        args = [
            self.input,
            self.output,
        ]
        with patch('sys.argv', ['', *args]):
            main()
        with open(self.output) as f:
            self.assertIn('--modified-files', f.read())

    def test_modified_components_argument(self):
        os.mkdir('component')
        with open(self.input, 'w') as f:
            f.write('component/file.c\n')
        args = [
            self.input,
            self.output,
        ]
        with patch('sys.argv', ['', *args]):
            main()
        with open(self.output) as f:
            self.assertIn('--modified-components', f.read())

    def test_no_modified_components(self):
        with open(self.input, 'w') as f:
            f.write('test/file.c\n')
        args = [
            self.input,
            self.output,
        ]
        with patch('sys.argv', ['', *args]):
            main()
        with open(self.output) as f:
            self.assertIn('--modified-components ";"', f.read())
