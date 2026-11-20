\# Lab 5 - Static Code Analysis

\## Reflection



\### 1. What is static code analysis?



Static code analysis is the process of examining source code without executing the program. It helps identify programming errors, security vulnerabilities, coding standard violations and maintainability issues before deployment.



\### 2. What is Pylint, and why is it used?



Pylint is a Python static analysis tool used to detect coding errors, unused imports, naming convention violations, missing documentation and code quality problems. It also provides a code quality score out of 10.



\### 3. What is Bandit, and why is it used?



Bandit is a Python security analysis tool. It scans source code for common security vulnerabilities, such as unsafe use of eval(), weak cryptographic hashing, insecure deserialization and shell command execution.



\### 4. What is Flake8, and why is it used?



Flake8 checks Python code for style and formatting violations based on PEP 8. It identifies problems such as incorrect indentation, excessive line length, missing blank lines and unused imports.



\### 5. What major issues were identified in the original program?



The original Pharmacy Manager program contained several issues:

\- Unsafe use of eval() for expression evaluation.

\- Weak MD5 hashing.

\- Unsafe pickle deserialization.

\- Potential shell command injection through os.system().

\- Hardcoded password.

\- Bare exception handling.

\- Mutable default arguments.

\- Missing input validation.

\- Weak random number generation.

\- Unused imports and formatting violations.



\### 6. How were the identified issues fixed?



The issues were addressed by:

\- Replacing eval() with a restricted arithmetic expression evaluator using AST.

\- Replacing MD5 with SHA-256.

\- Replacing pickle storage with JSON.

\- Removing shell command execution.

\- Moving password configuration to an environment variable.

\- Using specific exception handling.

\- Replacing mutable default arguments with None.

\- Adding validation for medicine names, quantities, prices and expiry dates.

\- Using the secrets module for prescription numbers.

\- Using context managers for file handling.

\- Improving naming conventions, documentation and formatting.



\### 7. What were the final results?



After correcting the program, all three static analysis tools were executed again.



\- Pylint: 10.00/10.

\- Bandit: No security issues identified.

\- Flake8: No style errors reported.



\### 8. What did you learn from this lab?



This lab demonstrated that a program can run successfully and still contain security vulnerabilities and code quality issues. I learned how to use Pylint, Bandit and Flake8 to identify these problems and improve Python code. I also understood the importance of input validation, secure password handling, safe file operations, secure hashing and following coding standards.

