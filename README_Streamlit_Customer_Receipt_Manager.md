# Customer Receipt Manager — Streamlit Learning README

This README explains the full Streamlit application for managing customers, calculating receipts, storing transactions in SQLite, and generating customer-based reports.

The goal is not only to document the app, but also to help you learn how Streamlit works by using your own project as the reference.

---

## 1. Project Overview

This application is a small billing and receipt management system built with:

- **Streamlit** for the web interface.
- **SQLite** for local database storage.
- **Pandas** for table/report generation.
- **Dataclasses** for clean data modeling.
- **CSV export** for downloading receipt and report data.

The app allows the user to:

1. Register customers with name, email, and phone.
2. Store each customer with a unique UUID.
3. Calculate a receipt using subtotal, tax rate, and tip percentage.
4. Assign every receipt to one customer.
5. Save receipts into a SQLite database.
6. View all receipts.
7. View customer summary reports.
8. View revenue filtered by selected customer(s).
9. Download receipt and report data as CSV files.

---

## 2. Main Technologies Used

### 2.1 Streamlit

Streamlit is a Python framework for building data apps quickly. Instead of writing HTML, CSS, JavaScript, backend routes, and frontend state logic manually, you write Python commands such as:

```python
st.title("Customer Receipt Manager")
st.text_input("Customer name")
st.number_input("Bill subtotal")
st.dataframe(df)
st.download_button(...)
```

Streamlit converts those commands into an interactive web interface.

### 2.2 SQLite

SQLite is a lightweight local database. It stores data in a single file:

```python
DB_PATH = Path("billing_app.sqlite3")
```

In this app, SQLite stores:

- Customers
- Receipts
- Relationships between receipts and customers

SQLite is good for learning, prototypes, small apps, and local tools.

### 2.3 Pandas

Pandas is used to load SQL query results into DataFrames:

```python
pd.read_sql_query(query, conn)
```

Then the app can:

- Show tables with `st.dataframe`
- Group data by customer
- Calculate total revenue
- Export reports to CSV

### 2.4 Dataclasses

The app uses Python dataclasses to represent clean structured objects:

```python
@dataclass(frozen=True)
class BillingResult:
    subtotal: float
    tax_rate: float
    tip_percentage: float
    tax_amount: float
    tip_amount: float
    total: float
```

Dataclasses help keep the code organized and readable.

---

## 3. Project File Structure

The current app is written in one Python file.

Recommended simple structure:

```text
customer_receipt_manager/
│
├── app.py
├── billing_app.sqlite3
├── requirements.txt
└── README.md
```

Recommended expanded structure for future growth:

```text
customer_receipt_manager/
│
├── app.py
├── database.py
├── models.py
├── services.py
├── reports.py
├── requirements.txt
└── README.md
```

For learning Streamlit, keeping everything in one file is acceptable. For a more professional app, splitting the code into modules is better.

---

## 4. Installation

### 4.1 Create a project folder

```bash
mkdir customer_receipt_manager
cd customer_receipt_manager
```

### 4.2 Create a virtual environment

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4.3 Install dependencies

Create a file named `requirements.txt`:

```txt
streamlit
pandas
```

Install:

```bash
pip install -r requirements.txt
```

---

## 5. Running the App

If your file is named `app.py`, run:

```bash
streamlit run app.py
```

Streamlit will start a local web server and open the app in your browser.

Typical local URL:

```text
http://localhost:8501
```

---

## 6. App Entry Point

At the bottom of the file, the app has:

```python
if __name__ == "__main__":
    main()
```

This means:

- When the file is executed directly, Python runs `main()`.
- `main()` builds the full Streamlit interface.
- This is the main controller of the application.

---

## 7. Streamlit Execution Model

This is one of the most important concepts.

Streamlit reruns the entire Python script from top to bottom every time the user interacts with the page.

Examples of actions that trigger reruns:

- Typing in an input
- Clicking a button
- Submitting a form
- Selecting an option
- Changing a tab
- Downloading data

This is different from traditional web frameworks.

In Streamlit, you do not usually write frontend event listeners. Instead, every widget returns a value, and the script uses that value during the current run.

Example:

```python
subtotal = st.number_input("Bill subtotal", value=50.0)
```

When the user changes the number, Streamlit reruns the script and `subtotal` receives the new value.

---

## 8. Page Configuration

The app starts with:

```python
st.set_page_config(
    page_title="Customer Receipt Manager",
    layout="wide",
)
```

### What this does

`page_title` changes the browser tab title.

`layout="wide"` gives the app more horizontal space. This is useful for dashboards, tables, and reports.

