# Tip & Tax Calculator - Streamlit

Streamlit version of `5098_State1CPProgram2026.py`.

## Run web interface

```bash
chmod +x start.sh
./start.sh
```

Open:

```text
http://127.0.0.1:8501
```

## Run terminal version

```bash
chmod +x run_cli.sh
./run_cli.sh
```

## Features

- Enter bill subtotal.
- Enter configurable tax rate.
- Enter configurable tip percentage.
- Show subtotal, tax amount, tip amount, and final total.
- Show formatted printable billing report.
- Export the result as `billing_report.csv`.

## Files

- `app.py`: Streamlit web application.
- `cli.py`: cleaned terminal version of the original script.
- `requirements.txt`: Python dependencies.
- `start.sh`: starts the Streamlit app.
- `run_cli.sh`: starts the terminal version.
