import sympy as sp
import string
import math


def convert_to_expr(equation_str):
    '''
    Converts a equation string to a sympy equation expression.
    
    Returns sympy equation expression.
    '''

    equation = sp.parse_expr(equation_str)
    return equation

def partial_der(equation, var):
    '''
    Returns partial derivative of sympy equation with respect to var.
    '''

    return sp.diff(equation, var)

def uncertainty_formula(equation_str):
    '''
    Returns the uncertainty equation .

    The returned equation will be a sympy expression and is the 
    partial derivative equation used to calculate the propagated
    uncertainty in a given equation.
    '''

    equation = convert_to_expr(equation_str)
    vars = equation.free_symbols
    print(vars)
    sum = -1
    for var in vars:
        partial_term = partial_der(equation, var)
        uncertainty = sp.Symbol("d" + str(var))
        partial_term = sp.Mul(partial_term, uncertainty)
        squared = sp.Pow(partial_term, 2)
        if sum == -1:
            sum = squared
        else:
            sum = sp.Add(sum, squared)
    
    uncertainty_form = sp.Pow(sum, 1/2)
    return equation, uncertainty_form

if __name__ == "__main__":
    print("Note, you must place * between any numbers multipled. Also, ** must be used instead of ^ for exponents.")
    equation = input("Enter the equation:")

    a = uncertainty_formula(equation)
    equation = a[0]
    uncert_form = a[1]

    num_var = len(equation.free_symbols)

    var_list = []

    for var in range(num_var):
        user_var = input("Enter the exact variable name followed by its value, separated by a space: ")
        input_list = user_var.split()
        var_tuple = (input_list[0], float(input_list[1]))
        
        uncert_var = input("Enter the variable's uncertainty: ")
        uncert_tuple = ("d" + var_tuple[0], float(uncert_var))

        var_list.append(var_tuple)
        var_list.append(uncert_tuple)

    print(uncert_form.subs(var_list).evalf())