Common options:

```python
st.set_page_config(page_title="My App")
st.set_page_config(layout="centered")
st.set_page_config(layout="wide")
```

Important rule:

`st.set_page_config()` should be one of the first Streamlit commands executed.

---

## 9. Database Path

```python
DB_PATH = Path("billing_app.sqlite3")
```

This defines the SQLite database file.

If the file does not exist, SQLite creates it automatically when the app connects.

The database file is local. That means:

- It exists on the machine running the app.
- If deployed to a temporary cloud environment, data may be lost unless persistent storage is configured.
- For production SaaS apps, PostgreSQL is usually better.

---

## 10. Data Models

### 10.1 BillingResult

```python
@dataclass(frozen=True)
class BillingResult:
    subtotal: float
    tax_rate: float
    tip_percentage: float
    tax_amount: float
    tip_amount: float
    total: float
```

This object stores the result of the bill calculation.

Fields:

| Field | Meaning |
|---|---|
| `subtotal` | Original bill value before tax and tip |
| `tax_rate` | Tax rate in decimal format, for example `0.08` |
| `tip_percentage` | Tip percentage in decimal format, for example `0.18` |
| `tax_amount` | Calculated tax amount |
| `tip_amount` | Calculated tip amount |
| `total` | Final amount to pay |

The class is marked as:

```python
frozen=True
```

That means the object is immutable after creation. This is useful because a calculation result should not be accidentally changed.

### 10.2 Customer

```python
@dataclass(frozen=True)
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str
```

This object represents a customer.

Fields:

| Field | Meaning |
|---|---|
| `customer_id` | Unique customer UUID |
| `name` | Customer name |
| `email` | Customer email |
| `phone` | Customer phone |

---

## 11. Database Connection

```python
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
```

### Explanation

This function creates a connection to SQLite.

#### `sqlite3.connect(DB_PATH)`

Opens the SQLite database file.

#### `check_same_thread=False`

Streamlit can rerun and reuse code in ways that may conflict with SQLite thread checks. This option avoids thread-related errors in this simple app.

#### `conn.row_factory = sqlite3.Row`

This makes SQL result rows behave like dictionaries.

Without it, you access values like:

```python
row[0]
```

With it, you can access values by column name:

```python
row["name"]
```

This is clearer and safer.

#### `PRAGMA foreign_keys = ON`

SQLite does not always enforce foreign keys unless explicitly enabled. This line ensures that the relationship between customers and receipts is respected.

---

## 12. Database Initialization

```python
def init_db(conn: sqlite3.Connection) -> None:
```

This function creates the database tables if they do not already exist.

It creates two tables:

1. `customers`
2. `receipts`

---

## 13. Customers Table

```sql
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

### Columns

| Column | Type | Meaning |
|---|---|---|
| `customer_id` | TEXT | UUID primary key |
| `name` | TEXT | Customer name |
| `email` | TEXT | Unique customer email |
| `phone` | TEXT | Customer phone |
| `created_at` | TEXT | Creation timestamp |

### Important constraints

#### `PRIMARY KEY`

Ensures every customer has a unique ID.

#### `NOT NULL`

The column is required.

#### `UNIQUE`

The email must be unique. This prevents duplicate customer records using the same email.

---

## 14. Receipts Table

```sql
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
```

### Columns

| Column | Type | Meaning |
|---|---|---|
| `receipt_id` | TEXT | UUID receipt ID |
| `customer_id` | TEXT | ID of the customer assigned to the receipt |
| `subtotal` | REAL | Original bill value |
| `tax_rate` | REAL | Tax rate as decimal |
| `tip_percentage` | REAL | Tip percentage as decimal |
| `tax_amount` | REAL | Calculated tax value |
| `tip_amount` | REAL | Calculated tip value |
| `total` | REAL | Final receipt total |
| `created_at` | TEXT | Receipt creation timestamp |

### Foreign key

```sql
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
```

This means every receipt must belong to a valid customer.

### `ON DELETE RESTRICT`

This prevents deleting a customer if receipts exist for that customer.

### `ON UPDATE CASCADE`

If a customer ID changes, related receipts are updated automatically. In practice, UUIDs should not usually change.

---

## 15. Billing Calculation

```python
def calculate_bill(
    subtotal: float,
    tax_rate: float,
    tip_percentage: float,
) -> BillingResult:
```

This function calculates:

```python
tax_amount = subtotal * tax_rate
tip_amount = subtotal * tip_percentage
total = subtotal + tax_amount + tip_amount
```

Example:

```text
Subtotal: 100.00
Tax rate: 8% = 0.08
Tip percentage: 18% = 0.18

