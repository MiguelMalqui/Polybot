import math
from enum import Enum
from PIL import Image, ImageDraw
from .Vector import Vector
from .DirectedEdge import DirectedEdge


class ConvexPolygon:
    """A class to represent convex polygons."""

    class InsideFlag(Enum):
        UNKNOWN = 0
        POLYGON1 = 1
        POLYGON2 = 2
        BOTH = 3

    PRECISION = 1e-6

    def __init__(self, points, color=(0, 0, 0)):
        """

        Parameters
        ----------
        points : list[Vector]
            The points that will be used to create the smallest convex polygon that contains them.
        (int, int, int)
            RGB representation of a color where the values are in the range 0 to 255.
            Defaults to (0, 0, 0).

        """
        self._vertices = ConvexPolygon._compute_convex_hull(points)
        self._color = color
        self._perimeter = None
        self._area = None
        self._centroid = None
        self._regular = None

    def __eq__(self, other):
        """

        Parameters
        ----------
        other : ConvexPolygon

        Returns
        -------
        bool
            True if they have the same vertices, False otherwise.

        """
        return self._vertices == other._vertices

    def __str__(self):
        return ' '.join(map(str, self._vertices))

    def __repr__(self):
        return 'ConvexPolygon({})'.format(self._vertices)

    @property
    def num_vertices(self):
        """int: The number of vertices of the convex polygon."""
        return len(self._vertices)

    @property
    def num_edges(self):
        """int: The number of edges of the convex polygon."""
        return len(self._vertices)

    @property
    def perimeter(self):
        """float: The perimeter of the convex polygon"""
        if self._perimeter is None:
            self._perimeter = ConvexPolygon._compute_perimeter(self._vertices)
        return self._perimeter

    @property
    def area(self):
        """float: The area of the convex polygon"""
        if self._area is None:
            self._area = ConvexPolygon._compute_area(self._vertices)
        return self._area

    @property
    def centroid(self):
        """Point: The geometric center of the convex polygon"""
        if self._centroid is None:
            self._centroid = ConvexPolygon._compute_centroid(self._vertices)
        return self._centroid

    @property
    def is_regular(self):
        """bool: True if all edges of the convex polygon have the same length with 6 decimals of precision"""
        if self._regular is None:
            self._regular = ConvexPolygon._check_regularity(self._vertices)
        return self._regular

    @property
    def color(self):
        """Tuple[int,int,int]: RGB representation of the color of the convex polygon.
        The values are in the range 0 to 255."""
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def is_point_inside(self, point):
        """

        Parameters
        ----------
        point : Vector

        Returns
        -------
        bool
            True if point is inside the polygon, False otherwise.

        """
        n = len(self._vertices)
        if n == 1:
            return self._vertices[0] == point
        if n == 2:
            p0 = self._vertices[0]
            p1 = self._vertices[1]
            return Vector.length(p0 - point) + Vector.length(p1 - point) == Vector.length(p0 - p1)
        if n >= 3:
            max_triangle = len(self._vertices) - 2
            min_triangle = 0
            vertex1 = self._vertices[0]
            while max_triangle > min_triangle:
                m = (max_triangle + min_triangle) // 2
                vertex2 = self._vertices[m + 1]
                vertex3 = self._vertices[m + 2]
                if DirectedEdge(vertex2, vertex3).left_of(point):
                    return False
                elif DirectedEdge(vertex1, vertex2).left_of(point):
                    max_triangle = m
                elif DirectedEdge(vertex3, vertex1).left_of(point):
                    min_triangle = m + 1
                else:
                    return True
            return False
        return False

    def is_polygon_inside(self, polygon):
        """

        Parameters
        ----------
        polygon : ConvexPolygon

        Returns
        -------
        bool
            True if all the points of polygon are inside. False otherwise.

        """
        which_is_inside, _ = ConvexPolygon._intersection(self, polygon)
        return which_is_inside == ConvexPolygon.InsideFlag.POLYGON2 or which_is_inside == ConvexPolygon.InsideFlag.BOTH

    @staticmethod
    def draw(polygons, image):
        """Draw all the polygons in the image

        Parameters
        ----------
        polygons : list[ConvexPolygon]
        image : Image

        Returns
        -------
        None

        """
        bounding_box = ConvexPolygon.bounding_box(polygons)
        draw = ImageDraw.Draw(image)
        if bounding_box.num_vertices == 1:  # the polygon with more vertices is a monogon, and all the monogon are equal
            for polygon in reversed(polygons):  # only the last monogon will be visible
                if polygon.num_vertices == 1:
                    color = polygon.color
                    xy = [(1, 1), (image.width - 2, image.height - 2)]
                    draw.rectangle(xy, fill=color, outline=color)
                    break
        elif bounding_box.num_vertices >= 2:    # 2 or 4 vertices
            width = image.width - 3
            height = image.height - 3
            min_point = min(bounding_box._vertices)
            max_point = max(bounding_box._vertices)
            width_bb = max_point.x - min_point.x
            height_bb = max_point.y - min_point.y
            if bounding_box.num_vertices == 2:
                if width_bb == 0.0:
                    width_bb = height_bb
                else:   # height_bb == 0.0:
                    height_bb = width_bb
            scale = min(height / height_bb, width / width_bb)
            for polygon in polygons:
                xy = []
                translation = (polygon.centroid - bounding_box._vertices[0]) * scale
                for vertex in polygon._vertices:
                    point = (vertex - polygon.centroid) * scale + translation
                    xy.append((point.x + 1, height - point.y + 1))
                if len(xy) == 1:
                    draw.point(xy, fill=polygon.color)
                elif len(xy) > 1:
                    draw.polygon(xy, outline=polygon.color)

    @staticmethod
    def convex_union(polygon1, polygon2):
        """

        Parameters
        ----------
        polygon1 : ConvexPolygon
        polygon2 : ConvexPolygon

        Returns
        -------
        ConvexPolygon
            The smallest convex polygon that contains both polygons.

        """
        points = polygon1._vertices + polygon2._vertices
        return ConvexPolygon(points)

    @staticmethod
    def intersection(polygon1, polygon2):
        """

        Parameters
        ----------
        polygon1 : ConvexPolygon
        polygon2 : ConvexPolygon

        Returns
        -------
        ConvexPolygon
            The intersection of the two convex polygon.

        """
        _, intersection = ConvexPolygon._intersection(polygon1, polygon2)
        return intersection

    @staticmethod
    def bounding_box(polygons):
        """

        Parameters
        ----------
        polygons : list of ConvexPolygon

        Returns
        -------
        ConvexPolygon
            The smallest axis-aligned box within which all the polygons lie.

        """
        max_x = None
        min_x = None
        max_y = None
        min_y = None
        for polygon in polygons:
            for vertex in polygon._vertices:
                if max_x is None or vertex.x > max_x:
                    max_x = vertex.x
                if min_x is None or vertex.x < min_x:
                    min_x = vertex.x
                if max_y is None or vertex.y > max_y:
                    max_y = vertex.y
                if min_y is None or vertex.y < min_y:
                    min_y = vertex.y
        if max_x is None:
            return ConvexPolygon([])
        return ConvexPolygon([Vector(max_x, min_y), Vector(max_x, max_y), Vector(min_x, max_y), Vector(min_x, min_y)])

    @staticmethod
    def _compute_convex_hull(points):
        """

        Parameters
        ----------
        points : list[Vector]

        Returns
        -------
        list[Vector]
            The smallest convex set of Point that contains points

        """
        convex_hull = points
        if len(points) >= 2:
            left_most_point = min(points)
            sorted_points = ConvexPolygon._sort_points_by_angle_distance(points, left_most_point)
            convex_hull = ConvexPolygon._graham_scan(sorted_points)
        return convex_hull

    @staticmethod
    def _sort_points_by_angle_distance(points, reference_point):
        def calculate_angle_distance(point):
            vector = point - reference_point
            return vector.angle(), vector.square_length()

        angle_distance = list(map(calculate_angle_distance, points))
        mig = list(zip(angle_distance, points))
        s_mig = sorted(mig)
        sorted_points = list(map(lambda x: x[1], s_mig))
        return ConvexPolygon._remove_duplicated_points(sorted_points)

    @staticmethod
    def _remove_duplicated_points(points):
        without_duplicates = []
        if len(points) >= 1:
            without_duplicates.append(points[0])
            old_point = points[0]
            for i in range(1, len(points)):
                if points[i] != old_point:
                    without_duplicates.append(points[i])
                    old_point = points[i]
        return without_duplicates

    @staticmethod
    def _graham_scan(points):
        convex_hull = points[:2]
        m = len(convex_hull)
        for k in range(2, len(points)):
            while m >= 2 and not DirectedEdge(convex_hull[m - 2], convex_hull[m - 1]).right_of(points[k]):
                convex_hull.pop()
                m = m - 1
            convex_hull.append(points[k])
            m = m + 1
        return convex_hull

    @staticmethod
    def _compute_perimeter(vertices):
        perimeter = 0.0
        n = len(vertices)
        if n >= 2:
            for i in range(1, n):
                perimeter += (vertices[i - 1] - vertices[i]).length()
            if n >= 3:
                perimeter += (vertices[0] - vertices[n - 1]).length()
        return perimeter

    @staticmethod
    def _compute_area(vertices):
        area = 0.0
        n = len(vertices)
        if n >= 3:
            v1 = vertices[0]
            for i in range(2, n):
                v2 = vertices[i - 1]
                v3 = vertices[i]
                area += abs(Vector.cross(v2 - v1, v3 - v1)) / 2.0
        return area

    @staticmethod
    def _compute_centroid(vertices):
        centroid = Vector()
        n = len(vertices)
        if n >= 1:
            for vertex in vertices:
                centroid += vertex
            centroid /= n
        return centroid

    @staticmethod
    def _check_regularity(vertices):
        regular = True
        n = len(vertices)
        if n >= 3:
            len_first_edge = (vertices[0] - vertices[1]).square_length()
            i = 2
            while i < n and regular:
                len_current_edge = (vertices[i] - vertices[i - 1]).square_length()
                regular = math.isclose(len_first_edge, len_current_edge, rel_tol=ConvexPolygon.PRECISION)
                i += 1
        return regular

    @staticmethod
    def _intersection_with_special_cases(polygon1, polygon2):
        """

        Parameters
        ----------
        polygon1 : ConvexPolygon
        polygon2 : ConvexPolygon

        Returns
        -------
        (ConvexPolygon.InsideFlag, ConvexPolygon)

        """
        intersection = ConvexPolygon([])
        inside_flag = ConvexPolygon.InsideFlag.UNKNOWN
        if polygon1.num_vertices != 0 and polygon2.num_vertices != 0:
            if polygon1.num_vertices < polygon2.num_vertices:
                for vertex in polygon1._vertices:
                    if polygon2.is_point_inside(vertex):
                        intersection._vertices.append(vertex)
                if intersection.num_vertices == polygon1.num_vertices:
                    inside_flag = ConvexPolygon.InsideFlag.POLYGON1
            else:
                for vertex in polygon2._vertices:
                    if polygon1.is_point_inside(vertex):
                        intersection._vertices.append(vertex)
                if intersection.num_vertices == polygon1.num_vertices == polygon2.num_vertices:
                    inside_flag = ConvexPolygon.InsideFlag.BOTH
                elif intersection.num_vertices == polygon2.num_vertices:
                    inside_flag = ConvexPolygon.InsideFlag.POLYGON2
        return inside_flag, intersection

    @staticmethod
    def _intersection(polygon1, polygon2):
        """

        Parameters
        ----------
        polygon1 : ConvexPolygon
        polygon2 : ConvexPolygon

        Returns
        -------
        (ConvexPolygon.InsideFlag, ConvexPolygon)

        """
        n, m = polygon1.num_vertices, polygon2.num_vertices
        if n < 3 or m < 3:
            return ConvexPolygon._intersection_with_special_cases(polygon1, polygon2)

        inside_flag = ConvexPolygon.InsideFlag.UNKNOWN
        vertices = []
        p1_always_inside = p2_always_inside = True
        aa = ba = 0
        i = j = 0
        while ((aa < n) or (ba < m)) and (aa < 2 * n) and (ba < 2 * m):
            edge_a = DirectedEdge(polygon1._vertices[(i + n - 1) % n], polygon1._vertices[i % n])
            edge_b = DirectedEdge(polygon2._vertices[(j + m - 1) % m], polygon2._vertices[j % m])
            cross = DirectedEdge.cross(edge_a, edge_b)
            a_position = edge_b.relative_position(edge_a.terminal_point)
            b_position = edge_a.relative_position(edge_b.terminal_point)
            p1_always_inside = p1_always_inside and a_position != DirectedEdge.RelativePosition.LEFT_OF
            p2_always_inside = p2_always_inside and b_position != DirectedEdge.RelativePosition.LEFT_OF
            code, intersection = DirectedEdge.intersect(edge_a, edge_b)
            if code == DirectedEdge.IntersectionType.POINT:
                if inside_flag == ConvexPolygon.InsideFlag.UNKNOWN and not vertices:
                    aa = ba = 0
                    ConvexPolygon._add_intersection(vertices, intersection[0])
                inside_flag = ConvexPolygon._in_out(vertices, intersection[0], inside_flag, a_position, b_position)

            # Special case: overlap and oppositely oriented
            if code == DirectedEdge.IntersectionType.OVERLAP and DirectedEdge.dot(edge_a, edge_b) < 0:
                return inside_flag, ConvexPolygon(intersection)
            # Special case: parallel and separated, polygons are disjoint
            if cross == 0 and a_position == b_position == DirectedEdge.RelativePosition.LEFT_OF:
                return inside_flag, ConvexPolygon([])
            # Special case: collinear
            elif cross == 0 and a_position == b_position == DirectedEdge.RelativePosition.COLLINEAR:
                if inside_flag == ConvexPolygon.InsideFlag.POLYGON1:
                    j, ba = ConvexPolygon._advance(j, ba, inside_flag == ConvexPolygon.InsideFlag.POLYGON2, vertices, edge_b)
                else:
                    i, aa = ConvexPolygon._advance(i, aa, inside_flag == ConvexPolygon.InsideFlag.POLYGON1, vertices, edge_a)
            # Generic cases
            elif cross >= 0:
                if a_position == DirectedEdge.RelativePosition.RIGHT_OF:
                    j, ba = ConvexPolygon._advance(j, ba, inside_flag == ConvexPolygon.InsideFlag.POLYGON2, vertices, edge_b)
                else:
                    i, aa = ConvexPolygon._advance(i, aa, inside_flag == ConvexPolygon.InsideFlag.POLYGON1, vertices, edge_a)
            else:
                if b_position == DirectedEdge.RelativePosition.RIGHT_OF:
                    i, aa = ConvexPolygon._advance(i, aa, inside_flag == ConvexPolygon.InsideFlag.POLYGON1, vertices, edge_a)
                else:
                    j, ba = ConvexPolygon._advance(j, ba, inside_flag == ConvexPolygon.InsideFlag.POLYGON2, vertices, edge_b)

        vertices = ConvexPolygon._start_with_leftmost_vertex(vertices)
        # The boundaries of polygon1 and polygon2 do not cross. One is inside of the other or are disjoint
        if inside_flag == ConvexPolygon.InsideFlag.UNKNOWN:
            if p1_always_inside:
                vertices = polygon1._vertices.copy()
            elif p2_always_inside:
                vertices = polygon2._vertices.copy()
        if p1_always_inside and p2_always_inside:
            inside_flag = ConvexPolygon.InsideFlag.BOTH
        elif p1_always_inside:
            inside_flag = ConvexPolygon.InsideFlag.POLYGON1
        elif p2_always_inside:
            inside_flag = ConvexPolygon.InsideFlag.POLYGON2
        else:
            inside_flag = ConvexPolygon.InsideFlag.UNKNOWN
        new_polygon = ConvexPolygon([])
        new_polygon._vertices = vertices
        return inside_flag, new_polygon

    @staticmethod
    def _start_with_leftmost_vertex(vertices):
        if vertices:
            index_min = vertices.index(min(vertices))
            vertices = vertices[index_min:] + vertices[:index_min]
        return vertices

    @staticmethod
    def _add_intersection(intersection, point):
        if not intersection:
            intersection.append(point)
        elif intersection[0] != point and intersection[-1] != point:
            intersection.append(point)

    @staticmethod
    def _in_out(intersection, point, inside_flag, a_position, b_position):
        ConvexPolygon._add_intersection(intersection, point)
        if a_position == DirectedEdge.RelativePosition.RIGHT_OF:
            return ConvexPolygon.InsideFlag.POLYGON1
        if b_position == DirectedEdge.RelativePosition.RIGHT_OF:
            return ConvexPolygon.InsideFlag.POLYGON2
        return inside_flag

    @staticmethod
    def _advance(index, counter, inside, intersection, edge):
        if inside:
            ConvexPolygon._add_intersection(intersection, edge.terminal_point)
        return (index + 1), (counter + 1)
