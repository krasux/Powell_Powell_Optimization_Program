from numbers import Number
from sympy.utilities.lambdify import lambdify
from sympy import var
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    convert_xor,
    implicit_multiplication,
    implicit_application,
    function_exponentiation,
    split_symbols_custom,
    _token_splittable
)


def can_split(symbol):
    if symbol not in ('x1', 'x2', 'x3', 'x4', 'x5'):
        return _token_splittable(symbol)
    return False
split_xn = split_symbols_custom(can_split)
trans = standard_transformations + (split_xn, implicit_multiplication,
                                    implicit_application, function_exponentiation, convert_xor)

var('x:6')


def str2fun(str):
    function = lambdify((x1,x2,x3,x4,x5), parse_expr(str, transformations=trans))
    def funcVec(x):
        x1 = 0
        x2 = 0
        x3 = 0
        x4 = 0
        x5 = 0
        if isinstance(x, Number):
            x1 = x
        else:
            if len(x) >= 1:
                x1 = x[0]
            if len(x) >= 2:
                x2 = x[1]
            if len(x) >= 3:
                x3 = x[2]
            if len(x) >= 4:
                x4 = x[3]
            if len(x) >= 5:
                x5 = x[4]
        return function(x1, x2, x3, x4, x5)
    return funcVec



