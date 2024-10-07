# SPDX-FileCopyrightText: 2024 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
import unittest
from typing import List

DEFAULT_UPLOAD_FILEPATTERNS = [
    '**/build_*/bootloader/bootloader.bin',
    '**/build_*/partition_table/partition-table.bin',
    '**/build_*/*.bin',
    '**/build_*/flasher_args.json',
    '**/build_*/config/sdkconfig.json',
]


def escape_newline_in_github_set_output(s: str) -> str:
    return s.replace('\n', '%0A')


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_paths', nargs='+', help='space separated list of input paths')
    return parser


def expand_input_paths(input_paths: List[str]) -> List[str]:
    expanded_filepatterns = set()

    for p in input_paths:
        for pat in DEFAULT_UPLOAD_FILEPATTERNS:
            expanded_filepatterns.add(os.path.join(p, pat))

    return sorted(expanded_filepatterns)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    print(escape_newline_in_github_set_output('\n'.join(expand_input_paths(args.input_paths))))


class TestExpandInputPaths(unittest.TestCase):
    def test_expand_input_paths(self):
        inputs = ['foo', 'bar']
        expected_output = sorted(
            [
                'bar/**/build_*/bootloader/bootloader.bin',
                'bar/**/build_*/partition_table/partition-table.bin',
                'bar/**/build_*/*.bin',
                'bar/**/build_*/flasher_args.json',
                'bar/**/build_*/config/sdkconfig.json',
                'foo/**/build_*/bootloader/bootloader.bin',
                'foo/**/build_*/partition_table/partition-table.bin',
                'foo/**/build_*/*.bin',
                'foo/**/build_*/flasher_args.json',
                'foo/**/build_*/config/sdkconfig.json',
            ]
        )
        self.assertEqual(expand_input_paths(inputs), expected_output)
