from __future__ import annotations

import io
from dataclasses import dataclass
from datetime import date, datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


@dataclass(frozen=True)
class SeriesConfig:
    name: str
    source: str
    code: str
    unit: str
    frequency: str


SERIES_CONFIGS = {
    "ipca": SeriesConfig(
        name="IPCA mensal",
        source="Banco Central SGS",
        code="433",
        unit="%",
        frequency="Mensal",
    ),
    "desemprego": SeriesConfig(
        name="Taxa de desemprego",
        source="Banco Central SGS",
        code="24369",
        unit="%",
        frequency="Mensal",
    ),
    "brent": SeriesConfig(
        name="Petróleo Brent",
        source="FRED",
        code="DCOILBRENTEU",
        unit="US$/barril",
        frequency="Diária",
    ),
}


def apply_theme(theme_mode: str) -> None:
    if theme_mode == "Dark":
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: #0f172a;
                    color: #e5e7eb;
                }

                [data-testid="stSidebar"] {
                    background-color: #111827;
                    color: #e5e7eb;
                }

                [data-testid="stMetric"] {
                    background-color: #1f2937;
                    border: 1px solid #374151;
                    padding: 16px;
                    border-radius: 14px;
                }

                div[data-testid="stDataFrame"] {
                    background-color: #111827;
                }

                h1, h2, h3, h4, h5, h6, p, span, label {
                    color: #e5e7eb !important;
                }

                .stDownloadButton button,
                .stButton button,
                div.stForm button {
                    background-color: #2563eb;
                    color: white;
                    border-radius: 10px;
                    border: none;
                }

                .stDownloadButton button:hover,
                .stButton button:hover,
                div.stForm button:hover {
                    background-color: #1d4ed8;
                    color: white;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: #f8fafc;
                    color: #0f172a;
                }

                [data-testid="stSidebar"] {
                    background-color: #ffffff;
                    color: #0f172a;
                    border-right: 1px solid #e5e7eb;
                }

                [data-testid="stMetric"] {
                    background-color: #ffffff;
                    border: 1px solid #e5e7eb;
                    padding: 16px;
                    border-radius: 14px;
                    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
                }

                .stDownloadButton button,
                .stButton button,
                div.stForm button {
                    background-color: #2563eb;
                    color: white;
                    border-radius: 10px;
                    border: none;
                }

                .stDownloadButton button:hover,
                .stButton button:hover,
                div.stForm button:hover {
                    background-color: #1d4ed8;
                    color: white;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )


def parse_bcb_value(value: object) -> float:
    return float(str(value).replace(",", "."))


