import unittest
from collections import OrderedDict

from pylibby import (
    ChapterMarker,
    parse_part_path,
    parse_toc,
    convert_seconds_to_timestamp,
)


class PyLibbyTests(unittest.TestCase):
    def test_convert_seconds_to_timestamp(self):
        self.assertEqual("00:00.000", convert_seconds_to_timestamp(str(0)))
        self.assertEqual("01:03.000", convert_seconds_to_timestamp(str(63)))

    def test_parse_part_path(self):
        marker = parse_part_path(
            "Test", "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part01.mp3"
        )
        self.assertEqual(marker.title, "Test")
        self.assertEqual(marker.second_stamp, 0)
        self.assertEqual(marker.part_name, "Fmt425-Part01.mp3")

        marker = parse_part_path(
            "Test", "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part01.mp3#123"
        )
        self.assertEqual(marker.title, "Test")
        self.assertEqual(marker.second_stamp, 123)
        self.assertEqual(marker.part_name, "Fmt425-Part01.mp3")

    def test_parse_toc(self):
        toc = [
            {
                "title": "Chapter 1",
                "path": "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part01.mp3",
                "contents": [
                    {
                        "title": "Chapter 1 (34:29)",
                        "path": "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part01.mp3#2069",
                    }
                ],
            },
            {
                "title": "Chapter 2",
                "path": "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part02.mp3",
                "contents": [
                    {
                        "title": "Chapter 2 (00:00)",
                        "path": "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part03.mp3",
                    },
                    {
                        "title": "Chapter 2 (08:18)",
                        "path": "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part03.mp3#498",
                    },
                ],
            },
            {
                "title": "Chapter 3",
                "path": "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part03.mp3#2140",
            },
            {
                "title": "Chapter 4",
                "path": "{AAAAAAAA-BBBB-CCCC-9999-ABCDEF123456}Fmt425-Part03.mp3#3000",
            },
        ]
        expected_result = OrderedDict(
            {
                "Fmt425-Part01.mp3": [
                    ChapterMarker("Chapter 1", "Fmt425-Part01.mp3", 0),
                ],
                "Fmt425-Part02.mp3": [
                    ChapterMarker("Chapter 2", "Fmt425-Part02.mp3", 0),
                ],
                "Fmt425-Part03.mp3": [
                    ChapterMarker("Chapter 2", "Fmt425-Part03.mp3", 0),
                    ChapterMarker("Chapter 3", "Fmt425-Part03.mp3", 2140),
                    ChapterMarker("Chapter 4", "Fmt425-Part03.mp3", 3000),
                ],
            }
        )

        self.assertEqual(parse_toc(toc), expected_result)
