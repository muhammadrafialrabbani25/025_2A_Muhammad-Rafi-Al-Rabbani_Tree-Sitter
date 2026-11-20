["and" "or" "not" "in" "contains"] @keyword

["=" "!=" ">" "<" ">=" "<="] @operator

["(" ")" "[" "]" ","] @punctuation

(string) @string
(number) @number
(boolean) @constant.builtin
(comparison_expression field: (identifier) @property)
(identifier) @variable