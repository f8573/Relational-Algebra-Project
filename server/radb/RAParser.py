# Generated from RAParser.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,74,214,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,
        0,1,0,1,0,1,0,3,0,34,8,0,1,0,1,0,1,0,3,0,39,8,0,1,0,1,0,1,0,3,0,
        44,8,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,
        0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,5,0,71,8,0,10,0,12,0,74,
        9,0,1,1,1,1,1,1,3,1,79,8,1,1,2,1,2,1,2,3,2,84,8,2,1,3,1,3,1,3,1,
        3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,103,8,
        3,1,3,3,3,106,8,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,
        3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,127,8,3,1,3,1,3,1,3,3,3,132,8,
        3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,140,8,3,1,3,1,3,1,3,1,3,1,3,1,3,1,
        3,1,3,1,3,1,3,1,3,1,3,1,3,5,3,155,8,3,10,3,12,3,158,9,3,1,4,1,4,
        3,4,162,8,4,1,4,1,4,1,4,1,5,1,5,1,5,3,5,170,8,5,1,5,1,5,3,5,174,
        8,5,1,5,1,5,3,5,178,8,5,1,5,1,5,3,5,182,8,5,1,5,1,5,1,5,1,5,1,5,
        1,5,3,5,190,8,5,1,6,1,6,1,6,3,6,195,8,6,1,6,1,6,1,7,5,7,200,8,7,
        10,7,12,7,203,9,7,1,7,1,7,1,8,1,8,1,8,3,8,210,8,8,1,8,1,8,1,8,0,
        2,0,6,9,0,2,4,6,8,10,12,14,16,0,14,1,0,46,47,1,0,48,49,1,0,57,62,
        2,0,23,23,35,35,2,0,21,21,36,36,2,0,22,22,37,37,2,0,24,24,43,43,
        2,0,29,32,38,38,2,0,28,28,39,39,2,0,26,26,40,40,2,0,41,41,49,49,
        2,0,27,27,42,42,2,0,25,25,55,55,2,0,34,34,46,46,255,0,43,1,0,0,0,
        2,75,1,0,0,0,4,80,1,0,0,0,6,131,1,0,0,0,8,161,1,0,0,0,10,189,1,0,
        0,0,12,194,1,0,0,0,14,201,1,0,0,0,16,206,1,0,0,0,18,19,6,0,-1,0,
        19,44,5,19,0,0,20,44,5,20,0,0,21,22,5,51,0,0,22,23,3,0,0,0,23,24,
        5,52,0,0,24,44,1,0,0,0,25,26,5,9,0,0,26,27,3,0,0,0,27,28,5,10,0,
        0,28,44,1,0,0,0,29,44,3,16,8,0,30,31,5,34,0,0,31,33,5,51,0,0,32,
        34,3,2,1,0,33,32,1,0,0,0,33,34,1,0,0,0,34,35,1,0,0,0,35,44,5,52,
        0,0,36,37,5,34,0,0,37,39,5,44,0,0,38,36,1,0,0,0,38,39,1,0,0,0,39,
        40,1,0,0,0,40,44,5,34,0,0,41,42,5,18,0,0,42,44,3,0,0,3,43,18,1,0,
        0,0,43,20,1,0,0,0,43,21,1,0,0,0,43,25,1,0,0,0,43,29,1,0,0,0,43,30,
        1,0,0,0,43,38,1,0,0,0,43,41,1,0,0,0,44,72,1,0,0,0,45,46,10,10,0,
        0,46,47,7,0,0,0,47,71,3,0,0,11,48,49,10,9,0,0,49,50,7,1,0,0,50,71,
        3,0,0,10,51,52,10,8,0,0,52,53,5,50,0,0,53,71,3,0,0,9,54,55,10,7,
        0,0,55,56,7,2,0,0,56,71,3,0,0,8,57,58,10,6,0,0,58,59,5,15,0,0,59,
        71,3,0,0,7,60,61,10,2,0,0,61,62,5,16,0,0,62,71,3,0,0,3,63,64,10,
        1,0,0,64,65,5,17,0,0,65,71,3,0,0,2,66,67,10,5,0,0,67,71,5,11,0,0,
        68,69,10,4,0,0,69,71,5,12,0,0,70,45,1,0,0,0,70,48,1,0,0,0,70,51,
        1,0,0,0,70,54,1,0,0,0,70,57,1,0,0,0,70,60,1,0,0,0,70,63,1,0,0,0,
        70,66,1,0,0,0,70,68,1,0,0,0,71,74,1,0,0,0,72,70,1,0,0,0,72,73,1,
        0,0,0,73,1,1,0,0,0,74,72,1,0,0,0,75,78,3,0,0,0,76,77,5,45,0,0,77,
        79,3,2,1,0,78,76,1,0,0,0,78,79,1,0,0,0,79,3,1,0,0,0,80,83,5,34,0,
        0,81,82,5,45,0,0,82,84,3,4,2,0,83,81,1,0,0,0,83,84,1,0,0,0,84,5,
        1,0,0,0,85,86,6,3,-1,0,86,87,5,51,0,0,87,88,3,6,3,0,88,89,5,52,0,
        0,89,132,1,0,0,0,90,91,5,9,0,0,91,92,3,6,3,0,92,93,5,10,0,0,93,132,
        1,0,0,0,94,132,5,34,0,0,95,132,3,16,8,0,96,97,7,3,0,0,97,105,5,53,
        0,0,98,99,5,34,0,0,99,102,5,56,0,0,100,103,5,46,0,0,101,103,3,4,
        2,0,102,100,1,0,0,0,102,101,1,0,0,0,103,106,1,0,0,0,104,106,3,4,
        2,0,105,98,1,0,0,0,105,104,1,0,0,0,106,107,1,0,0,0,107,108,5,54,
        0,0,108,132,3,6,3,9,109,110,7,4,0,0,110,111,5,53,0,0,111,112,3,2,
        1,0,112,113,5,54,0,0,113,114,3,6,3,8,114,132,1,0,0,0,115,116,7,5,
        0,0,116,117,5,53,0,0,117,118,3,0,0,0,118,119,5,54,0,0,119,120,3,
        6,3,7,120,132,1,0,0,0,121,122,7,6,0,0,122,123,5,53,0,0,123,126,3,
        2,1,0,124,125,5,56,0,0,125,127,3,2,1,0,126,124,1,0,0,0,126,127,1,
        0,0,0,127,128,1,0,0,0,128,129,5,54,0,0,129,130,3,6,3,1,130,132,1,
        0,0,0,131,85,1,0,0,0,131,90,1,0,0,0,131,94,1,0,0,0,131,95,1,0,0,
        0,131,96,1,0,0,0,131,109,1,0,0,0,131,115,1,0,0,0,131,121,1,0,0,0,
        132,156,1,0,0,0,133,134,10,6,0,0,134,139,7,7,0,0,135,136,5,53,0,
        0,136,137,3,0,0,0,137,138,5,54,0,0,138,140,1,0,0,0,139,135,1,0,0,
        0,139,140,1,0,0,0,140,141,1,0,0,0,141,155,3,6,3,7,142,143,10,5,0,
        0,143,144,7,8,0,0,144,155,3,6,3,6,145,146,10,4,0,0,146,147,7,9,0,
        0,147,155,3,6,3,5,148,149,10,3,0,0,149,150,7,10,0,0,150,155,3,6,
        3,4,151,152,10,2,0,0,152,153,7,11,0,0,153,155,3,6,3,3,154,133,1,
        0,0,0,154,142,1,0,0,0,154,145,1,0,0,0,154,148,1,0,0,0,154,151,1,
        0,0,0,155,158,1,0,0,0,156,154,1,0,0,0,156,157,1,0,0,0,157,7,1,0,
        0,0,158,156,1,0,0,0,159,162,5,34,0,0,160,162,3,16,8,0,161,159,1,
        0,0,0,161,160,1,0,0,0,162,163,1,0,0,0,163,164,7,12,0,0,164,165,3,
        6,3,0,165,9,1,0,0,0,166,190,5,63,0,0,167,173,5,64,0,0,168,170,5,
        5,0,0,169,168,1,0,0,0,169,170,1,0,0,0,170,171,1,0,0,0,171,174,5,
        34,0,0,172,174,5,46,0,0,173,169,1,0,0,0,173,172,1,0,0,0,174,190,
        1,0,0,0,175,177,5,65,0,0,176,178,5,5,0,0,177,176,1,0,0,0,177,178,
        1,0,0,0,178,179,1,0,0,0,179,181,7,13,0,0,180,182,5,19,0,0,181,180,
        1,0,0,0,181,182,1,0,0,0,182,190,1,0,0,0,183,184,5,66,0,0,184,190,
        5,19,0,0,185,190,5,67,0,0,186,190,5,68,0,0,187,188,5,69,0,0,188,
        190,5,73,0,0,189,166,1,0,0,0,189,167,1,0,0,0,189,175,1,0,0,0,189,
        183,1,0,0,0,189,185,1,0,0,0,189,186,1,0,0,0,189,187,1,0,0,0,190,
        11,1,0,0,0,191,195,3,6,3,0,192,195,3,8,4,0,193,195,3,10,5,0,194,
        191,1,0,0,0,194,192,1,0,0,0,194,193,1,0,0,0,195,196,1,0,0,0,196,
        197,5,4,0,0,197,13,1,0,0,0,198,200,3,12,6,0,199,198,1,0,0,0,200,
        203,1,0,0,0,201,199,1,0,0,0,201,202,1,0,0,0,202,204,1,0,0,0,203,
        201,1,0,0,0,204,205,5,0,0,1,205,15,1,0,0,0,206,207,5,33,0,0,207,
        209,5,70,0,0,208,210,5,71,0,0,209,208,1,0,0,0,209,210,1,0,0,0,210,
        211,1,0,0,0,211,212,5,72,0,0,212,17,1,0,0,0,23,33,38,43,70,72,78,
        83,102,105,126,131,139,154,156,161,169,173,177,181,189,194,201,209
    ]

