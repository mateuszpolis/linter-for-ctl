# Linter for .ctl ("Control") language files

!WARNING! This is a work in progress. The linter is not yet complete.

## Language Grammar

The language is defined by the following grammar:

**Non-terminals** are in PascalCase, **terminals** are in lowercase.

```
Program             -> Statement*
Statement           -> Assignment 
                    | Declaration 
                    | FunctionDeclaration 
                    | FunctionCall ";"
                    | IfStatement
                    | DividingLine
                    | Comment
                    | MultiLineComment
                    | ReturnStatement
                    | BreakStatement
                    | WhileLoop       
                    | LibraryImport    
                    | InlineIfStatement
IfStatement         -> "if" "(" Comparison ")" (InlineStatement | Block) (ElseIfClause)* (ElseClause)?
InlineStatement     -> Statement
ElseIfClause        -> "else" "if" "(" Comparison ")" (InlineStatement | Block)
ElseClause          -> "else" (InlineStatement | Block)
Assignment          -> identifier "=" ConditionalExpression ";"
Declaration         -> Type identifier ("=" ConditionalExpression)? (";" | ("," identifier ("=" ConditionalExpression)*)? ";")
FunctionDeclaration -> Type identifier "(" ParameterList? ")" Block
FunctionCall        -> (identifier | AttributeAccess | IndexAccess) "(" (Expression ("," Expression)*)? ")"
Block               -> "{" Statement* "}"
ConditionalExpression -> TernaryExpression | Comparison
TernaryExpression   -> Comparison "?" Expression ":" Expression
Comparison          -> Expression ( ("==" | "!=" | ">" | ">=" | "<" | "<=") Expression )*
Expression          -> Term ( ("+" | "-") Term )*
Term                -> Factor ( ("*" | "/") Factor )*
Factor              -> Primary
Primary             -> number 
                    | identifier 
                    | "$" identifier
                    | "(" ConditionalExpression ")"
                    | FunctionCall
                    | AttributeAccess
                    | IndexAccess
                    | String
                    | Character
AttributeAccess     -> (identifier | IndexAccess) "." identifier
IndexAccess         -> (identifier | AttributeAccess) "[" Expression "]"
Comment             -> "//" (any_character)*
MultiLineComment    -> "/**" (any_character)* "*/"
ReturnStatement     -> "return" (Expression)? ";"
BreakStatement      -> "break" ";"
WhileLoop           -> "while" "(" Comparison ")" Block
Type                -> type_keyword | TemplateType
TemplateType        -> template_type_keyword "<" Type ("," Type)* ">"
Parameter           -> Type identifier
ParameterList       -> Parameter ("," Parameter)*
LibraryImport       -> "#" "uses" String
String              -> '"' (any_character)* '"'
Character           -> "'" any_character "'"
```
