module.exports = grammar({
  name: 'filter',

  extras: $ => [/\s/],

  rules: {
    source_file: $ => $._expression,

    _expression: $ => choice(
      $.or_expression,
      $.and_expression,
      $.comparison_expression,
      $.in_expression,
      $.contains_expression,
      $.parenthesized_expression,
      $.identifier,
      $.string,
      $.number,
      $.list,
    ),

    or_expression: $ => prec.left(1, seq($._expression, 'or', $._expression)),
    and_expression: $ => prec.left(2, seq($._expression, 'and', $._expression)),

    comparison_expression: $ => prec.left(3, seq(
      $._expression,
      choice('=', '!=', '>', '<', '>=', '<='),
      $._expression,
    )),

    in_expression: $ => prec.left(3, seq($._expression, 'in', $._expression)),
    contains_expression: $ => prec.left(3, seq($._expression, 'contains', $._expression)),

    parenthesized_expression: $ => seq('(', $._expression, ')'),

    list: $ => seq(
      '[',
      optional(seq($._expression, repeat(seq(',', $._expression)))),
      ']',
    ),

    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,
    string: $ => /"[^"]*"/,
    number: $ => /[0-9]+/,
  }
});