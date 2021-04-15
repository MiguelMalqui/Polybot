from enum import Enum
from .Vector import Vector


class DirectedEdge:
    """A class to represent directed edges in 2D."""

    class RelativePosition(Enum):
        RIGHT_OF = -1
        COLLINEAR = 0
        LEFT_OF = 1

    class IntersectionType(Enum):
        NONE = 0
        OVERLAP = 1
        POINT = 2

    def __init__(self, initial_point, terminal_point):
        """

        Parameters
        ----------
        initial_point : Vector
            The initial point of the directed edge.
        terminal_point : Vector
            The terminal point of the directed edge.

        """
        self._initial_point = initial_point
        self._terminal_point = terminal_point

    def __repr__(self):
        return 'DirectedEdge({} -> {})'.format(self._initial_point, self._terminal_point)

    def length(self):
        """

        Returns
        -------
        float
            Euclidean distance between the two points of the vector.

        """
        return (self._terminal_point - self._initial_point).length()

    @property
    def initial_point(self):
        """Vector: The initial point of the directed edge."""
        return self._initial_point

    @property
    def terminal_point(self):
        """Vector: The terminal point of the directed edge."""
        return self._terminal_point

    def square_length(self):
        """

        Returns
        -------
        float
            Euclidean squared distance between the two points of the vector.

        """
        return (self._terminal_point - self._initial_point).square_length()

    def left_of(self, other):
        """

        Parameters
        ----------
        other : Vector

        Returns
        -------
        bool
            True if other is at the left of self, False otherwise.

        """
        vector1 = self._terminal_point - self._initial_point
        vector2 = other - self._initial_point
        cross = Vector.cross(vector1, vector2)
        return cross > 0.0

    def right_of(self, other):
        """

        Parameters
        ----------
        other : Vector

        Returns
        -------
        bool
            True if other is at right of self, False otherwise.

        """
        vector1 = self._terminal_point - self._initial_point
        vector2 = other - self._initial_point
        cross = Vector.cross(vector1, vector2)
        return cross < 0.0

    def collinear(self, other):
        """

        Parameters
        ----------
        other : Vector

        Returns
        -------
        bool
            True if other is at the same line as self, False otherwise.

        """
        vector1 = self._terminal_point - self._initial_point
        vector2 = other - self._initial_point
        cross = Vector.cross(vector1, vector2)
        return cross == 0.0

    def relative_position(self, point):
        """

        Parameters
        ----------
        point : Vector

        Returns
        -------
        DirectedEdge.RelativePosition

        """
        cross = Vector.cross(self._terminal_point - self._initial_point, point - self._initial_point)
        if cross > 0.0:
            return DirectedEdge.RelativePosition.LEFT_OF
        if cross < 0.0:
            return DirectedEdge.RelativePosition.RIGHT_OF
        return DirectedEdge.RelativePosition.COLLINEAR

    @staticmethod
    def intersect(edge1, edge2):
        """

        Parameters
        ----------
        edge1 : DirectedEdge
        edge2 : DirectedEdge

        Returns
        -------
        (DirectedEdge.IntersectionType, list[Vector])
            The intersection type and intersection of the two directed edges.

        """
        r = edge1._terminal_point - edge1._initial_point
        s = edge2._terminal_point - edge2._initial_point
        r_cross_s = Vector.cross(r, s)
        qp = edge2._initial_point - edge1._initial_point
        qp_cross_r = Vector.cross(qp, r)
        code = DirectedEdge.IntersectionType.NONE
        intersection = []
        if r_cross_s == 0:
            if qp_cross_r == 0:
                # express edge2 points in function of the first point of edge1
                r2 = Vector.dot(r, r)
                t0 = Vector.dot(qp, r) / r2
                t1 = t0 + Vector.dot(s, r) / r2
                if 0.0 <= t0 <= 1.0 and 0.0 <= t1 <= 1.0:
                    intersection = [(edge1._initial_point + t0 * r), (edge1._initial_point + t1 * r)]
                elif 0.0 <= t0 <= 1.0 and not 0.0 <= t1 <= 1.0:
                    intersection.append(edge1._initial_point + t0 * r)
                    if t1 > 1.0 and t0 < 1.0:
                        intersection.append(edge1._terminal_point)
                    elif t1 < 0.0 and t0 > 0.0:
                        intersection.insert(0, edge1._initial_point)
                elif not 0.0 <= t0 <= 1.0 and 0.0 <= t1 <= 1.0:
                    intersection.append(edge1._initial_point + t1 * r)
                    if t0 > 1.0 and t1 < 1.0:
                        intersection.append(edge1._terminal_point)
                    elif t0 < 0.0 and t1 > 0.0:
                        intersection.insert(0, edge1._initial_point)
                if intersection:
                    code = DirectedEdge.IntersectionType.OVERLAP
        else:
            qp_cross_s = Vector.cross(qp, s)
            t = qp_cross_s / r_cross_s
            u = qp_cross_r / r_cross_s
            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
                code = DirectedEdge.IntersectionType.POINT
                intersection.append(edge1._initial_point + t * r)
        return code, intersection

    @staticmethod
    def cross(edge1, edge2):
        """

        Parameters
        ----------
        edge1 : DirectedEdge
        edge2 : DirectedEdge

        Returns
        -------
        float
            Cross product of two directed edges.

        """
        vector1 = edge1._terminal_point - edge1._initial_point
        vector2 = edge2._terminal_point - edge2._initial_point
        return Vector.cross(vector1, vector2)

    @staticmethod
    def dot(edge1, edge2):
        """

        Parameters
        ----------
        edge1 : DirectedEdge
        edge2 : DirectedEdge

        Returns
        -------
        float
            Dot product of two directed edges

        """
        vector1 = edge1._terminal_point - edge1._initial_point
        vector2 = edge2._terminal_point - edge2._initial_point
        return Vector.dot(vector1, vector2)