Tax amount = 100 * 0.08 = 8.00
Tip amount = 100 * 0.18 = 18.00
Total = 100 + 8 + 18 = 126.00
```

The function returns a `BillingResult`.

This is good design because calculation logic is separated from the Streamlit interface.

---

## 16. Formatting Helpers

### 16.1 Money formatting

```python
def format_money(value: float) -> str:
    return f"${value:,.2f}"
```

Example:

```python
format_money(1234.5)
```

Returns:

```text
$1,234.50
```

### 16.2 Percentage formatting

```python
def format_percent(value: float) -> str:
    return f"{value * 100:.2f}%"
```

Example:

```python
format_percent(0.08)
```

Returns:

```text
8.00%
```

### 16.3 Email normalization

```python
def normalize_email(email: str) -> str:
    return email.strip().lower()
```

This removes spaces and converts the email to lowercase.

Example:

```text
" John@Example.COM " -> "john@example.com"
```

This is important because emails should not be duplicated just because of uppercase/lowercase differences.

---

## 17. Customer Creation

```python
def create_customer(
    conn: sqlite3.Connection,
    name: str,
    email: str,
    phone: str,
) -> tuple[bool, str]:
```

This function:

1. Cleans user input.
2. Validates required fields.
3. Generates a UUID.
4. Saves the customer into SQLite.
5. Returns success or error message.

### Input cleanup

```python
name = name.strip()
email = normalize_email(email)
phone = phone.strip()
```

### Required validations

```python
if not name:
    return False, "Customer name is required."
```

The same rule is applied to email and phone.

### UUID generation

```python
customer_id = str(uuid.uuid4())
```

A UUID is a unique identifier such as:

```text
9f6a4e9d-0d7d-4c66-8c58-bbd6a6dfb49e
```

### Timestamp

```python
created_at = datetime.utcnow().isoformat(timespec="seconds")
```

This stores the creation time in UTC.

### Duplicate email handling

```python
except sqlite3.IntegrityError:
    return False, "A customer with this email already exists."
```

Because email is unique in the database, SQLite raises an integrity error when a duplicate email is inserted.

The app catches the error and shows a readable message.

---

## 18. Loading Customers

```python
def get_customers(conn: sqlite3.Connection) -> list[Customer]:
```

This function reads all customers from the database:

```sql
SELECT
    customer_id,
    name,
    email,
    phone
FROM customers
ORDER BY name ASC;
```

Then it converts each row into a `Customer` dataclass.

This is useful because the UI can work with Python objects instead of raw database rows.

---

## 19. Saving Receipts

```python
def save_receipt(
    conn: sqlite3.Connection,
    customer_id: str,
    result: BillingResult,
) -> str:
```

This function saves a calculated receipt into the database.

It receives:

- SQLite connection
- Customer ID
- Billing result

It creates:

```python
receipt_id = str(uuid.uuid4())
created_at = datetime.utcnow().isoformat(timespec="seconds")
```

Then inserts all receipt fields into the `receipts` table.

It returns the new `receipt_id`.

---

## 20. Loading Receipts as a DataFrame

```python
def get_receipts_dataframe(conn: sqlite3.Connection) -> pd.DataFrame:
```

This function joins receipts with customers:

```sql
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
```

### Why use `INNER JOIN`

Receipts store only `customer_id`.

The customer details live in the `customers` table.

The join combines both tables, so the report can display:

- Receipt information
- Customer name
- Customer email
- Customer phone

### Why return a DataFrame

Streamlit works very well with Pandas DataFrames:

```python
st.dataframe(receipts_df)
```

Pandas also makes summaries easy:

```python
receipts_df.groupby(...).agg(...)
```

---

## 21. CSV Export Functions

### 21.1 Current receipt CSV

```python
def result_to_csv(result: BillingResult, customer: Customer | None = None) -> str:
```

This converts one receipt result into CSV text.

If a customer is provided, the customer fields are included.

This CSV is used by:

```python
st.download_button(...)
```

### 21.2 DataFrame CSV

```python
def dataframe_to_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)
```

This converts a full DataFrame into CSV text.

Used for exporting:

- All receipts
- Customer summary
- Selected customer revenue

---

## 22. Printable Report

```python
def result_to_report(result: BillingResult, customer: Customer | None = None) -> str:
```

This builds a text-based printable receipt.

It uses string formatting to align values:

```python
f"{'Subtotal':<{width_text}} {format_money(result.subtotal):>{width_num}}"
```

This means:

- Label is aligned left.
- Value is aligned right.
- Output looks like a receipt.

The report is displayed with:

```python
st.code(result_to_report(result, selected_customer), language="text")
```

`st.code` is usually used for code blocks, but it also works well for fixed-width text reports.

---

## 23. Finding a Customer by ID

```python
def get_customer_by_id(
    customers: list[Customer],
    customer_id: str,
) -> Customer | None:
```

This function loops through the list of customers and returns the one that matches the selected ID.

If no customer is found, it returns `None`.

This is used after the user selects a customer from the dropdown.

---

## 24. Customer Registration Screen

```python
def render_customer_registration(conn: sqlite3.Connection) -> None:
```

This function renders the customer registration UI.

### Streamlit form

```python
with st.form("customer_registration_form", clear_on_submit=True):
```

A form groups inputs and prevents Streamlit from rerunning the full app after every single field change.

The form only submits when the user clicks:

```python
submitted = st.form_submit_button("Register customer")
```

### Inputs

```python
name = st.text_input("Customer name")
email = st.text_input("Customer email")
phone = st.text_input("Customer phone")
```

Each input returns a value.

### Submit logic

```python
if submitted:
    success, message = create_customer(conn, name, email, phone)
