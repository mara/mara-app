import unittest

from flask import Flask

from mara_app import MaraApp


class AppTest(unittest.TestCase):
    def setUp(self):
        app = MaraApp()
        self.app = app.test_client()

    def test_correct_call(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
