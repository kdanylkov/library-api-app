from django.test import TestCase

from store.logic import operations


class LogicTestCase(TestCase):

    def test_plus(self):
        result = operations(6, 13, '+')
        self.assertEqual(result, 19)

    def test_minus(self):
        result = operations(6, 13, '-')
        self.assertEqual(result, -7)

    def test_multiply(self):
        result = operations(6, 2, '*')
        self.assertEqual(result, 12)

    def test_devision(self):
        result = operations(6, 2, '/')
        self.assertEqual(result, 3)

    def test_unknown(self):
        result = operations(6, 2, '')
        self.assertEqual(result, 'Operation unknown')
