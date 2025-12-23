parser grammar RAParser;
options { tokenVocab=RALexer; }

valExpr : STRING                                        # stringLiteralValExpr
        | NUMBER                                        # numberLiteralValExpr
        | PAREN_L valExpr PAREN_R                       # valExprParenthesized
        | LBRACE_ESC valExpr RBRACE_ESC                 # valExprBraced        
        | textAtom                                      # textValExpr          
        | ID PAREN_L listOfValExprs? PAREN_R            # funcExpr
        | (ID DOT)? ID                                  # attrRef
        | valExpr (STAR|SLASH) valExpr                  # multDivExpr
        | valExpr (PLUS|MINUS) valExpr                  # plusMinusExpr
        | valExpr CONCAT valExpr                        # concatExpr
        | valExpr (LT|LE|EQ|NE|GE|GT) valExpr           # compareExpr
        | valExpr LIKE valExpr                          # likeExpr
        | valExpr IS_NULL                               # isNullExpr
        | valExpr IS_NOT_NULL                           # isNotNullExpr
        | NOT valExpr                                   # notExpr
        | valExpr AND valExpr                           # andExpr
        | valExpr OR valExpr                            # orExpr
        ;

listOfValExprs : valExpr (COMMA listOfValExprs)?;

listOfIDs : ID (COMMA listOfIDs)?;

relExpr  : PAREN_L relExpr PAREN_R                      # relExprParenthesized
         | LBRACE_ESC relExpr RBRACE_ESC                # relExprBraced        
         | ID                                           # relRef
         | textAtom                                     # textRelExpr          
         | (RENAME | RHO) ARG_L ((ID COLON (STAR|listOfIDs)) | listOfIDs) ARG_R relExpr # renameExpr
         | (PROJECT | PI) ARG_L listOfValExprs ARG_R relExpr   # projectExpr
         | (SELECT | SIGMA) ARG_L valExpr ARG_R relExpr           # selectExpr
         | relExpr (JOIN | NATURAL_JOIN_SYMBOL | LEFT_OUTER_JOIN | RIGHT_OUTER_JOIN | FULL_OUTER_JOIN) (ARG_L valExpr ARG_R)? relExpr  # joinExpr
         | relExpr (CROSS | TIMES) relExpr                        # crossExpr
         | relExpr (UNION | CUP) relExpr                        # unionExpr
         | relExpr (DIFF | MINUS) relExpr                         # diffExpr
         | relExpr (INTERSECT | CAP) relExpr                    # intersectExpr
         | (AGGR | GAMMA) ARG_L listOfValExprs (COLON listOfValExprs)? ARG_R relExpr      # aggrExpr
         ;

definition : (ID | textAtom) (GETS | LEFT_ARROW) relExpr;

command : LIST                                          # listCommand
        | CLEAR (FORCE? ID|STAR)                        # clearCommand
        | SAVE FORCE? (ID|STAR) STRING?                 # saveCommand
        | SOURCE STRING                                 # sourceCommand
        | HELP                                          # helpCommand
        | QUIT                                          # quitCommand
        | SQLEXEC SQLEXEC_CONTENT                       # sqlexecCommand
        ;

statement : (relExpr|definition|command) TERMINATOR;
program : (statement)* EOF;

textAtom : TEXT_CMD TEXT_LBRACE TEXT_CONTENT? TEXT_RBRACE;