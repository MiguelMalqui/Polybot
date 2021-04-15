import math


class Vector:
    """A class used to represent 2D vectors."""

    PRECISION = 1e-6

    def __init__(self, x=0.0, y=0.0):
        """

        Parameters
        ----------
        x : float
            The x component. Default to 0.0.
        y : float
            The y component. Default to 0.0.

        """
        self._x = x
        self._y = y

    def __eq__(self, other):
        """

        Parameters
        ----------
        other : Vector

        Returns
        -------
        bool
            True if their x and y components are equal with six digits of precision, False otherwise.

        """
        return \
            math.isclose(self._x, other._x, rel_tol=Vector.PRECISION) and \
            math.isclose(self._y, other._y, rel_tol=Vector.PRECISION)

    def __lt__(self, other):
        """

        Parameters
        ----------
        other : Vector

        Returns
        -------
        bool
            True if its x component is lower than the other's x component
            or in case of tie, if its y component is lower than the other's y component,
            False otherwise.

        """
        if self._x == other.x:
            return self._y < other.y
        return self._x < other.x

    def __gt__(self, other):
        """

        Parameters
        ----------
        other : Vector

        Returns
        -------
        bool
            True if its x component is greater than the other's x component
            or in case of tie, if its y component is greater than the other's y component,
            False otherwise.

        """
        if self._x == other.x:
            return self._y > other.y
        return self._x > other.x

    def __add__(self, other):
        """

        Parameters
        ----------
        other : Vector

        Returns
        -------
        Vector
            A new vector with the addition of the components of the two vectors.

        """
        x = self._x + other.x
        y = self._y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        """

        Parameters
        ----------
        other : Vector

        Returns
        -------
        Vector
            A new vector with the subtraction of the components of the two vectors.

        """
        x = self._x - other.x
        y = self._y - other.y
        return Vector(x, y)

    def __truediv__(self, other):
        """

        Parameters
        ----------
        other : float

        Returns
        -------
        Vector
            A new vector with the components divided by other.

        """
        x = self._x / other
        y = self._y / other
        return Vector(x, y)

    def __mul__(self, other):
        """

        Parameters
        ----------
        other : float

        Returns
        -------
        Vector
            A new vector with the components multiplied by other.

        """
        x = self._x * other
        y = self._y * other
        return Vector(x, y)

    def __rmul__(self, other):
        """

        Parameters
        ----------
        other : float

        Returns
        -------
        Vector
            A new vector with the components multiplied by other.

        """
        x = self._x * other
        y = self._y * other
        return Vector(x, y)

    def __str__(self):
        return '{:.3f} {:.3f}'.format(self._x, self._y)

    def __repr__(self):
        return 'Vector({}, {})'.format(self._x, self._y)

    @property
    def x(self):
        """float: The x component of the vector."""
        return self._x

    @property
    def y(self):
        """float: The y component of the vector."""
        return self._y

    def length(self):
        """

        Returns
        -------
        float
            Euclidean norm of the vector.

        """
        return math.sqrt(self._x ** 2 + self._y ** 2)

    def square_length(self):
        """

        Returns
        -------
        float
            Euclidean squared norm of the vector.

        """
        return self._x ** 2 + self._y ** 2

    def angle(self):
        """

        Returns
        -------
        float
            Angle that the vector forms with the y-axis, in radians. The result is between 0 and 2*pi.

        """
        angle = math.atan2(self._x, self._y)
        if angle < 0:
            angle = 2 * math.pi + angle
        return angle

    @staticmethod
    def cross(vector1, vector2):
        """

        Parameters
        ----------
        vector1 : Vector
        vector2 : Vector

        Returns
        -------
        float
            The cross product of the two vectors

        """
        return vector1._x * vector2.y - vector1._y * vector2.x

    @staticmethod
    def dot(vector1, vector2):
        """

        Parameters
        ----------
        vector1 : Vector
        vector2 : Vector

        Returns
        -------
        float
            Dot product of the two vectors.

        """
        return vector1._x * vector2.x + vector1._y * vector2.y
