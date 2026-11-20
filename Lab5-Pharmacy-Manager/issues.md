# Lab 5 - Static Code Analysis

## Pharmacy Manager - Issue Analysis

The following table identifies issues found in the original Pharmacy Manager
program before applying the corrections.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe eval() | Security - Medium | 48 | eval() can execute arbitrary code and may allow malicious input to run commands. | Replaced eval() with a restricted arithmetic expression evaluator using AST. |
| Weak MD5 hashing | Security - High | 51 | MD5 is not suitable for security-sensitive hashing. | Replaced MD5 with SHA-256. |
| Unsafe pickle deserialization | Security - Medium | 3, 64 | pickle.load() can execute malicious code when loading untrusted files. | Replaced pickle storage with JSON and validated loaded data. |
| Shell command injection | Security - High | 68 | os.system() can execute shell commands using externally supplied input. | Removed shell execution and used a normal print statement. |
| Hardcoded password | Security - Low | 11 | The pharmacist password was stored directly in source code. | Moved password configuration to an environment variable. |
| Bare exception | Reliability / Style | 27 | A bare except can hide unexpected errors. | Replaced it with specific exception handling. |
| Mutable default argument | Code Quality | 13 | A shared default list can retain data between function calls. | Changed the default to None and handled list creation safely. |
| Missing input validation | Reliability | Multiple | Invalid names, negative quantities and invalid prices could enter inventory. | Added validation for medicine names, quantities, prices and expiry dates. |
| Weak random number generation | Security - Low | Multiple | The random module is not intended for security-sensitive identifiers. | Used the secrets module for prescription number generation. |
| Unsafe resource handling | Code Quality | Multiple | Files were opened and closed manually. | Used context managers with the with statement. |
| Unused imports | Code Quality | Multiple | Unused imports increased unnecessary dependencies and reduced code cleanliness. | Removed unused imports. |
| Missing docstrings and naming conventions | Maintainability | Multiple | Functions lacked documentation and some names did not follow Python conventions. | Added docstrings and adopted snake_case naming. |
| Formatting problems | Style | Multiple | Long lines, missing blank lines and inconsistent formatting violated PEP 8 conventions. | Reformatted the code and verified it using Flake8. |
| Invalid stock data | Functional Correctness | Multiple | The original demonstration included negative stock and an invalid numeric medicine name. | Added input validation and corrected the demonstration data. |

## Summary

The original program had security, reliability, maintainability and
formatting issues.

After applying the corrections, the program was analysed again using
Pylint, Bandit and Flake8.

Final results:
- Pylint: 10.00/10
- Bandit: No issues identified
- Flake8: No errors reported

The line numbers above refer to the original source code, before corrections.