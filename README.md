# OptiSense

![License](https://img.shields.io/badge/License-GPL--3.0-blue)

## Table of Contents

1. [About the Project](#about-the-project)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Application Structure](#application-structure)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

## About the Project

**OptiSense** is an educational tool designed to solve **linear programming (LP)**, **integer linear programming (ILP)**, and **mixed-integer linear programming (MILP)** problems, including **sensitivity analysis**. 

The application was developed as part of a bachelor's thesis titled:  
*"Shiny in Python: An interactive visualization, solution, and sensitivity analysis tool for simple LP and (M)ILP problems using `scipy.optimize.milp` and `lp_solve`."*

This tool is intended to help users understand linear programming concepts and sensitivity analysis fundamentals.

## Technologies Used

OptiSense is built using the following technologies:

- **Python** – Core programming language.
- **Shiny for Python** – Framework for interactive web applications.
- **Matplotlib & Pandas** – For visualization and data handling.
- **Scipy.optimize** – Used for optimization:
  - `scipy.optimize.LinearConstraint` – Defines linear constraints.
  - `scipy.optimize.milp` – Solves mixed-integer linear programming (MILP) problems.
  - `scipy.optimize.OptimizeResult` – Represents the results of optimization computations.
- **lp_solve** – External solver for additional optimization tasks.

## Installation

To install and run OptiSense locally, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/IVIcSunShine/shiny-python-linear-programming-education-tool.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd shiny-python-linear-programming-education-tool
    ```

3. **Create a virtual environment**:

    ```bash
    python -m venv env
    ```

4. **Activate the virtual environment**:

    - On Windows:

        ```bash
        .\env\Scriptsctivate
        ```

    - On macOS/Linux:

        ```bash
        source env/bin/activate
        ```

5. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

After installing the dependencies, launch the application with:

```bash
python shiny_files/app.py
```

Then, open your browser and go to `http://localhost:5000` to use OptiSense.

### Features:

- **Define optimization models** – Set an objective function and constraints.
- **Solve problems** – Compute optimal solutions using `scipy.optimize` and `lp_solve`.
- **Perform sensitivity analysis** – Evaluate parameter impact on the solution.
- **Visualize results** – View solutions graphically and numerically.
- **Import & Export** – Save and load problem configurations.

## Application Structure

OptiSense provides an intuitive user interface with structured panels:

### **Main Interface (Problem Definition & Solution)**
![OptiSense Main Interface](./path-to-screenshot1.png)  
This screen allows users to:
- **Define the objective function** (Enter, Change, or Delete).
- **Add constraints** to the problem.
- **Perform calculations**, including:
  - **Linear Optimization**
  - **Sensitivity Analysis**
- **Export and import models** for later use.
- **Visualize results** graphically and numerically.
- **Reset all inputs** to start a new problem.

### **Help & Guide Interface**
![OptiSense Guide Interface](./path-to-screenshot2.png)  
The guide section provides step-by-step instructions for using OptiSense. Users can:
- **Learn about Linear Programming** and Sensitivity Analysis.
- **Follow a structured workflow** from setup to solving the problem.
- **Understand each function with detailed descriptions.**

These sections make OptiSense a **powerful yet easy-to-use educational tool** for optimization problems.

## Contributing

Contributions are welcome! If you find a bug or have an idea for an improvement, feel free to open an **Issue** or a **Pull Request**. Please follow the contribution guidelines.

## License

Distributed under the **GPL-3.0** License. See `LICENSE` for more information.

## Contact

For inquiries or collaboration, please contact:

- **GitHub**: [IVIcSunShine](https://github.com/IVIcSunShine)
- **Email**: [Your Email Here]

---

We hope you enjoy using **OptiSense**! 🚀
