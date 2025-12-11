parser grammar RAParser;
options { tokenVocab=RALexer; }

valExpr : STRING                                        # stringLiteralValExpr
        | NUMBER                                        # numberLiteralValExpr
        | PAREN_L valExpr PAREN_R                       # valExprParenthesized
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
         | ID                                           # relRef
         // Allow \rho OR \rename
         | (RENAME | RHO) ARG_L ((ID COLON (STAR|listOfIDs)) | listOfIDs) ARG_R relExpr # renameExpr
         // Allow \project OR \pi
         | (PROJECT | PI) ARG_L listOfValExprs ARG_R relExpr   # projectExpr
         // Allow \select OR \sigma
         | (SELECT | SIGMA) ARG_L valExpr ARG_R relExpr           # selectExpr
         // Allow \join OR ⋈ OR Outer Joins
         | relExpr (JOIN | NATURAL_JOIN_SYMBOL | LEFT_OUTER_JOIN | RIGHT_OUTER_JOIN | FULL_OUTER_JOIN) (ARG_L valExpr ARG_R)? relExpr  # joinExpr
         // Allow \cross OR \times (×)
         | relExpr (CROSS | TIMES) relExpr                        # crossExpr
         // Allow \union OR \cup (∪)
         | relExpr (UNION | CUP) relExpr                        # unionExpr
         // Allow \diff OR minus sign (-)
         | relExpr (DIFF | MINUS) relExpr                         # diffExpr
         // Allow \intersect OR \cap (∩)
         | relExpr (INTERSECT | CAP) relExpr                    # intersectExpr
         // Allow \aggr OR \gamma
         | (AGGR | GAMMA) ARG_L listOfValExprs (COLON listOfValExprs)? ARG_R relExpr      # aggrExpr
         ;

// Allow :- OR \leftarrow (←)
definition : ID (GETS | LEFT_ARROW) relExpr;

command : LIST                                          # listCommand
        | CLEAR (FORCE? ID|STAR)                        # clearCommand
        | SAVE FORCE? (ID|STAR) STRING?                 # saveCommand
        | SOURCE STRING                                 # sourceCommand
        | HELP                                          # helpCommand
        | QUIT                                          # quitCommand
        | SQLEXEC SQLEXEC_TEXT                          # sqlexecCommand
        ;

statement : (relExpr|definition|command) TERMINATOR;
program : (statement)* EOF;
