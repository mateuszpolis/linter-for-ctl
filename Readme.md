# Linter for .ctl **CTRL** [(Control) language](https://www.winccoa.com/documentation/WinCCOA/latest/en_US/Control_Grundlagen/Control_Grundlagen.html)

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
                    | IfStatement ";"?
                    | DividingLine
                    | Comment
                    | MultiLineComment
                    | ReturnStatement
                    | BreakStatement
                    | WhileLoop       
                    | LibraryImport
                    | PropertySetter
                    | InlineIfStatement
                    | ForLoop
                    | EnumDeclaration
                    | SwitchStatement
                    | Block
                    | ContinueStatement
                    | TryCatchStatement
                    | DoWhileLoop
                    | DoubleColonAccess ";"
                    | Event
IfStatement         -> "if" Comment? "(" Comparison ")" (InlineStatement | Block) (ElseIfClause)* (ElseClause)?
ElseIfClause        -> "else" "if" Comment? "(" Comparison ")" (InlineStatement | Block)
ElseClause          -> "else" Comment? (InlineStatement | Block)
InlineStatement     -> Statement
Assignment          -> Identifier "=" ConditionalExpression ";"
                     | IncrementAssignment
                     | CompoundAssignment
IncrementAssignment -> Identifier ("++" | "--") ";"
                     | ("++" | "--") Identifier ";"
CompoundAssignment  -> Identifier ("+=" | "-=" | "*=" | "/=" | "%=") ConditionalExpression ";"
AccessModifier      -> "public" | "private" | "protected"
Declaration         -> AccessModifier? Modifier? ("const" (Type | ε) | Type) identifier ("=" ConditionalExpression)? Comment? ("," identifier ("=" ConditionalExpression)*)? Comment? ";"
FunctionDeclaration -> AccessModifier? Modifier? Type? (identifier | "main") "(" ParameterList? ")" Block
Modifier            -> "static" | "global"
FunctionCall        -> (identifier | AttributeAccess | IndexAccess) "(" ArgumentList? ")"
ArgumentList        -> ConditionalExpression Comment? ("," Comment? ConditionalExpression)*
Block               -> "{" Statement* "}"
ConditionalExpression -> TernaryExpression | Comparison | DoubleColonAccess
TernaryExpression   -> Comparison "?" (Expression | TernaryExpression) ":" Expression
Comparison          -> LogicalOr | Declaration | Assignment
LogicalOr           -> LogicalAnd ("||" LogicalAnd)*
LogicalAnd          -> Negation ("&&" Negation)*
Negation            -> ("!" | "~")? BitwiseOr
BitwiseOr           -> BitwiseXor ("|" BitwiseXor)*
BitwiseXor          -> BitwiseAnd ("^" BitwiseAnd)*
BitwiseAnd          -> Shift ("&" Shift)*
Shift               -> Relational (("<<" | ">>") Relational)*
Relational          -> Expression ( ("==" | "!=" | ">" | ">=" | "<" | "<=") Expression )?
Expression          -> Term ( ("+" | "-") Term )*
Term                -> Factor ( ("*" | "/" | "%") Factor )*
Factor              -> Comment? Primary Comment?
Primary             -> number "."?
                    | identifier 
                    | "$" (identifier | number)
                    | "&" identifier
                    | TypeCast
                    | "(" Comparison ")"
                    | FunctionCall
                    | AttributeAccess
                    | IndexAccess
                    | String
                    | Character
                    | EnumAccess
                    | ClassInitialization
AttributeAccess     -> (identifier | IndexAccess) "." identifier
IndexAccess         -> (identifier | AttributeAccess) "[" Expression "]"
Comment             -> "//" (any_character)* | MultiLineComment
MultiLineComment    -> "/**" (any_character)* "*/" | "/*" (any_character)* "*/"
ReturnStatement     -> "return" (ConditionalExpression)? ";"
BreakStatement      -> "break" ";"
WhileLoop           -> "while" "(" Comparison ")" (Block | Statement)
TemplateType        -> template_type_keyword "<" Type ("," Type)* ">"
ParameterList       -> Parameter ("," Parameter)*
Parameter           -> ("const")? Type identifier
Type                -> type_keyword | TemplateType | DynamicType
DynamicType         -> identifier
LibraryImport       -> "#" "uses" String
String              -> '"' (any_character)* '"'
Character           -> "'" any_character "'"
ForLoop             -> "for" "(" ForInitialization ";" Comparison ";" Assignment? ")" (Block | Statement)
ForInitialization   -> Declaration | Assignment | identifier
EnumDeclaration     -> "enum" identifier "{" EnumValue ("," EnumValue)* "}"
EnumAccess          -> identifier "::" identifier
ClassStaticAccess   -> identifier "::" (FunctionCall | identifier)
EnumValue           -> identifier ("=" number)?
SwitchStatement     -> "switch" "(" Expression ")" "{" (SwitchCase | Comment | MultiLineComment)* "}"
SwitchCase          -> "case" Expression ":" Statement*
                     | "default" ":" Statement*
StructDeclaration   -> "struct" identifier Inheritance? Block ";"
Inheritance         -> ":" identifier
ClassDeclaration    -> "class" identifier Inheritance? Block ";"
TypeCast            -> "(" Type ")" Expression
ClassInitialization -> ("new")? Type "(" ArgumentList? ")"
ContinueStatement   -> "continue" ";"
TryCatchStatement   -> "try" Block "catch" Block ("finally" Block)?
DoWhileLoop         -> "do" Block "while" "(" Comparison ")" ";"
PropertySetter      -> # "property" (Type | identifier) identifier
DoubleColonAccess   -> EnumAccessNode | ClassStaticAccessNode
Event               -> # "event" ( ParameterList? )
```
