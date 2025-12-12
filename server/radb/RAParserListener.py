# Generated from RAParser.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .RAParser import RAParser
else:
    from RAParser import RAParser

# This class defines a complete listener for a parse tree produced by RAParser.
class RAParserListener(ParseTreeListener):

    # Enter a parse tree produced by RAParser#numberLiteralValExpr.
    def enterNumberLiteralValExpr(self, ctx:RAParser.NumberLiteralValExprContext):
        pass

    # Exit a parse tree produced by RAParser#numberLiteralValExpr.
    def exitNumberLiteralValExpr(self, ctx:RAParser.NumberLiteralValExprContext):
        pass


    # Enter a parse tree produced by RAParser#textValExpr.
    def enterTextValExpr(self, ctx:RAParser.TextValExprContext):
        pass

    # Exit a parse tree produced by RAParser#textValExpr.
    def exitTextValExpr(self, ctx:RAParser.TextValExprContext):
        pass


    # Enter a parse tree produced by RAParser#isNotNullExpr.
    def enterIsNotNullExpr(self, ctx:RAParser.IsNotNullExprContext):
        pass

    # Exit a parse tree produced by RAParser#isNotNullExpr.
    def exitIsNotNullExpr(self, ctx:RAParser.IsNotNullExprContext):
        pass


    # Enter a parse tree produced by RAParser#funcExpr.
    def enterFuncExpr(self, ctx:RAParser.FuncExprContext):
        pass

    # Exit a parse tree produced by RAParser#funcExpr.
    def exitFuncExpr(self, ctx:RAParser.FuncExprContext):
        pass


    # Enter a parse tree produced by RAParser#attrRef.
    def enterAttrRef(self, ctx:RAParser.AttrRefContext):
        pass

    # Exit a parse tree produced by RAParser#attrRef.
    def exitAttrRef(self, ctx:RAParser.AttrRefContext):
        pass


    # Enter a parse tree produced by RAParser#plusMinusExpr.
    def enterPlusMinusExpr(self, ctx:RAParser.PlusMinusExprContext):
        pass

    # Exit a parse tree produced by RAParser#plusMinusExpr.
    def exitPlusMinusExpr(self, ctx:RAParser.PlusMinusExprContext):
        pass


    # Enter a parse tree produced by RAParser#orExpr.
    def enterOrExpr(self, ctx:RAParser.OrExprContext):
        pass

    # Exit a parse tree produced by RAParser#orExpr.
    def exitOrExpr(self, ctx:RAParser.OrExprContext):
        pass


    # Enter a parse tree produced by RAParser#valExprBraced.
    def enterValExprBraced(self, ctx:RAParser.ValExprBracedContext):
        pass

    # Exit a parse tree produced by RAParser#valExprBraced.
    def exitValExprBraced(self, ctx:RAParser.ValExprBracedContext):
        pass


    # Enter a parse tree produced by RAParser#valExprParenthesized.
    def enterValExprParenthesized(self, ctx:RAParser.ValExprParenthesizedContext):
        pass

    # Exit a parse tree produced by RAParser#valExprParenthesized.
    def exitValExprParenthesized(self, ctx:RAParser.ValExprParenthesizedContext):
        pass


    # Enter a parse tree produced by RAParser#concatExpr.
    def enterConcatExpr(self, ctx:RAParser.ConcatExprContext):
        pass

    # Exit a parse tree produced by RAParser#concatExpr.
    def exitConcatExpr(self, ctx:RAParser.ConcatExprContext):
        pass


    # Enter a parse tree produced by RAParser#notExpr.
    def enterNotExpr(self, ctx:RAParser.NotExprContext):
        pass

    # Exit a parse tree produced by RAParser#notExpr.
    def exitNotExpr(self, ctx:RAParser.NotExprContext):
        pass


    # Enter a parse tree produced by RAParser#isNullExpr.
    def enterIsNullExpr(self, ctx:RAParser.IsNullExprContext):
        pass

    # Exit a parse tree produced by RAParser#isNullExpr.
    def exitIsNullExpr(self, ctx:RAParser.IsNullExprContext):
        pass


    # Enter a parse tree produced by RAParser#stringLiteralValExpr.
    def enterStringLiteralValExpr(self, ctx:RAParser.StringLiteralValExprContext):
        pass

    # Exit a parse tree produced by RAParser#stringLiteralValExpr.
    def exitStringLiteralValExpr(self, ctx:RAParser.StringLiteralValExprContext):
        pass


    # Enter a parse tree produced by RAParser#likeExpr.
    def enterLikeExpr(self, ctx:RAParser.LikeExprContext):
        pass

    # Exit a parse tree produced by RAParser#likeExpr.
    def exitLikeExpr(self, ctx:RAParser.LikeExprContext):
        pass


    # Enter a parse tree produced by RAParser#multDivExpr.
    def enterMultDivExpr(self, ctx:RAParser.MultDivExprContext):
        pass

    # Exit a parse tree produced by RAParser#multDivExpr.
    def exitMultDivExpr(self, ctx:RAParser.MultDivExprContext):
        pass


    # Enter a parse tree produced by RAParser#compareExpr.
    def enterCompareExpr(self, ctx:RAParser.CompareExprContext):
        pass

    # Exit a parse tree produced by RAParser#compareExpr.
    def exitCompareExpr(self, ctx:RAParser.CompareExprContext):
        pass


    # Enter a parse tree produced by RAParser#andExpr.
    def enterAndExpr(self, ctx:RAParser.AndExprContext):
        pass

    # Exit a parse tree produced by RAParser#andExpr.
    def exitAndExpr(self, ctx:RAParser.AndExprContext):
        pass


    # Enter a parse tree produced by RAParser#listOfValExprs.
    def enterListOfValExprs(self, ctx:RAParser.ListOfValExprsContext):
        pass

    # Exit a parse tree produced by RAParser#listOfValExprs.
    def exitListOfValExprs(self, ctx:RAParser.ListOfValExprsContext):
        pass


    # Enter a parse tree produced by RAParser#listOfIDs.
    def enterListOfIDs(self, ctx:RAParser.ListOfIDsContext):
        pass

    # Exit a parse tree produced by RAParser#listOfIDs.
    def exitListOfIDs(self, ctx:RAParser.ListOfIDsContext):
        pass


    # Enter a parse tree produced by RAParser#intersectExpr.
    def enterIntersectExpr(self, ctx:RAParser.IntersectExprContext):
        pass

    # Exit a parse tree produced by RAParser#intersectExpr.
    def exitIntersectExpr(self, ctx:RAParser.IntersectExprContext):
        pass


    # Enter a parse tree produced by RAParser#textRelExpr.
    def enterTextRelExpr(self, ctx:RAParser.TextRelExprContext):
        pass

    # Exit a parse tree produced by RAParser#textRelExpr.
    def exitTextRelExpr(self, ctx:RAParser.TextRelExprContext):
        pass


    # Enter a parse tree produced by RAParser#relExprParenthesized.
    def enterRelExprParenthesized(self, ctx:RAParser.RelExprParenthesizedContext):
        pass

    # Exit a parse tree produced by RAParser#relExprParenthesized.
    def exitRelExprParenthesized(self, ctx:RAParser.RelExprParenthesizedContext):
        pass


    # Enter a parse tree produced by RAParser#diffExpr.
    def enterDiffExpr(self, ctx:RAParser.DiffExprContext):
        pass

    # Exit a parse tree produced by RAParser#diffExpr.
    def exitDiffExpr(self, ctx:RAParser.DiffExprContext):
        pass


    # Enter a parse tree produced by RAParser#unionExpr.
    def enterUnionExpr(self, ctx:RAParser.UnionExprContext):
        pass

    # Exit a parse tree produced by RAParser#unionExpr.
    def exitUnionExpr(self, ctx:RAParser.UnionExprContext):
        pass


    # Enter a parse tree produced by RAParser#relRef.
    def enterRelRef(self, ctx:RAParser.RelRefContext):
        pass

    # Exit a parse tree produced by RAParser#relRef.
    def exitRelRef(self, ctx:RAParser.RelRefContext):
        pass


    # Enter a parse tree produced by RAParser#renameExpr.
    def enterRenameExpr(self, ctx:RAParser.RenameExprContext):
        pass

    # Exit a parse tree produced by RAParser#renameExpr.
    def exitRenameExpr(self, ctx:RAParser.RenameExprContext):
        pass


    # Enter a parse tree produced by RAParser#joinExpr.
    def enterJoinExpr(self, ctx:RAParser.JoinExprContext):
        pass

    # Exit a parse tree produced by RAParser#joinExpr.
    def exitJoinExpr(self, ctx:RAParser.JoinExprContext):
        pass


    # Enter a parse tree produced by RAParser#selectExpr.
    def enterSelectExpr(self, ctx:RAParser.SelectExprContext):
        pass

    # Exit a parse tree produced by RAParser#selectExpr.
    def exitSelectExpr(self, ctx:RAParser.SelectExprContext):
        pass


    # Enter a parse tree produced by RAParser#crossExpr.
    def enterCrossExpr(self, ctx:RAParser.CrossExprContext):
        pass

    # Exit a parse tree produced by RAParser#crossExpr.
    def exitCrossExpr(self, ctx:RAParser.CrossExprContext):
        pass


    # Enter a parse tree produced by RAParser#relExprBraced.
    def enterRelExprBraced(self, ctx:RAParser.RelExprBracedContext):
        pass

    # Exit a parse tree produced by RAParser#relExprBraced.
    def exitRelExprBraced(self, ctx:RAParser.RelExprBracedContext):
        pass


    # Enter a parse tree produced by RAParser#aggrExpr.
    def enterAggrExpr(self, ctx:RAParser.AggrExprContext):
        pass

    # Exit a parse tree produced by RAParser#aggrExpr.
    def exitAggrExpr(self, ctx:RAParser.AggrExprContext):
        pass


    # Enter a parse tree produced by RAParser#projectExpr.
    def enterProjectExpr(self, ctx:RAParser.ProjectExprContext):
        pass

    # Exit a parse tree produced by RAParser#projectExpr.
    def exitProjectExpr(self, ctx:RAParser.ProjectExprContext):
        pass


    # Enter a parse tree produced by RAParser#definition.
    def enterDefinition(self, ctx:RAParser.DefinitionContext):
        pass

    # Exit a parse tree produced by RAParser#definition.
    def exitDefinition(self, ctx:RAParser.DefinitionContext):
        pass


    # Enter a parse tree produced by RAParser#listCommand.
    def enterListCommand(self, ctx:RAParser.ListCommandContext):
        pass

    # Exit a parse tree produced by RAParser#listCommand.
    def exitListCommand(self, ctx:RAParser.ListCommandContext):
        pass


    # Enter a parse tree produced by RAParser#clearCommand.
    def enterClearCommand(self, ctx:RAParser.ClearCommandContext):
        pass

    # Exit a parse tree produced by RAParser#clearCommand.
    def exitClearCommand(self, ctx:RAParser.ClearCommandContext):
        pass


    # Enter a parse tree produced by RAParser#saveCommand.
    def enterSaveCommand(self, ctx:RAParser.SaveCommandContext):
        pass

    # Exit a parse tree produced by RAParser#saveCommand.
    def exitSaveCommand(self, ctx:RAParser.SaveCommandContext):
        pass


    # Enter a parse tree produced by RAParser#sourceCommand.
    def enterSourceCommand(self, ctx:RAParser.SourceCommandContext):
        pass

    # Exit a parse tree produced by RAParser#sourceCommand.
    def exitSourceCommand(self, ctx:RAParser.SourceCommandContext):
        pass


    # Enter a parse tree produced by RAParser#helpCommand.
    def enterHelpCommand(self, ctx:RAParser.HelpCommandContext):
        pass

    # Exit a parse tree produced by RAParser#helpCommand.
    def exitHelpCommand(self, ctx:RAParser.HelpCommandContext):
        pass


    # Enter a parse tree produced by RAParser#quitCommand.
    def enterQuitCommand(self, ctx:RAParser.QuitCommandContext):
        pass

    # Exit a parse tree produced by RAParser#quitCommand.
    def exitQuitCommand(self, ctx:RAParser.QuitCommandContext):
        pass


    # Enter a parse tree produced by RAParser#sqlexecCommand.
    def enterSqlexecCommand(self, ctx:RAParser.SqlexecCommandContext):
        pass

    # Exit a parse tree produced by RAParser#sqlexecCommand.
    def exitSqlexecCommand(self, ctx:RAParser.SqlexecCommandContext):
        pass


    # Enter a parse tree produced by RAParser#statement.
    def enterStatement(self, ctx:RAParser.StatementContext):
        pass

    # Exit a parse tree produced by RAParser#statement.
    def exitStatement(self, ctx:RAParser.StatementContext):
        pass


    # Enter a parse tree produced by RAParser#program.
    def enterProgram(self, ctx:RAParser.ProgramContext):
        pass

    # Exit a parse tree produced by RAParser#program.
    def exitProgram(self, ctx:RAParser.ProgramContext):
        pass


    # Enter a parse tree produced by RAParser#textAtom.
    def enterTextAtom(self, ctx:RAParser.TextAtomContext):
        pass

    # Exit a parse tree produced by RAParser#textAtom.
    def exitTextAtom(self, ctx:RAParser.TextAtomContext):
        pass



del RAParser