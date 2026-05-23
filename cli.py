from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path

SAVE_PATH = Path("billing_report.csv")


@dataclass(frozen=True)
class BillingResult:
    subtotal: float
    tax_rate: float
    tip_percentage: float
    tax_amount: float
    tip_amount: float
    total: float


def get_float(prompt: str, is_percentage: bool = False) -> float:
    """Read a positive float from user input. Type exit to quit."""
    while True:
        try:
            raw = input(prompt).strip().lower()

            if raw == "exit":
                raise SystemExit("Program terminated by user.")

            value = float(raw)

            if value < 0:
                raise ValueError("Value must be greater than or equal to 0.")

            if is_percentage and value >= 1:
                while True:
                    control = input(
                        "Warning: percentage is greater than or equal to 100%. Keep it? (Y/N) "
                    ).strip().lower()
                    if control in {"y", "n"}:
                        break

                if control == "n":
                    continue

            return value

        except ValueError as error:
            print(f"Invalid input: {error}")
        except OverflowError:
            print("Input too large.")
        except KeyboardInterrupt:
            raise SystemExit("\nProgram interrupted by user.")
        except EOFError:
            raise SystemExit("\nNo input detected. Exiting.")


def calculate_bill(subtotal: float, tax_rate: float, tip_percentage: float) -> BillingResult:
    tax_amount = subtotal * tax_rate
    tip_amount = subtotal * tip_percentage
    total = subtotal + tax_amount + tip_amount

    return BillingResult(
        subtotal=subtotal,
        tax_rate=tax_rate,
        tip_percentage=tip_percentage,
        tax_amount=tax_amount,
        tip_amount=tip_amount,
        total=total,
    )


def format_money(value: float) -> str:
    return f"${value:,.2f}"


def format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def generate_report(result: BillingResult) -> str:
    width_text = 25
    width_num = 12
    width_total = width_text + width_num + 1

    rows = [
        f"{'Billing Report':-^{width_total}}",
        f"{'Subtotal':<{width_text}} {format_money(result.subtotal):>{width_num}}",
        f"{'Tax Rate':<{width_text}} {format_percent(result.tax_rate):>{width_num}}",
        f"{'Tax Amount':<{width_text}} {format_money(result.tax_amount):>{width_num}}",
        f"{'Tip Percentage':<{width_text}} {format_percent(result.tip_percentage):>{width_num}}",
        f"{'Tip Amount':<{width_text}} {format_money(result.tip_amount):>{width_num}}",
        f"{'Summary':-^{width_total}}",
        f"{'Total amount to pay is':<{width_text}} {format_money(result.total):>{width_num}}",
        f"{'Thank you!':-^{width_total}}",
    ]
    return "\n".join(rows)


def save_report(result: BillingResult, path: Path = SAVE_PATH) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(asdict(result).keys()))
        writer.writeheader()
        writer.writerow(asdict(result))


def main() -> None:
    print("\nSmall Restaurant bill calculator")

    subtotal = get_float("Enter bill subtotal: (exit to quit) ")
    tax_rate = get_float("Enter the tax rate as decimal, example 0.08: (exit to quit) ", True)
    tip_percentage = get_float(
        "Enter the tip percentage as decimal, example 0.18: (exit to quit) ", True
    )

    result = calculate_bill(subtotal, tax_rate, tip_percentage)
    print("\n" + generate_report(result))

    save_report(result)
    print(f"\nReport saved to {SAVE_PATH}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as error:
        print(error)
