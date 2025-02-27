import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sympy
from sympy import symbols, Eq, expand, collect, degree, solve, sympify, CRootOf
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
    
    def simplify(self):
        changed = True
        while changed:
            changed = False
            if self.expand_step():
                changed = True
            if self.collect_terms_step():
                changed = True
        return self.steps, self.expr

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
            # Преобразуем CRootOf в численные значения
            solutions = [sol.evalf() if isinstance(sol, CRootOf) else sol for sol in solutions]
            self.steps.append(f"Уравнение {deg}-й степени. Решения: {solutions}")
            return solutions

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Упрощение выражений и решение уравнений")
        self.setGeometry(100, 100, 800, 600)
        
        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Поле для ввода выражения/уравнения
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Введите выражение или уравнение...")
        layout.addWidget(self.input_field)
        
        # Кнопка для выполнения вычислений
        self.solve_button = QPushButton("Вычислить")
        self.solve_button.clicked.connect(self.solve_expression)
        layout.addWidget(self.solve_button)
        
        # Область для вывода шагов решения
        self.output_steps = QTextEdit()
        self.output_steps.setReadOnly(True)
        layout.addWidget(self.output_steps)
        
        # Область для отображения LaTeX
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
    
    def solve_expression(self):
        user_input = self.input_field.toPlainText().strip()
        self.output_steps.clear()
        
        try:
            if '=' in user_input:
                lhs, rhs = user_input.split('=', 1)
                lhs_expr = parse_expr(lhs, transformations=transformations)
                rhs_expr = parse_expr(rhs, transformations=transformations)
                equation = Eq(lhs_expr, rhs_expr)
                
                solver = EquationSolver(equation)
                solutions = solver.solve()
                
                # Выводим этапы решения
                for i, step in enumerate(solver.steps, 1):
                    self.output_steps.append(f"{i}. {step}")
                
                # Отображаем результат в LaTeX
                self.display_latex(solutions)
            else:
                expr = parse_expr(user_input, transformations=transformations)
                simplifier = Simplifier(expr)
                steps, result = simplifier.simplify()
                
                # Выводим этапы упрощения
                for i, step in enumerate(steps, 1):
                    self.output_steps.append(f"{i}. {step}")
                
                # Отображаем результат в LaTeX
                self.display_latex(result)
        
        except Exception as e:
            self.output_steps.append(f"Ошибка: {e}")
    
    def display_latex(self, result):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.axis('off')  # Убираем оси
        
        if isinstance(result, list):
            latex_result = ", ".join([sympy.latex(sol) for sol in result])
        else:
            latex_result = sympy.latex(result)
        
        ax.text(0.5, 0.5, f"${latex_result}$", fontsize=16, ha='center', va='center')
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())