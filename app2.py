from __future__ import annotations

import csv
import io
import sqlite3
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


DB_PATH = Path("billing_app.sqlite3")


@dataclass(frozen=True)
class BillingResult:
    subtotal: float
    tax_rate: float
    tip_percentage: float
    tax_amount: float
    tip_amount: float
    total: float


@dataclass(frozen=True)
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS receipts (
            receipt_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax_rate REAL NOT NULL,
            tip_percentage REAL NOT NULL,
            tax_amount REAL NOT NULL,
            tip_amount REAL NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        );
        """
    )

    conn.commit()


def calculate_bill(
    subtotal: float,
    tax_rate: float,
    tip_percentage: float,
) -> BillingResult:
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


def normalize_email(email: str) -> str:
    return email.strip().lower()


def create_customer(
    conn: sqlite3.Connection,
    name: str,
    email: str,
    phone: str,
) -> tuple[bool, str]:
    name = name.strip()
    email = normalize_email(email)
    phone = phone.strip()

    if not name:
        return False, "Customer name is required."

    if not email:
        return False, "Customer email is required."

    if not phone:
        return False, "Customer phone is required."

    customer_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat(timespec="seconds")

    try:
        conn.execute(
            """
            INSERT INTO customers (
                customer_id,
                name,
                email,
                phone,
                created_at
            )
            VALUES (?, ?, ?, ?, ?);
            """,
            (customer_id, name, email, phone, created_at),
        )
        conn.commit()
        return True, "Customer registered successfully."
    except sqlite3.IntegrityError:
        return False, "A customer with this email already exists."


def get_customers(conn: sqlite3.Connection) -> list[Customer]:
    rows = conn.execute(
        """
        SELECT
            customer_id,
            name,
            email,
            phone
        FROM customers
        ORDER BY name ASC;
        """
    ).fetchall()

    return [
        Customer(
            customer_id=row["customer_id"],
            name=row["name"],
            email=row["email"],
            phone=row["phone"],
        )
        for row in rows
    ]


def save_receipt(
    conn: sqlite3.Connection,
    customer_id: str,
    result: BillingResult,
) -> str:
    receipt_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat(timespec="seconds")

    conn.execute(
        """
        INSERT INTO receipts (
            receipt_id,
            customer_id,
            subtotal,
            tax_rate,
            tip_percentage,
            tax_amount,
            tip_amount,
            total,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            receipt_id,
            customer_id,
            result.subtotal,
            result.tax_rate,
            result.tip_percentage,
            result.tax_amount,
            result.tip_amount,
            result.total,
            created_at,
        ),
    )

    conn.commit()
    return receipt_id