@st.cache_data(ttl=60 * 60)
def fetch_bcb_sgs(
    series_code: str,
    variable_name: str,
    unit: str,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_code}/dados"

    params = {
        "formato": "json",
        "dataInicial": start_date.strftime("%d/%m/%Y"),
        "dataFinal": end_date.strftime("%d/%m/%Y"),
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not data:
        return pd.DataFrame(columns=["date", "variable", "value", "unit", "source"])

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
    df["value"] = df["valor"].map(parse_bcb_value)
    df["variable"] = variable_name
    df["unit"] = unit
    df["source"] = "Banco Central SGS"

    return df[["date", "variable", "value", "unit", "source"]].dropna()


@st.cache_data(ttl=60 * 60)
def fetch_fred_series(
    series_code: str,
    variable_name: str,
    unit: str,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_code}"

    df = pd.read_csv(url)

    if "DATE" not in df.columns or series_code not in df.columns:
        return pd.DataFrame(columns=["date", "variable", "value", "unit", "source"])

    df = df.rename(columns={"DATE": "date", series_code: "value"})

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    df = df[(df["date"] >= start_ts) & (df["date"] <= end_ts)]
    df = df.dropna(subset=["date", "value"])

    df["variable"] = variable_name
    df["unit"] = unit
    df["source"] = "FRED"

    return df[["date", "variable", "value", "unit", "source"]]


def load_macro_data(start_date: date, end_date: date) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []

    try:
        frames.append(
            fetch_bcb_sgs(
                series_code=SERIES_CONFIGS["ipca"].code,
                variable_name=SERIES_CONFIGS["ipca"].name,
                unit=SERIES_CONFIGS["ipca"].unit,
                start_date=start_date,
                end_date=end_date,
            )
        )
    except Exception as exc:
        st.warning(f"Falha ao carregar IPCA: {exc}")

    try:
        frames.append(
            fetch_bcb_sgs(
                series_code=SERIES_CONFIGS["desemprego"].code,
                variable_name=SERIES_CONFIGS["desemprego"].name,
                unit=SERIES_CONFIGS["desemprego"].unit,
                start_date=start_date,
                end_date=end_date,
            )
        )
    except Exception as exc:
        st.warning(f"Falha ao carregar desemprego: {exc}")

    try:
        frames.append(
            fetch_fred_series(
                series_code=SERIES_CONFIGS["brent"].code,
                variable_name=SERIES_CONFIGS["brent"].name,
                unit=SERIES_CONFIGS["brent"].unit,
                start_date=start_date,
                end_date=end_date,
            )
        )
    except Exception as exc:
        st.warning(f"Falha ao carregar Brent: {exc}")

    valid_frames = [frame for frame in frames if not frame.empty]

    if not valid_frames:
        return pd.DataFrame(columns=["date", "variable", "value", "unit", "source"])

    result = pd.concat(valid_frames, ignore_index=True)
    result = result.dropna(subset=["date", "variable", "value"])
    result = result.sort_values(["variable", "date"])

    return result


def normalize_base_100(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()

    if normalized.empty:
        normalized["value_index"] = pd.Series(dtype="float")
        return normalized

    if "variable" not in normalized.columns:
        normalized = normalized.reset_index()

    if "variable" not in normalized.columns:
        raise ValueError("A coluna 'variable' não existe no DataFrame.")

    normalized = normalized.sort_values(["variable", "date"]).copy()

    first_values = normalized.groupby("variable")["value"].transform("first")

    normalized["value_index"] = normalized["value"] / first_values * 100
    normalized.loc[first_values == 0, "value_index"] = None

    return normalized


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for variable, group in df.groupby("variable"):
        ordered = group.sort_values("date").copy()

        if ordered.empty:
            continue

        first = ordered.iloc[0]
        last = ordered.iloc[-1]

        absolute_change = float(last["value"]) - float(first["value"])

        percentage_change = (
            (float(last["value"]) / float(first["value"]) - 1) * 100
            if float(first["value"]) != 0
            else None
        )

        rows.append(
            {
                "Variável": variable,
                "Último valor": round(float(last["value"]), 4),
                "Unidade": last["unit"],
                "Data inicial": first["date"].date().isoformat(),
                "Valor inicial": round(float(first["value"]), 4),
                "Data final": last["date"].date().isoformat(),
                "Variação absoluta": round(float(absolute_change), 4),
                "Variação %": round(float(percentage_change), 2)
                if percentage_change is not None
                else None,
                "Fonte": last["source"],
            }
        )

    return pd.DataFrame(rows)


def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    export_df = df.copy()

    if "date" in export_df.columns:
        export_df["date"] = pd.to_datetime(export_df["date"], errors="coerce")
        export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")

    return export_df.to_csv(index=False).encode("utf-8")


def create_pdf_chart(df: pd.DataFrame, chart_mode: str) -> io.BytesIO:
    chart_df = normalize_base_100(df) if chart_mode == "Índice base 100" else df.copy()

    y_column = "value_index" if chart_mode == "Índice base 100" else "value"
    y_label = "Índice base 100" if chart_mode == "Índice base 100" else "Valor"

    fig, ax = plt.subplots(figsize=(10, 4.5))

    for variable, group in chart_df.groupby("variable"):
        group = group.sort_values("date")
        ax.plot(group["date"], group[y_column], label=variable)

    ax.set_title("Séries macroeconômicas filtradas")
    ax.set_xlabel("Data")
    ax.set_ylabel(y_label)
    ax.legend()
    ax.grid(True, alpha=0.3)

    buffer = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png", dpi=160)
    plt.close(fig)

    buffer.seek(0)
    return buffer


def create_pdf_report(
    df: pd.DataFrame,
    kpis_df: pd.DataFrame,
    start_date: date,
    end_date: date,
    selected_variables: list[str],
    chart_mode: str,
) -> bytes:
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Dashboard Macroeconômico - Visão Exportada", styles["Title"]))
    elements.append(Spacer(1, 0.2 * inch))

    filter_text = (
        f"<b>Período:</b> {start_date.isoformat()} até {end_date.isoformat()}<br/>"
        f"<b>Variáveis:</b> {', '.join(selected_variables)}<br/>"
        f"<b>Modo do gráfico:</b> {chart_mode}<br/>"
        f"<b>Gerado em:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    elements.append(Paragraph(filter_text, styles["Normal"]))
    elements.append(Spacer(1, 0.25 * inch))

    if not kpis_df.empty:
        kpi_table_data = [list(kpis_df.columns)] + kpis_df.astype(str).values.tolist()

        kpi_table = Table(kpi_table_data, repeatRows=1)
        kpi_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        elements.append(Paragraph("Resumo dos indicadores", styles["Heading2"]))
        elements.append(kpi_table)
        elements.append(Spacer(1, 0.25 * inch))

    if not df.empty:
        chart_buffer = create_pdf_chart(df, chart_mode)
        elements.append(Paragraph("Gráfico da visão filtrada", styles["Heading2"]))
        elements.append(Image(chart_buffer, width=9.5 * inch, height=4.1 * inch))
        elements.append(Spacer(1, 0.25 * inch))

    preview_df = df.copy()
    preview_df["date"] = pd.to_datetime(preview_df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    preview_df = preview_df.sort_values(["variable", "date"]).tail(40)

    if not preview_df.empty:
        table_data = [list(preview_df.columns)] + preview_df.astype(str).values.tolist()

        data_table = Table(table_data, repeatRows=1)
        data_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        elements.append(Paragraph("Últimos registros da visão filtrada", styles["Heading2"]))
        elements.append(data_table)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


def build_uploaded_dataframe(uploaded_file) -> pd.DataFrame:
    external_df = pd.read_csv(uploaded_file)

    required_columns = {"date", "variable", "value", "unit", "source"}

    if not required_columns.issubset(external_df.columns):
        missing = required_columns - set(external_df.columns)
        raise ValueError(f"CSV externo inválido. Colunas ausentes: {', '.join(missing)}")

    external_df["date"] = pd.to_datetime(external_df["date"], errors="coerce")
    external_df["value"] = pd.to_numeric(external_df["value"], errors="coerce")
    external_df = external_df.dropna(subset=["date", "value", "variable"])

    return external_df[["date", "variable", "value", "unit", "source"]]


def render_series_catalog() -> None:
    catalog = []

    for config in SERIES_CONFIGS.values():
        catalog.append(
            {
                "Variável": config.name,
                "Fonte": config.source,
                "Código": config.code,
                "Unidade": config.unit,
                "Frequência": config.frequency,
            }
        )

    st.dataframe(
        pd.DataFrame(catalog),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Macro Dashboard",
        layout="wide",
    )

    with st.sidebar:
        st.header("Aparência")

        theme_mode = st.radio(
            "Tema",
            options=["Light", "Dark"],
            index=0,
            horizontal=True,
        )

    apply_theme(theme_mode)

    st.title("Macro Dashboard")
    st.caption(
        "Dashboard para acompanhar IPCA, desemprego e preço do petróleo com filtros, gráficos e exportação PDF."
    )

    default_end = date.today()
    default_start = default_end - timedelta(days=365 * 5)

    with st.sidebar:
        st.divider()
        st.header("Filtros")

        start_date = st.date_input(
            "Data inicial",
            value=default_start,
        )

        end_date = st.date_input(
            "Data final",
            value=default_end,
        )

        if start_date > end_date:
            st.error("A data inicial não pode ser maior que a data final.")
            st.stop()

        available_variables = [config.name for config in SERIES_CONFIGS.values()]

        selected_variables = st.multiselect(
            "Variáveis",
            options=available_variables,
            default=available_variables,
        )

        chart_mode = st.radio(
            "Modo do gráfico principal",
            options=["Valor original", "Índice base 100"],
            index=1,
        )

        chart_type = st.radio(
            "Tipo de gráfico",
            options=["Linha", "Área", "Barras"],
            index=0,
        )

        show_raw_data = st.checkbox("Mostrar tabela completa", value=True)

        st.divider()

        st.subheader("Upload opcional")

        uploaded_file = st.file_uploader(
            "Adicionar CSV externo",
            type=["csv"],
            help="Use colunas: date, variable, value, unit, source.",
        )

    with st.spinner("Carregando séries macroeconômicas..."):
        df = load_macro_data(start_date, end_date)

    if uploaded_file is not None:
        try:
            external_df = build_uploaded_dataframe(uploaded_file)
            df = pd.concat([df, external_df], ignore_index=True)
            st.success("CSV externo carregado com sucesso.")
        except Exception as exc:
            st.warning(str(exc))

    if df.empty:
        st.error("Nenhum dado encontrado para o período selecionado.")
        st.stop()

    df = df.dropna(subset=["date", "variable", "value"]).copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["date", "value"])

    if not selected_variables:
        st.warning("Selecione pelo menos uma variável.")
        st.stop()

    df = df[df["variable"].isin(selected_variables)].copy()

    if df.empty:
        st.warning("Nenhum dado encontrado para as variáveis selecionadas.")
        st.stop()

    df = df.sort_values(["variable", "date"]).copy()

    kpis_df = calculate_kpis(df)

    st.subheader("Catálogo das séries")

    with st.expander("Ver fontes e códigos das séries", expanded=False):
        render_series_catalog()

    st.subheader("Resumo executivo")

    if kpis_df.empty:
        st.warning("Não foi possível calcular os indicadores.")
        st.stop()

    metric_cols = st.columns(min(len(kpis_df), 4))

    for index, (_, row) in enumerate(kpis_df.iterrows()):
        col = metric_cols[index % len(metric_cols)]

        variation = row["Variação %"]
        delta = f"{variation}%" if pd.notna(variation) else None

        col.metric(
            label=row["Variável"],
            value=f"{row['Último valor']} {row['Unidade']}",
            delta=delta,
        )

    st.divider()

    st.subheader("Indicadores")

    st.dataframe(
        kpis_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Gráfico principal")

    try:
        chart_df = normalize_base_100(df) if chart_mode == "Índice base 100" else df.copy()
    except Exception as exc:
        st.error(f"Erro ao preparar dados do gráfico: {exc}")
        st.stop()

    if "variable" not in chart_df.columns:
        chart_df = chart_df.reset_index()

    if "variable" not in chart_df.columns:
        st.error("Erro interno: a coluna 'variable' não existe no DataFrame do gráfico.")
        st.write(chart_df.head())
        st.stop()

    y_column = "value_index" if chart_mode == "Índice base 100" else "value"
    y_title = "Índice base 100" if chart_mode == "Índice base 100" else "Valor original"

    if y_column not in chart_df.columns:
        st.error(f"Erro interno: a coluna '{y_column}' não existe no DataFrame do gráfico.")
        st.write(chart_df.head())
        st.stop()

    if chart_type == "Linha":
        fig = px.line(
            chart_df,
            x="date",
            y=y_column,
            color="variable",
            markers=True,
            labels={
                "date": "Data",
                y_column: y_title,
                "variable": "Variável",
            },
        )
    elif chart_type == "Área":
        fig = px.area(
            chart_df,
            x="date",
            y=y_column,
            color="variable",
            labels={
                "date": "Data",
                y_column: y_title,
                "variable": "Variável",
            },
        )
    else:
        fig = px.bar(
            chart_df,
            x="date",
            y=y_column,
            color="variable",
            barmode="group",
            labels={
                "date": "Data",
                y_column: y_title,
                "variable": "Variável",
            },
        )

    fig.update_layout(
        height=520,
        hovermode="x unified",
        legend_title_text="Variável",
        template="plotly_dark" if theme_mode == "Dark" else "plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Análise por variável")

    tabs = st.tabs(selected_variables)

    for tab, variable in zip(tabs, selected_variables):
        variable_df = df[df["variable"] == variable].sort_values("date").copy()

        with tab:
            if variable_df.empty:
                st.warning(f"Sem dados para {variable}.")
                continue

            col1, col2, col3 = st.columns(3)

            latest_row = variable_df.iloc[-1]
            min_row = variable_df.loc[variable_df["value"].idxmin()]
            max_row = variable_df.loc[variable_df["value"].idxmax()]

            col1.metric(
                "Último valor",
                f"{latest_row['value']:.4f} {latest_row['unit']}",
            )
            col2.metric(
                "Mínimo no período",
                f"{min_row['value']:.4f} {min_row['unit']}",
            )
            col3.metric(
                "Máximo no período",
                f"{max_row['value']:.4f} {max_row['unit']}",
            )

            variable_fig = px.line(
                variable_df,
                x="date",
                y="value",
                markers=True,
                labels={
                    "date": "Data",
                    "value": f"Valor ({latest_row['unit']})",
                },
                title=variable,
            )

            variable_fig.update_layout(
                height=420,
                template="plotly_dark" if theme_mode == "Dark" else "plotly_white",
            )

            st.plotly_chart(variable_fig, use_container_width=True)

            st.dataframe(
                variable_df.assign(date=variable_df["date"].dt.date),
                use_container_width=True,
                hide_index=True,
            )

    if show_raw_data:
        st.divider()
        st.subheader("Base filtrada")

        table_df = df.copy()
        table_df["date"] = table_df["date"].dt.date

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Exportações")

    col_csv, col_pdf = st.columns(2)

    col_csv.download_button(
        "Baixar CSV da visão filtrada",
        data=dataframe_to_csv(df),
        file_name="macro_dashboard_filtrado.csv",
        mime="text/csv",
    )

    pdf_bytes = create_pdf_report(
        df=df,
        kpis_df=kpis_df,
        start_date=start_date,
        end_date=end_date,
        selected_variables=selected_variables,
        chart_mode=chart_mode,
    )

    col_pdf.download_button(
        "Baixar PDF da visão filtrada",
        data=pdf_bytes,
        file_name="macro_dashboard_filtrado.pdf",
        mime="application/pdf",
    )

    st.caption("Fontes: Banco Central SGS para IPCA/desemprego e FRED para Brent.")


if __name__ == "__main__":
    main()