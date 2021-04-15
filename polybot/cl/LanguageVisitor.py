# Generated from Language.g by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LanguageParser import LanguageParser
else:
    from LanguageParser import LanguageParser

# This class defines a complete generic visitor for a parse tree produced by LanguageParser.

class LanguageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LanguageParser#root.
    def visitRoot(self, ctx:LanguageParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#command.
    def visitCommand(self, ctx:LanguageParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#assign.
    def visitAssign(self, ctx:LanguageParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#write.
    def visitWrite(self, ctx:LanguageParser.WriteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#print_string.
    def visitPrint_string(self, ctx:LanguageParser.Print_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#print_expression.
    def visitPrint_expression(self, ctx:LanguageParser.Print_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#area.
    def visitArea(self, ctx:LanguageParser.AreaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#perimeter.
    def visitPerimeter(self, ctx:LanguageParser.PerimeterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#vertices.
    def visitVertices(self, ctx:LanguageParser.VerticesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#centroid.
    def visitCentroid(self, ctx:LanguageParser.CentroidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#color.
    def visitColor(self, ctx:LanguageParser.ColorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#inside.
    def visitInside(self, ctx:LanguageParser.InsideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#equal.
    def visitEqual(self, ctx:LanguageParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#draw.
    def visitDraw(self, ctx:LanguageParser.DrawContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#expression.
    def visitExpression(self, ctx:LanguageParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#expression1.
    def visitExpression1(self, ctx:LanguageParser.Expression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#expression2.
    def visitExpression2(self, ctx:LanguageParser.Expression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#expression3.
    def visitExpression3(self, ctx:LanguageParser.Expression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#polygon_id.
    def visitPolygon_id(self, ctx:LanguageParser.Polygon_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LanguageParser#point_list.
    def visitPoint_list(self, ctx:LanguageParser.Point_listContext):
        return self.visitChildren(ctx)



del LanguageParser