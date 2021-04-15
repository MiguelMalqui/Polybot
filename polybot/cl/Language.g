grammar Language;

root: command* EOF;
command
    : assign
    | write
    | area
    | perimeter
    | vertices
    | centroid
    | color
    | inside
    | equal
    | draw
    ;
assign: POLYGON_ID ASSIGN expression;
write
    : print_string
    | print_expression
    ;
print_string: PRINT STRING;
print_expression: PRINT expression;
area: AREA expression;
perimeter: PERIMETER expression;
vertices: VERTICES expression;
centroid: CENTROID expression;
color: COLOR polygon_id ',' '{' NUMBER NUMBER NUMBER'}';
inside: INSIDE expression ',' expression;
equal: EQUAL expression ','  expression;
draw: DRAW STRING  (',' expression)+ ;
expression
    : expression '+' expression1
    | expression1
    ;
expression1
    : expression1 '*' expression2
    | expression2
    ;
expression2
    : '#' expression2
    | '(' expression ')'
    | expression3
    ;
expression3
    : '!' NUMBER
    | point_list
    | polygon_id
    ;
polygon_id: POLYGON_ID;
point_list: '[' NUMBER* ']';


ASSIGN: ':=';
PRINT: 'print';
AREA: 'area';
PERIMETER: 'perimeter';
VERTICES: 'vertices';
CENTROID: 'centroid';
COLOR: 'color';
INSIDE: 'inside';
EQUAL: 'equal';
DRAW: 'draw';
POLYGON_ID: [a-zA-Z] ([a-zA-Z] | [0-9] | '_')*;
NUMBER: [-+]?[0-9]+('.'[0-9]+)?;

STRING: '"' ([a-zA-Z] | [0-9] | ' ' | '_' | PUNTUATION_SYMBOL | MATH_SYMBOL )* '"';

COMMENT:  '//' ~('\n')* ('\n'|EOF) -> skip;
WS : [ \n\t]+ -> skip ;

fragment MATH_SYMBOL: ( '+' | '-' | '*' | '/' | '=' | '<' | '>' | '^' );
fragment PUNTUATION_SYMBOL: (',' | '.' | ';' | '?' | '!');