```

If the customer is created successfully:

```python
st.success(message)
st.rerun()
```

`st.rerun()` forces the app to reload immediately, so the new customer appears in the customer table.

If there is an error:

```python
st.error(message)
```

---

## 25. Receipt Creation Screen

```python
def render_receipt_creator(
    conn: sqlite3.Connection,
    customers: list[Customer],
) -> None:
```

This screen allows the user to create a receipt and assign it to a customer.

### Customer requirement

```python
if not customers:
    st.warning("Register at least one customer before creating receipts.")
    return
```

The app does not allow receipt creation if there are no customers.

This is correct because every receipt must have a customer.

### Customer selectbox

```python
customer_options = {
    f"{customer.name} | {customer.email} | {customer.phone}": customer.customer_id
    for customer in customers
}
```

This creates a dictionary where:

- The key is the label shown to the user.
- The value is the customer UUID.

Example:

```python
{
    "John Doe | john@example.com | 555-1234": "uuid-here"
}
```

The selectbox shows readable labels:

```python
selected_customer_label = st.selectbox(
    "Assign receipt to customer",
    options=list(customer_options.keys()),
)
```

Then the app gets the selected customer ID:

```python
customer_id = customer_options[selected_customer_label]
```

### Number inputs

```python
subtotal = st.number_input(...)
tax_rate_percent = st.number_input(...)
tip_percentage_percent = st.number_input(...)
```

The user enters percentages as human-readable numbers:

```text
8.00
18.00
```

The app converts them to decimal:

```python
tax_rate = tax_rate_percent / 100
tip_percentage = tip_percentage_percent / 100
```

This is important because calculations use decimal values.

### Metrics

```python
col1, col2, col3, col4 = st.columns(4)
col1.metric("Subtotal", format_money(result.subtotal))
col2.metric("Tax amount", format_money(result.tax_amount))
col3.metric("Tip amount", format_money(result.tip_amount))
col4.metric("Total", format_money(result.total))
```

`st.columns(4)` creates a four-column layout.

`st.metric()` displays a KPI-style value.

This is useful for quick summaries.

### Summary table

```python
st.dataframe(summary_data, use_container_width=True, hide_index=True)
```

Although `summary_data` is a list of dictionaries, Streamlit can display it as a table.

### Save button

```python
if st.button("Save receipt to database", type="primary"):
    receipt_id = save_receipt(conn, customer_id, result)
    st.success(f"Receipt saved. Receipt ID: {receipt_id}")
```

This saves the calculated result.

Important behavior:

- `st.button()` returns `True` only on the click run.
- After the next rerun, it returns `False`.

### Download button

```python
st.download_button(
    "Download current receipt CSV",
    data=result_to_csv(result, selected_customer),
    file_name="billing_report.csv",
    mime="text/csv",
)
```

This lets the user download the current receipt without saving it to the database.

---

## 26. Reports Screen

```python
def render_customer_reports(
    conn: sqlite3.Connection,
    customers: list[Customer],
) -> None:
```

This screen loads saved receipts and generates reports.

### Empty state

```python
if receipts_df.empty:
    st.info("No receipts saved yet.")
    return
