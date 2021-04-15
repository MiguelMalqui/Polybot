import unittest
from polybot.polygons import Vector
import math


class TestVector(unittest.TestCase):

    def test_equal(self):
        self.assertTrue(Vector(1, 1) == Vector(1, 1))
        self.assertFalse(Vector(1, 1) == Vector(2, 2))

    def test_less_than(self):
        vector55 = Vector(5, 5)
        vector44 = Vector(4, 4)
        vector54 = Vector(5, 4)
        self.assertTrue(vector44 < vector55)
        self.assertTrue(vector54 < vector55)

    def test_greater_than(self):
        vector55 = Vector(5, 5)
        vector44 = Vector(4, 4)
        vector54 = Vector(5, 4)
        self.assertTrue(vector55 > vector44)
        self.assertTrue(vector55 > vector54)

    def test_add(self):
        self.assertEqual(Vector(10, 5.5) + Vector(-3, 3), Vector(7, 8.5))

    def test_truediv(self):
        self.assertEqual(Vector(10, 20) / 2, Vector(5, 10))

    def test_multiplication(self):
        self.assertEqual(Vector(1, 3) * 3, Vector(3, 9))
        self.assertEqual(2 * Vector(4, -1), Vector(8, -2))

    def test_cross(self):
        cross_product = Vector.cross(Vector(0, 1), Vector(-1, 1))
        expected_cross_product = 1
        self.assertEqual(cross_product, expected_cross_product)

    def test_angle(self):
        self.assertEqual(Vector(0, 1).angle(), 0)
        self.assertEqual(Vector(1, 1).angle(), (1 / 4) * math.pi)
        self.assertEqual(Vector(1, -1).angle(), (3 / 4) * math.pi)
        self.assertEqual(Vector(-1, -1).angle(), (5 / 4) * math.pi)
        self.assertEqual(Vector(-1, 1).angle(), (7 / 4) * math.pi)


if __name__ == "__main__":
    unittest.main()
