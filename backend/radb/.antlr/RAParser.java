// Generated from c:/Users/James/Downloads/Relational-Algebra-Project/backend/radb/RAParser.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class RAParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		WS=1, COMMENT=2, LINE_COMMENT=3, TERMINATOR=4, FORCE=5, LEFT=6, RIGHT=7, 
		SPACE_CMD=8, LBRACE_ESC=9, RBRACE_ESC=10, IS_NULL=11, IS_NOT_NULL=12, 
		IS=13, NULL=14, LIKE=15, AND=16, OR=17, NOT=18, STRING=19, NUMBER=20, 
		PI=21, SIGMA=22, RHO=23, GAMMA=24, LEFT_ARROW=25, CUP=26, CAP=27, TIMES=28, 
		NATURAL_JOIN_SYMBOL=29, LEFT_OUTER_JOIN=30, RIGHT_OUTER_JOIN=31, FULL_OUTER_JOIN=32, 
		TEXT_CMD=33, ID=34, RENAME=35, PROJECT=36, SELECT=37, JOIN=38, CROSS=39, 
		UNION=40, DIFF=41, INTERSECT=42, AGGR=43, DOT=44, COMMA=45, STAR=46, SLASH=47, 
		PLUS=48, MINUS=49, CONCAT=50, PAREN_L=51, PAREN_R=52, ARG_L=53, ARG_R=54, 
		GETS=55, COLON=56, LE=57, NE=58, GE=59, LT=60, EQ=61, GT=62, LIST=63, 
		CLEAR=64, SAVE=65, SOURCE=66, HELP=67, QUIT=68, SQLEXEC=69, TEXT_LBRACE=70, 
		TEXT_CONTENT=71, TEXT_RBRACE=72, SQLEXEC_CONTENT=73, ARG_R_SQL=74;
	public static final int
		RULE_valExpr = 0, RULE_listOfValExprs = 1, RULE_listOfIDs = 2, RULE_relExpr = 3, 
		RULE_definition = 4, RULE_command = 5, RULE_statement = 6, RULE_program = 7, 
		RULE_textAtom = 8;
	private static String[] makeRuleNames() {
		return new String[] {
			"valExpr", "listOfValExprs", "listOfIDs", "relExpr", "definition", "command", 
			"statement", "program", "textAtom"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, null, null, null, "';'", "'!'", "'\\left'", "'\\right'", "'\\space'", 
			"'\\{'", "'\\}'", null, null, null, null, null, null, null, null, null, 
			null, "'\\pi'", "'\\sigma'", "'\\rho'", "'\\gamma'", null, null, null, 
			null, "'\\u22C8'", "'\\u27D5'", "'\\u27D6'", "'\\u27D7'", "'\\text'", 
			null, "'\\rename'", "'\\project'", "'\\select'", "'\\join'", "'\\cross'", 
			"'\\union'", "'\\diff'", "'\\intersect'", "'\\aggr'", "'.'", "','", "'*'", 
			"'/'", "'+'", "'-'", "'||'", "'('", "')'", "'_{'", null, "':-'", "':'", 
			"'<='", "'<>'", "'>='", "'<'", "'='", "'>'", "'\\list'", "'\\clear'", 
			"'\\save'", "'\\source'", "'\\help'", "'\\quit'", "'\\sqlexec'", "'{'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "WS", "COMMENT", "LINE_COMMENT", "TERMINATOR", "FORCE", "LEFT", 
			"RIGHT", "SPACE_CMD", "LBRACE_ESC", "RBRACE_ESC", "IS_NULL", "IS_NOT_NULL", 
			"IS", "NULL", "LIKE", "AND", "OR", "NOT", "STRING", "NUMBER", "PI", "SIGMA", 
			"RHO", "GAMMA", "LEFT_ARROW", "CUP", "CAP", "TIMES", "NATURAL_JOIN_SYMBOL", 
			"LEFT_OUTER_JOIN", "RIGHT_OUTER_JOIN", "FULL_OUTER_JOIN", "TEXT_CMD", 
			"ID", "RENAME", "PROJECT", "SELECT", "JOIN", "CROSS", "UNION", "DIFF", 
			"INTERSECT", "AGGR", "DOT", "COMMA", "STAR", "SLASH", "PLUS", "MINUS", 
			"CONCAT", "PAREN_L", "PAREN_R", "ARG_L", "ARG_R", "GETS", "COLON", "LE", 
			"NE", "GE", "LT", "EQ", "GT", "LIST", "CLEAR", "SAVE", "SOURCE", "HELP", 
			"QUIT", "SQLEXEC", "TEXT_LBRACE", "TEXT_CONTENT", "TEXT_RBRACE", "SQLEXEC_CONTENT", 
			"ARG_R_SQL"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "RAParser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public RAParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ValExprContext extends ParserRuleContext {
		public ValExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_valExpr; }
	 
		public ValExprContext() { }
		public void copyFrom(ValExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NumberLiteralValExprContext extends ValExprContext {
		public TerminalNode NUMBER() { return getToken(RAParser.NUMBER, 0); }
		public NumberLiteralValExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterNumberLiteralValExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitNumberLiteralValExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TextValExprContext extends ValExprContext {
		public TextAtomContext textAtom() {
			return getRuleContext(TextAtomContext.class,0);
		}
		public TextValExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterTextValExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitTextValExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IsNotNullExprContext extends ValExprContext {
		public ValExprContext valExpr() {
			return getRuleContext(ValExprContext.class,0);
		}
		public TerminalNode IS_NOT_NULL() { return getToken(RAParser.IS_NOT_NULL, 0); }
		public IsNotNullExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterIsNotNullExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitIsNotNullExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FuncExprContext extends ValExprContext {
		public TerminalNode ID() { return getToken(RAParser.ID, 0); }
		public TerminalNode PAREN_L() { return getToken(RAParser.PAREN_L, 0); }
		public TerminalNode PAREN_R() { return getToken(RAParser.PAREN_R, 0); }
		public ListOfValExprsContext listOfValExprs() {
			return getRuleContext(ListOfValExprsContext.class,0);
		}
		public FuncExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterFuncExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitFuncExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AttrRefContext extends ValExprContext {
		public List<TerminalNode> ID() { return getTokens(RAParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(RAParser.ID, i);
		}
		public TerminalNode DOT() { return getToken(RAParser.DOT, 0); }
		public AttrRefContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterAttrRef(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitAttrRef(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class PlusMinusExprContext extends ValExprContext {
		public List<ValExprContext> valExpr() {
			return getRuleContexts(ValExprContext.class);
		}
		public ValExprContext valExpr(int i) {
			return getRuleContext(ValExprContext.class,i);
		}
		public TerminalNode PLUS() { return getToken(RAParser.PLUS, 0); }
		public TerminalNode MINUS() { return getToken(RAParser.MINUS, 0); }
		public PlusMinusExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterPlusMinusExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitPlusMinusExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class OrExprContext extends ValExprContext {
		public List<ValExprContext> valExpr() {
			return getRuleContexts(ValExprContext.class);
		}
		public ValExprContext valExpr(int i) {
			return getRuleContext(ValExprContext.class,i);
		}
		public TerminalNode OR() { return getToken(RAParser.OR, 0); }
		public OrExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterOrExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitOrExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ValExprBracedContext extends ValExprContext {
		public TerminalNode LBRACE_ESC() { return getToken(RAParser.LBRACE_ESC, 0); }
		public ValExprContext valExpr() {
			return getRuleContext(ValExprContext.class,0);
		}
		public TerminalNode RBRACE_ESC() { return getToken(RAParser.RBRACE_ESC, 0); }
		public ValExprBracedContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterValExprBraced(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitValExprBraced(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ValExprParenthesizedContext extends ValExprContext {
		public TerminalNode PAREN_L() { return getToken(RAParser.PAREN_L, 0); }
		public ValExprContext valExpr() {
			return getRuleContext(ValExprContext.class,0);
		}
		public TerminalNode PAREN_R() { return getToken(RAParser.PAREN_R, 0); }
		public ValExprParenthesizedContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterValExprParenthesized(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitValExprParenthesized(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ConcatExprContext extends ValExprContext {
		public List<ValExprContext> valExpr() {
			return getRuleContexts(ValExprContext.class);
		}
		public ValExprContext valExpr(int i) {
			return getRuleContext(ValExprContext.class,i);
		}
		public TerminalNode CONCAT() { return getToken(RAParser.CONCAT, 0); }
		public ConcatExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterConcatExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitConcatExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NotExprContext extends ValExprContext {
		public TerminalNode NOT() { return getToken(RAParser.NOT, 0); }
		public ValExprContext valExpr() {
			return getRuleContext(ValExprContext.class,0);
		}
		public NotExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterNotExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitNotExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IsNullExprContext extends ValExprContext {
		public ValExprContext valExpr() {
			return getRuleContext(ValExprContext.class,0);
		}
		public TerminalNode IS_NULL() { return getToken(RAParser.IS_NULL, 0); }
		public IsNullExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterIsNullExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitIsNullExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class StringLiteralValExprContext extends ValExprContext {
		public TerminalNode STRING() { return getToken(RAParser.STRING, 0); }
		public StringLiteralValExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterStringLiteralValExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitStringLiteralValExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class LikeExprContext extends ValExprContext {
		public List<ValExprContext> valExpr() {
			return getRuleContexts(ValExprContext.class);
		}
		public ValExprContext valExpr(int i) {
			return getRuleContext(ValExprContext.class,i);
		}
		public TerminalNode LIKE() { return getToken(RAParser.LIKE, 0); }
		public LikeExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterLikeExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitLikeExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MultDivExprContext extends ValExprContext {
		public List<ValExprContext> valExpr() {
			return getRuleContexts(ValExprContext.class);
		}
		public ValExprContext valExpr(int i) {
			return getRuleContext(ValExprContext.class,i);
		}
		public TerminalNode STAR() { return getToken(RAParser.STAR, 0); }
		public TerminalNode SLASH() { return getToken(RAParser.SLASH, 0); }
		public MultDivExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterMultDivExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitMultDivExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CompareExprContext extends ValExprContext {
		public List<ValExprContext> valExpr() {
			return getRuleContexts(ValExprContext.class);
		}
		public ValExprContext valExpr(int i) {
			return getRuleContext(ValExprContext.class,i);
		}
		public TerminalNode LT() { return getToken(RAParser.LT, 0); }
		public TerminalNode LE() { return getToken(RAParser.LE, 0); }
		public TerminalNode EQ() { return getToken(RAParser.EQ, 0); }
		public TerminalNode NE() { return getToken(RAParser.NE, 0); }
		public TerminalNode GE() { return getToken(RAParser.GE, 0); }
		public TerminalNode GT() { return getToken(RAParser.GT, 0); }
		public CompareExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterCompareExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitCompareExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AndExprContext extends ValExprContext {
		public List<ValExprContext> valExpr() {
			return getRuleContexts(ValExprContext.class);
		}
		public ValExprContext valExpr(int i) {
			return getRuleContext(ValExprContext.class,i);
		}
		public TerminalNode AND() { return getToken(RAParser.AND, 0); }
		public AndExprContext(ValExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterAndExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitAndExpr(this);
		}
	}

	public final ValExprContext valExpr() throws RecognitionException {
		return valExpr(0);
	}

	private ValExprContext valExpr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ValExprContext _localctx = new ValExprContext(_ctx, _parentState);
		ValExprContext _prevctx = _localctx;
		int _startState = 0;
		enterRecursionRule(_localctx, 0, RULE_valExpr, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(43);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
			case 1:
				{
				_localctx = new StringLiteralValExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(19);
				match(STRING);
				}
				break;
			case 2:
				{
				_localctx = new NumberLiteralValExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(20);
				match(NUMBER);
				}
				break;
			case 3:
				{
				_localctx = new ValExprParenthesizedContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(21);
				match(PAREN_L);
				setState(22);
				valExpr(0);
				setState(23);
				match(PAREN_R);
				}
				break;
			case 4:
				{
				_localctx = new ValExprBracedContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(25);
				match(LBRACE_ESC);
				setState(26);
				valExpr(0);
				setState(27);
				match(RBRACE_ESC);
				}
				break;
			case 5:
				{
				_localctx = new TextValExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(29);
				textAtom();
				}
				break;
			case 6:
				{
				_localctx = new FuncExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(30);
				match(ID);
				setState(31);
				match(PAREN_L);
				setState(33);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 2251825585324544L) != 0)) {
					{
					setState(32);
					listOfValExprs();
					}
				}

				setState(35);
				match(PAREN_R);
				}
				break;
			case 7:
				{
				_localctx = new AttrRefContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(38);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
				case 1:
					{
					setState(36);
					match(ID);
					setState(37);
					match(DOT);
					}
					break;
				}
				setState(40);
				match(ID);
				}
				break;
			case 8:
				{
				_localctx = new NotExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(41);
				match(NOT);
				setState(42);
				valExpr(3);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(72);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(70);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
					case 1:
						{
						_localctx = new MultDivExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(45);
						if (!(precpred(_ctx, 10))) throw new FailedPredicateException(this, "precpred(_ctx, 10)");
						setState(46);
						_la = _input.LA(1);
						if ( !(_la==STAR || _la==SLASH) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(47);
						valExpr(11);
						}
						break;
					case 2:
						{
						_localctx = new PlusMinusExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(48);
						if (!(precpred(_ctx, 9))) throw new FailedPredicateException(this, "precpred(_ctx, 9)");
						setState(49);
						_la = _input.LA(1);
						if ( !(_la==PLUS || _la==MINUS) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(50);
						valExpr(10);
						}
						break;
					case 3:
						{
						_localctx = new ConcatExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(51);
						if (!(precpred(_ctx, 8))) throw new FailedPredicateException(this, "precpred(_ctx, 8)");
						setState(52);
						match(CONCAT);
						setState(53);
						valExpr(9);
						}
						break;
					case 4:
						{
						_localctx = new CompareExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(54);
						if (!(precpred(_ctx, 7))) throw new FailedPredicateException(this, "precpred(_ctx, 7)");
						setState(55);
						_la = _input.LA(1);
						if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 9079256848778919936L) != 0)) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(56);
						valExpr(8);
						}
						break;
					case 5:
						{
						_localctx = new LikeExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(57);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(58);
						match(LIKE);
						setState(59);
						valExpr(7);
						}
						break;
					case 6:
						{
						_localctx = new AndExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(60);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(61);
						match(AND);
						setState(62);
						valExpr(3);
						}
						break;
					case 7:
						{
						_localctx = new OrExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(63);
						if (!(precpred(_ctx, 1))) throw new FailedPredicateException(this, "precpred(_ctx, 1)");
						setState(64);
						match(OR);
						setState(65);
						valExpr(2);
						}
						break;
					case 8:
						{
						_localctx = new IsNullExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(66);
						if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
						setState(67);
						match(IS_NULL);
						}
						break;
					case 9:
						{
						_localctx = new IsNotNullExprContext(new ValExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_valExpr);
						setState(68);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(69);
						match(IS_NOT_NULL);
						}
						break;
					}
					} 
				}
				setState(74);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ListOfValExprsContext extends ParserRuleContext {
		public ValExprContext valExpr() {
			return getRuleContext(ValExprContext.class,0);
		}
		public TerminalNode COMMA() { return getToken(RAParser.COMMA, 0); }
		public ListOfValExprsContext listOfValExprs() {
			return getRuleContext(ListOfValExprsContext.class,0);
		}
		public ListOfValExprsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listOfValExprs; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterListOfValExprs(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitListOfValExprs(this);
		}
	}

	public final ListOfValExprsContext listOfValExprs() throws RecognitionException {
		ListOfValExprsContext _localctx = new ListOfValExprsContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_listOfValExprs);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(75);
			valExpr(0);
			setState(78);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==COMMA) {
				{
				setState(76);
				match(COMMA);
				setState(77);
				listOfValExprs();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ListOfIDsContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(RAParser.ID, 0); }
		public TerminalNode COMMA() { return getToken(RAParser.COMMA, 0); }
		public ListOfIDsContext listOfIDs() {
			return getRuleContext(ListOfIDsContext.class,0);
		}
		public ListOfIDsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listOfIDs; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterListOfIDs(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitListOfIDs(this);
		}
	}

	public final ListOfIDsContext listOfIDs() throws RecognitionException {
		ListOfIDsContext _localctx = new ListOfIDsContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_listOfIDs);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(80);
			match(ID);
			setState(83);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==COMMA) {
				{
				setState(81);
				match(COMMA);
				setState(82);
				listOfIDs();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RelExprContext extends ParserRuleContext {
		public RelExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relExpr; }
	 
		public RelExprContext() { }
		public void copyFrom(RelExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IntersectExprContext extends RelExprContext {
		public List<RelExprContext> relExpr() {
			return getRuleContexts(RelExprContext.class);
		}
		public RelExprContext relExpr(int i) {
			return getRuleContext(RelExprContext.class,i);
		}
		public TerminalNode INTERSECT() { return getToken(RAParser.INTERSECT, 0); }
		public TerminalNode CAP() { return getToken(RAParser.CAP, 0); }
		public IntersectExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterIntersectExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitIntersectExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class TextRelExprContext extends RelExprContext {
		public TextAtomContext textAtom() {
			return getRuleContext(TextAtomContext.class,0);
		}
		public TextRelExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterTextRelExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitTextRelExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RelExprParenthesizedContext extends RelExprContext {
		public TerminalNode PAREN_L() { return getToken(RAParser.PAREN_L, 0); }
		public RelExprContext relExpr() {
			return getRuleContext(RelExprContext.class,0);
		}
		public TerminalNode PAREN_R() { return getToken(RAParser.PAREN_R, 0); }
		public RelExprParenthesizedContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterRelExprParenthesized(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitRelExprParenthesized(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DiffExprContext extends RelExprContext {
		public List<RelExprContext> relExpr() {
			return getRuleContexts(RelExprContext.class);
		}
		public RelExprContext relExpr(int i) {
			return getRuleContext(RelExprContext.class,i);
		}
		public TerminalNode DIFF() { return getToken(RAParser.DIFF, 0); }
		public TerminalNode MINUS() { return getToken(RAParser.MINUS, 0); }
		public DiffExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterDiffExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitDiffExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnionExprContext extends RelExprContext {
		public List<RelExprContext> relExpr() {
			return getRuleContexts(RelExprContext.class);
		}
		public RelExprContext relExpr(int i) {
			return getRuleContext(RelExprContext.class,i);
		}
		public TerminalNode UNION() { return getToken(RAParser.UNION, 0); }
		public TerminalNode CUP() { return getToken(RAParser.CUP, 0); }
		public UnionExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterUnionExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitUnionExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RelRefContext extends RelExprContext {
		public TerminalNode ID() { return getToken(RAParser.ID, 0); }
		public RelRefContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterRelRef(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitRelRef(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RenameExprContext extends RelExprContext {
		public TerminalNode ARG_L() { return getToken(RAParser.ARG_L, 0); }
		public TerminalNode ARG_R() { return getToken(RAParser.ARG_R, 0); }
		public RelExprContext relExpr() {
			return getRuleContext(RelExprContext.class,0);
		}
		public TerminalNode RENAME() { return getToken(RAParser.RENAME, 0); }
		public TerminalNode RHO() { return getToken(RAParser.RHO, 0); }
		public ListOfIDsContext listOfIDs() {
			return getRuleContext(ListOfIDsContext.class,0);
		}
		public TerminalNode ID() { return getToken(RAParser.ID, 0); }
		public TerminalNode COLON() { return getToken(RAParser.COLON, 0); }
		public TerminalNode STAR() { return getToken(RAParser.STAR, 0); }
		public RenameExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterRenameExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitRenameExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class JoinExprContext extends RelExprContext {
		public List<RelExprContext> relExpr() {
			return getRuleContexts(RelExprContext.class);
		}
		public RelExprContext relExpr(int i) {
			return getRuleContext(RelExprContext.class,i);
		}
		public TerminalNode JOIN() { return getToken(RAParser.JOIN, 0); }
		public TerminalNode NATURAL_JOIN_SYMBOL() { return getToken(RAParser.NATURAL_JOIN_SYMBOL, 0); }
		public TerminalNode LEFT_OUTER_JOIN() { return getToken(RAParser.LEFT_OUTER_JOIN, 0); }
		public TerminalNode RIGHT_OUTER_JOIN() { return getToken(RAParser.RIGHT_OUTER_JOIN, 0); }
		public TerminalNode FULL_OUTER_JOIN() { return getToken(RAParser.FULL_OUTER_JOIN, 0); }
		public TerminalNode ARG_L() { return getToken(RAParser.ARG_L, 0); }
		public ValExprContext valExpr() {
			return getRuleContext(ValExprContext.class,0);
		}
		public TerminalNode ARG_R() { return getToken(RAParser.ARG_R, 0); }
		public JoinExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterJoinExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitJoinExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SelectExprContext extends RelExprContext {
		public TerminalNode ARG_L() { return getToken(RAParser.ARG_L, 0); }
		public ValExprContext valExpr() {
			return getRuleContext(ValExprContext.class,0);
		}
		public TerminalNode ARG_R() { return getToken(RAParser.ARG_R, 0); }
		public RelExprContext relExpr() {
			return getRuleContext(RelExprContext.class,0);
		}
		public TerminalNode SELECT() { return getToken(RAParser.SELECT, 0); }
		public TerminalNode SIGMA() { return getToken(RAParser.SIGMA, 0); }
		public SelectExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterSelectExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitSelectExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CrossExprContext extends RelExprContext {
		public List<RelExprContext> relExpr() {
			return getRuleContexts(RelExprContext.class);
		}
		public RelExprContext relExpr(int i) {
			return getRuleContext(RelExprContext.class,i);
		}
		public TerminalNode CROSS() { return getToken(RAParser.CROSS, 0); }
		public TerminalNode TIMES() { return getToken(RAParser.TIMES, 0); }
		public CrossExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterCrossExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitCrossExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class RelExprBracedContext extends RelExprContext {
		public TerminalNode LBRACE_ESC() { return getToken(RAParser.LBRACE_ESC, 0); }
		public RelExprContext relExpr() {
			return getRuleContext(RelExprContext.class,0);
		}
		public TerminalNode RBRACE_ESC() { return getToken(RAParser.RBRACE_ESC, 0); }
		public RelExprBracedContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterRelExprBraced(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitRelExprBraced(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AggrExprContext extends RelExprContext {
		public TerminalNode ARG_L() { return getToken(RAParser.ARG_L, 0); }
		public List<ListOfValExprsContext> listOfValExprs() {
			return getRuleContexts(ListOfValExprsContext.class);
		}
		public ListOfValExprsContext listOfValExprs(int i) {
			return getRuleContext(ListOfValExprsContext.class,i);
		}
		public TerminalNode ARG_R() { return getToken(RAParser.ARG_R, 0); }
		public RelExprContext relExpr() {
			return getRuleContext(RelExprContext.class,0);
		}
		public TerminalNode AGGR() { return getToken(RAParser.AGGR, 0); }
		public TerminalNode GAMMA() { return getToken(RAParser.GAMMA, 0); }
		public TerminalNode COLON() { return getToken(RAParser.COLON, 0); }
		public AggrExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterAggrExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitAggrExpr(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ProjectExprContext extends RelExprContext {
		public TerminalNode ARG_L() { return getToken(RAParser.ARG_L, 0); }
		public ListOfValExprsContext listOfValExprs() {
			return getRuleContext(ListOfValExprsContext.class,0);
		}
		public TerminalNode ARG_R() { return getToken(RAParser.ARG_R, 0); }
		public RelExprContext relExpr() {
			return getRuleContext(RelExprContext.class,0);
		}
		public TerminalNode PROJECT() { return getToken(RAParser.PROJECT, 0); }
		public TerminalNode PI() { return getToken(RAParser.PI, 0); }
		public ProjectExprContext(RelExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterProjectExpr(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitProjectExpr(this);
		}
	}

	public final RelExprContext relExpr() throws RecognitionException {
		return relExpr(0);
	}

	private RelExprContext relExpr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		RelExprContext _localctx = new RelExprContext(_ctx, _parentState);
		RelExprContext _prevctx = _localctx;
		int _startState = 6;
		enterRecursionRule(_localctx, 6, RULE_relExpr, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(131);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case PAREN_L:
				{
				_localctx = new RelExprParenthesizedContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(86);
				match(PAREN_L);
				setState(87);
				relExpr(0);
				setState(88);
				match(PAREN_R);
				}
				break;
			case LBRACE_ESC:
				{
				_localctx = new RelExprBracedContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(90);
				match(LBRACE_ESC);
				setState(91);
				relExpr(0);
				setState(92);
				match(RBRACE_ESC);
				}
				break;
			case ID:
				{
				_localctx = new RelRefContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(94);
				match(ID);
				}
				break;
			case TEXT_CMD:
				{
				_localctx = new TextRelExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(95);
				textAtom();
				}
				break;
			case RHO:
			case RENAME:
				{
				_localctx = new RenameExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(96);
				_la = _input.LA(1);
				if ( !(_la==RHO || _la==RENAME) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(97);
				match(ARG_L);
				setState(105);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,8,_ctx) ) {
				case 1:
					{
					{
					setState(98);
					match(ID);
					setState(99);
					match(COLON);
					setState(102);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case STAR:
						{
						setState(100);
						match(STAR);
						}
						break;
					case ID:
						{
						setState(101);
						listOfIDs();
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					}
					}
					break;
				case 2:
					{
					setState(104);
					listOfIDs();
					}
					break;
				}
				setState(107);
				match(ARG_R);
				setState(108);
				relExpr(9);
				}
				break;
			case PI:
			case PROJECT:
				{
				_localctx = new ProjectExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(109);
				_la = _input.LA(1);
				if ( !(_la==PI || _la==PROJECT) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(110);
				match(ARG_L);
				setState(111);
				listOfValExprs();
				setState(112);
				match(ARG_R);
				setState(113);
				relExpr(8);
				}
				break;
			case SIGMA:
			case SELECT:
				{
				_localctx = new SelectExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(115);
				_la = _input.LA(1);
				if ( !(_la==SIGMA || _la==SELECT) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(116);
				match(ARG_L);
				setState(117);
				valExpr(0);
				setState(118);
				match(ARG_R);
				setState(119);
				relExpr(7);
				}
				break;
			case GAMMA:
			case AGGR:
				{
				_localctx = new AggrExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(121);
				_la = _input.LA(1);
				if ( !(_la==GAMMA || _la==AGGR) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(122);
				match(ARG_L);
				setState(123);
				listOfValExprs();
				setState(126);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==COLON) {
					{
					setState(124);
					match(COLON);
					setState(125);
					listOfValExprs();
					}
				}

				setState(128);
				match(ARG_R);
				setState(129);
				relExpr(1);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(156);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,13,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(154);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
					case 1:
						{
						_localctx = new JoinExprContext(new RelExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_relExpr);
						setState(133);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(134);
						_la = _input.LA(1);
						if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 282930970624L) != 0)) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(139);
						_errHandler.sync(this);
						_la = _input.LA(1);
						if (_la==ARG_L) {
							{
							setState(135);
							match(ARG_L);
							setState(136);
							valExpr(0);
							setState(137);
							match(ARG_R);
							}
						}

						setState(141);
						relExpr(7);
						}
						break;
					case 2:
						{
						_localctx = new CrossExprContext(new RelExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_relExpr);
						setState(142);
						if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
						setState(143);
						_la = _input.LA(1);
						if ( !(_la==TIMES || _la==CROSS) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(144);
						relExpr(6);
						}
						break;
					case 3:
						{
						_localctx = new UnionExprContext(new RelExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_relExpr);
						setState(145);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(146);
						_la = _input.LA(1);
						if ( !(_la==CUP || _la==UNION) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(147);
						relExpr(5);
						}
						break;
					case 4:
						{
						_localctx = new DiffExprContext(new RelExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_relExpr);
						setState(148);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(149);
						_la = _input.LA(1);
						if ( !(_la==DIFF || _la==MINUS) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(150);
						relExpr(4);
						}
						break;
					case 5:
						{
						_localctx = new IntersectExprContext(new RelExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_relExpr);
						setState(151);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(152);
						_la = _input.LA(1);
						if ( !(_la==CAP || _la==INTERSECT) ) {
						_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(153);
						relExpr(3);
						}
						break;
					}
					} 
				}
				setState(158);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,13,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DefinitionContext extends ParserRuleContext {
		public RelExprContext relExpr() {
			return getRuleContext(RelExprContext.class,0);
		}
		public TerminalNode GETS() { return getToken(RAParser.GETS, 0); }
		public TerminalNode LEFT_ARROW() { return getToken(RAParser.LEFT_ARROW, 0); }
		public TerminalNode ID() { return getToken(RAParser.ID, 0); }
		public TextAtomContext textAtom() {
			return getRuleContext(TextAtomContext.class,0);
		}
		public DefinitionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_definition; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterDefinition(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitDefinition(this);
		}
	}

	public final DefinitionContext definition() throws RecognitionException {
		DefinitionContext _localctx = new DefinitionContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_definition);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(161);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ID:
				{
				setState(159);
				match(ID);
				}
				break;
			case TEXT_CMD:
				{
				setState(160);
				textAtom();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			setState(163);
			_la = _input.LA(1);
			if ( !(_la==LEFT_ARROW || _la==GETS) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			setState(164);
			relExpr(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CommandContext extends ParserRuleContext {
		public CommandContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_command; }
	 
		public CommandContext() { }
		public void copyFrom(CommandContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ListCommandContext extends CommandContext {
		public TerminalNode LIST() { return getToken(RAParser.LIST, 0); }
		public ListCommandContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterListCommand(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitListCommand(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ClearCommandContext extends CommandContext {
		public TerminalNode CLEAR() { return getToken(RAParser.CLEAR, 0); }
		public TerminalNode ID() { return getToken(RAParser.ID, 0); }
		public TerminalNode STAR() { return getToken(RAParser.STAR, 0); }
		public TerminalNode FORCE() { return getToken(RAParser.FORCE, 0); }
		public ClearCommandContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterClearCommand(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitClearCommand(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class QuitCommandContext extends CommandContext {
		public TerminalNode QUIT() { return getToken(RAParser.QUIT, 0); }
		public QuitCommandContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterQuitCommand(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitQuitCommand(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SourceCommandContext extends CommandContext {
		public TerminalNode SOURCE() { return getToken(RAParser.SOURCE, 0); }
		public TerminalNode STRING() { return getToken(RAParser.STRING, 0); }
		public SourceCommandContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterSourceCommand(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitSourceCommand(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class HelpCommandContext extends CommandContext {
		public TerminalNode HELP() { return getToken(RAParser.HELP, 0); }
		public HelpCommandContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterHelpCommand(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitHelpCommand(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SaveCommandContext extends CommandContext {
		public TerminalNode SAVE() { return getToken(RAParser.SAVE, 0); }
		public TerminalNode ID() { return getToken(RAParser.ID, 0); }
		public TerminalNode STAR() { return getToken(RAParser.STAR, 0); }
		public TerminalNode FORCE() { return getToken(RAParser.FORCE, 0); }
		public TerminalNode STRING() { return getToken(RAParser.STRING, 0); }
		public SaveCommandContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterSaveCommand(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitSaveCommand(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SqlexecCommandContext extends CommandContext {
		public TerminalNode SQLEXEC() { return getToken(RAParser.SQLEXEC, 0); }
		public TerminalNode SQLEXEC_CONTENT() { return getToken(RAParser.SQLEXEC_CONTENT, 0); }
		public SqlexecCommandContext(CommandContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterSqlexecCommand(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitSqlexecCommand(this);
		}
	}

	public final CommandContext command() throws RecognitionException {
		CommandContext _localctx = new CommandContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_command);
		int _la;
		try {
			setState(189);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case LIST:
				_localctx = new ListCommandContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(166);
				match(LIST);
				}
				break;
			case CLEAR:
				_localctx = new ClearCommandContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(167);
				match(CLEAR);
				setState(173);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case FORCE:
				case ID:
					{
					setState(169);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==FORCE) {
						{
						setState(168);
						match(FORCE);
						}
					}

					setState(171);
					match(ID);
					}
					break;
				case STAR:
					{
					setState(172);
					match(STAR);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				break;
			case SAVE:
				_localctx = new SaveCommandContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(175);
				match(SAVE);
				setState(177);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==FORCE) {
					{
					setState(176);
					match(FORCE);
					}
				}

				setState(179);
				_la = _input.LA(1);
				if ( !(_la==ID || _la==STAR) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(181);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(180);
					match(STRING);
					}
				}

				}
				break;
			case SOURCE:
				_localctx = new SourceCommandContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(183);
				match(SOURCE);
				setState(184);
				match(STRING);
				}
				break;
			case HELP:
				_localctx = new HelpCommandContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(185);
				match(HELP);
				}
				break;
			case QUIT:
				_localctx = new QuitCommandContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(186);
				match(QUIT);
				}
				break;
			case SQLEXEC:
				_localctx = new SqlexecCommandContext(_localctx);
				enterOuterAlt(_localctx, 7);
				{
				setState(187);
				match(SQLEXEC);
				setState(188);
				match(SQLEXEC_CONTENT);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StatementContext extends ParserRuleContext {
		public TerminalNode TERMINATOR() { return getToken(RAParser.TERMINATOR, 0); }
		public RelExprContext relExpr() {
			return getRuleContext(RelExprContext.class,0);
		}
		public DefinitionContext definition() {
			return getRuleContext(DefinitionContext.class,0);
		}
		public CommandContext command() {
			return getRuleContext(CommandContext.class,0);
		}
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterStatement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitStatement(this);
		}
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_statement);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(194);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,20,_ctx) ) {
			case 1:
				{
				setState(191);
				relExpr(0);
				}
				break;
			case 2:
				{
				setState(192);
				definition();
				}
				break;
			case 3:
				{
				setState(193);
				command();
				}
				break;
			}
			setState(196);
			match(TERMINATOR);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(RAParser.EOF, 0); }
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterProgram(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitProgram(this);
		}
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(201);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (((((_la - 9)) & ~0x3f) == 0 && ((1L << (_la - 9)) & 2287833026450747393L) != 0)) {
				{
				{
				setState(198);
				statement();
				}
				}
				setState(203);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(204);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TextAtomContext extends ParserRuleContext {
		public TerminalNode TEXT_CMD() { return getToken(RAParser.TEXT_CMD, 0); }
		public TerminalNode TEXT_LBRACE() { return getToken(RAParser.TEXT_LBRACE, 0); }
		public TerminalNode TEXT_RBRACE() { return getToken(RAParser.TEXT_RBRACE, 0); }
		public TerminalNode TEXT_CONTENT() { return getToken(RAParser.TEXT_CONTENT, 0); }
		public TextAtomContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_textAtom; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).enterTextAtom(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof RAParserListener ) ((RAParserListener)listener).exitTextAtom(this);
		}
	}

	public final TextAtomContext textAtom() throws RecognitionException {
		TextAtomContext _localctx = new TextAtomContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_textAtom);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(206);
			match(TEXT_CMD);
			setState(207);
			match(TEXT_LBRACE);
			setState(209);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==TEXT_CONTENT) {
				{
				setState(208);
				match(TEXT_CONTENT);
				}
			}

			setState(211);
			match(TEXT_RBRACE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 0:
			return valExpr_sempred((ValExprContext)_localctx, predIndex);
		case 3:
			return relExpr_sempred((RelExprContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean valExpr_sempred(ValExprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 10);
		case 1:
			return precpred(_ctx, 9);
		case 2:
			return precpred(_ctx, 8);
		case 3:
			return precpred(_ctx, 7);
		case 4:
			return precpred(_ctx, 6);
		case 5:
			return precpred(_ctx, 2);
		case 6:
			return precpred(_ctx, 1);
		case 7:
			return precpred(_ctx, 5);
		case 8:
			return precpred(_ctx, 4);
		}
		return true;
	}
	private boolean relExpr_sempred(RelExprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 9:
			return precpred(_ctx, 6);
		case 10:
			return precpred(_ctx, 5);
		case 11:
			return precpred(_ctx, 4);
		case 12:
			return precpred(_ctx, 3);
		case 13:
			return precpred(_ctx, 2);
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u0001J\u00d6\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0003\u0000\"\b\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0000\u0003\u0000\'\b\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0003\u0000,\b\u0000\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0005\u0000"+
		"G\b\u0000\n\u0000\f\u0000J\t\u0000\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0003\u0001O\b\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0003\u0002"+
		"T\b\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0003\u0003g\b\u0003\u0001\u0003\u0003\u0003j\b\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0003"+
		"\u0003\u007f\b\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0003\u0003\u0084"+
		"\b\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0003\u0003\u008c\b\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0005\u0003\u009b\b\u0003\n"+
		"\u0003\f\u0003\u009e\t\u0003\u0001\u0004\u0001\u0004\u0003\u0004\u00a2"+
		"\b\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0003\u0005\u00aa\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u00ae"+
		"\b\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u00b2\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0003\u0005\u00b6\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u00be\b\u0005\u0001\u0006"+
		"\u0001\u0006\u0001\u0006\u0003\u0006\u00c3\b\u0006\u0001\u0006\u0001\u0006"+
		"\u0001\u0007\u0005\u0007\u00c8\b\u0007\n\u0007\f\u0007\u00cb\t\u0007\u0001"+
		"\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0003\b\u00d2\b\b\u0001\b\u0001"+
		"\b\u0001\b\u0000\u0002\u0000\u0006\t\u0000\u0002\u0004\u0006\b\n\f\u000e"+
		"\u0010\u0000\u000e\u0001\u0000./\u0001\u000001\u0001\u00009>\u0002\u0000"+
		"\u0017\u0017##\u0002\u0000\u0015\u0015$$\u0002\u0000\u0016\u0016%%\u0002"+
		"\u0000\u0018\u0018++\u0002\u0000\u001d &&\u0002\u0000\u001c\u001c\'\'"+
		"\u0002\u0000\u001a\u001a((\u0002\u0000))11\u0002\u0000\u001b\u001b**\u0002"+
		"\u0000\u0019\u001977\u0002\u0000\"\"..\u00ff\u0000+\u0001\u0000\u0000"+
		"\u0000\u0002K\u0001\u0000\u0000\u0000\u0004P\u0001\u0000\u0000\u0000\u0006"+
		"\u0083\u0001\u0000\u0000\u0000\b\u00a1\u0001\u0000\u0000\u0000\n\u00bd"+
		"\u0001\u0000\u0000\u0000\f\u00c2\u0001\u0000\u0000\u0000\u000e\u00c9\u0001"+
		"\u0000\u0000\u0000\u0010\u00ce\u0001\u0000\u0000\u0000\u0012\u0013\u0006"+
		"\u0000\uffff\uffff\u0000\u0013,\u0005\u0013\u0000\u0000\u0014,\u0005\u0014"+
		"\u0000\u0000\u0015\u0016\u00053\u0000\u0000\u0016\u0017\u0003\u0000\u0000"+
		"\u0000\u0017\u0018\u00054\u0000\u0000\u0018,\u0001\u0000\u0000\u0000\u0019"+
		"\u001a\u0005\t\u0000\u0000\u001a\u001b\u0003\u0000\u0000\u0000\u001b\u001c"+
		"\u0005\n\u0000\u0000\u001c,\u0001\u0000\u0000\u0000\u001d,\u0003\u0010"+
		"\b\u0000\u001e\u001f\u0005\"\u0000\u0000\u001f!\u00053\u0000\u0000 \""+
		"\u0003\u0002\u0001\u0000! \u0001\u0000\u0000\u0000!\"\u0001\u0000\u0000"+
		"\u0000\"#\u0001\u0000\u0000\u0000#,\u00054\u0000\u0000$%\u0005\"\u0000"+
		"\u0000%\'\u0005,\u0000\u0000&$\u0001\u0000\u0000\u0000&\'\u0001\u0000"+
		"\u0000\u0000\'(\u0001\u0000\u0000\u0000(,\u0005\"\u0000\u0000)*\u0005"+
		"\u0012\u0000\u0000*,\u0003\u0000\u0000\u0003+\u0012\u0001\u0000\u0000"+
		"\u0000+\u0014\u0001\u0000\u0000\u0000+\u0015\u0001\u0000\u0000\u0000+"+
		"\u0019\u0001\u0000\u0000\u0000+\u001d\u0001\u0000\u0000\u0000+\u001e\u0001"+
		"\u0000\u0000\u0000+&\u0001\u0000\u0000\u0000+)\u0001\u0000\u0000\u0000"+
		",H\u0001\u0000\u0000\u0000-.\n\n\u0000\u0000./\u0007\u0000\u0000\u0000"+
		"/G\u0003\u0000\u0000\u000b01\n\t\u0000\u000012\u0007\u0001\u0000\u0000"+
		"2G\u0003\u0000\u0000\n34\n\b\u0000\u000045\u00052\u0000\u00005G\u0003"+
		"\u0000\u0000\t67\n\u0007\u0000\u000078\u0007\u0002\u0000\u00008G\u0003"+
		"\u0000\u0000\b9:\n\u0006\u0000\u0000:;\u0005\u000f\u0000\u0000;G\u0003"+
		"\u0000\u0000\u0007<=\n\u0002\u0000\u0000=>\u0005\u0010\u0000\u0000>G\u0003"+
		"\u0000\u0000\u0003?@\n\u0001\u0000\u0000@A\u0005\u0011\u0000\u0000AG\u0003"+
		"\u0000\u0000\u0002BC\n\u0005\u0000\u0000CG\u0005\u000b\u0000\u0000DE\n"+
		"\u0004\u0000\u0000EG\u0005\f\u0000\u0000F-\u0001\u0000\u0000\u0000F0\u0001"+
		"\u0000\u0000\u0000F3\u0001\u0000\u0000\u0000F6\u0001\u0000\u0000\u0000"+
		"F9\u0001\u0000\u0000\u0000F<\u0001\u0000\u0000\u0000F?\u0001\u0000\u0000"+
		"\u0000FB\u0001\u0000\u0000\u0000FD\u0001\u0000\u0000\u0000GJ\u0001\u0000"+
		"\u0000\u0000HF\u0001\u0000\u0000\u0000HI\u0001\u0000\u0000\u0000I\u0001"+
		"\u0001\u0000\u0000\u0000JH\u0001\u0000\u0000\u0000KN\u0003\u0000\u0000"+
		"\u0000LM\u0005-\u0000\u0000MO\u0003\u0002\u0001\u0000NL\u0001\u0000\u0000"+
		"\u0000NO\u0001\u0000\u0000\u0000O\u0003\u0001\u0000\u0000\u0000PS\u0005"+
		"\"\u0000\u0000QR\u0005-\u0000\u0000RT\u0003\u0004\u0002\u0000SQ\u0001"+
		"\u0000\u0000\u0000ST\u0001\u0000\u0000\u0000T\u0005\u0001\u0000\u0000"+
		"\u0000UV\u0006\u0003\uffff\uffff\u0000VW\u00053\u0000\u0000WX\u0003\u0006"+
		"\u0003\u0000XY\u00054\u0000\u0000Y\u0084\u0001\u0000\u0000\u0000Z[\u0005"+
		"\t\u0000\u0000[\\\u0003\u0006\u0003\u0000\\]\u0005\n\u0000\u0000]\u0084"+
		"\u0001\u0000\u0000\u0000^\u0084\u0005\"\u0000\u0000_\u0084\u0003\u0010"+
		"\b\u0000`a\u0007\u0003\u0000\u0000ai\u00055\u0000\u0000bc\u0005\"\u0000"+
		"\u0000cf\u00058\u0000\u0000dg\u0005.\u0000\u0000eg\u0003\u0004\u0002\u0000"+
		"fd\u0001\u0000\u0000\u0000fe\u0001\u0000\u0000\u0000gj\u0001\u0000\u0000"+
		"\u0000hj\u0003\u0004\u0002\u0000ib\u0001\u0000\u0000\u0000ih\u0001\u0000"+
		"\u0000\u0000jk\u0001\u0000\u0000\u0000kl\u00056\u0000\u0000l\u0084\u0003"+
		"\u0006\u0003\tmn\u0007\u0004\u0000\u0000no\u00055\u0000\u0000op\u0003"+
		"\u0002\u0001\u0000pq\u00056\u0000\u0000qr\u0003\u0006\u0003\br\u0084\u0001"+
		"\u0000\u0000\u0000st\u0007\u0005\u0000\u0000tu\u00055\u0000\u0000uv\u0003"+
		"\u0000\u0000\u0000vw\u00056\u0000\u0000wx\u0003\u0006\u0003\u0007x\u0084"+
		"\u0001\u0000\u0000\u0000yz\u0007\u0006\u0000\u0000z{\u00055\u0000\u0000"+
		"{~\u0003\u0002\u0001\u0000|}\u00058\u0000\u0000}\u007f\u0003\u0002\u0001"+
		"\u0000~|\u0001\u0000\u0000\u0000~\u007f\u0001\u0000\u0000\u0000\u007f"+
		"\u0080\u0001\u0000\u0000\u0000\u0080\u0081\u00056\u0000\u0000\u0081\u0082"+
		"\u0003\u0006\u0003\u0001\u0082\u0084\u0001\u0000\u0000\u0000\u0083U\u0001"+
		"\u0000\u0000\u0000\u0083Z\u0001\u0000\u0000\u0000\u0083^\u0001\u0000\u0000"+
		"\u0000\u0083_\u0001\u0000\u0000\u0000\u0083`\u0001\u0000\u0000\u0000\u0083"+
		"m\u0001\u0000\u0000\u0000\u0083s\u0001\u0000\u0000\u0000\u0083y\u0001"+
		"\u0000\u0000\u0000\u0084\u009c\u0001\u0000\u0000\u0000\u0085\u0086\n\u0006"+
		"\u0000\u0000\u0086\u008b\u0007\u0007\u0000\u0000\u0087\u0088\u00055\u0000"+
		"\u0000\u0088\u0089\u0003\u0000\u0000\u0000\u0089\u008a\u00056\u0000\u0000"+
		"\u008a\u008c\u0001\u0000\u0000\u0000\u008b\u0087\u0001\u0000\u0000\u0000"+
		"\u008b\u008c\u0001\u0000\u0000\u0000\u008c\u008d\u0001\u0000\u0000\u0000"+
		"\u008d\u009b\u0003\u0006\u0003\u0007\u008e\u008f\n\u0005\u0000\u0000\u008f"+
		"\u0090\u0007\b\u0000\u0000\u0090\u009b\u0003\u0006\u0003\u0006\u0091\u0092"+
		"\n\u0004\u0000\u0000\u0092\u0093\u0007\t\u0000\u0000\u0093\u009b\u0003"+
		"\u0006\u0003\u0005\u0094\u0095\n\u0003\u0000\u0000\u0095\u0096\u0007\n"+
		"\u0000\u0000\u0096\u009b\u0003\u0006\u0003\u0004\u0097\u0098\n\u0002\u0000"+
		"\u0000\u0098\u0099\u0007\u000b\u0000\u0000\u0099\u009b\u0003\u0006\u0003"+
		"\u0003\u009a\u0085\u0001\u0000\u0000\u0000\u009a\u008e\u0001\u0000\u0000"+
		"\u0000\u009a\u0091\u0001\u0000\u0000\u0000\u009a\u0094\u0001\u0000\u0000"+
		"\u0000\u009a\u0097\u0001\u0000\u0000\u0000\u009b\u009e\u0001\u0000\u0000"+
		"\u0000\u009c\u009a\u0001\u0000\u0000\u0000\u009c\u009d\u0001\u0000\u0000"+
		"\u0000\u009d\u0007\u0001\u0000\u0000\u0000\u009e\u009c\u0001\u0000\u0000"+
		"\u0000\u009f\u00a2\u0005\"\u0000\u0000\u00a0\u00a2\u0003\u0010\b\u0000"+
		"\u00a1\u009f\u0001\u0000\u0000\u0000\u00a1\u00a0\u0001\u0000\u0000\u0000"+
		"\u00a2\u00a3\u0001\u0000\u0000\u0000\u00a3\u00a4\u0007\f\u0000\u0000\u00a4"+
		"\u00a5\u0003\u0006\u0003\u0000\u00a5\t\u0001\u0000\u0000\u0000\u00a6\u00be"+
		"\u0005?\u0000\u0000\u00a7\u00ad\u0005@\u0000\u0000\u00a8\u00aa\u0005\u0005"+
		"\u0000\u0000\u00a9\u00a8\u0001\u0000\u0000\u0000\u00a9\u00aa\u0001\u0000"+
		"\u0000\u0000\u00aa\u00ab\u0001\u0000\u0000\u0000\u00ab\u00ae\u0005\"\u0000"+
		"\u0000\u00ac\u00ae\u0005.\u0000\u0000\u00ad\u00a9\u0001\u0000\u0000\u0000"+
		"\u00ad\u00ac\u0001\u0000\u0000\u0000\u00ae\u00be\u0001\u0000\u0000\u0000"+
		"\u00af\u00b1\u0005A\u0000\u0000\u00b0\u00b2\u0005\u0005\u0000\u0000\u00b1"+
		"\u00b0\u0001\u0000\u0000\u0000\u00b1\u00b2\u0001\u0000\u0000\u0000\u00b2"+
		"\u00b3\u0001\u0000\u0000\u0000\u00b3\u00b5\u0007\r\u0000\u0000\u00b4\u00b6"+
		"\u0005\u0013\u0000\u0000\u00b5\u00b4\u0001\u0000\u0000\u0000\u00b5\u00b6"+
		"\u0001\u0000\u0000\u0000\u00b6\u00be\u0001\u0000\u0000\u0000\u00b7\u00b8"+
		"\u0005B\u0000\u0000\u00b8\u00be\u0005\u0013\u0000\u0000\u00b9\u00be\u0005"+
		"C\u0000\u0000\u00ba\u00be\u0005D\u0000\u0000\u00bb\u00bc\u0005E\u0000"+
		"\u0000\u00bc\u00be\u0005I\u0000\u0000\u00bd\u00a6\u0001\u0000\u0000\u0000"+
		"\u00bd\u00a7\u0001\u0000\u0000\u0000\u00bd\u00af\u0001\u0000\u0000\u0000"+
		"\u00bd\u00b7\u0001\u0000\u0000\u0000\u00bd\u00b9\u0001\u0000\u0000\u0000"+
		"\u00bd\u00ba\u0001\u0000\u0000\u0000\u00bd\u00bb\u0001\u0000\u0000\u0000"+
		"\u00be\u000b\u0001\u0000\u0000\u0000\u00bf\u00c3\u0003\u0006\u0003\u0000"+
		"\u00c0\u00c3\u0003\b\u0004\u0000\u00c1\u00c3\u0003\n\u0005\u0000\u00c2"+
		"\u00bf\u0001\u0000\u0000\u0000\u00c2\u00c0\u0001\u0000\u0000\u0000\u00c2"+
		"\u00c1\u0001\u0000\u0000\u0000\u00c3\u00c4\u0001\u0000\u0000\u0000\u00c4"+
		"\u00c5\u0005\u0004\u0000\u0000\u00c5\r\u0001\u0000\u0000\u0000\u00c6\u00c8"+
		"\u0003\f\u0006\u0000\u00c7\u00c6\u0001\u0000\u0000\u0000\u00c8\u00cb\u0001"+
		"\u0000\u0000\u0000\u00c9\u00c7\u0001\u0000\u0000\u0000\u00c9\u00ca\u0001"+
		"\u0000\u0000\u0000\u00ca\u00cc\u0001\u0000\u0000\u0000\u00cb\u00c9\u0001"+
		"\u0000\u0000\u0000\u00cc\u00cd\u0005\u0000\u0000\u0001\u00cd\u000f\u0001"+
		"\u0000\u0000\u0000\u00ce\u00cf\u0005!\u0000\u0000\u00cf\u00d1\u0005F\u0000"+
		"\u0000\u00d0\u00d2\u0005G\u0000\u0000\u00d1\u00d0\u0001\u0000\u0000\u0000"+
		"\u00d1\u00d2\u0001\u0000\u0000\u0000\u00d2\u00d3\u0001\u0000\u0000\u0000"+
		"\u00d3\u00d4\u0005H\u0000\u0000\u00d4\u0011\u0001\u0000\u0000\u0000\u0017"+
		"!&+FHNSfi~\u0083\u008b\u009a\u009c\u00a1\u00a9\u00ad\u00b1\u00b5\u00bd"+
		"\u00c2\u00c9\u00d1";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}