def get_receipts_dataframe(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
        SELECT
            r.receipt_id,
            r.created_at,
            c.customer_id,
            c.name AS customer_name,
            c.email AS customer_email,
            c.phone AS customer_phone,
            r.subtotal,
            r.tax_rate,
            r.tip_percentage,
            r.tax_amount,
            r.tip_amount,
            r.total
        FROM receipts r
        INNER JOIN customers c
            ON c.customer_id = r.customer_id
        ORDER BY r.created_at DESC;
    """

    return pd.read_sql_query(query, conn)


def result_to_csv(result: BillingResult, customer: Customer | None = None) -> str:
    output = io.StringIO()

    row: dict[str, Any] = asdict(result)

    if customer:
        row = {
            "customer_id": customer.customer_id,
            "customer_name": customer.name,
            "customer_email": customer.email,
            "customer_phone": customer.phone,
            **row,
        }

    writer = csv.DictWriter(output, fieldnames=list(row.keys()))
    writer.writeheader()
    writer.writerow(row)

    return output.getvalue()


def dataframe_to_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)


def result_to_report(result: BillingResult, customer: Customer | None = None) -> str:
    width_text = 25
    width_num = 12
    width_total = width_text + width_num + 1

    customer_rows = []

    if customer:
        customer_rows = [
            f"{'Customer':-^{width_total}}",
            f"{'Name':<{width_text}} {customer.name:>{width_num}}",
            f"{'Email':<{width_text}} {customer.email:>{width_num}}",
            f"{'Phone':<{width_text}} {customer.phone:>{width_num}}",
        ]

    rows = [
        f"{'Billing Report':-^{width_total}}",
        *customer_rows,
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


def get_customer_by_id(
    customers: list[Customer],
    customer_id: str,
) -> Customer | None:
    for customer in customers:
        if customer.customer_id == customer_id:
            return customer

    return None


def render_customer_registration(conn: sqlite3.Connection) -> None:
    st.subheader("Customer registration")

    with st.form("customer_registration_form", clear_on_submit=True):
        name = st.text_input("Customer name")
        email = st.text_input("Customer email")
        phone = st.text_input("Customer phone")

        submitted = st.form_submit_button("Register customer")

    if submitted:
        success, message = create_customer(conn, name, email, phone)

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)


def render_receipt_creator(
    conn: sqlite3.Connection,
    customers: list[Customer],
) -> None:
    st.subheader("Create receipt")

    if not customers:
        st.warning("Register at least one customer before creating receipts.")
        return

    customer_options = {
        f"{customer.name} | {customer.email} | {customer.phone}": customer.customer_id
        for customer in customers
    }

    with st.form("billing_form"):
        selected_customer_label = st.selectbox(
            "Assign receipt to customer",
            options=list(customer_options.keys()),
        )

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

        calculate_submitted = st.form_submit_button("Calculate receipt")

    customer_id = customer_options[selected_customer_label]
    selected_customer = get_customer_by_id(customers, customer_id)

    tax_rate = tax_rate_percent / 100
    tip_percentage = tip_percentage_percent / 100

    result = calculate_bill(
        subtotal=float(subtotal),
        tax_rate=tax_rate,
        tip_percentage=tip_percentage,
    )

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
        {"Item": "Customer", "Value": selected_customer.name if selected_customer else ""},
        {"Item": "Email", "Value": selected_customer.email if selected_customer else ""},
        {"Item": "Phone", "Value": selected_customer.phone if selected_customer else ""},
        {"Item": "Subtotal", "Value": format_money(result.subtotal)},
        {"Item": "Tax rate", "Value": format_percent(result.tax_rate)},
        {"Item": "Tax amount", "Value": format_money(result.tax_amount)},
        {"Item": "Tip percentage", "Value": format_percent(result.tip_percentage)},
        {"Item": "Tip amount", "Value": format_money(result.tip_amount)},
        {"Item": "Total amount to pay", "Value": format_money(result.total)},
    ]

    st.dataframe(summary_data, use_container_width=True, hide_index=True)

    st.subheader("Printable report")
    st.code(result_to_report(result, selected_customer), language="text")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Save receipt to database", type="primary"):
            receipt_id = save_receipt(conn, customer_id, result)
            st.success(f"Receipt saved. Receipt ID: {receipt_id}")

    with col_b:
        st.download_button(
            "Download current receipt CSV",
            data=result_to_csv(result, selected_customer),
            file_name="billing_report.csv",
            mime="text/csv",
        )

    if calculate_submitted:
        st.success("Receipt calculated.")


def render_customer_reports(
    conn: sqlite3.Connection,
    customers: list[Customer],
) -> None:
    st.subheader("Reports by customer")

    receipts_df = get_receipts_dataframe(conn)

    if receipts_df.empty:
        st.info("No receipts saved yet.")
        return

    all_tab, customer_summary_tab, revenue_by_customer_tab = st.tabs(
        [
            "All receipts",
            "Customer summary",
            "Revenue by Customer",
        ]
    )

    with all_tab:
        st.dataframe(receipts_df, use_container_width=True, hide_index=True)

        st.download_button(
            "Download all receipts CSV",
            data=dataframe_to_csv(receipts_df),
            file_name="all_receipts.csv",
            mime="text/csv",
        )

    with customer_summary_tab:
        summary_df = (
            receipts_df.groupby(
                ["customer_id", "customer_name", "customer_email", "customer_phone"],
                as_index=False,
            )
            .agg(
                receipts_count=("receipt_id", "count"),
                subtotal_sum=("subtotal", "sum"),
                tax_sum=("tax_amount", "sum"),
                tip_sum=("tip_amount", "sum"),
                total_sum=("total", "sum"),
            )
            .sort_values("total_sum", ascending=False)
        )

        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        st.download_button(
            "Download customer summary CSV",
            data=dataframe_to_csv(summary_df),
            file_name="customer_summary.csv",
            mime="text/csv",
        )

    with revenue_by_customer_tab:
        st.subheader("Revenue by Customer")

        customer_options = {
            f"{customer.name} | {customer.email} | {customer.phone}": customer.customer_id
            for customer in customers
        }

        selected_customer_labels = st.multiselect(
            "Select customer",
            options=list(customer_options.keys()),
            default=list(customer_options.keys())[:1],
        )

        selected_customer_ids = [
            customer_options[label]
            for label in selected_customer_labels
        ]

        if not selected_customer_ids:
            st.warning("Select at least one customer.")
            return

        customer_df = receipts_df[
            receipts_df["customer_id"].isin(selected_customer_ids)
        ].copy()

        if customer_df.empty:
            st.info("No receipts found for the selected customer.")
            return

        revenue_summary_df = (
            customer_df.groupby(
                ["customer_id", "customer_name", "customer_email", "customer_phone"],
                as_index=False,
            )
            .agg(
                receipts_count=("receipt_id", "count"),
                subtotal_sum=("subtotal", "sum"),
                tax_sum=("tax_amount", "sum"),
                tip_sum=("tip_amount", "sum"),
                total_revenue=("total", "sum"),
                average_receipt=("total", "mean"),
            )
            .sort_values("total_revenue", ascending=False)
        )

        total_revenue = customer_df["total"].sum()
        total_receipts = len(customer_df)
        average_receipt = total_revenue / total_receipts if total_receipts else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Selected receipts", f"{total_receipts}")
        col2.metric("Selected revenue", format_money(total_revenue))
        col3.metric("Average receipt", format_money(average_receipt))

        st.divider()

        st.markdown("### Revenue summary")
        st.dataframe(
            revenue_summary_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### Receipt details")
        st.dataframe(
            customer_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download selected customer revenue CSV",
            data=dataframe_to_csv(customer_df),
            file_name="selected_customer_revenue.csv",
            mime="text/csv",
        )

def main() -> None:
    st.set_page_config(
        page_title="Customer Receipt Manager",
        layout="wide",
    )

    conn = get_connection()
    init_db(conn)

    st.title("Customer Receipt Manager")
    st.caption(
        "Register customers, calculate receipts, assign each receipt to a customer, and report transactions using SQLite."
    )

    customers = get_customers(conn)

    page_customer, page_receipt, page_reports = st.tabs(
        [
            "Customer registration",
            "Create receipt",
            "Reports",
        ]
    )

    with page_customer:
        render_customer_registration(conn)

        st.divider()

        st.subheader("Registered customers")

        if customers:
            customers_df = pd.DataFrame([asdict(customer) for customer in customers])
            st.dataframe(customers_df, use_container_width=True, hide_index=True)
        else:
            st.info("No customers registered yet.")

    with page_receipt:
        render_receipt_creator(conn, customers)

    with page_reports:
        render_customer_reports(conn, customers)


if __name__ == "__main__":
    main()