```

If there are no receipts, the report screen stops early.

This is good UI design because it avoids showing empty charts/tables.

---

## 27. Report Tabs

```python
all_tab, customer_summary_tab, revenue_by_customer_tab = st.tabs(
    [
        "All receipts",
        "Customer summary",
        "Revenue by Customer",
    ]
)
```

Streamlit tabs split the report page into sections.

The app has:

1. All receipts
2. Customer summary
3. Revenue by Customer

---

## 28. All Receipts Tab

```python
with all_tab:
    st.dataframe(receipts_df, use_container_width=True, hide_index=True)
```

This shows every saved receipt.

Then the user can download all records:

```python
st.download_button(
    "Download all receipts CSV",
    data=dataframe_to_csv(receipts_df),
    file_name="all_receipts.csv",
    mime="text/csv",
)
```

---

## 29. Customer Summary Tab

The app groups receipts by customer:

```python
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
```

### What this does

For each customer, it calculates:

| Field | Meaning |
|---|---|
| `receipts_count` | Number of receipts |
| `subtotal_sum` | Sum of subtotal values |
| `tax_sum` | Sum of tax amounts |
| `tip_sum` | Sum of tip amounts |
| `total_sum` | Sum of final receipt totals |

Then it sorts customers by the highest total revenue.

---

## 30. Revenue by Customer Tab

This tab allows selecting one or more customers:

```python
selected_customer_labels = st.multiselect(
    "Select customer",
    options=list(customer_options.keys()),
    default=list(customer_options.keys())[:1],
)
```

### Why `multiselect` is better than one tab per customer

Creating a separate tab for every customer is not scalable.

If the app has 5 customers, it may be okay.

If the app has 500 customers, the UI becomes unusable.

A `multiselect` is better because:

- It handles many customers.
- It allows one or many selections.
- It keeps the UI clean.
- It avoids dynamically creating too many tabs.

### Filtering the DataFrame

```python
customer_df = receipts_df[
    receipts_df["customer_id"].isin(selected_customer_ids)
].copy()
```

This keeps only receipts where `customer_id` is one of the selected customer IDs.

### Revenue summary

```python
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
```

This gives a customer-level revenue report.

### Revenue metrics

```python
total_revenue = customer_df["total"].sum()
total_receipts = len(customer_df)
average_receipt = total_revenue / total_receipts if total_receipts else 0
```

Then the app displays:

```python
col1.metric("Selected receipts", f"{total_receipts}")
col2.metric("Selected revenue", format_money(total_revenue))
col3.metric("Average receipt", format_money(average_receipt))
```

This gives a dashboard-like summary.

---

## 31. Main Function

```python
def main() -> None:
```

The `main()` function organizes the full app.

### Steps inside `main`

1. Configure page.
2. Connect to database.
3. Initialize database tables.
4. Render title and caption.
5. Load customers.
6. Create main tabs.
7. Render each page.

```python
conn = get_connection()
init_db(conn)
customers = get_customers(conn)
```

This ensures the database is ready before rendering the interface.

---

## 32. Main App Tabs

```python
page_customer, page_receipt, page_reports = st.tabs(
    [
        "Customer registration",
        "Create receipt",
        "Reports",
    ]
)
```

These are the main sections of the application.

### Customer registration tab

Contains:

- Customer form
- Registered customers table

### Create receipt tab

Contains:

- Customer selector
- Bill inputs
- Calculation metrics
- Printable report
- Save button
- CSV download

### Reports tab

Contains:

- All receipts
- Customer summary
- Revenue by Customer

---

## 33. Important Streamlit Components Used

### `st.title`

Displays the main page title.

```python
st.title("Customer Receipt Manager")
```

### `st.caption`

Displays small descriptive text.

```python
st.caption("Register customers...")
```

### `st.subheader`

Creates section titles.

```python
st.subheader("Customer registration")
```

### `st.form`

Creates a form that submits as a group.

```python
with st.form("form_name"):
    ...