class RAParser ( Parser ):

    grammarFileName = "RAParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "';'", "'!'", "'\\left'", "'\\right'", "'\\space'", 
                     "'\\{'", "'\\}'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'\\pi'", "'\\sigma'", 
                     "'\\rho'", "'\\gamma'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'\\u22C8'", "'\\u27D5'", "'\\u27D6'", 
                     "'\\u27D7'", "'\\text'", "<INVALID>", "'\\rename'", 
                     "'\\project'", "'\\select'", "'\\join'", "'\\cross'", 
                     "'\\union'", "'\\diff'", "'\\intersect'", "'\\aggr'", 
                     "'.'", "','", "'*'", "'/'", "'+'", "'-'", "'||'", "'('", 
                     "')'", "'_{'", "<INVALID>", "':-'", "':'", "'<='", 
                     "'<>'", "'>='", "'<'", "'='", "'>'", "'\\list'", "'\\clear'", 
                     "'\\save'", "'\\source'", "'\\help'", "'\\quit'", "'\\sqlexec'", 
                     "'{'" ]

    symbolicNames = [ "<INVALID>", "WS", "COMMENT", "LINE_COMMENT", "TERMINATOR", 
                      "FORCE", "LEFT", "RIGHT", "SPACE_CMD", "LBRACE_ESC", 
                      "RBRACE_ESC", "IS_NULL", "IS_NOT_NULL", "IS", "NULL", 
                      "LIKE", "AND", "OR", "NOT", "STRING", "NUMBER", "PI", 
                      "SIGMA", "RHO", "GAMMA", "LEFT_ARROW", "CUP", "CAP", 
                      "TIMES", "NATURAL_JOIN_SYMBOL", "LEFT_OUTER_JOIN", 
                      "RIGHT_OUTER_JOIN", "FULL_OUTER_JOIN", "TEXT_CMD", 
                      "ID", "RENAME", "PROJECT", "SELECT", "JOIN", "CROSS", 
                      "UNION", "DIFF", "INTERSECT", "AGGR", "DOT", "COMMA", 
                      "STAR", "SLASH", "PLUS", "MINUS", "CONCAT", "PAREN_L", 
                      "PAREN_R", "ARG_L", "ARG_R", "GETS", "COLON", "LE", 
                      "NE", "GE", "LT", "EQ", "GT", "LIST", "CLEAR", "SAVE", 
                      "SOURCE", "HELP", "QUIT", "SQLEXEC", "TEXT_LBRACE", 
                      "TEXT_CONTENT", "TEXT_RBRACE", "SQLEXEC_CONTENT", 
                      "ARG_R_SQL" ]

    RULE_valExpr = 0
    RULE_listOfValExprs = 1
    RULE_listOfIDs = 2
    RULE_relExpr = 3
    RULE_definition = 4
    RULE_command = 5
    RULE_statement = 6
    RULE_program = 7
    RULE_textAtom = 8

    ruleNames =  [ "valExpr", "listOfValExprs", "listOfIDs", "relExpr", 
                   "definition", "command", "statement", "program", "textAtom" ]

    EOF = Token.EOF
    WS=1
    COMMENT=2
    LINE_COMMENT=3
    TERMINATOR=4
    FORCE=5
    LEFT=6
    RIGHT=7
    SPACE_CMD=8
    LBRACE_ESC=9
    RBRACE_ESC=10
    IS_NULL=11
    IS_NOT_NULL=12
    IS=13
    NULL=14
    LIKE=15
    AND=16
    OR=17
    NOT=18
    STRING=19
    NUMBER=20
    PI=21
    SIGMA=22
    RHO=23
    GAMMA=24
    LEFT_ARROW=25
    CUP=26
    CAP=27
    TIMES=28
    NATURAL_JOIN_SYMBOL=29
    LEFT_OUTER_JOIN=30
    RIGHT_OUTER_JOIN=31
    FULL_OUTER_JOIN=32
    TEXT_CMD=33
    ID=34
    RENAME=35
    PROJECT=36
    SELECT=37
    JOIN=38
    CROSS=39
    UNION=40
    DIFF=41
    INTERSECT=42
    AGGR=43
    DOT=44
    COMMA=45
    STAR=46
    SLASH=47
    PLUS=48
    MINUS=49
    CONCAT=50
    PAREN_L=51
    PAREN_R=52
    ARG_L=53
    ARG_R=54
    GETS=55
    COLON=56
    LE=57
    NE=58
    GE=59
    LT=60
    EQ=61
    GT=62
    LIST=63
    CLEAR=64
    SAVE=65
    SOURCE=66
    HELP=67
    QUIT=68
    SQLEXEC=69
    TEXT_LBRACE=70
    TEXT_CONTENT=71
    TEXT_RBRACE=72
    SQLEXEC_CONTENT=73
    ARG_R_SQL=74

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ValExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return RAParser.RULE_valExpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class NumberLiteralValExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(RAParser.NUMBER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberLiteralValExpr" ):
                listener.enterNumberLiteralValExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberLiteralValExpr" ):
                listener.exitNumberLiteralValExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberLiteralValExpr" ):
                return visitor.visitNumberLiteralValExpr(self)
            else:
                return visitor.visitChildren(self)


    class TextValExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def textAtom(self):
            return self.getTypedRuleContext(RAParser.TextAtomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTextValExpr" ):
                listener.enterTextValExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTextValExpr" ):
                listener.exitTextValExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTextValExpr" ):
                return visitor.visitTextValExpr(self)
            else:
                return visitor.visitChildren(self)


    class IsNotNullExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self):
            return self.getTypedRuleContext(RAParser.ValExprContext,0)

        def IS_NOT_NULL(self):
            return self.getToken(RAParser.IS_NOT_NULL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIsNotNullExpr" ):
                listener.enterIsNotNullExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIsNotNullExpr" ):
                listener.exitIsNotNullExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIsNotNullExpr" ):
                return visitor.visitIsNotNullExpr(self)
            else:
                return visitor.visitChildren(self)


    class FuncExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(RAParser.ID, 0)
        def PAREN_L(self):
            return self.getToken(RAParser.PAREN_L, 0)
        def PAREN_R(self):
            return self.getToken(RAParser.PAREN_R, 0)
        def listOfValExprs(self):
            return self.getTypedRuleContext(RAParser.ListOfValExprsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncExpr" ):
                listener.enterFuncExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncExpr" ):
                listener.exitFuncExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncExpr" ):
                return visitor.visitFuncExpr(self)
            else:
                return visitor.visitChildren(self)


    class AttrRefContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(RAParser.ID)
            else:
                return self.getToken(RAParser.ID, i)
        def DOT(self):
            return self.getToken(RAParser.DOT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttrRef" ):
                listener.enterAttrRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttrRef" ):
                listener.exitAttrRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttrRef" ):
                return visitor.visitAttrRef(self)
            else:
                return visitor.visitChildren(self)


    class PlusMinusExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.ValExprContext)
            else:
                return self.getTypedRuleContext(RAParser.ValExprContext,i)

        def PLUS(self):
            return self.getToken(RAParser.PLUS, 0)
        def MINUS(self):
            return self.getToken(RAParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlusMinusExpr" ):
                listener.enterPlusMinusExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlusMinusExpr" ):
                listener.exitPlusMinusExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPlusMinusExpr" ):
                return visitor.visitPlusMinusExpr(self)
            else:
                return visitor.visitChildren(self)


    class OrExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.ValExprContext)
            else:
                return self.getTypedRuleContext(RAParser.ValExprContext,i)

        def OR(self):
            return self.getToken(RAParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpr" ):
                listener.enterOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpr" ):
                listener.exitOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)


    class ValExprBracedContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACE_ESC(self):
            return self.getToken(RAParser.LBRACE_ESC, 0)
        def valExpr(self):
            return self.getTypedRuleContext(RAParser.ValExprContext,0)

        def RBRACE_ESC(self):
            return self.getToken(RAParser.RBRACE_ESC, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValExprBraced" ):
                listener.enterValExprBraced(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValExprBraced" ):
                listener.exitValExprBraced(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValExprBraced" ):
                return visitor.visitValExprBraced(self)
            else:
                return visitor.visitChildren(self)


    class ValExprParenthesizedContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PAREN_L(self):
            return self.getToken(RAParser.PAREN_L, 0)
        def valExpr(self):
            return self.getTypedRuleContext(RAParser.ValExprContext,0)

        def PAREN_R(self):
            return self.getToken(RAParser.PAREN_R, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValExprParenthesized" ):
                listener.enterValExprParenthesized(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValExprParenthesized" ):
                listener.exitValExprParenthesized(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValExprParenthesized" ):
                return visitor.visitValExprParenthesized(self)
            else:
                return visitor.visitChildren(self)


    class ConcatExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.ValExprContext)
            else:
                return self.getTypedRuleContext(RAParser.ValExprContext,i)

        def CONCAT(self):
            return self.getToken(RAParser.CONCAT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConcatExpr" ):
                listener.enterConcatExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConcatExpr" ):
                listener.exitConcatExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConcatExpr" ):
                return visitor.visitConcatExpr(self)
            else:
                return visitor.visitChildren(self)


    class NotExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(RAParser.NOT, 0)
        def valExpr(self):
            return self.getTypedRuleContext(RAParser.ValExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNotExpr" ):
                listener.enterNotExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNotExpr" ):
                listener.exitNotExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotExpr" ):
                return visitor.visitNotExpr(self)
            else:
                return visitor.visitChildren(self)


    class IsNullExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self):
            return self.getTypedRuleContext(RAParser.ValExprContext,0)

        def IS_NULL(self):
            return self.getToken(RAParser.IS_NULL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIsNullExpr" ):
                listener.enterIsNullExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIsNullExpr" ):
                listener.exitIsNullExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIsNullExpr" ):
                return visitor.visitIsNullExpr(self)
            else:
                return visitor.visitChildren(self)


    class StringLiteralValExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(RAParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringLiteralValExpr" ):
                listener.enterStringLiteralValExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringLiteralValExpr" ):
                listener.exitStringLiteralValExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLiteralValExpr" ):
                return visitor.visitStringLiteralValExpr(self)
            else:
                return visitor.visitChildren(self)


    class LikeExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.ValExprContext)
            else:
                return self.getTypedRuleContext(RAParser.ValExprContext,i)

        def LIKE(self):
            return self.getToken(RAParser.LIKE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLikeExpr" ):
                listener.enterLikeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLikeExpr" ):
                listener.exitLikeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLikeExpr" ):
                return visitor.visitLikeExpr(self)
            else:
                return visitor.visitChildren(self)


    class MultDivExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.ValExprContext)
            else:
                return self.getTypedRuleContext(RAParser.ValExprContext,i)

        def STAR(self):
            return self.getToken(RAParser.STAR, 0)
        def SLASH(self):
            return self.getToken(RAParser.SLASH, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultDivExpr" ):
                listener.enterMultDivExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultDivExpr" ):
                listener.exitMultDivExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultDivExpr" ):
                return visitor.visitMultDivExpr(self)
            else:
                return visitor.visitChildren(self)


    class CompareExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.ValExprContext)
            else:
                return self.getTypedRuleContext(RAParser.ValExprContext,i)

        def LT(self):
            return self.getToken(RAParser.LT, 0)
        def LE(self):
            return self.getToken(RAParser.LE, 0)
        def EQ(self):
            return self.getToken(RAParser.EQ, 0)
        def NE(self):
            return self.getToken(RAParser.NE, 0)
        def GE(self):
            return self.getToken(RAParser.GE, 0)
        def GT(self):
            return self.getToken(RAParser.GT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompareExpr" ):
                listener.enterCompareExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompareExpr" ):
                listener.exitCompareExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompareExpr" ):
                return visitor.visitCompareExpr(self)
            else:
                return visitor.visitChildren(self)


    class AndExprContext(ValExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.ValExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def valExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.ValExprContext)
            else:
                return self.getTypedRuleContext(RAParser.ValExprContext,i)

        def AND(self):
            return self.getToken(RAParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpr" ):
                listener.enterAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpr" ):
                listener.exitAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)



    def valExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RAParser.ValExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_valExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = RAParser.StringLiteralValExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 19
                self.match(RAParser.STRING)
                pass

            elif la_ == 2:
                localctx = RAParser.NumberLiteralValExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 20
                self.match(RAParser.NUMBER)
                pass

            elif la_ == 3:
                localctx = RAParser.ValExprParenthesizedContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 21
                self.match(RAParser.PAREN_L)
                self.state = 22
                self.valExpr(0)
                self.state = 23
                self.match(RAParser.PAREN_R)
                pass

            elif la_ == 4:
                localctx = RAParser.ValExprBracedContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 25
                self.match(RAParser.LBRACE_ESC)
                self.state = 26
                self.valExpr(0)
                self.state = 27
                self.match(RAParser.RBRACE_ESC)
                pass

            elif la_ == 5:
                localctx = RAParser.TextValExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 29
                self.textAtom()
                pass

            elif la_ == 6:
                localctx = RAParser.FuncExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 30
                self.match(RAParser.ID)
                self.state = 31
                self.match(RAParser.PAREN_L)
                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 2251825585324544) != 0):
                    self.state = 32
                    self.listOfValExprs()


                self.state = 35
                self.match(RAParser.PAREN_R)
                pass

            elif la_ == 7:
                localctx = RAParser.AttrRefContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 38
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                if la_ == 1:
                    self.state = 36
                    self.match(RAParser.ID)
                    self.state = 37
                    self.match(RAParser.DOT)


                self.state = 40
                self.match(RAParser.ID)
                pass

            elif la_ == 8:
                localctx = RAParser.NotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 41
                self.match(RAParser.NOT)
                self.state = 42
                self.valExpr(3)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 72
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 70
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        localctx = RAParser.MultDivExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 45
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 46
                        _la = self._input.LA(1)
                        if not(_la==46 or _la==47):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 47
                        self.valExpr(11)
                        pass

                    elif la_ == 2:
                        localctx = RAParser.PlusMinusExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 48
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 49
                        _la = self._input.LA(1)
                        if not(_la==48 or _la==49):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 50
                        self.valExpr(10)
                        pass

                    elif la_ == 3:
                        localctx = RAParser.ConcatExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 51
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 52
                        self.match(RAParser.CONCAT)
                        self.state = 53
                        self.valExpr(9)
                        pass

                    elif la_ == 4:
                        localctx = RAParser.CompareExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 54
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 55
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 9079256848778919936) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 56
                        self.valExpr(8)
                        pass

                    elif la_ == 5:
                        localctx = RAParser.LikeExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 57
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 58
                        self.match(RAParser.LIKE)
                        self.state = 59
                        self.valExpr(7)
                        pass

                    elif la_ == 6:
                        localctx = RAParser.AndExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 60
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 61
                        self.match(RAParser.AND)
                        self.state = 62
                        self.valExpr(3)
                        pass

                    elif la_ == 7:
                        localctx = RAParser.OrExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 63
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 64
                        self.match(RAParser.OR)
                        self.state = 65
                        self.valExpr(2)
                        pass

                    elif la_ == 8:
                        localctx = RAParser.IsNullExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 66
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 67
                        self.match(RAParser.IS_NULL)
                        pass

                    elif la_ == 9:
                        localctx = RAParser.IsNotNullExprContext(self, RAParser.ValExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_valExpr)
                        self.state = 68
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 69
                        self.match(RAParser.IS_NOT_NULL)
                        pass

             
                self.state = 74
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ListOfValExprsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def valExpr(self):
            return self.getTypedRuleContext(RAParser.ValExprContext,0)


        def COMMA(self):
            return self.getToken(RAParser.COMMA, 0)

        def listOfValExprs(self):
            return self.getTypedRuleContext(RAParser.ListOfValExprsContext,0)


        def getRuleIndex(self):
            return RAParser.RULE_listOfValExprs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListOfValExprs" ):
                listener.enterListOfValExprs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListOfValExprs" ):
                listener.exitListOfValExprs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListOfValExprs" ):
                return visitor.visitListOfValExprs(self)
            else:
                return visitor.visitChildren(self)




    def listOfValExprs(self):

        localctx = RAParser.ListOfValExprsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_listOfValExprs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.valExpr(0)
            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 76
                self.match(RAParser.COMMA)
                self.state = 77
                self.listOfValExprs()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListOfIDsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(RAParser.ID, 0)

        def COMMA(self):
            return self.getToken(RAParser.COMMA, 0)

        def listOfIDs(self):
            return self.getTypedRuleContext(RAParser.ListOfIDsContext,0)


        def getRuleIndex(self):
            return RAParser.RULE_listOfIDs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListOfIDs" ):
                listener.enterListOfIDs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListOfIDs" ):
                listener.exitListOfIDs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListOfIDs" ):
                return visitor.visitListOfIDs(self)
            else:
                return visitor.visitChildren(self)




    def listOfIDs(self):

        localctx = RAParser.ListOfIDsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_listOfIDs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(RAParser.ID)
            self.state = 83
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 81
                self.match(RAParser.COMMA)
                self.state = 82
                self.listOfIDs()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return RAParser.RULE_relExpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class IntersectExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.RelExprContext)
            else:
                return self.getTypedRuleContext(RAParser.RelExprContext,i)

        def INTERSECT(self):
            return self.getToken(RAParser.INTERSECT, 0)
        def CAP(self):
            return self.getToken(RAParser.CAP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIntersectExpr" ):
                listener.enterIntersectExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIntersectExpr" ):
                listener.exitIntersectExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIntersectExpr" ):
                return visitor.visitIntersectExpr(self)
            else:
                return visitor.visitChildren(self)


    class TextRelExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def textAtom(self):
            return self.getTypedRuleContext(RAParser.TextAtomContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTextRelExpr" ):
                listener.enterTextRelExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTextRelExpr" ):
                listener.exitTextRelExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTextRelExpr" ):
                return visitor.visitTextRelExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelExprParenthesizedContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PAREN_L(self):
            return self.getToken(RAParser.PAREN_L, 0)
        def relExpr(self):
            return self.getTypedRuleContext(RAParser.RelExprContext,0)

        def PAREN_R(self):
            return self.getToken(RAParser.PAREN_R, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelExprParenthesized" ):
                listener.enterRelExprParenthesized(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelExprParenthesized" ):
                listener.exitRelExprParenthesized(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelExprParenthesized" ):
                return visitor.visitRelExprParenthesized(self)
            else:
                return visitor.visitChildren(self)


    class DiffExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.RelExprContext)
            else:
                return self.getTypedRuleContext(RAParser.RelExprContext,i)

        def DIFF(self):
            return self.getToken(RAParser.DIFF, 0)
        def MINUS(self):
            return self.getToken(RAParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDiffExpr" ):
                listener.enterDiffExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDiffExpr" ):
                listener.exitDiffExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDiffExpr" ):
                return visitor.visitDiffExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnionExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.RelExprContext)
            else:
                return self.getTypedRuleContext(RAParser.RelExprContext,i)

        def UNION(self):
            return self.getToken(RAParser.UNION, 0)
        def CUP(self):
            return self.getToken(RAParser.CUP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnionExpr" ):
                listener.enterUnionExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnionExpr" ):
                listener.exitUnionExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnionExpr" ):
                return visitor.visitUnionExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelRefContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(RAParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelRef" ):
                listener.enterRelRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelRef" ):
                listener.exitRelRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelRef" ):
                return visitor.visitRelRef(self)
            else:
                return visitor.visitChildren(self)


    class RenameExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ARG_L(self):
            return self.getToken(RAParser.ARG_L, 0)
        def ARG_R(self):
            return self.getToken(RAParser.ARG_R, 0)
        def relExpr(self):
            return self.getTypedRuleContext(RAParser.RelExprContext,0)

        def RENAME(self):
            return self.getToken(RAParser.RENAME, 0)
        def RHO(self):
            return self.getToken(RAParser.RHO, 0)
        def listOfIDs(self):
            return self.getTypedRuleContext(RAParser.ListOfIDsContext,0)

        def ID(self):
            return self.getToken(RAParser.ID, 0)
        def COLON(self):
            return self.getToken(RAParser.COLON, 0)
        def STAR(self):
            return self.getToken(RAParser.STAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRenameExpr" ):
                listener.enterRenameExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRenameExpr" ):
                listener.exitRenameExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRenameExpr" ):
                return visitor.visitRenameExpr(self)
            else:
                return visitor.visitChildren(self)


    class JoinExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.RelExprContext)
            else:
                return self.getTypedRuleContext(RAParser.RelExprContext,i)

        def JOIN(self):
            return self.getToken(RAParser.JOIN, 0)
        def NATURAL_JOIN_SYMBOL(self):
            return self.getToken(RAParser.NATURAL_JOIN_SYMBOL, 0)
        def LEFT_OUTER_JOIN(self):
            return self.getToken(RAParser.LEFT_OUTER_JOIN, 0)
        def RIGHT_OUTER_JOIN(self):
            return self.getToken(RAParser.RIGHT_OUTER_JOIN, 0)
        def FULL_OUTER_JOIN(self):
            return self.getToken(RAParser.FULL_OUTER_JOIN, 0)
        def ARG_L(self):
            return self.getToken(RAParser.ARG_L, 0)
        def valExpr(self):
            return self.getTypedRuleContext(RAParser.ValExprContext,0)

        def ARG_R(self):
            return self.getToken(RAParser.ARG_R, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJoinExpr" ):
                listener.enterJoinExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJoinExpr" ):
                listener.exitJoinExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJoinExpr" ):
                return visitor.visitJoinExpr(self)
            else:
                return visitor.visitChildren(self)


    class SelectExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ARG_L(self):
            return self.getToken(RAParser.ARG_L, 0)
        def valExpr(self):
            return self.getTypedRuleContext(RAParser.ValExprContext,0)

        def ARG_R(self):
            return self.getToken(RAParser.ARG_R, 0)
        def relExpr(self):
            return self.getTypedRuleContext(RAParser.RelExprContext,0)

        def SELECT(self):
            return self.getToken(RAParser.SELECT, 0)
        def SIGMA(self):
            return self.getToken(RAParser.SIGMA, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSelectExpr" ):
                listener.enterSelectExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSelectExpr" ):
                listener.exitSelectExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectExpr" ):
                return visitor.visitSelectExpr(self)
            else:
                return visitor.visitChildren(self)


    class CrossExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def relExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.RelExprContext)
            else:
                return self.getTypedRuleContext(RAParser.RelExprContext,i)

        def CROSS(self):
            return self.getToken(RAParser.CROSS, 0)
        def TIMES(self):
            return self.getToken(RAParser.TIMES, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCrossExpr" ):
                listener.enterCrossExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCrossExpr" ):
                listener.exitCrossExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCrossExpr" ):
                return visitor.visitCrossExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelExprBracedContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACE_ESC(self):
            return self.getToken(RAParser.LBRACE_ESC, 0)
        def relExpr(self):
            return self.getTypedRuleContext(RAParser.RelExprContext,0)

        def RBRACE_ESC(self):
            return self.getToken(RAParser.RBRACE_ESC, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelExprBraced" ):
                listener.enterRelExprBraced(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelExprBraced" ):
                listener.exitRelExprBraced(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelExprBraced" ):
                return visitor.visitRelExprBraced(self)
            else:
                return visitor.visitChildren(self)


    class AggrExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ARG_L(self):
            return self.getToken(RAParser.ARG_L, 0)
        def listOfValExprs(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.ListOfValExprsContext)
            else:
                return self.getTypedRuleContext(RAParser.ListOfValExprsContext,i)

        def ARG_R(self):
            return self.getToken(RAParser.ARG_R, 0)
        def relExpr(self):
            return self.getTypedRuleContext(RAParser.RelExprContext,0)

        def AGGR(self):
            return self.getToken(RAParser.AGGR, 0)
        def GAMMA(self):
            return self.getToken(RAParser.GAMMA, 0)
        def COLON(self):
            return self.getToken(RAParser.COLON, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAggrExpr" ):
                listener.enterAggrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAggrExpr" ):
                listener.exitAggrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAggrExpr" ):
                return visitor.visitAggrExpr(self)
            else:
                return visitor.visitChildren(self)


    class ProjectExprContext(RelExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.RelExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ARG_L(self):
            return self.getToken(RAParser.ARG_L, 0)
        def listOfValExprs(self):
            return self.getTypedRuleContext(RAParser.ListOfValExprsContext,0)

        def ARG_R(self):
            return self.getToken(RAParser.ARG_R, 0)
        def relExpr(self):
            return self.getTypedRuleContext(RAParser.RelExprContext,0)

        def PROJECT(self):
            return self.getToken(RAParser.PROJECT, 0)
        def PI(self):
            return self.getToken(RAParser.PI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProjectExpr" ):
                listener.enterProjectExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProjectExpr" ):
                listener.exitProjectExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProjectExpr" ):
                return visitor.visitProjectExpr(self)
            else:
                return visitor.visitChildren(self)



    def relExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = RAParser.RelExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_relExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [51]:
                localctx = RAParser.RelExprParenthesizedContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 86
                self.match(RAParser.PAREN_L)
                self.state = 87
                self.relExpr(0)
                self.state = 88
                self.match(RAParser.PAREN_R)
                pass
            elif token in [9]:
                localctx = RAParser.RelExprBracedContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 90
                self.match(RAParser.LBRACE_ESC)
                self.state = 91
                self.relExpr(0)
                self.state = 92
                self.match(RAParser.RBRACE_ESC)
                pass
            elif token in [34]:
                localctx = RAParser.RelRefContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 94
                self.match(RAParser.ID)
                pass
            elif token in [33]:
                localctx = RAParser.TextRelExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 95
                self.textAtom()
                pass
            elif token in [23, 35]:
                localctx = RAParser.RenameExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 96
                _la = self._input.LA(1)
                if not(_la==23 or _la==35):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 97
                self.match(RAParser.ARG_L)
                self.state = 105
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                if la_ == 1:
                    self.state = 98
                    self.match(RAParser.ID)
                    self.state = 99
                    self.match(RAParser.COLON)
                    self.state = 102
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [46]:
                        self.state = 100
                        self.match(RAParser.STAR)
                        pass
                    elif token in [34]:
                        self.state = 101
                        self.listOfIDs()
                        pass
                    else:
                        raise NoViableAltException(self)

                    pass

                elif la_ == 2:
                    self.state = 104
                    self.listOfIDs()
                    pass


                self.state = 107
                self.match(RAParser.ARG_R)
                self.state = 108
                self.relExpr(9)
                pass
            elif token in [21, 36]:
                localctx = RAParser.ProjectExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 109
                _la = self._input.LA(1)
                if not(_la==21 or _la==36):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 110
                self.match(RAParser.ARG_L)
                self.state = 111
                self.listOfValExprs()
                self.state = 112
                self.match(RAParser.ARG_R)
                self.state = 113
                self.relExpr(8)
                pass
            elif token in [22, 37]:
                localctx = RAParser.SelectExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 115
                _la = self._input.LA(1)
                if not(_la==22 or _la==37):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 116
                self.match(RAParser.ARG_L)
                self.state = 117
                self.valExpr(0)
                self.state = 118
                self.match(RAParser.ARG_R)
                self.state = 119
                self.relExpr(7)
                pass
            elif token in [24, 43]:
                localctx = RAParser.AggrExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 121
                _la = self._input.LA(1)
                if not(_la==24 or _la==43):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 122
                self.match(RAParser.ARG_L)
                self.state = 123
                self.listOfValExprs()
                self.state = 126
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==56:
                    self.state = 124
                    self.match(RAParser.COLON)
                    self.state = 125
                    self.listOfValExprs()


                self.state = 128
                self.match(RAParser.ARG_R)
                self.state = 129
                self.relExpr(1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 156
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,13,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 154
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
                    if la_ == 1:
                        localctx = RAParser.JoinExprContext(self, RAParser.RelExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relExpr)
                        self.state = 133
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 134
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 282930970624) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 139
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==53:
                            self.state = 135
                            self.match(RAParser.ARG_L)
                            self.state = 136
                            self.valExpr(0)
                            self.state = 137
                            self.match(RAParser.ARG_R)


                        self.state = 141
                        self.relExpr(7)
                        pass

                    elif la_ == 2:
                        localctx = RAParser.CrossExprContext(self, RAParser.RelExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relExpr)
                        self.state = 142
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 143
                        _la = self._input.LA(1)
                        if not(_la==28 or _la==39):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 144
                        self.relExpr(6)
                        pass

                    elif la_ == 3:
                        localctx = RAParser.UnionExprContext(self, RAParser.RelExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relExpr)
                        self.state = 145
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 146
                        _la = self._input.LA(1)
                        if not(_la==26 or _la==40):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 147
                        self.relExpr(5)
                        pass

                    elif la_ == 4:
                        localctx = RAParser.DiffExprContext(self, RAParser.RelExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relExpr)
                        self.state = 148
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 149
                        _la = self._input.LA(1)
                        if not(_la==41 or _la==49):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 150
                        self.relExpr(4)
                        pass

                    elif la_ == 5:
                        localctx = RAParser.IntersectExprContext(self, RAParser.RelExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_relExpr)
                        self.state = 151
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 152
                        _la = self._input.LA(1)
                        if not(_la==27 or _la==42):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 153
                        self.relExpr(3)
                        pass

             
                self.state = 158
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,13,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class DefinitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relExpr(self):
            return self.getTypedRuleContext(RAParser.RelExprContext,0)


        def GETS(self):
            return self.getToken(RAParser.GETS, 0)

        def LEFT_ARROW(self):
            return self.getToken(RAParser.LEFT_ARROW, 0)

        def ID(self):
            return self.getToken(RAParser.ID, 0)

        def textAtom(self):
            return self.getTypedRuleContext(RAParser.TextAtomContext,0)


        def getRuleIndex(self):
            return RAParser.RULE_definition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefinition" ):
                listener.enterDefinition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefinition" ):
                listener.exitDefinition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefinition" ):
                return visitor.visitDefinition(self)
            else:
                return visitor.visitChildren(self)




    def definition(self):

        localctx = RAParser.DefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_definition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [34]:
                self.state = 159
                self.match(RAParser.ID)
                pass
            elif token in [33]:
                self.state = 160
                self.textAtom()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 163
            _la = self._input.LA(1)
            if not(_la==25 or _la==55):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 164
            self.relExpr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return RAParser.RULE_command

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ListCommandContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LIST(self):
            return self.getToken(RAParser.LIST, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListCommand" ):
                listener.enterListCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListCommand" ):
                listener.exitListCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListCommand" ):
                return visitor.visitListCommand(self)
            else:
                return visitor.visitChildren(self)


    class ClearCommandContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CLEAR(self):
            return self.getToken(RAParser.CLEAR, 0)
        def ID(self):
            return self.getToken(RAParser.ID, 0)
        def STAR(self):
            return self.getToken(RAParser.STAR, 0)
        def FORCE(self):
            return self.getToken(RAParser.FORCE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClearCommand" ):
                listener.enterClearCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClearCommand" ):
                listener.exitClearCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClearCommand" ):
                return visitor.visitClearCommand(self)
            else:
                return visitor.visitChildren(self)


    class QuitCommandContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def QUIT(self):
            return self.getToken(RAParser.QUIT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuitCommand" ):
                listener.enterQuitCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuitCommand" ):
                listener.exitQuitCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuitCommand" ):
                return visitor.visitQuitCommand(self)
            else:
                return visitor.visitChildren(self)


    class SourceCommandContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SOURCE(self):
            return self.getToken(RAParser.SOURCE, 0)
        def STRING(self):
            return self.getToken(RAParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSourceCommand" ):
                listener.enterSourceCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSourceCommand" ):
                listener.exitSourceCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSourceCommand" ):
                return visitor.visitSourceCommand(self)
            else:
                return visitor.visitChildren(self)


    class HelpCommandContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def HELP(self):
            return self.getToken(RAParser.HELP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHelpCommand" ):
                listener.enterHelpCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHelpCommand" ):
                listener.exitHelpCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHelpCommand" ):
                return visitor.visitHelpCommand(self)
            else:
                return visitor.visitChildren(self)


    class SaveCommandContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SAVE(self):
            return self.getToken(RAParser.SAVE, 0)
        def ID(self):
            return self.getToken(RAParser.ID, 0)
        def STAR(self):
            return self.getToken(RAParser.STAR, 0)
        def FORCE(self):
            return self.getToken(RAParser.FORCE, 0)
        def STRING(self):
            return self.getToken(RAParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSaveCommand" ):
                listener.enterSaveCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSaveCommand" ):
                listener.exitSaveCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSaveCommand" ):
                return visitor.visitSaveCommand(self)
            else:
                return visitor.visitChildren(self)


    class SqlexecCommandContext(CommandContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a RAParser.CommandContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SQLEXEC(self):
            return self.getToken(RAParser.SQLEXEC, 0)
        def SQLEXEC_CONTENT(self):
            return self.getToken(RAParser.SQLEXEC_CONTENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSqlexecCommand" ):
                listener.enterSqlexecCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSqlexecCommand" ):
                listener.exitSqlexecCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSqlexecCommand" ):
                return visitor.visitSqlexecCommand(self)
            else:
                return visitor.visitChildren(self)



    def command(self):

        localctx = RAParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_command)
        self._la = 0 # Token type
        try:
            self.state = 189
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [63]:
                localctx = RAParser.ListCommandContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 166
                self.match(RAParser.LIST)
                pass
            elif token in [64]:
                localctx = RAParser.ClearCommandContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 167
                self.match(RAParser.CLEAR)
                self.state = 173
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [5, 34]:
                    self.state = 169
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==5:
                        self.state = 168
                        self.match(RAParser.FORCE)


                    self.state = 171
                    self.match(RAParser.ID)
                    pass
                elif token in [46]:
                    self.state = 172
                    self.match(RAParser.STAR)
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            elif token in [65]:
                localctx = RAParser.SaveCommandContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 175
                self.match(RAParser.SAVE)
                self.state = 177
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==5:
                    self.state = 176
                    self.match(RAParser.FORCE)


                self.state = 179
                _la = self._input.LA(1)
                if not(_la==34 or _la==46):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 181
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==19:
                    self.state = 180
                    self.match(RAParser.STRING)


                pass
            elif token in [66]:
                localctx = RAParser.SourceCommandContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 183
                self.match(RAParser.SOURCE)
                self.state = 184
                self.match(RAParser.STRING)
                pass
            elif token in [67]:
                localctx = RAParser.HelpCommandContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 185
                self.match(RAParser.HELP)
                pass
            elif token in [68]:
                localctx = RAParser.QuitCommandContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 186
                self.match(RAParser.QUIT)
                pass
            elif token in [69]:
                localctx = RAParser.SqlexecCommandContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 187
                self.match(RAParser.SQLEXEC)
                self.state = 188
                self.match(RAParser.SQLEXEC_CONTENT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TERMINATOR(self):
            return self.getToken(RAParser.TERMINATOR, 0)

        def relExpr(self):
            return self.getTypedRuleContext(RAParser.RelExprContext,0)


        def definition(self):
            return self.getTypedRuleContext(RAParser.DefinitionContext,0)


        def command(self):
            return self.getTypedRuleContext(RAParser.CommandContext,0)


        def getRuleIndex(self):
            return RAParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = RAParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_statement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.state = 191
                self.relExpr(0)
                pass

            elif la_ == 2:
                self.state = 192
                self.definition()
                pass

            elif la_ == 3:
                self.state = 193
                self.command()
                pass


            self.state = 196
            self.match(RAParser.TERMINATOR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(RAParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RAParser.StatementContext)
            else:
                return self.getTypedRuleContext(RAParser.StatementContext,i)


        def getRuleIndex(self):
            return RAParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = RAParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 201
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 9)) & ~0x3f) == 0 and ((1 << (_la - 9)) & 2287833026450747393) != 0):
                self.state = 198
                self.statement()
                self.state = 203
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 204
            self.match(RAParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TextAtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TEXT_CMD(self):
            return self.getToken(RAParser.TEXT_CMD, 0)

        def TEXT_LBRACE(self):
            return self.getToken(RAParser.TEXT_LBRACE, 0)

        def TEXT_RBRACE(self):
            return self.getToken(RAParser.TEXT_RBRACE, 0)

        def TEXT_CONTENT(self):
            return self.getToken(RAParser.TEXT_CONTENT, 0)

        def getRuleIndex(self):
            return RAParser.RULE_textAtom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTextAtom" ):
                listener.enterTextAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTextAtom" ):
                listener.exitTextAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTextAtom" ):
                return visitor.visitTextAtom(self)
            else:
                return visitor.visitChildren(self)




    def textAtom(self):

        localctx = RAParser.TextAtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_textAtom)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self.match(RAParser.TEXT_CMD)
            self.state = 207
            self.match(RAParser.TEXT_LBRACE)
            self.state = 209
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==71:
                self.state = 208
                self.match(RAParser.TEXT_CONTENT)


            self.state = 211
            self.match(RAParser.TEXT_RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.valExpr_sempred
        self._predicates[3] = self.relExpr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def valExpr_sempred(self, localctx:ValExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 1)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 4)
         

    def relExpr_sempred(self, localctx:RelExprContext, predIndex:int):
            if predIndex == 9:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 10:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 11:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 12:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 13:
                return self.precpred(self._ctx, 2)
         




