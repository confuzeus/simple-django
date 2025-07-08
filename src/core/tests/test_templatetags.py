import collections.abc

from django.core.paginator import Paginator
from django.test import RequestFactory, SimpleTestCase

from src.core.templatetags import pagination_tags
from src.core.templatetags.url_tags import active_url, get_qs
from src.core.templatetags.useful_filters import is_number, is_string


class TemplateTagsTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super(TemplateTagsTests, cls).setUpClass()
        cls.rf = RequestFactory()

    def test_active_url(self):
        request = self.rf.get("/")
        test_url = "/"
        active = active_url(request, test_url)
        self.assertEqual(active, "active")

        test_url = "/other"
        active = active_url(request, test_url)
        self.assertEqual(active, "")

        request = self.rf.get("/other")
        active = active_url(request, test_url)
        self.assertEqual(active, "active")

        test_url = "/"
        active = active_url(request, test_url)
        self.assertEqual(active, "")

    def test_get_qs(self):
        request = self.rf.get("/")
        qs = get_qs(request)
        self.assertEqual(qs, "")

        query = "one=two&three=four"
        request = self.rf.get(f"/path?{query}")
        qs = get_qs(request)
        self.assertEqual(qs, query + "&")

        qs = get_qs(request, "one")
        self.assertEqual(qs, "three=four&")

        qs = get_qs(request, "five")
        self.assertEqual(qs, query + "&")

    def test_is_number(self):
        self.assertTrue(is_number(1))
        self.assertFalse(is_number("1"))
        self.assertFalse(is_number(True))
        self.assertTrue(is_number(1.0))
        self.assertFalse(is_number({}))

    def test_is_string(self):
        self.assertTrue(is_string(""))
        self.assertFalse(is_string(1))
        self.assertFalse(is_string(False))
        self.assertFalse(is_string({}))
        self.assertFalse(is_string(1.0))

    def test_get_elided_page_range(self):
        """
        Tests borrowed from django project.
        """
        # Range is not elided if not enough pages when using default arguments:
        paginator = Paginator(range(10 * 100), 100)
        page_range = pagination_tags.get_elided_page_range(1, paginator)
        self.assertIsInstance(page_range, collections.abc.Generator)
        self.assertNotIn(pagination_tags.ELLIPSIS, page_range)
        paginator = Paginator(range(10 * 100 + 1), 100)
        self.assertIsInstance(page_range, collections.abc.Generator)
        page_range = pagination_tags.get_elided_page_range(1, paginator)
        self.assertIn(pagination_tags.ELLIPSIS, page_range)

        # Range should be elided if enough pages when using default arguments:
        tests = [
            # on_each_side=3, on_ends=2
            (1, [1, 2, 3, 4, pagination_tags.ELLIPSIS, 49, 50]),
            (6, [1, 2, 3, 4, 5, 6, 7, 8, 9, pagination_tags.ELLIPSIS, 49, 50]),
            (7, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, pagination_tags.ELLIPSIS, 49, 50]),
            (
                8,
                [
                    1,
                    2,
                    pagination_tags.ELLIPSIS,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    pagination_tags.ELLIPSIS,
                    49,
                    50,
                ],
            ),
            (
                43,
                [
                    1,
                    2,
                    pagination_tags.ELLIPSIS,
                    40,
                    41,
                    42,
                    43,
                    44,
                    45,
                    46,
                    pagination_tags.ELLIPSIS,
                    49,
                    50,
                ],
            ),
            (
                44,
                [
                    1,
                    2,
                    pagination_tags.ELLIPSIS,
                    41,
                    42,
                    43,
                    44,
                    45,
                    46,
                    47,
                    48,
                    49,
                    50,
                ],
            ),
            (45, [1, 2, pagination_tags.ELLIPSIS, 42, 43, 44, 45, 46, 47, 48, 49, 50]),
            (50, [1, 2, pagination_tags.ELLIPSIS, 47, 48, 49, 50]),
        ]
        paginator = Paginator(range(5000), 100)
        for number, expected in tests:
            with self.subTest(number=number):
                page_range = pagination_tags.get_elided_page_range(number, paginator)
                self.assertIsInstance(page_range, collections.abc.Generator)
                self.assertEqual(list(page_range), expected)

        # Range is not elided if not enough pages when using custom arguments:
        tests = [
            (6, 2, 1, 1),
            (8, 1, 3, 1),
            (8, 4, 0, 1),
            (4, 1, 1, 1),
            # When on_each_side and on_ends are both <= 1 but not both == 1 it
            # is a special case where the range is not elided until an extra
            # page is added.
            (2, 0, 1, 2),
            (2, 1, 0, 2),
            (1, 0, 0, 2),
        ]
        for pages, on_each_side, on_ends, elided_after in tests:
            for offset in range(elided_after + 1):
                with self.subTest(
                    pages=pages,
                    offset=elided_after,
                    on_each_side=on_each_side,
                    on_ends=on_ends,
                ):
                    paginator = Paginator(range((pages + offset) * 100), 100)
                    page_range = pagination_tags.get_elided_page_range(
                        1, paginator, on_each_side=on_each_side, on_ends=on_ends
                    )
                    self.assertIsInstance(page_range, collections.abc.Generator)
                    if offset < elided_after:
                        self.assertNotIn(pagination_tags.ELLIPSIS, page_range)
                    else:
                        self.assertIn(pagination_tags.ELLIPSIS, page_range)

        # Range should be elided if enough pages when using custom arguments:
        tests = [
            # on_each_side=2, on_ends=1
            (1, 2, 1, [1, 2, 3, pagination_tags.ELLIPSIS, 50]),
            (4, 2, 1, [1, 2, 3, 4, 5, 6, pagination_tags.ELLIPSIS, 50]),
            (5, 2, 1, [1, 2, 3, 4, 5, 6, 7, pagination_tags.ELLIPSIS, 50]),
            (
                6,
                2,
                1,
                [
                    1,
                    pagination_tags.ELLIPSIS,
                    4,
                    5,
                    6,
                    7,
                    8,
                    pagination_tags.ELLIPSIS,
                    50,
                ],
            ),
            (
                45,
                2,
                1,
                [
                    1,
                    pagination_tags.ELLIPSIS,
                    43,
                    44,
                    45,
                    46,
                    47,
                    pagination_tags.ELLIPSIS,
                    50,
                ],
            ),
            (46, 2, 1, [1, pagination_tags.ELLIPSIS, 44, 45, 46, 47, 48, 49, 50]),
            (47, 2, 1, [1, pagination_tags.ELLIPSIS, 45, 46, 47, 48, 49, 50]),
            (50, 2, 1, [1, pagination_tags.ELLIPSIS, 48, 49, 50]),
            # on_each_side=1, on_ends=3
            (1, 1, 3, [1, 2, pagination_tags.ELLIPSIS, 48, 49, 50]),
            (5, 1, 3, [1, 2, 3, 4, 5, 6, pagination_tags.ELLIPSIS, 48, 49, 50]),
            (6, 1, 3, [1, 2, 3, 4, 5, 6, 7, pagination_tags.ELLIPSIS, 48, 49, 50]),
            (
                7,
                1,
                3,
                [
                    1,
                    2,
                    3,
                    pagination_tags.ELLIPSIS,
                    6,
                    7,
                    8,
                    pagination_tags.ELLIPSIS,
                    48,
                    49,
                    50,
                ],
            ),
            (
                44,
                1,
                3,
                [
                    1,
                    2,
                    3,
                    pagination_tags.ELLIPSIS,
                    43,
                    44,
                    45,
                    pagination_tags.ELLIPSIS,
                    48,
                    49,
                    50,
                ],
            ),
            (45, 1, 3, [1, 2, 3, pagination_tags.ELLIPSIS, 44, 45, 46, 47, 48, 49, 50]),
            (46, 1, 3, [1, 2, 3, pagination_tags.ELLIPSIS, 45, 46, 47, 48, 49, 50]),
            (50, 1, 3, [1, 2, 3, pagination_tags.ELLIPSIS, 49, 50]),
            # on_each_side=4, on_ends=0
            (1, 4, 0, [1, 2, 3, 4, 5, pagination_tags.ELLIPSIS]),
            (5, 4, 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, pagination_tags.ELLIPSIS]),
            (6, 4, 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, pagination_tags.ELLIPSIS]),
            (
                7,
                4,
                0,
                [
                    pagination_tags.ELLIPSIS,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    pagination_tags.ELLIPSIS,
                ],
            ),
            (
                44,
                4,
                0,
                [
                    pagination_tags.ELLIPSIS,
                    40,
                    41,
                    42,
                    43,
                    44,
                    45,
                    46,
                    47,
                    48,
                    pagination_tags.ELLIPSIS,
                ],
            ),
            (
                45,
                4,
                0,
                [pagination_tags.ELLIPSIS, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
            ),
            (46, 4, 0, [pagination_tags.ELLIPSIS, 42, 43, 44, 45, 46, 47, 48, 49, 50]),
            (50, 4, 0, [pagination_tags.ELLIPSIS, 46, 47, 48, 49, 50]),
            # on_each_side=0, on_ends=1
            (1, 0, 1, [1, pagination_tags.ELLIPSIS, 50]),
            (2, 0, 1, [1, 2, pagination_tags.ELLIPSIS, 50]),
            (3, 0, 1, [1, 2, 3, pagination_tags.ELLIPSIS, 50]),
            (4, 0, 1, [1, pagination_tags.ELLIPSIS, 4, pagination_tags.ELLIPSIS, 50]),
            (47, 0, 1, [1, pagination_tags.ELLIPSIS, 47, pagination_tags.ELLIPSIS, 50]),
            (48, 0, 1, [1, pagination_tags.ELLIPSIS, 48, 49, 50]),
            (49, 0, 1, [1, pagination_tags.ELLIPSIS, 49, 50]),
            (50, 0, 1, [1, pagination_tags.ELLIPSIS, 50]),
            # on_each_side=0, on_ends=0
            (1, 0, 0, [1, pagination_tags.ELLIPSIS]),
            (2, 0, 0, [1, 2, pagination_tags.ELLIPSIS]),
            (3, 0, 0, [pagination_tags.ELLIPSIS, 3, pagination_tags.ELLIPSIS]),
            (48, 0, 0, [pagination_tags.ELLIPSIS, 48, pagination_tags.ELLIPSIS]),
            (49, 0, 0, [pagination_tags.ELLIPSIS, 49, 50]),
            (50, 0, 0, [pagination_tags.ELLIPSIS, 50]),
        ]
        paginator = Paginator(range(5000), 100)
        for number, on_each_side, on_ends, expected in tests:
            with self.subTest(
                number=number, on_each_side=on_each_side, on_ends=on_ends
            ):
                page_range = pagination_tags.get_elided_page_range(
                    number, paginator, on_each_side=on_each_side, on_ends=on_ends
                )
                self.assertIsInstance(page_range, collections.abc.Generator)
                self.assertEqual(list(page_range), expected)
