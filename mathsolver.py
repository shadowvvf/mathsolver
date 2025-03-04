import sympy
from sympy import symbols, Eq, expand, collect, degree, solve, sympify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication, convert_xor

transformations = (standard_transformations + (implicit_multiplication, convert_xor))

class Simplifier:
    def __init__(self, expr):
        self.expr = expr
        self.steps = []
    
    def expand_step(self):
        expanded = expand(self.expr)
        if expanded != self.expr:
            self.steps.append(f"Раскрываем скобки: {self.expr} → {expanded}")
            self.expr = expanded
            return True
        return False
    
    def collect_terms_step(self):
        variables = self.expr.free_symbols
        if not variables:
            return False
        var = next(iter(variables))
        collected = collect(self.expr, var)
        if collected != self.expr:
            self.steps.append(f"Собираем подобные члены: {self.expr} → {collected}")
            self.expr = collected
            return True
        return False
    
    def simplify_trig(self):
        simplified = sympy.simplify(self.expr)
        if simplified != self.expr:
            self.steps.append(f"Упрощение тригонометрической функции: {self.expr} → {simplified}")
            self.expr = simplified
            return True
        return False
    
    def simplify(self):
        changed = True
        while changed:
            changed = False
            if self.expand_step():
                changed = True
            if self.collect_terms_step():
                changed = True
            if self.simplify_trig():
                changed = True
        return self.steps, self.expr
    
    def get_steps(self):
        return self.steps

class EquationSolver:
    def __init__(self, equation):
        self.equation = equation
        self.steps = []
        self.var = self.find_variable()
    
    def find_variable(self):
        variables = self.equation.lhs.free_symbols.union(self.equation.rhs.free_symbols)
        return next(iter(variables)) if variables else symbols('x')
    
    def simplify_equation(self):
        lhs = self.equation.lhs
        rhs = self.equation.rhs
        
        simplifier = Simplifier(lhs - rhs)
        steps, simplified = simplifier.simplify()
        self.steps.extend(steps)
        self.equation = Eq(simplified, 0)
        self.steps.append(f"Упрощенное уравнение: {self.equation.lhs} = 0")
    
    def solve_linear(self, a, b):
        self.steps.append(f"Линейное уравнение: {a}*{self.var} + {b} = 0")
        solution = -b / a
        self.steps.append(f"Решение: {self.var} = -{b}/{a} = {solution}")
        return [solution]
    
    def solve_quadratic(self, a, b, c):
        self.steps.append(f"Квадратное уравнение: {a}*{self.var}² + {b}*{self.var} + {c} = 0")
        D = b**2 - 4*a*c
        self.steps.append(f"Дискриминант D = {b}² - 4*{a}*{c} = {D}")
        
        if D > 0:
            sqrt_D = sympy.sqrt(D)
            x1 = (-b + sqrt_D) / (2*a)
            x2 = (-b - sqrt_D) / (2*a)
            self.steps.append(f"D > 0. Корни: {self.var}₁ = {x1}, {self.var}₂ = {x2}")
            return [x1, x2]
        elif D == 0:
            x = -b / (2*a)
            self.steps.append(f"D = 0. Один корень: {self.var} = {x}")
            return [x]
        else:
            sqrt_D = sympy.sqrt(-D)
            x1 = (-b + sympy.I*sqrt_D) / (2*a)
            x2 = (-b - sympy.I*sqrt_D) / (2*a)
            self.steps.append(f"D < 0. Комплексные корни: {self.var}₁ = {x1}, {self.var}₂ = {x2}")
            return [x1, x2]
    
    def solve(self):
        self.simplify_equation()
        expr = self.equation.lhs
        poly = sympy.Poly(expr, self.var)
        coeffs = poly.all_coeffs()
        deg = len(coeffs) - 1
        
        if deg == 1:
            return self.solve_linear(coeffs[0], coeffs[1])
        elif deg == 2:
            return self.solve_quadratic(coeffs[0], coeffs[1], coeffs[2])
        else:
            solutions = solve(self.equation, self.var)
            self.steps.append(f"Уравнение {deg}-й степени. Решения: {solutions}")
            return solutions

    def solve_polynomial(self):
        coefficients = [self.expr.coeff(x, i) for i in range(self.expr.as_poly().degree() + 1)]
        roots = solve(self.expr, x)
        return roots

def main():
    user_input = input("Введите задачу: ").strip()
    try:
        if '=' in user_input:
            lhs, rhs = user_input.split('=', 1)
            lhs_expr = parse_expr(lhs, transformations=transformations)
            rhs_expr = parse_expr(rhs, transformations=transformations)
            equation = Eq(lhs_expr, rhs_expr)
            
            solver = EquationSolver(equation)
            solutions = solver.solve()
            
            print("\nЭтапы решения:")
            for i, step in enumerate(solver.steps, 1):
                print(f"{i}. {step}")
            print("\nРезультат:")
            for sol in solutions:
                print(f"{solver.var} = {sol}")
        else:
            expr = parse_expr(user_input, transformations=transformations)
            simplifier = Simplifier(expr)
            steps, result = simplifier.simplify()
            
            print("\nЭтапы упрощения:")
            for i, step in enumerate(steps, 1):
                print(f"{i}. {step}")
            print(f"\nРезультат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()