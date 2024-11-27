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
                    | ForLoop
                    | MainFunction
                    | EnumDeclaration
                    | SwitchStatement
IfStatement         -> "if" "(" Comparison ")" (InlineStatement | Block) (ElseIfClause)* (ElseClause)?
InlineStatement     -> Statement
ElseIfClause        -> "else" "if" "(" Comparison ")" (InlineStatement | Block)
ElseClause          -> "else" (InlineStatement | Block)
Assignment          -> Identifier "=" ConditionalExpression ";"
                     | IncrementAssignment
                     | CompoundAssignment
IncrementAssignment -> Identifier ("++" | "--") ";"
                     | ("++" | "--") Identifier ";"
CompoundAssignment  -> Identifier ("+=" | "-=" | "*=" | "/=" | "%=") ConditionalExpression ";"
Declaration         -> ("public")? ("const" (Type | ε) | Type) identifier ("=" ConditionalExpression)? ("," identifier ("=" ConditionalExpression)*)? ";"
FunctionDeclaration -> ("public")? (Type)? identifier "(" ParameterList? ")" Block
FunctionCall        -> (identifier | AttributeAccess | IndexAccess) "(" (Expression ("," Expression)*)? ")"
Block               -> "{" Statement* "}"
ConditionalExpression -> TernaryExpression | Comparison
TernaryExpression   -> Comparison "?" Expression ":" Expression
Comparison          -> LogicalOr
LogicalOr           -> LogicalAnd ("||" LogicalAnd)*
LogicalAnd          -> Negation ("&&" Negation)*
Negation            -> ("!" | "~")? BitwiseOr
BitwiseOr           -> BitwiseXor ("|" BitwiseXor)*
BitwiseXor          -> BitwiseAnd ("^" BitwiseAnd)*
BitwiseAnd          -> Shift ("&" Shift)*
Shift               -> Relational (("<<" | ">>") Relational)*
Relational          -> Expression ( ("==" | "!=" | ">" | ">=" | "<" | "<=") Expression )?
Expression          -> Term ( ("+" | "-") Term )*
Term                -> Factor ( ("*" | "/") Factor )*
Factor              -> Primary
Primary             -> number "."?
                    | identifier 
                    | "$" identifier
                    | "&" identifier
                    | "(" Comparison ")"
                    | FunctionCall
                    | AttributeAccess
                    | IndexAccess
                    | String
                    | Character
                    | EnumAccess
AttributeAccess     -> (identifier | IndexAccess) "." identifier
IndexAccess         -> (identifier | AttributeAccess) "[" Expression "]"
Comment             -> "//" (any_character)*
MultiLineComment    -> "/**" (any_character)* "*/" | "/*" (any_character)* "*/"
ReturnStatement     -> "return" (ConditionalExpression)? ";"
BreakStatement      -> "break" ";"
WhileLoop           -> "while" "(" Comparison ")" (Block | Statement)
TemplateType        -> template_type_keyword "<" Type ("," Type)* ">"
ParameterList       -> Parameter ("," Parameter)*
Parameter           -> Type identifier
Type                -> type_keyword | TemplateType | DynamicType
DynamicType         -> identifier
LibraryImport       -> "#" "uses" String
String              -> '"' (any_character)* '"'
Character           -> "'" any_character "'"
ForLoop             -> "for" "(" Declaration ";" Comparison ";" Assignment ")" Block
MainFunction        -> Type? "main" "(" ")" Block
EnumDeclaration     -> "enum" identifier "{" EnumValue ("," EnumValue)* "}"
EnumAccess          -> identifier "::" identifier
EnumValue           -> identifier "=" number
SwitchStatement     -> "switch" "(" Expression ")" "{" SwitchCase* "}"
SwitchCase          -> "case" Expression ":" ReturnStatement
                    | "default" ":" ReturnStatement
```
