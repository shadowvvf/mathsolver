# Math Solver

A Python-based mathematical expression and equation solver with both command-line and graphical user interfaces. The application can simplify mathematical expressions and solve various types of equations, including linear, quadratic, and higher-degree equations.

## Features

- Expression simplification
  - Expanding brackets
  - Collecting like terms
- Equation solving
  - Linear equations
  - Quadratic equations (with real and complex solutions)
  - Higher-degree equations
- Step-by-step solution display
- Both CLI and GUI interfaces
- LaTeX rendering of results in the GUI version

## Requirements

- Python 3.6+
- SymPy (for mathematical operations)
- PySide6 (for GUI version)
- Matplotlib (for LaTeX rendering in GUI)

## Installation

1. Clone this repository or download the source files
2. Install the required dependencies:
```bash
pip install sympy pyside6 matplotlib
```

## Usage

### Command Line Interface (CLI)

Run the CLI version using:
```bash
python mathsolver.py
```

Enter your expression or equation when prompted. For example:
- Expression: `(x + 2)^2`
- Equation: `x^2 + 2x + 1 = 0`

### Graphical User Interface (GUI)

Run the GUI version using:
```bash
python mathsolver_gui.py
```

1. Enter your expression or equation in the input field
2. Click "Вычислить" (Calculate) button
3. View the step-by-step solution and final result

## Examples

### Expressions
- `(x + 1)(x - 1)` → `x^2 - 1`
- `(a + b)^2` → `a^2 + 2ab + b^2`

### Equations
- Linear: `2x + 3 = 0`
- Quadratic: `x^2 + 2x + 1 = 0`
- Higher degree: `x^3 - x = 0`

## Features in Detail

### Expression Simplification
- Expands brackets using algebraic rules
- Collects like terms
- Shows step-by-step simplification process

### Equation Solving
- Automatically detects equation type
- Handles linear equations with direct solution
- Solves quadratic equations using the discriminant method
- Finds real and complex solutions
- Provides detailed solution steps

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.