import unittest
from polybot.polygons import *
import math
from PIL import Image


class TestConvexPolygon(unittest.TestCase):

    IMAGE_MODE = 'RGB'
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 400
    WHITE = (255, 255, 255)

    def test_creation_of_particular_cases_of_polygons(self):
        empty = ConvexPolygon([])
        monogon = ConvexPolygon([Vector(1, 1)])
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        self.assertEqual(empty.num_vertices, 0)
        self.assertEqual(monogon.num_vertices, 1)
        self.assertEqual(digon.num_vertices, 2)

    def test_remove_repeated_vertices(self):
        monogon = ConvexPolygon([Vector(1, 1), Vector(1, 1), Vector(1, 1)])
        self.assertEqual(monogon.num_vertices, 1)

    def test_remove_aligned_Vectors(self):
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 0), Vector(2, 0), Vector(3, 0)])
        representation = 'ConvexPolygon([Vector(0, 0), Vector(3, 0)])'
        self.assertEqual(repr(digon), representation)

    def test_clockwise_and_starts_leftmost_point(self):
        polygon = ConvexPolygon(
            [Vector(1, 0), Vector(1.2, 0.4), Vector(1, 1), Vector(0, 1), Vector(0, 0.7), Vector(0.5, 0.5),
             Vector(0, 0.3), Vector(0, 0)])
        representation = 'ConvexPolygon([Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1.2, 0.4), Vector(1, 0)])'
        self.assertEqual(repr(polygon), representation)

    def test_perimeter_of_empty_polygon(self):
        empty = ConvexPolygon([])
        self.assertEqual(empty.perimeter, 0)

    def test_perimeter_of_monogon(self):
        monogon = ConvexPolygon([Vector(1, 1)])
        self.assertEqual(monogon.perimeter, 0)

    def test_perimeter_of_digon(self):
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        self.assertAlmostEqual(digon.perimeter, math.sqrt(2))

    def test_perimeter_of_normal_polygon(self):
        decagon = TestConvexPolygon._create_regular_polygon(10)
        self.assertAlmostEqual(decagon.perimeter, 10 * 2 * math.cos(math.pi / 2 - math.pi / 10))

    def test_area_of_empty_polygon(self):
        empty = ConvexPolygon([])
        self.assertEqual(empty.area, 0)

    def test_area_of_monogon(self):
        monogon = ConvexPolygon([Vector(1, 1)])
        self.assertEqual(monogon.area, 0)

    def test_area_of_digon(self):
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        self.assertEqual(digon.area, 0)

    def test_area_of_normal_polygon(self):
        polygon = ConvexPolygon([Vector(0, 0), Vector(1, 1), Vector(0, 1), Vector(1, 0), Vector(0.5, 2)])
        self.assertEqual(polygon.area, 1 + 0.5)

    def test_centroid_of_empty_polygon(self):
        empty = ConvexPolygon([])
        self.assertEqual(empty.centroid, Vector(0.0, 0.0))

    def test_centroid_of_monogon(self):
        monogon = ConvexPolygon([Vector(1, 1)])
        self.assertEqual(monogon.centroid, Vector(1, 1))

    def test_centroid_of_digon(self):
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        self.assertEqual(digon.centroid, Vector(0.5, 0.5))

    def test_centroid_of_normal_polygon(self):
        decagon = TestConvexPolygon._create_regular_polygon(10)
        self.assertAlmostEqual(decagon.centroid.x, 0)
        self.assertAlmostEqual(decagon.centroid.y, 0)

    def test_is_regular_of_empty_polygon(self):
        empty = ConvexPolygon([])
        self.assertTrue(empty.is_regular)

    def test_is_regular_of_monogon(self):
        monogon = ConvexPolygon([Vector(1, 1)])
        self.assertTrue(monogon.is_regular)

    def test_is_regular_of_digon(self):
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        self.assertTrue(digon.is_regular)

    def test_is_regular_of_normal_regular_polygon(self):
        decagon = TestConvexPolygon._create_regular_polygon(10)
        self.assertTrue(decagon.is_regular)

    def test_is_regular_of_normal_irregular_polygon(self):
        irregular = ConvexPolygon([Vector(0, 0), Vector(1, 0), Vector(-5, -5)])
        self.assertFalse(irregular.is_regular)

    def test_is_point_inside_of_empty_polygon(self):
        empty = ConvexPolygon([])
        self.assertFalse(empty.is_point_inside(Vector(0, 0)))

    def test_is_point_inside_of_monogon(self):
        monogon = ConvexPolygon([Vector(1, 1)])
        self.assertTrue(monogon.is_point_inside(Vector(1, 1)))
        self.assertFalse(monogon.is_point_inside(Vector(0, 0)))

    def test_is_point_inside_of_digon(self):
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        self.assertTrue(digon.is_point_inside(Vector(0.0, 0.0)))
        self.assertTrue(digon.is_point_inside(Vector(0.5, 0.5)))
        self.assertFalse(digon.is_point_inside(Vector(2.0, 2.0)))

    def test_is_point_inside_of_normal_polygon_when_point_is_inside(self):
        polygon = TestConvexPolygon._create_regular_polygon(10)
        self.assertTrue(polygon.is_point_inside(Vector(0, 0)))

    def test_is_point_inside_of_normal_polygon_when_point_is_in_perimeter(self):
        polygon = TestConvexPolygon._create_regular_polygon(10)
        self.assertTrue(polygon.is_point_inside(Vector(1, 0)))

    def test_is_point_inside_of_normal_polygon_when_point_is_outside(self):
        polygon = TestConvexPolygon._create_regular_polygon(10)
        self.assertFalse(polygon.is_point_inside(Vector(2, 2)))
        self.assertFalse(polygon.is_point_inside(Vector(-10, 0)))

    def test_is_polygon_inside_of_empty_polygon_(self):
        empty = ConvexPolygon([])
        monogon = ConvexPolygon([Vector(1, 1)])
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        unit_square = ConvexPolygon([Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1, 0)])
        self.assertFalse(empty.is_polygon_inside(empty))
        self.assertFalse(empty.is_polygon_inside(monogon))
        self.assertFalse(empty.is_polygon_inside(digon))
        self.assertFalse(empty.is_polygon_inside(unit_square))

    def test_is_polygon_inside_of_monogon(self):
        monogon = ConvexPolygon([Vector(1, 1)])
        empty = ConvexPolygon([])
        monogon2 = ConvexPolygon([Vector(2, 2)])
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        unit_square = ConvexPolygon([Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1, 0)])
        self.assertTrue(monogon.is_polygon_inside(monogon))
        self.assertFalse(monogon.is_polygon_inside(empty))
        self.assertFalse(monogon.is_polygon_inside(monogon2))
        self.assertFalse(monogon.is_polygon_inside(digon))
        self.assertFalse(monogon.is_polygon_inside(unit_square))

    def test_is_polygon_inside_of_digon(self):
        digon = ConvexPolygon([Vector(0, 0), Vector(1, 1)])
        empty = ConvexPolygon([])
        monogon1 = ConvexPolygon([Vector(1, 1)])
        monogon2 = ConvexPolygon([Vector(2, 2)])
        digon2 = ConvexPolygon([Vector(0, 0), Vector(2, 2)])
        unit_square = ConvexPolygon([Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1, 0)])
        self.assertTrue(digon.is_polygon_inside(digon))
        self.assertFalse(digon.is_polygon_inside(empty))
        self.assertTrue(digon.is_polygon_inside(monogon1))
        self.assertFalse(digon.is_polygon_inside(monogon2))
        self.assertFalse(digon.is_polygon_inside(digon2))
        self.assertFalse(digon.is_polygon_inside(unit_square))

    def test_is_polygon_inside_of_normal_polygon(self):
        decagon = TestConvexPolygon._create_regular_polygon(10)
        heptagon = TestConvexPolygon._create_regular_polygon(7, center=Vector(1, 0))
        hexagon = TestConvexPolygon._create_regular_polygon(6, center=Vector(5, 0))
        pentagon = TestConvexPolygon._create_regular_polygon(5, max_dist_center=0.5)
        triangle = ConvexPolygon([Vector(-0.5, -0.5), Vector(-0.5, 0.5), Vector(1, 0)])
        self.assertTrue(decagon.is_polygon_inside(decagon))
        self.assertFalse(decagon.is_polygon_inside(heptagon))
        self.assertFalse(decagon.is_polygon_inside(hexagon))
        self.assertTrue(decagon.is_polygon_inside(pentagon))
        self.assertTrue(decagon.is_polygon_inside(triangle))

    def test_convex_union(self):
        polygon1 = ConvexPolygon([Vector(0, 0), Vector(1, 1), Vector(0, 1), Vector(1, 0)])
        polygon2 = ConvexPolygon([Vector(0.5, 1.5), Vector(1.5, 0.5), Vector(-1.5, 0.5)])
        poly_union = ConvexPolygon.convex_union(polygon1, polygon2)
        expected_union = ConvexPolygon(
            [Vector(1.5, 0.5), Vector(0.5, 1.5), Vector(-1.5, 0.5), Vector(0, 0), Vector(1, 0)])
        self.assertEqual(poly_union, expected_union)

    def test_intersection_polygon_inside_other_polygon(self):
        polygon1 = ConvexPolygon([Vector(-1, 0), Vector(0, 1), Vector(1, 0), Vector(0, -1)])
        polygon2 = ConvexPolygon([Vector(-2, 0), Vector(0, 2), Vector(2, 0), Vector(0, -2)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = ConvexPolygon([Vector(-1, 0), Vector(0, 1), Vector(1, 0), Vector(0, -1)])
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_common_vertex(self):
        polygon1 = ConvexPolygon([Vector(-1, -1), Vector(-1, 0), Vector(0, 0), Vector(0, -1)])
        polygon2 = ConvexPolygon([Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1, 0)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = ConvexPolygon([Vector(0.0, 0.0)])
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_one_inside_other_and_common_vertex(self):
        polygon1 = ConvexPolygon([Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1, 0)])
        polygon2 = ConvexPolygon([Vector(0.2, 0.2), Vector(0.5, 0.9), Vector(1, 1)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = polygon2
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_common_point(self):
        polygon1 = ConvexPolygon([Vector(-1, -1), Vector(-1, 1), Vector(0, 1), Vector(0, -1)])
        polygon2 = ConvexPolygon([Vector(0, 0), Vector(1, 1), Vector(2, 0), Vector(1, -11)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = ConvexPolygon([Vector(0.0, 0.0)])
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_one_inside_other_and_common_point(self):
        polygon1 = ConvexPolygon([Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1, 0)])
        polygon2 = ConvexPolygon([Vector(0.2, 0.2), Vector(0.5, 0.9), Vector(1, 0.5)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = polygon2
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_common_edge(self):
        polygon1 = ConvexPolygon([Vector(-1, 0), Vector(-1, 1), Vector(0, 1), Vector(0, 0)])
        polygon2 = ConvexPolygon([Vector(0, 0), Vector(0, 1), Vector(1, 1), Vector(1, 0)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = ConvexPolygon([Vector(0.0, 0.0), Vector(0.0, 1.0)])
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_one_inside_other_and_common_edge(self):
        polygon1 = ConvexPolygon([Vector(-1, 0), Vector(-1, 1), Vector(0, 1), Vector(0, 0)])
        polygon2 = ConvexPolygon([Vector(-0.5, 0.5), Vector(0, 0), Vector(0, 1)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = polygon2
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_common_segment(self):
        polygon1 = ConvexPolygon([Vector(-1, 0), Vector(-1, 1), Vector(0, 1), Vector(0, 0)])
        polygon2 = ConvexPolygon([Vector(0, 0.5), Vector(0, 1.5), Vector(1, 1.5), Vector(1, 0.5)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = ConvexPolygon([Vector(0.0, 0.5), Vector(0.0, 1.0)])
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_one_inside_other_and_common_segment(self):
        polygon1 = ConvexPolygon([Vector(-1, 0), Vector(-1, 1), Vector(0, 1), Vector(0, 0)])
        polygon2 = ConvexPolygon([Vector(-0.5, 0.5), Vector(0, 0.7), Vector(0, 0.3)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = polygon2
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_overlapping_polygons(self):
        polygon1 = ConvexPolygon([Vector(0, 0), Vector(1, 1), Vector(2, 0), Vector(1, -1)])
        intersection = ConvexPolygon.intersection(polygon1, polygon1)
        expected_intersection = polygon1
        self.assertEqual(intersection, expected_intersection)

    def test_intersection_new_polygon(self):
        polygon1 = ConvexPolygon([Vector(0, 0), Vector(1, 1), Vector(2, 0), Vector(1, -1)])
        polygon2 = ConvexPolygon([Vector(1, 0), Vector(2, 1), Vector(3, 0), Vector(2, -1)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = ConvexPolygon([Vector(1, 0), Vector(1.5, 0.5), Vector(2, 0), Vector(1.5, -0.5)])
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_intersection_empty_polygon(self):
        polygon1 = ConvexPolygon([Vector(-1, 0), Vector(-1, 1), Vector(0, 1), Vector(0, 0)])
        polygon2 = ConvexPolygon([Vector(1, 0), Vector(1, 1), Vector(2, 1), Vector(2, 0)])
        intersection12 = ConvexPolygon.intersection(polygon1, polygon2)
        intersection21 = ConvexPolygon.intersection(polygon2, polygon1)
        expected_intersection = ConvexPolygon([])
        self.assertEqual(intersection12, expected_intersection)
        self.assertEqual(intersection21, expected_intersection)

    def test_bounding_box(self):
        empty = ConvexPolygon([])
        monogon = ConvexPolygon([Vector(10, 10)])
        octagon = TestConvexPolygon._create_regular_polygon(10, 3, Vector(-1, -1))
        irregular = ConvexPolygon([Vector(0, 0), Vector(1, 0), Vector(-2, -5)])
        bounding_box1 = ConvexPolygon.bounding_box([monogon, octagon, irregular])
        expected_bounding_box1 = ConvexPolygon([Vector(10, -5), Vector(10, 10), Vector(-4, 10), Vector(-4, -5)])
        bounding_box2 = ConvexPolygon.bounding_box([empty])
        expected_bounding_box2 = ConvexPolygon([])
        self.assertEqual(bounding_box1, expected_bounding_box1)
        self.assertEqual(bounding_box2, expected_bounding_box2)

    def test_draw_when_bounding_box_is_wider_than_high(self):
        icosagon = TestConvexPolygon._create_regular_polygon(20, 100, Vector(800, 200))
        irregular = ConvexPolygon([Vector(50, 100), Vector(100, 0), Vector(150, 300)], (220, 20, 60))
        image = Image.new('RGB', (400, 400), 'White')
        ConvexPolygon.draw([icosagon, irregular], image)
        image.save('./images/test_draw_when_bounding_box_is_wider_than_high.png')

    def test_draw_when_bounding_box_is_higher_than_wide(self):
        decagon = TestConvexPolygon._create_regular_polygon(10, 100, Vector(200, 800))
        triangle = TestConvexPolygon._create_regular_polygon(3, 200, Vector(100, -10))
        image = Image.new('RGB', (400, 400), 'White')
        ConvexPolygon.draw([decagon, triangle], image)
        image.save('./images/test_draw_when_bounding_box_is_higher_than_wide.png')

    def test_draw_when_bounding_box_is_empty_polygon(self):
        empty = ConvexPolygon([], (255, 0, 0))
        image = Image.new('RGB', (400, 400), 'White')
        ConvexPolygon.draw([empty], image)
        image.save('./images/test_draw_when_bounding_box_is_empty_polygon.png')

    def test_draw_when_bounding_bos_is_monogon(self):
        monogon = ConvexPolygon([Vector(0, 1)], (0, 255, 0))
        image = Image.new('RGB', (400, 400), 'White')
        ConvexPolygon.draw([monogon], image)
        image.save('./images/test_draw_when_bounding_bos_is_monogon.png')

    def test_draw_when_bounding_box_is_digon(self):
        digon = ConvexPolygon([Vector(0, 0), Vector(1.0, 0.0)], (0, 0, 255))
        image = Image.new('RGB', (400, 400), 'White')
        ConvexPolygon.draw([digon], image)
        image.save('./images/test_draw_when_bounding_box_is_digon.png')

    @staticmethod
    def _create_regular_polygon(sides, max_dist_center=1.0, center=Vector(0.0, 0.0)):
        points = []
        for d in [(i / sides) * 2 * math.pi for i in range(sides)]:
            points.append(Vector(math.cos(d), math.sin(d)) * max_dist_center + center)
        return ConvexPolygon(points)


if __name__ == "__main__":
    unittest.main()
