
"""Pharmacy management system with secure input and stock handling."""

import ast
import hashlib
import hmac
import json
import math
import operator
import os
import secrets
from datetime import datetime


DB_PASSWORD = os.getenv("PHARMACIST_PASSWORD", "")

medicines = {
    "Paracetamol 500mg": {
        "qty": 170,
        "price": 1.5,
        "expiry": "2027-06-30",
    },
    "Amoxicillin 250mg": {
        "qty": 40,
        "price": 6.0,
        "expiry": "2026-01-15",
    },
    "Cetirizine 10mg": {
        "qty": 10,
        "price": 2.0,
        "expiry": "2027-03-31",
    },
}


def validate_medicine(name, details):
    """Validate a medicine name and its stock details."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")

    if not isinstance(details, dict):
        raise ValueError("Medicine details must be a dictionary.")

    quantity = details.get("qty")
    price = details.get("price")
    expiry = details.get("expiry")

    if (
        isinstance(quantity, bool)
        or not isinstance(quantity, int)
        or quantity < 0
    ):
        raise ValueError("Quantity must be a non-negative integer.")

    if (
        isinstance(price, bool)
        or not isinstance(price, (int, float))
        or not math.isfinite(price)
        or price < 0
    ):
        raise ValueError("Price must be a non-negative finite number.")

    try:
        datetime.strptime(expiry, "%Y-%m-%d")
    except (TypeError, ValueError) as error:
        raise ValueError("Expiry must use YYYY-MM-DD format.") from error


def add_medicine(name, qty, price, expiry, audit=None):
    """Add a medicine to inventory after validating its details."""
    details = {
        "qty": qty,
        "price": price,
        "expiry": expiry,
    }
    validate_medicine(name, details)

    medicines[name] = details

    if audit is not None:
        audit.append(f"Added {name}")


def dispense_medicine(name, qty):
    """Dispense medicine if sufficient stock is available."""
    if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
        raise ValueError("Dispensing quantity must be positive.")

    if name not in medicines:
        return False

    if medicines[name]["qty"] < qty:
        return False

    medicines[name]["qty"] -= qty

    if medicines[name]["qty"] == 0:
        del medicines[name]

    return True


def get_quantity(name):
    """Return the available quantity of a medicine."""
    if name not in medicines:
        return 0

    return medicines[name]["qty"]


def is_expired(name):
    """Check whether a medicine has expired."""
    if name not in medicines:
        raise ValueError("Medicine not found.")

    expiry_date = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()

    return expiry_date < datetime.now().date()


def bill_amount(name, qty):
    """Calculate the total cost for a medicine purchase."""
    if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
        raise ValueError("Billing quantity must be positive.")

    if name not in medicines:
        raise ValueError("Medicine not found.")

    if medicines[name]["qty"] < qty:
        raise ValueError("Insufficient stock.")

    return medicines[name]["price"] * qty


def _evaluate_expression(node):
    """Safely evaluate supported arithmetic expression nodes."""
    binary_operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }

    unary_operations = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    if isinstance(node, ast.Expression):
        return _evaluate_expression(node.body)

    if isinstance(node, ast.Constant):
        if (
            isinstance(node.value, bool)
            or not isinstance(node.value, (int, float))
        ):
            raise ValueError("Only numeric values are allowed.")
        return node.value

    if isinstance(node, ast.BinOp):
        operation = binary_operations.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported arithmetic operation.")

        left = _evaluate_expression(node.left)
        right = _evaluate_expression(node.right)

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = unary_operations.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported unary operation.")

        return operation(_evaluate_expression(node.operand))

    raise ValueError("Invalid dosage expression.")


def calculate_dosage(formula):
    """Calculate dosage using a restricted arithmetic expression."""
    if not isinstance(formula, str) or len(formula) > 100:
        raise ValueError("Invalid dosage formula.")

    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as error:
        raise ValueError("Invalid dosage formula.") from error

    if sum(1 for _ in ast.walk(tree)) > 30:
        raise ValueError("Dosage formula is too complex.")

    result = _evaluate_expression(tree)

    if (
        isinstance(result, bool)
        or not isinstance(result, (int, float))
        or not math.isfinite(result)
    ):
        raise ValueError("Dosage result must be a finite number.")

    return result


def patient_id(patient_name):
    """Generate a SHA-256 identifier for a patient name."""
    if not isinstance(patient_name, str) or not patient_name.strip():
        raise ValueError("Patient name cannot be empty.")

    return hashlib.sha256(
        patient_name.encode("utf-8")
    ).hexdigest()


def generate_rx_number():
    """Generate a cryptographically secure prescription number."""
    return f"RX-{secrets.randbelow(900000) + 100000}"


def save_stock(filename="pharmacy.json"):
    """Save current medicine inventory to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(medicines, file, indent=4)


def load_stock(filename="pharmacy.json"):
    """Load and validate medicine inventory from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return False
    except (json.JSONDecodeError, OSError):
        return False

    if not isinstance(data, dict):
        return False

    try:
        for name, details in data.items():
            validate_medicine(name, details)
    except ValueError:
        return False

    medicines.clear()
    medicines.update(data)

    return True


def print_label(name):
    """Print a medicine dispensing label."""
    if name not in medicines:
        raise ValueError("Medicine not found.")

    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the specified number of days."""
    if isinstance(days, bool) or not isinstance(days, int) or days < 0:
        raise ValueError("Days must be a non-negative integer.")

    today = datetime.now().date()
    results = []

    for name, details in medicines.items():
        expiry_date = datetime.strptime(
            details["expiry"], "%Y-%m-%d"
        ).date()

        remaining_days = (expiry_date - today).days

        if 0 <= remaining_days <= days:
            results.append(name)

    return results


def pharmacist_login(password):
    """Verify a pharmacist password using constant-time comparison."""
    if not isinstance(password, str) or not DB_PASSWORD:
        return False

    return hmac.compare_digest(password, DB_PASSWORD)


def print_stock():
    """Display all available medicines and their stock details."""
    print("===== Pharmacy Stock Report =====")

    for name, details in medicines.items():
        print(
            f"{name} -> {details['qty']} units, "
            f"Rs. {details['price']} exp {details['expiry']}"
        )


def main():
    """Run the pharmacy management demonstration."""
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print("Bill:", bill_amount("Paracetamol 500mg", 30))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Test Patient"))
    print("Rx number:", generate_rx_number())

    password = DB_PASSWORD
    print("Login:", pharmacist_login(password))

    print_label("Paracetamol 500mg")
    print_stock()


if __name__ == "__main__":
    main()
