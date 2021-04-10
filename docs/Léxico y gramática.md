---
title: \vspace{-3cm} Léxico y gramática del lenguaje _Hivar_
author:
- Roberta González Garza - A01570010
- Mariano García Alipi - A00822247
date: 9 de abril de 2021
---

## Léxico

Token                   | Expresión regular | Ejemplo
 ---------------------- | ----------------- | -------
`PROGRAM_KEYWORD`       | `program`         | `program`
`MAIN_KEYWORD`          | `main`            | `main`
`CLASS_KEYWORD`         | `class`           | `class`
`INHERITS`              | `inherits`        | `inherits`
`ATTRIBUTES_KEYWORD`    | `attributes`      | `attributes`
`VARS_KEYWORD`          | `variables`       | `variables`
`END_VARS`              | `byevar`          | `byevar`  
`METHODS_KEYWORD`       | `methods`         | `methods`
`FUNCTION`              | `function`        | `function`
`RETURN`                | `return`          | `return`
`READ`                  | `read`            | `read`
`WRITE`                 | `write`           | `write`
`INT`                   | `int`             | `int`  
`FLOAT`                 | `float`           | `float`
`CHAR`                  | `char`            | `char`
`VOID`                  | `void`            | `void`
`IF`                    | `if`              | `if`
`ELSIF`                 | `elsif`           | `elsif`
`ELSE`                  | `else`            | `else`
`WHILE`                 | `while`           | `while`
`DO`                    | `do`              | `do`
`FROM`                  | `from`            | `from`
`TO`                    | `to`              | `to`
`COMMA`                 | `,`               | `,`
`PERIOD`                | `\.`              | `.`
`COLON`                 | `:`               | `:`
`SEMICOLON`             | `;`               | `;`
`LEFT_PARENTHESIS`      | `\(`              | `(`
`RIGHT_PARENTHESIS`     | `\)`              | `)`
`LEFT_CURLY`            | `\{`              | `{`
`RIGHT_CURLY`           | `\}`              | `}`
`LEFT_BRACKET`          | `\[`              | `[`
`RIGHT_BRACKET`         | `\]`              | `]`
`NOT_EQUALS`            | `!=`              | `!=`
`EQUALS_COMPARISON`     | `==`              | `==`
`EQUALS_ASSIGNMENT`     | `=`               | `=`
`LESS_THAN`             | `<`               | `<`
`GREATER_THAN`          | `>`               | `>`
`PLUS`                  | `\+`              | `+`
`MINUS`                 | `\-`              | `-`
`MULTIPLY`              | `\*`              | `*`
`DIVIDE`                | `\/`              | `/`
`AND`                   | `&&`              | `&&`
`OR`                    | `\|\|`            | `||`
`ID`                    | `[a-zA-Z][a-zA-Z0-9_]*`   | `foo`
`CONST_FLOAT`           | `\d+\.\d+`                | `3.14`
`CONST_INT`             | `\d+`                     | `123`
`CONST_STRING`          | `\"([^\\\n]\|(\\.))+\"`   | `"Hello, world!"`

## Gramática

### Diagramas de sintaxis

![Diagrama 1](docs/img/diagram_1.jpeg)\

![Diagrama 2](docs/img/diagram_2.jpeg)\

![Diagrama 3](docs/img/diagram_3.jpeg)\

![Diagrama 4](docs/img/diagram_4.jpeg)\

### Gramática formal

```default
program      →  PROGRAM_KEYWORD ID SEMICOLON classes vars funcs main
```

```default
classes      →  CLASS_KEYWORD ID inheritance LEFT_CURLY attributes methods
                RIGHT_CURLY SEMICOLON classes
             |  empty
```

```default
inheritance  →  INHERITS ID
             |  empty
```

```default
attributes   →  ATTRIBUTES_KEYWORD vars_1
             |  empty
```

```default
methods      →  METHODS_KEYWORD funcs
             |  empty
```

```default
vars         →  VARS_KEYWORD vars_1 END_VARS
             |  empty
```

