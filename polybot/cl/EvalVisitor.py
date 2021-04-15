if __name__ is not None and "." in __name__:
    from .LanguageParser import LanguageParser
    from .LanguageVisitor import LanguageVisitor
else:
    from LanguageParser import LanguageParser
    from LanguageVisitor import LanguageVisitor

from polybot.polygons import *
from PIL import Image
from random import uniform


class EvalVisitor(LanguageVisitor):

    IMAGE_MODE = 'RGB'
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 400
    WHITE = (255, 255, 255)

    def __init__(self, variables=None):
        if variables is None:
            variables = {}
        self.variables = variables

    def visitRoot(self, ctx: LanguageParser.RootContext):
        outputs = []
        images_filenames = []
        for child in ctx.getChildren():
            value = self.visit(child)
            if isinstance(value, str):
                if value.endswith('.png'):
                    images_filenames.append(value)
                else:
                    outputs.append(value)
        return '\n'.join(outputs), images_filenames

    def visitAssign(self, ctx: LanguageParser.AssignContext):
        polygon_id = ctx.getChild(0).getText()
        polygon = self.visit(ctx.getChild(2))
        self.variables[polygon_id] = polygon

    def visitPrint_string(self, ctx: LanguageParser.Print_stringContext):
        text = ctx.getChild(1).getText()
        return text[1:-1]

    def visitPrint_expression(self, ctx: LanguageParser.Print_expressionContext):
        polygon = self.visit(ctx.getChild(1))
        return str(polygon)

    def visitArea(self, ctx: LanguageParser.AreaContext):
        polygon = self.visit(ctx.getChild(1))
        return '{:.3f}'.format(polygon.area)

    def visitPerimeter(self, ctx: LanguageParser.PerimeterContext):
        polygon = self.visit(ctx.getChild(1))
        return '{:.3f}'.format(polygon.perimeter)

    def visitVertices(self, ctx: LanguageParser.VerticesContext):
        polygon = self.visit(ctx.getChild(1))
        return str(polygon.num_vertices)

    def visitCentroid(self, ctx: LanguageParser.CentroidContext):
        polygon = self.visit(ctx.getChild(1))
        return str(polygon.centroid)

    def visitColor(self, ctx: LanguageParser.ColorContext):
        polygon = self.visit(ctx.getChild(1))
        r = int(float(ctx.getChild(4).getText()) * 255)
        g = int(float(ctx.getChild(5).getText()) * 255)
        b = int(float(ctx.getChild(6).getText()) * 255)
        polygon.color = (r, g, b)

    def visitInside(self, ctx: LanguageParser.InsideContext):
        polygon1 = self.visit(ctx.getChild(1))
        polygon2 = self.visit(ctx.getChild(3))
        if polygon2.is_polygon_inside(polygon1):
            return 'yes'
        else:
            return 'no'

    def visitEqual(self, ctx: LanguageParser.EqualContext):
        polygon1 = self.visit(ctx.getChild(1))
        polygon2 = self.visit(ctx.getChild(3))
        if polygon1 == polygon2:
            return 'yes'
        else:
            return 'no'

    def visitDraw(self, ctx: LanguageParser.DrawContext):
        filename = ctx.getChild(1).getText()[1:-1]
        polygons = [self.visit(ctx.getChild(i)) for i in range(3, ctx.getChildCount(), 2)]
        image = Image.new(self.IMAGE_MODE, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), self.WHITE)
        ConvexPolygon.draw(polygons, image)
        image.save(filename)
        return filename

    def visitExpression(self, ctx: LanguageParser.Expression1Context):
        if ctx.getChildCount() == 3:
            polygon1 = self.visit(ctx.getChild(0))
            polygon2 = self.visit(ctx.getChild(2))
            return ConvexPolygon.convex_union(polygon1, polygon2)
        else:
            return self.visit(ctx.getChild(0))

    def visitExpression1(self, ctx: LanguageParser.Expression2Context):
        if ctx.getChildCount() == 3:
            polygon1 = self.visit(ctx.getChild(0))
            polygon2 = self.visit(ctx.getChild(2))
            return ConvexPolygon.intersection(polygon1, polygon2)
        else:
            return self.visit(ctx.getChild(0))

    def visitExpression2(self, ctx: LanguageParser.Expression3Context):
        if ctx.getChildCount() == 2:
            polygon = self.visit(ctx.getChild(1))
            return ConvexPolygon.bounding_box([polygon])
        elif ctx.getChildCount() == 3:
            return self.visit(ctx.getChild(1))
        else:
            return self.visit(ctx.getChild(0))

    def visitExpression3(self, ctx: LanguageParser.Expression3Context):
        if ctx.getChildCount() == 2:
            num_points = int(ctx.getChild(1).getText())
            xs = [uniform(0.0, 1.0) for _ in range(num_points)]
            ys = [uniform(0.0, 1.0) for _ in range(num_points)]
            points = [Vector(x, y) for (x, y) in zip(xs, ys)]
            return ConvexPolygon(points)
        else:
            return self.visit(ctx.getChild(0))

    def visitPolygon_id(self, ctx: LanguageParser.Polygon_idContext):
        polygon_id = ctx.getChild(0).getText()
        return self.variables.get(polygon_id)

    def visitPoint_list(self, ctx: LanguageParser.Point_listContext):
        point_list = []
        for i in range(1, ctx.getChildCount() - 1, 2):
            x = float(ctx.getChild(i).getText())
            y = float(ctx.getChild(i + 1).getText())
            point_list.append(Vector(x, y))
        return ConvexPolygon(point_list)
