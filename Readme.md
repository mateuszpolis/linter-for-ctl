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
                    | DividingLine
Assignment          -> identifier "=" Expression ";"
Declaration         -> type_keyword identifier ("=" Expression)? (";" | ("," identifier ("=" Expression)*)? ";")
FunctionDeclaration -> type_keyword identifier "(" (type_keyword identifier ("," type_keyword identifier)*)? ")" Block
FunctionCall        -> identifier "(" (Expression ("," Expression)*)? ")"
Block               -> "{" Statement* "}"
Expression          -> Term ( ("+" | "-") Term )*
Term                -> Factor ( ("*" | "/") Factor )*
Factor              -> Primary | AttributeAccess | IndexAccess
Primary             -> number 
                    | identifier 
                    | "$" identifier
                    | "(" Expression ")"
                    | FunctionCall
AttributeAccess     -> identifier "." identifier
IndexAccess         -> identifier "[" Expression "]"
```