```default
vars_1       →  var_type COLON vars_2 vars_arr SEMICOLON vars_1
             |  var_type COLON vars_2 vars_arr SEMICOLON
```

```default
vars_arr     →  LEFT_BRACKET vars_arr_1 RIGHT_BRACKET
             |  empty
```

```default
vars_arr_1   →  vars_arr_2 COMMA vars_arr_2
             |  vars_arr_2
```

```default
vars_arr_2   →  CONST_INT
             |  exp
```

```default
type         →  INT
             |  FLOAT
             |  CHAR
```

```default
var_type     →  type
             |  ID
```

```default
vars_2       →  ID COMMA vars_2
             |  ID
```

```default
funcs        →  FUNCTION func_type ID
                LEFT_PARENTHESIS parameters RIGHT_PARENTHESIS
                LEFT_CURLY vars block_1 RIGHT_CURLY SEMICOLON funcs_1
```

```default
funcs_1      →  funcs
             |  empty
```

```default
func_type    →  type
             |  VOID
```

```default
parameters   →  parameters_1
             |  empty
```

```default
parameters_1 →  var_type COLON ID parameters_2
```

```default
parameters_2 →  COMMA parameters_1
             |  empty
```

```default
main         →  MAIN_KEYWORD LEFT_PARENTHESIS RIGHT_PARENTHESIS block
                SEMICOLON
```

```default
block        →  LEFT_CURLY block_1 RIGHT_CURLY
```

```default
block_1      →  statement block_1
             |  empty
```

```default
statement    →  statement_1 SEMICOLON
```

```default
statement_1  →  assignment
             |  func_call
             |  return
             |  read
             |  write
             |  decision
             |  cond_loop
             |  non_cond_loop
             |  empty
```

```default
assignment   →  variable EQUALS_ASSIGNMENT exp
             |  variable EQUALS_ASSIGNMENT func_call
```

```default
variable     →  ID LEFT_BRACKET exp COMMA exp RIGHT_BRACKET
             |  ID PERIOD ID
             |  ID
```

```default
expression   →  exp relational_op exp
             |  exp
```

```default
relational_op → NOT_EQUALS
              | EQUALS_COMPARISON
              | LESS_THAN
              | GREATER_THAN
              | AND
              | OR
```

```default
exp          →  term PLUS exp
             |  term MINUS exp
             |  term
```

```default
term         →  factor MULTIPLY factor
             |  factor DIVIDE factor
             |  factor
```

```default
factor       →  LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
             | constant
             | variable
             | func_call
             | PLUS constant
             | MINUS constant 
```

```default
constant    →   CONST_INT
            |   CONST_FLOAT
```

```default
func_call   →   ID PERIOD ID LEFT_PARENTHESIS func_call_1
                RIGHT_PARENTHESIS
            |   ID LEFT_PARENTHESIS func_call_1 RIGHT_PARENTHESIS
```

```default
func_call_1  →  func_call_2
             |  empty
```

```default
func_call_2  →  exp func_call_3
```

```default
func_call_3  →  COMMA func_call_2
             |  empty
```

```default
return       →  RETURN LEFT_PARENTHESIS exp RIGHT_PARENTHESIS
```

```default
read         →  READ LEFT_PARENTHESIS read_1 RIGHT_PARENTHESIS
```

```default
read_1       →  variable read_2
```

```default
read_2       →  COMMA variable read_2
             |  empty
```

```default
write        →  WRITE LEFT_PARENTHESIS write_1 RIGHT_PARENTHESIS
```

```default
write_1      →  expression write_2
             |  CONST_STRING write_2
```

```default
write_2      →  COMMA write_1
             |  empty
```

```default
decision     →  IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
                block elsif else
```

```default
elsif        →  ELSIF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
                block elsif
             |  empty
```

```default
else         →  ELSE block
             |  empty
```

```default
cond_loop    →  WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS DO block
```

```default
non_cond_loop → FROM ID EQUALS_ASSIGNMENT exp TO exp DO block
```
