import unittest

from mara_app.app import MaraApp
from mara_app import monkey_patch
from tests import wrap_target


class AppTest(unittest.TestCase):
    def setUp(self):
        app = MaraApp()
        self.app = app.test_client()

    @monkey_patch.patch(wrap_target.multiply_by_two, 'test the monkey patch tracking for patch')
    def wrapper(a: int):
        return a + 100


    @monkey_patch.wrap(wrap_target.multiply_by_three, 'test the monkey patch tracking for wrap')
    def wrapper(original_fn, a: int):
        return original_fn(a) + 1000

    def test_config_page_exists(self):
        response = self.app.get("/admin/configuration")
        self.assertEqual(response.status_code, 200)

    def test_patch_is_listed(self):
        patches = monkey_patch.list_patches()
        self.assertEqual(len(patches), 2)
        # NOTE: the list follow the same order of patch/wrapping
        self.assertEqual(patches[0].original_module, 'tests.wrap_target')
        self.assertEqual(patches[0].original_name, 'multiply_by_two')
        self.assertEqual(patches[0].description, 'test the monkey patch tracking for patch')
        self.assertTrue(patches[0].replaces)

        self.assertEqual(patches[1].original_module, 'tests.wrap_target')
        self.assertEqual(patches[1].original_name, 'multiply_by_three')
        self.assertEqual(patches[1].description, 'test the monkey patch tracking for wrap')
        self.assertFalse(patches[1].replaces)

    def test_patches_are_actually_applied(self):
        # this has been replaced, it does add 100
        self.assertEqual(wrap_target.multiply_by_two(1), 101)
        # this has been wrapped, it does multiply by 3 AND add 1000
        self.assertEqual(wrap_target.multiply_by_three(1), 1003)



if __name__ == "__main__":
    unittest.main()