```

### `st.text_input`

Creates a text field.

```python
st.text_input("Customer name")
```

### `st.number_input`

Creates a numeric input.

```python
st.number_input("Bill subtotal", min_value=0.0)
```

### `st.selectbox`

Creates a dropdown for one selection.

```python
st.selectbox("Assign receipt to customer", options=...)
```

### `st.multiselect`

Creates a dropdown for multiple selections.

```python
st.multiselect("Select customer", options=...)
```

### `st.button`

Creates a normal button.

```python
st.button("Save receipt to database")
```

### `st.form_submit_button`

Creates a submit button inside a form.

```python
st.form_submit_button("Register customer")
```

### `st.dataframe`

Displays a table.

```python
st.dataframe(df, use_container_width=True, hide_index=True)
```

### `st.metric`

Displays KPI values.

```python
st.metric("Total", "$126.00")
```

### `st.columns`

Creates horizontal layout columns.

```python
col1, col2 = st.columns(2)
```

### `st.tabs`

Creates tabs.

```python
tab1, tab2 = st.tabs(["One", "Two"])
```

### `st.download_button`

Creates a downloadable file button.

```python
st.download_button("Download CSV", data=csv_text)
```

### `st.success`

Shows a success message.

```python
st.success("Saved successfully.")
```

### `st.error`

Shows an error message.

```python
st.error("Something failed.")
```

### `st.warning`

Shows a warning message.

```python
st.warning("Register at least one customer.")
```

### `st.info`

Shows an informational message.

```python
st.info("No receipts saved yet.")
```

### `st.divider`

Adds a visual separator.

```python
st.divider()
```

### `st.code`

Shows fixed-width text or code.

```python
st.code(report_text, language="text")
```

### `st.rerun`

Forces Streamlit to rerun the app.

```python
st.rerun()
```

---

## 34. Why Forms Matter in Streamlit

Without a form, every input change triggers a rerun immediately.

Example without form:

```python
name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
```

Every time the user types, the app reruns.

With a form:

```python
with st.form("customer_registration_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    submitted = st.form_submit_button("Save")
```

The app waits until the user clicks submit.

Forms are better when:

- You have multiple related inputs.
- You only want to process data after the user confirms.
- You want cleaner behavior.

---

## 35. Streamlit State in This App

This app does not use `st.session_state`.

Instead, persistent data is stored in SQLite.

That means:

- Customers remain after app reruns.
- Receipts remain after app reruns.
- The database file stores the real state.

For learning, this is simpler.

However, `st.session_state` would be useful for:

- Remembering selected filters
- Keeping temporary form data
- Managing multi-step flows
- Avoiding accidental duplicate saves
- Tracking user-specific UI state

Example:

```python
if "selected_customer_id" not in st.session_state:
    st.session_state.selected_customer_id = None
```

---

## 36. Current Data Flow

### Customer registration flow

```text
User enters name/email/phone
        ↓
Streamlit form submits
        ↓
create_customer()
        ↓
Validate fields
        ↓
Generate UUID
        ↓
Insert into customers table
        ↓
Show success or error
        ↓
Reload customers
```

### Receipt creation flow

```text
User selects customer
        ↓
User enters subtotal, tax, tip
        ↓
calculate_bill()
        ↓
Show metrics and printable report
        ↓
User clicks save
        ↓
save_receipt()
        ↓
Insert receipt into receipts table
        ↓
Show receipt ID
```

### Report flow

```text
Load receipts with customer data
        ↓
Display all receipts
        ↓
Group by customer for summary
        ↓
Allow customer filtering
        ↓
Calculate selected revenue
        ↓
Display tables and metrics
        ↓
Allow CSV download
```

---

## 37. Database Relationship

The relationship is:

```text
customers 1 ──── many receipts
```

One customer can have many receipts.

One receipt belongs to one customer.

This is implemented with:

```sql
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
```

This relationship is correct for this app.

---

## 38. Why UUIDs Are Used

The app uses UUIDs instead of simple numbers.

Example:

```python
str(uuid.uuid4())
```

Benefits:

- Unique across systems
- Good for syncing later
- Good for APIs
- Avoids exposing sequential IDs
- Useful when building more professional systems

For a small local app, integer IDs would also work, but UUIDs are a good habit for scalable systems.

---

## 39. Why Email Is Unique

The customers table has:

```sql
email TEXT NOT NULL UNIQUE
```

This prevents registering the same customer email twice.

This is useful because email is commonly used as a customer identifier.

However, in real business systems, you might allow duplicate emails if:

- One email belongs to a family
- One email is shared by an office
- Customers do not have email addresses

For this learning app, unique email is a good simple rule.

---

## 40. Potential Improvements

### 40.1 Add customer editing

Currently, customers can be created but not edited.

Possible feature:

- Edit name
- Edit phone
- Edit email with duplicate validation

### 40.2 Add customer deletion

Because receipts depend on customers, deletion must be handled carefully.

Possible strategies:

1. Prevent deleting customers with receipts.
2. Soft-delete customers using an `is_active` column.
3. Allow deletion only if no receipts exist.

Recommended professional approach:

```sql
ALTER TABLE customers ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1;
```

Then hide inactive customers instead of deleting them.

### 40.3 Add receipt deletion

The app could allow deleting incorrect receipts.

Recommended:

- Add a confirmation step.
- Or add soft-delete using `deleted_at`.

### 40.4 Add date filters

Reports could include:

- Start date
- End date
- Current month
- Last month
- Current year

### 40.5 Add charts

Streamlit supports charts:

```python
st.bar_chart(...)
st.line_chart(...)
```

For this app, useful charts would be:

- Revenue by customer
- Revenue by day
- Receipt count by customer
- Average receipt by customer

### 40.6 Add database indexes

For better performance, add indexes:

```sql
CREATE INDEX IF NOT EXISTS idx_receipts_customer_id
ON receipts(customer_id);

CREATE INDEX IF NOT EXISTS idx_receipts_created_at
ON receipts(created_at);
```

### 40.7 Add better email validation

Current validation only checks if email is empty.

You could add basic format validation:

```python
import re

def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", email))
```

### 40.8 Add phone formatting

Phone input could be cleaned and standardized.

Example:

```python
phone = phone.replace(" ", "").replace("-", "")
```

### 40.9 Add authentication

For a local learning app, no login is needed.

For production, add:

- User login
- Password hashing
- Role-based permissions
- Per-user data access

### 40.10 Move database logic to a separate file

Current app is acceptable for learning.

For cleaner architecture:

```text
database.py
models.py
services.py
ui.py
app.py
```

---

## 41. Suggested Professional Refactor

A more professional structure:

```text
customer_receipt_manager/
│
├── app.py
├── db/
│   ├── connection.py
│   └── schema.py
│
├── models/
│   ├── billing.py
│   └── customer.py
│
├── services/
│   ├── billing_service.py
│   ├── customer_service.py
│   └── receipt_service.py
│
├── ui/
│   ├── customer_page.py
│   ├── receipt_page.py
│   └── reports_page.py
│
├── utils/
│   ├── formatting.py
│   └── export.py
│
├── requirements.txt
└── README.md
```

This separates responsibilities.

### `app.py`

Starts the app and controls page navigation.

### `db/`

Handles database connection and schema creation.

### `models/`

Stores dataclasses and typed objects.

### `services/`

Stores business logic.

### `ui/`

Stores Streamlit rendering functions.

### `utils/`

Stores helper functions like formatting and CSV export.

---

## 42. Common Streamlit Mistakes to Avoid

### 42.1 Saving data accidentally on every rerun

Bad pattern:

```python
save_receipt(conn, customer_id, result)
```

If this runs outside a button, it saves repeatedly.

Correct pattern:

```python
if st.button("Save"):
    save_receipt(conn, customer_id, result)
```

### 42.2 Using too many tabs dynamically

Bad pattern:

```python
st.tabs([customer.name for customer in customers])
```

This becomes unusable with many customers.

Better pattern:

```python
st.multiselect("Select customer", options=...)
```

### 42.3 Forgetting `conn.commit()`

If you insert data but do not commit, the data may not be saved.

Correct:

```python
conn.execute(...)
conn.commit()
```

### 42.4 Not enabling foreign keys in SQLite

SQLite may not enforce relationships unless enabled:

```python
conn.execute("PRAGMA foreign_keys = ON;")
```

### 42.5 Mixing UI and business logic too much

The current app separates some logic well.

Good examples:

```python
calculate_bill()
create_customer()
save_receipt()
get_receipts_dataframe()
```

These functions are independent from Streamlit and easier to test.

---

## 43. Learning Checklist

Use this checklist to study Streamlit with this app.

### Streamlit basics

- [ ] Understand `st.title`
- [ ] Understand `st.caption`
- [ ] Understand `st.subheader`
- [ ] Understand `st.text_input`
- [ ] Understand `st.number_input`
- [ ] Understand `st.button`
- [ ] Understand `st.form`
- [ ] Understand `st.form_submit_button`
- [ ] Understand `st.dataframe`
- [ ] Understand `st.tabs`
- [ ] Understand `st.columns`
- [ ] Understand `st.metric`
- [ ] Understand `st.download_button`
- [ ] Understand `st.rerun`

### Python structure

- [ ] Understand functions
- [ ] Understand dataclasses
- [ ] Understand type hints
- [ ] Understand tuples
- [ ] Understand dictionaries
- [ ] Understand list comprehensions
- [ ] Understand exception handling

### SQLite

- [ ] Understand database connection
- [ ] Understand table creation
- [ ] Understand primary keys
- [ ] Understand foreign keys
- [ ] Understand `INSERT`
- [ ] Understand `SELECT`
- [ ] Understand `JOIN`
- [ ] Understand `UNIQUE`
- [ ] Understand `commit`

### Pandas

- [ ] Understand DataFrames
- [ ] Understand `read_sql_query`
- [ ] Understand `groupby`
- [ ] Understand `agg`
- [ ] Understand `sort_values`
- [ ] Understand CSV export

---

## 44. Practice Exercises

### Exercise 1: Add address to customer

Add a new customer field:

```text
address
```

You need to update:

- `Customer` dataclass
- `customers` table
- Customer registration form
- Insert query
- Select query
- Registered customers table

### Exercise 2: Add receipt notes

Add a notes field to receipts.

Example:

```text
"Customer paid cash"
```

You need to update:

- `receipts` table
- Receipt form
- Save receipt function
- Reports table

### Exercise 3: Add date filter to reports

Add two date inputs:

```python
start_date = st.date_input("Start date")
end_date = st.date_input("End date")
```

Then filter `receipts_df` by `created_at`.

### Exercise 4: Add revenue chart

Create a customer revenue chart.

Suggested approach:

```python
chart_df = summary_df.set_index("customer_name")["total_sum"]
st.bar_chart(chart_df)
```

### Exercise 5: Add search by customer name

Add:

```python
search = st.text_input("Search customer")
```

Then filter customers by name, email, or phone.

### Exercise 6: Prevent duplicate receipt save

Use `st.session_state` to store the last saved receipt inputs and prevent accidental duplicate saves.

---

## 45. Basic Testing Plan

### Customer registration

Test:

- Empty name
- Empty email
- Empty phone
- Valid customer
- Duplicate email

Expected:

- Empty fields show errors
- Valid customer saves
- Duplicate email is blocked

### Receipt creation

Test:

- No customers registered
- Valid customer selected
- Subtotal = 0
- Normal subtotal
- Tax greater than 100%
- Tip greater than 100%

Expected:

- No customer shows warning
- Valid receipt calculates correctly
- High percentages show warning

### Reports

Test:

- No receipts saved
- One receipt saved
- Multiple receipts for one customer
- Multiple receipts for many customers
- Select one customer
- Select multiple customers
- Select no customer

Expected:

- Empty report shows info
- Tables display correctly
- Revenue summary matches receipt totals
- CSV downloads work

---

## 46. Deployment Notes

For local use:

```bash
streamlit run app.py
```

For cloud deployment, consider:

- Streamlit Community Cloud
- Docker
- VPS
- Cloud Run
- Render
- Railway

Important SQLite warning:

SQLite stores data in a local file. Some cloud environments reset files when the app restarts.

For production, use:

- PostgreSQL
- MySQL
- Supabase
- Cloud SQL

---

## 47. Example `requirements.txt`

```txt
streamlit>=1.30
pandas>=2.0
```

SQLite does not need to be added because it is included in Python's standard library.

The following modules are also standard library modules:

- `csv`
- `io`
- `sqlite3`
- `uuid`
- `dataclasses`
- `datetime`
- `pathlib`
- `typing`

---

## 48. Example Commands

### Run the app

```bash
streamlit run app.py
```

### Install dependencies

```bash
pip install streamlit pandas
```

### Freeze dependencies

```bash
pip freeze > requirements.txt
```

### Delete local database and start fresh

Linux/macOS:

```bash
rm billing_app.sqlite3
```

Windows PowerShell:

```powershell
Remove-Item billing_app.sqlite3
```

The app will recreate the database on the next run.

---

## 49. Key Lessons From This App

This app teaches several important concepts:

1. How Streamlit turns Python code into an interactive interface.
2. How forms work in Streamlit.
3. How to persist data with SQLite.
4. How to model data with dataclasses.
5. How to calculate business logic separately from UI.
6. How to join relational data from two tables.
7. How to display DataFrames in Streamlit.
8. How to build summary reports with Pandas.
9. How to export CSV files.
10. How to organize an app into reusable functions.

---

## 50. Final Summary

The Customer Receipt Manager is a good Streamlit learning project because it combines UI, database, calculations, reporting, and downloads in a single practical app.

The most important concept to understand is this:

```text
Streamlit reruns the script from top to bottom after user interactions.
```

The second most important concept is this:

```text
Persistent data should be stored outside the Streamlit script, such as in SQLite.
```

The third most important concept is this:

```text
Keep business logic separate from UI rendering.
```

Your app already follows several good patterns:

- Uses SQLite for persistence.
- Uses dataclasses for structured data.
- Uses forms for controlled submission.
- Uses UUIDs for unique keys.
- Uses Pandas for reporting.
- Uses tabs for organization.
- Uses CSV downloads for exporting data.
- Uses a `Revenue by Customer` tab instead of creating one tab per customer.

This gives you a solid base to continue learning Streamlit and gradually evolve the app into a more professional billing/reporting system.
