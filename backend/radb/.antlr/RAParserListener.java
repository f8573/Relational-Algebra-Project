// Generated from c:/Users/James/Downloads/Relational-Algebra-Project/backend/radb/RAParser.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link RAParser}.
 */
public interface RAParserListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by the {@code numberLiteralValExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterNumberLiteralValExpr(RAParser.NumberLiteralValExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code numberLiteralValExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitNumberLiteralValExpr(RAParser.NumberLiteralValExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code textValExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterTextValExpr(RAParser.TextValExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code textValExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitTextValExpr(RAParser.TextValExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code isNotNullExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterIsNotNullExpr(RAParser.IsNotNullExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code isNotNullExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitIsNotNullExpr(RAParser.IsNotNullExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code funcExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterFuncExpr(RAParser.FuncExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code funcExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitFuncExpr(RAParser.FuncExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code attrRef}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterAttrRef(RAParser.AttrRefContext ctx);
	/**
	 * Exit a parse tree produced by the {@code attrRef}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitAttrRef(RAParser.AttrRefContext ctx);
	/**
	 * Enter a parse tree produced by the {@code plusMinusExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterPlusMinusExpr(RAParser.PlusMinusExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code plusMinusExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitPlusMinusExpr(RAParser.PlusMinusExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code orExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterOrExpr(RAParser.OrExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code orExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitOrExpr(RAParser.OrExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code valExprBraced}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterValExprBraced(RAParser.ValExprBracedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code valExprBraced}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitValExprBraced(RAParser.ValExprBracedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code valExprParenthesized}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterValExprParenthesized(RAParser.ValExprParenthesizedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code valExprParenthesized}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitValExprParenthesized(RAParser.ValExprParenthesizedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code concatExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterConcatExpr(RAParser.ConcatExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code concatExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitConcatExpr(RAParser.ConcatExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code notExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterNotExpr(RAParser.NotExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code notExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitNotExpr(RAParser.NotExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code isNullExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterIsNullExpr(RAParser.IsNullExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code isNullExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitIsNullExpr(RAParser.IsNullExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code stringLiteralValExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterStringLiteralValExpr(RAParser.StringLiteralValExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code stringLiteralValExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitStringLiteralValExpr(RAParser.StringLiteralValExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code likeExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterLikeExpr(RAParser.LikeExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code likeExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitLikeExpr(RAParser.LikeExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multDivExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterMultDivExpr(RAParser.MultDivExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multDivExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitMultDivExpr(RAParser.MultDivExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code compareExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterCompareExpr(RAParser.CompareExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code compareExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitCompareExpr(RAParser.CompareExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code andExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void enterAndExpr(RAParser.AndExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code andExpr}
	 * labeled alternative in {@link RAParser#valExpr}.
	 * @param ctx the parse tree
	 */
	void exitAndExpr(RAParser.AndExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link RAParser#listOfValExprs}.
	 * @param ctx the parse tree
	 */
	void enterListOfValExprs(RAParser.ListOfValExprsContext ctx);
	/**
	 * Exit a parse tree produced by {@link RAParser#listOfValExprs}.
	 * @param ctx the parse tree
	 */
	void exitListOfValExprs(RAParser.ListOfValExprsContext ctx);
	/**
	 * Enter a parse tree produced by {@link RAParser#listOfIDs}.
	 * @param ctx the parse tree
	 */
	void enterListOfIDs(RAParser.ListOfIDsContext ctx);
	/**
	 * Exit a parse tree produced by {@link RAParser#listOfIDs}.
	 * @param ctx the parse tree
	 */
	void exitListOfIDs(RAParser.ListOfIDsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code intersectExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterIntersectExpr(RAParser.IntersectExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code intersectExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitIntersectExpr(RAParser.IntersectExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code textRelExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterTextRelExpr(RAParser.TextRelExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code textRelExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitTextRelExpr(RAParser.TextRelExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code relExprParenthesized}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterRelExprParenthesized(RAParser.RelExprParenthesizedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code relExprParenthesized}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitRelExprParenthesized(RAParser.RelExprParenthesizedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code diffExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterDiffExpr(RAParser.DiffExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code diffExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitDiffExpr(RAParser.DiffExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unionExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterUnionExpr(RAParser.UnionExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unionExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitUnionExpr(RAParser.UnionExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code relRef}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterRelRef(RAParser.RelRefContext ctx);
	/**
	 * Exit a parse tree produced by the {@code relRef}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitRelRef(RAParser.RelRefContext ctx);
	/**
	 * Enter a parse tree produced by the {@code renameExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterRenameExpr(RAParser.RenameExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code renameExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitRenameExpr(RAParser.RenameExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code joinExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterJoinExpr(RAParser.JoinExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code joinExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitJoinExpr(RAParser.JoinExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code selectExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterSelectExpr(RAParser.SelectExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code selectExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitSelectExpr(RAParser.SelectExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code crossExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterCrossExpr(RAParser.CrossExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code crossExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitCrossExpr(RAParser.CrossExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code relExprBraced}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterRelExprBraced(RAParser.RelExprBracedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code relExprBraced}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitRelExprBraced(RAParser.RelExprBracedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code aggrExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterAggrExpr(RAParser.AggrExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code aggrExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitAggrExpr(RAParser.AggrExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code projectExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void enterProjectExpr(RAParser.ProjectExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code projectExpr}
	 * labeled alternative in {@link RAParser#relExpr}.
	 * @param ctx the parse tree
	 */
	void exitProjectExpr(RAParser.ProjectExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link RAParser#definition}.
	 * @param ctx the parse tree
	 */
	void enterDefinition(RAParser.DefinitionContext ctx);
	/**
	 * Exit a parse tree produced by {@link RAParser#definition}.
	 * @param ctx the parse tree
	 */
	void exitDefinition(RAParser.DefinitionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code listCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void enterListCommand(RAParser.ListCommandContext ctx);
	/**
	 * Exit a parse tree produced by the {@code listCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void exitListCommand(RAParser.ListCommandContext ctx);
	/**
	 * Enter a parse tree produced by the {@code clearCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void enterClearCommand(RAParser.ClearCommandContext ctx);
	/**
	 * Exit a parse tree produced by the {@code clearCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void exitClearCommand(RAParser.ClearCommandContext ctx);
	/**
	 * Enter a parse tree produced by the {@code saveCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void enterSaveCommand(RAParser.SaveCommandContext ctx);
	/**
	 * Exit a parse tree produced by the {@code saveCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void exitSaveCommand(RAParser.SaveCommandContext ctx);
	/**
	 * Enter a parse tree produced by the {@code sourceCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void enterSourceCommand(RAParser.SourceCommandContext ctx);
	/**
	 * Exit a parse tree produced by the {@code sourceCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void exitSourceCommand(RAParser.SourceCommandContext ctx);
	/**
	 * Enter a parse tree produced by the {@code helpCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void enterHelpCommand(RAParser.HelpCommandContext ctx);
	/**
	 * Exit a parse tree produced by the {@code helpCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void exitHelpCommand(RAParser.HelpCommandContext ctx);
	/**
	 * Enter a parse tree produced by the {@code quitCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void enterQuitCommand(RAParser.QuitCommandContext ctx);
	/**
	 * Exit a parse tree produced by the {@code quitCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void exitQuitCommand(RAParser.QuitCommandContext ctx);
	/**
	 * Enter a parse tree produced by the {@code sqlexecCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void enterSqlexecCommand(RAParser.SqlexecCommandContext ctx);
	/**
	 * Exit a parse tree produced by the {@code sqlexecCommand}
	 * labeled alternative in {@link RAParser#command}.
	 * @param ctx the parse tree
	 */
	void exitSqlexecCommand(RAParser.SqlexecCommandContext ctx);
	/**
	 * Enter a parse tree produced by {@link RAParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(RAParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link RAParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(RAParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link RAParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(RAParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link RAParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(RAParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link RAParser#textAtom}.
	 * @param ctx the parse tree
	 */
	void enterTextAtom(RAParser.TextAtomContext ctx);
	/**
	 * Exit a parse tree produced by {@link RAParser#textAtom}.
	 * @param ctx the parse tree
	 */
	void exitTextAtom(RAParser.TextAtomContext ctx);
}