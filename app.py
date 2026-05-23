from __future__ import annotations

import csv
import io
from dataclasses import asdict, dataclass

import streamlit as st


@dataclass(frozen=True)
class BillingResult:
    subtotal: float
    tax_rate: float
    tip_percentage: float
    tax_amount: float
    tip_amount: float
    total: float


def calculate_bill(subtotal: float, tax_rate: float, tip_percentage: float) -> BillingResult:
    """Calculate tax, tip, and final total."""
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


def result_to_csv(result: BillingResult) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(asdict(result).keys()))
    writer.writeheader()
    writer.writerow(asdict(result))
    return output.getvalue()


def result_to_report(result: BillingResult) -> str:
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


def main() -> None:
    st.set_page_config(
        page_title="Tip & Tax Calculator",
        layout="wide",
    )

    st.title("Tip & Tax Calculator")
    st.caption(
        "Calculate a restaurant bill using subtotal, configurable tax rate, and tip percentage."
    )

    with st.sidebar:
        st.header("Bill inputs")

        with st.form("billing_form"):
            subtotal = st.number_input(
                "Bill subtotal",
                min_value=0.0,
                value=50.0,
                step=1.0,
                format="%.2f",
            )

            tax_rate_percent = st.number_input(
                "Tax rate (%)",
                min_value=0.0,
                value=8.00,
                step=0.25,
                format="%.2f",
            )

            tip_percentage_percent = st.number_input(
                "Tip percentage (%)",
                min_value=0.0,
                value=18.00,
                step=1.0,
                format="%.2f",
            )

            submitted = st.form_submit_button("Calculate bill")

    tax_rate = tax_rate_percent / 100
    tip_percentage = tip_percentage_percent / 100
    result = calculate_bill(float(subtotal), tax_rate, tip_percentage)

    if tax_rate >= 1 or tip_percentage >= 1:
        st.warning(
            "One percentage is greater than or equal to 100%. The calculator will still use it."
        )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Subtotal", format_money(result.subtotal))
    col2.metric("Tax amount", format_money(result.tax_amount))
    col3.metric("Tip amount", format_money(result.tip_amount))
    col4.metric("Total", format_money(result.total))

    st.divider()

    st.subheader("Billing summary")
    summary_data = [
        {"Item": "Subtotal", "Value": format_money(result.subtotal)},
        {"Item": "Tax rate", "Value": format_percent(result.tax_rate)},
        {"Item": "Tax amount", "Value": format_money(result.tax_amount)},
        {"Item": "Tip percentage", "Value": format_percent(result.tip_percentage)},
        {"Item": "Tip amount", "Value": format_money(result.tip_amount)},
        {"Item": "Total amount to pay", "Value": format_money(result.total)},
    ]
    st.dataframe(summary_data, use_container_width=True, hide_index=True)

    st.subheader("Printable report")
    st.code(result_to_report(result), language="text")

    st.download_button(
        "Download billing_report.csv",
        data=result_to_csv(result),
        file_name="billing_report.csv",
        mime="text/csv",
    )

    if submitted:
        st.success("Bill calculated.")


if __name__ == "__main__":
    main()
