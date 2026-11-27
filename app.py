import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import calculator
import visualization
import scenario_analysis
import scenario_visualization


st.set_page_config(
    page_title="Finance Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)


COLORS = {
    "background": "#0B1016",
    "surface": "#141C25",
    "primary": "#69D3B5",
    "secondary": "#639CC9",
    "accent": "#D6B77A",
    "text": "#E5E9EF",
    "muted": "#94A3B8",
    "grid": "#293440"
}


def currency(value):
    return f"${value:,.2f}"


def style_chart(figure, title, xlabel, ylabel):
    figure.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor=COLORS["background"],
        plot_bgcolor=COLORS["surface"],
        font=dict(
            color=COLORS["text"],
            size=13
        ),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        hovermode="closest",
        height=480,
        margin=dict(l=30, r=30, t=70, b=50),
        legend=dict(
            orientation="h",
            y=-0.2
        )
    )

    figure.update_xaxes(
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"]
    )

    figure.update_yaxes(
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"],
        tickprefix="$",
        tickformat=",.0f"
    )

    return figure


def page_header(section, title, description):
    st.caption(
        f"FINANCE CALCULATOR / {section.upper()}"
    )

    st.title(title)
    st.write(description)
    st.divider()


def amount_input(label, value, key):
    return st.number_input(
        label,
        min_value=0.0,
        max_value=1_000_000_000.0,
        value=float(value),
        step=100.0,
        format="%.2f",
        key=key
    )


def rate_input(label, value, key):
    return st.number_input(
        label,
        min_value=-99.0,
        max_value=100.0,
        value=float(value),
        step=0.5,
        format="%.2f",
        key=key
    )


def duration_input(key, value=10):
    return st.slider(
        "Projection duration (years)",
        min_value=1,
        max_value=50,
        value=value,
        key=key
    )


def overview_page():
    page_header(
        "Overview",
        "Financial Mathematics Laboratory",
        (
            "An interactive workspace for compound growth, "
            "time value of money, purchasing power, "
            "and deterministic scenario analysis."
        )
    )

    columns = st.columns(4)

    columns[0].metric(
        "Mathematical models",
        "7"
    )

    columns[1].metric(
        "CLI visualizations",
        "8"
    )

    columns[2].metric(
        "Recorded core tests",
        "191"
    )

    columns[3].metric(
        "Export formats",
        "CSV / PNG"
    )

    st.subheader("Analytical workspaces")

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.subheader("Growth Laboratory")
            st.write(
                "Explore combined principal and contribution "
                "projections, nominal growth and "
                "inflation-adjusted balances."
            )

        with st.container(border=True):
            st.subheader("Financial Mathematics")
            st.write(
                "Evaluate compound accumulation, discounting, "
                "annuity contributions and interest-rate "
                "conversions."
            )

    with right:
        with st.container(border=True):
            st.subheader("Scenario Analytics")
            st.write(
                "Compare hypothetical assumptions using "
                "structured scenario matrices and "
                "baseline sensitivity analysis."
            )

        with st.container(border=True):
            st.subheader("Mathematical Methodology")
            st.write(
                "Review model equations, numerical stability, "
                "validation methods and analytical limitations."
            )

    st.subheader("Illustrative projection")

    records = visualization.calculate_projection_data(
        1000, 100, 5, 20, 2
    )

    frame = pd.DataFrame(records)

    render_growth_chart(frame)

    st.caption(
        "Synthetic example: $1,000 principal, "
        "$100 monthly contribution, 5% effective annual "
        "growth and 2% annual inflation."
    )

    st.info(
        "All calculations are deterministic educational "
        "models. They do not predict actual market outcomes."
    )

    st.subheader("Project resources")

    st.markdown(
        "[Source repository]"
        "(https://github.com/LakshSuri/finance-calculator)"
    )

    st.markdown(
        "[Derivatives Pricing Laboratory]"
        "(https://derivatives-research-lab.streamlit.app)"
    )


def render_growth_chart(frame):
    figure = go.Figure()

    series = [
        (
            "nominal_future_value",
            "Nominal balance",
            COLORS["primary"]
        ),
        (
            "inflation_adjusted_value",
            "Inflation-adjusted balance",
            COLORS["secondary"]
        ),
        (
            "total_principal",
            "Total principal",
            COLORS["muted"]
        )
    ]

    for column, label, color in series:
        figure.add_trace(
            go.Scatter(
                x=frame["years"],
                y=frame[column],
                mode="lines",
                name=label,
                line=dict(
                    color=color,
                    width=3,
                    dash=(
                        "dash"
                        if column == "total_principal"
                        else "solid"
                    )
                ),
                hovertemplate=(
                    "Year %{x}<br>"
                    "$%{y:,.2f}<extra></extra>"
                )
            )
        )

    style_chart(
        figure,
        "Principal, Growth and Purchasing Power",
        "Years",
        "Calculated value"
    )

    st.plotly_chart(figure)


def render_breakdown_chart(frame):
    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=frame["years"],
            y=frame["starting_amount"],
            name="Starting principal",
            marker_color=COLORS["secondary"]
        )
    )

    figure.add_trace(
        go.Bar(
            x=frame["years"],
            y=frame["total_contributions"],
            name="Monthly contributions",
            marker_color=COLORS["muted"]
        )
    )

    figure.add_trace(
        go.Scatter(
            x=frame["years"],
            y=frame["nominal_future_value"],
            mode="lines",
            name="Calculated balance",
            line=dict(
                color=COLORS["primary"],
                width=3
            )
        )
    )

    style_chart(
        figure,
        "Principal and Contribution Decomposition",
        "Years",
        "Calculated value"
    )

    figure.update_layout(
        barmode="stack"
    )

    st.plotly_chart(figure)


def growth_page():
    page_header(
        "Growth Laboratory",
        "Combined Growth Projection",
        (
            "Analyze the mathematical relationship between "
            "initial principal, periodic contributions, "
            "compound accumulation and purchasing power."
        )
    )

    left, right = st.columns(2)

    with left:
        principal = amount_input(
            "Hypothetical starting principal ($)",
            1000,
            "growth_principal"
        )

        monthly = amount_input(
            "Monthly contribution ($)",
            100,
            "growth_monthly"
        )

        years = duration_input(
            "growth_years"
        )

    with right:
        rate = rate_input(
            "Effective annual growth assumption (%)",
            5,
            "growth_rate"
        )

        inflation = rate_input(
            "Annual inflation assumption (%)",
            2,
            "growth_inflation"
        )

        st.caption(
            "Contributions occur at the end of each month."
        )

    result = calculator.projection_breakdown(
        principal,
        monthly,
        rate,
        years,
        inflation
    )

    columns = st.columns(4)

    columns[0].metric(
        "Nominal balance",
        currency(result["nominal_future_value"])
    )

    columns[1].metric(
        "Purchasing power",
        currency(result["inflation_adjusted_value"])
    )

    columns[2].metric(
        "Total principal",
        currency(result["total_principal"])
    )

    columns[3].metric(
        "Nominal growth or loss",
        currency(result["nominal_growth"])
    )

    records = visualization.calculate_projection_data(
        principal,
        monthly,
        rate,
        years,
        inflation
    )

    frame = pd.DataFrame(records)

    growth_tab, breakdown_tab, data_tab = st.tabs(
        [
            "Growth projection",
            "Contribution breakdown",
            "Numerical data"
        ]
    )

    with growth_tab:
        render_growth_chart(frame)

    with breakdown_tab:
        render_breakdown_chart(frame)

    with data_tab:
        st.dataframe(
            frame,
            hide_index=True
        )

        st.download_button(
            "Download projection CSV",
            data=frame.to_csv(index=False),
            file_name="financial_projection.csv",
            mime="text/csv"
        )


def mathematics_page():
    page_header(
        "Financial Mathematics",
        "Time Value of Money",
        (
            "Evaluate mathematical relationships under "
            "explicit interest-rate conventions."
        )
    )

    operation = st.selectbox(
        "Mathematical operation",
        [
            "Compound future value",
            "Monthly contribution accumulation",
            "Hypothetical goal calculation",
            "Present value",
            "Inflation adjustment",
            "Interest-rate conversion"
        ]
    )

    left, right = st.columns(2)

    if operation == "Compound future value":
        with left:
            amount = amount_input(
                "Starting principal ($)",
                1000,
                "fv_amount"
            )

            years = duration_input("fv_years")

        with right:
            rate = rate_input(
                "Effective annual rate (%)",
                5,
                "fv_rate"
            )

        result = calculator.future_value(
            amount, rate, years
        )

        st.metric(
            "Calculated future value",
            currency(result)
        )

        st.latex(
            r"FV=P(1+r)^t"
        )

        st.write(
            "The initial principal compounds at the "
            "specified effective annual rate."
        )

    elif operation == "Monthly contribution accumulation":
        with left:
            amount = amount_input(
                "Monthly contribution ($)",
                100,
                "monthly_amount"
            )

            years = duration_input("monthly_years")

        with right:
            rate = rate_input(
                "Nominal annual rate (%)",
                5,
                "monthly_rate"
            )

        result = calculator.future_value_monthly(
            amount, rate, years
        )

        st.metric(
            "Accumulated value",
            currency(result)
        )

        st.latex(
            r"FV=C\frac{(1+i)^n-1}{i}"
        )

        st.write(
            "This model uses end-of-month contributions "
            "and a monthly rate equal to the nominal "
            "annual rate divided by twelve."
        )

    elif operation == "Hypothetical goal calculation":
        with left:
            target = amount_input(
                "Synthetic target amount ($)",
                50000,
                "goal_amount"
            )

            years = duration_input("goal_years")

        with right:
            rate = rate_input(
                "Nominal annual rate (%)",
                5,
                "goal_rate"
            )

        result = calculator.monthly_investment_goal(
            target, rate, years
        )

        st.metric(
            "Calculated periodic contribution",
            currency(result)
        )

        st.latex(
            r"C=FV\frac{i}{(1+i)^n-1}"
        )

        st.caption(
            "Mathematical solution for the specified "
            "hypothetical scenario, not a personalized "
            "financial recommendation."
        )

    elif operation == "Present value":
        with left:
            amount = amount_input(
                "Future amount ($)",
                10000,
                "pv_amount"
            )

            years = duration_input("pv_years")

        with right:
            rate = rate_input(
                "Effective annual discount rate (%)",
                5,
                "pv_rate"
            )

        result = calculator.present_value(
            amount, rate, years
        )

        st.metric(
            "Calculated present value",
            currency(result)
        )

        st.latex(
            r"PV=\frac{FV}{(1+r)^t}"
        )

    elif operation == "Inflation adjustment":
        with left:
            amount = amount_input(
                "Nominal future amount ($)",
                10000,
                "inflation_amount"
            )

            years = duration_input(
                "inflation_years"
            )

        with right:
            rate = rate_input(
                "Annual inflation assumption (%)",
                2,
                "inflation_rate"
            )

        result = calculator.inflation_adjusted_value(
            amount, rate, years
        )

        st.metric(
            "Inflation-adjusted value",
            currency(result)
        )

        st.latex(
            r"V_{\mathrm{real}}="
            r"\frac{V_{\mathrm{nominal}}}{(1+\pi)^t}"
        )

    else:
        rate = rate_input(
            "Effective annual rate (%)",
            5,
            "conversion_rate"
        )

        monthly = calculator.effective_monthly_rate(
            rate
        )

        columns = st.columns(3)

        columns[0].metric(
            "Effective annual rate",
            f"{rate:.6f}%"
        )

        columns[1].metric(
            "Equivalent monthly rate",
            f"{monthly * 100:.6f}%"
        )

        columns[2].metric(
            "Equivalent nominal annual rate",
            f"{monthly * 1200:.6f}%"
        )

        st.latex(
            r"i=(1+r)^{1/12}-1"
        )

    st.divider()

    st.caption(
        "All amounts and rates are hypothetical inputs. "
        "The models exclude taxes, fees and market uncertainty."
    )


def scenario_page():
    page_header(
        "Scenario Analytics",
        "Growth and Inflation Sensitivity",
        (
            "Compare deterministic financial projections "
            "across multiple mathematical assumptions."
        )
    )

    left, right = st.columns(2)

    with left:
        principal = amount_input(
            "Starting principal ($)",
            1000,
            "scenario_principal"
        )

        monthly = amount_input(
            "Monthly contribution ($)",
            100,
            "scenario_monthly"
        )

        years = duration_input(
            "scenario_years"
        )

    with right:
        annual_rates = st.multiselect(
            "Effective annual growth assumptions (%)",
            options=[-20, -10, -5, 0, 3, 5, 7, 10, 15, 20],
            default=[-5, 0, 5, 10]
        )

        inflation_rates = st.multiselect(
            "Annual inflation assumptions (%)",
            options=[-2, 0, 1, 2, 3, 4, 6, 8, 10],
            default=[0, 2, 4]
        )

        baseline_rate = rate_input(
            "Baseline annual growth (%)",
            5,
            "scenario_baseline_rate"
        )

        baseline_inflation = rate_input(
            "Baseline inflation (%)",
            2,
            "scenario_baseline_inflation"
        )

    if not annual_rates or not inflation_rates:
        st.warning(
            "Select at least one growth assumption "
            "and one inflation assumption."
        )
        return

    records = scenario_analysis.compare_scenarios(
        principal,
        monthly,
        years,
        annual_rates,
        inflation_rates,
        baseline_rate,
        baseline_inflation
    )

    summary = scenario_analysis.summarize_scenarios(
        records
    )

    columns = st.columns(4)

    columns[0].metric(
        "Scenarios",
        summary["scenario_count"]
    )

    columns[1].metric(
        "Minimum modeled value",
        currency(summary["minimum_real_value"])
    )

    columns[2].metric(
        "Maximum modeled value",
        currency(summary["maximum_real_value"])
    )

    columns[3].metric(
        "Modeled value range",
        currency(summary["real_value_range"])
    )

    growth_rates, inflation_rates, matrix = (
        scenario_visualization.build_sensitivity_matrix(
            records
        )
    )

    heatmap_tab, baseline_tab, data_tab = st.tabs(
        [
            "Sensitivity heatmap",
            "Baseline comparison",
            "Scenario data"
        ]
    )

    with heatmap_tab:
        figure = go.Figure(
            go.Heatmap(
                z=matrix,
                x=[
                    f"{rate:g}%"
                    for rate in inflation_rates
                ],
                y=[
                    f"{rate:g}%"
                    for rate in growth_rates
                ],
                colorscale="Viridis",
                text=[
                    [
                        f"${value:,.0f}"
                        for value in row
                    ]
                    for row in matrix
                ],
                texttemplate="%{text}",
                colorbar=dict(
                    title="Real value",
                    tickprefix="$",
                    tickformat=",.0f"
                ),
                hovertemplate=(
                    "Inflation: %{x}<br>"
                    "Growth: %{y}<br>"
                    "Real value: $%{z:,.2f}"
                    "<extra></extra>"
                )
            )
        )

        style_chart(
            figure,
            "Growth and Inflation Sensitivity",
            "Annual inflation assumption",
            "Effective annual growth assumption"
        )

        figure.update_yaxes(
            tickprefix="",
            tickformat=None,
            type="category"
        )

        figure.update_xaxes(
            type="category"
        )

        st.plotly_chart(figure)

    with baseline_tab:
        ordered = sorted(
            records,
            key=lambda row: row[
                "real_value_change_from_baseline"
            ]
        )

        labels = [
            (
                f"{row['annual_rate']:g}% growth / "
                f"{row['inflation_rate']:g}% inflation"
            )
            for row in ordered
        ]

        values = [
            row["real_value_change_from_baseline"]
            for row in ordered
        ]

        figure = go.Figure(
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker_color=[
                    COLORS["primary"]
                    if value >= 0
                    else COLORS["accent"]
                    for value in values
                ],
                hovertemplate=(
                    "%{y}<br>"
                    "Difference: $%{x:,.2f}"
                    "<extra></extra>"
                )
            )
        )

        style_chart(
            figure,
            "Differences from Baseline",
            "Change in inflation-adjusted value",
            "Scenario"
        )

        figure.update_layout(
            height=max(480, len(records) * 27)
        )

        figure.update_xaxes(
            tickprefix="$",
            tickformat=",.0f"
        )

        figure.update_yaxes(
            tickprefix="",
            tickformat=None,
            automargin=True
        )

        st.plotly_chart(figure)

        st.caption(
            f"Baseline: {baseline_rate:g}% growth "
            f"and {baseline_inflation:g}% inflation."
        )

    with data_tab:
        frame = pd.DataFrame(records)

        st.dataframe(
            frame,
            hide_index=True
        )

        st.download_button(
            "Download scenario CSV",
            data=scenario_analysis.scenarios_to_csv(
                records
            ),
            file_name="scenario_analysis.csv",
            mime="text/csv"
        )

    st.info(
        "Minimum and maximum values describe only "
        "the selected scenario grid. They are not "
        "statistical confidence intervals, probability "
        "estimates or bounds on actual future outcomes."
    )


def methodology_page():
    page_header(
        "Methodology",
        "Mathematical Foundations",
        (
            "Equations, numerical methods, assumptions "
            "and limitations underlying the laboratory."
        )
    )

    st.subheader("1. Compound accumulation")

    st.latex(
        r"FV=P(1+r)^t"
    )

    st.write(
        "P represents initial principal, r represents "
        "the effective annual rate in decimal form, "
        "and t represents time in years."
    )

    st.subheader("2. Ordinary annuity")

    st.latex(
        r"FV=C\frac{(1+i)^n-1}{i}"
    )

    st.write(
        "C represents the end-of-month contribution, "
        "i represents the monthly interest rate, "
        "and n represents the number of months."
    )

    st.latex(
        r"\lim_{i\to0}C\frac{(1+i)^n-1}{i}=Cn"
    )

    st.subheader("3. Rate conventions")

    st.latex(
        r"i_{\mathrm{effective}}=(1+r)^{1/12}-1"
    )

    st.latex(
        r"i_{\mathrm{nominal}}=\frac{j}{12}"
    )

    st.write(
        "The original monthly contribution and goal "
        "functions use nominal annual rates. Combined "
        "projections use effective annual rates."
    )

    st.subheader("4. Combined projection")

    st.latex(
        r"FV=P(1+r)^t+C\frac{(1+i)^{12t}-1}{i}"
    )

    st.subheader("5. Present value and purchasing power")

    st.latex(
        r"PV=\frac{FV}{(1+r)^t}"
    )

    st.latex(
        r"V_{\mathrm{real}}="
        r"\frac{V_{\mathrm{nominal}}}{(1+\pi)^t}"
    )

    st.subheader("6. Numerical stability")

    st.write(
        "The mathematical engine evaluates compound "
        "growth using log1p and expm1 where appropriate "
        "to reduce loss of numerical precision near zero."
    )

    st.latex(
        r"(1+i)^n-1="
        r"\operatorname{expm1}"
        r"\left(n\operatorname{log1p}(i)\right)"
    )

    st.subheader("7. Deterministic scenario analysis")

    st.write(
        "The scenario engine evaluates combinations of "
        "growth and inflation assumptions and measures "
        "their differences from a common baseline."
    )

    st.latex(
        r"\Delta V=V_{\mathrm{scenario}}-V_{\mathrm{baseline}}"
    )

    st.subheader("8. Model limitations")

    st.markdown(
        """
- Constant growth and inflation assumptions.
- End-of-month contributions.
- No taxes, transaction costs or management fees.
- No stochastic asset-price behavior.
- No probability-weighted scenario estimates.
- No personalized investment recommendations.
        """
    )

    st.subheader("9. Software validation")

    st.write(
        "The core test suite evaluates mathematical "
        "identities, independent iterative calculations, "
        "boundary conditions, invalid inputs, interface "
        "behavior, chart generation and data exports."
    )

    st.markdown(
        "[Automated quality checks]"
        "(https://github.com/LakshSuri/finance-calculator/actions)"
    )


def main():
    with st.sidebar:
        st.caption("QUANTITATIVE FINANCE")
        st.title("Finance Calculator")

        st.caption(
            "Financial Mathematics Laboratory"
        )

        st.divider()

        page = st.radio(
            "Research workspace",
            [
                "Overview",
                "Growth Laboratory",
                "Financial Mathematics",
                "Scenario Analytics",
                "Methodology"
            ]
        )

        st.divider()

        st.caption(
            "Deterministic models. "
            "Explicit assumptions. "
            "Reproducible calculations."
        )

        st.markdown(
            "[GitHub repository]"
            "(https://github.com/LakshSuri/finance-calculator)"
        )

    pages = {
        "Overview": overview_page,
        "Growth Laboratory": growth_page,
        "Financial Mathematics": mathematics_page,
        "Scenario Analytics": scenario_page,
        "Methodology": methodology_page
    }

    try:
        pages[page]()

    except (ValueError, OverflowError):
        st.error(
            "The specified assumptions exceed the "
            "supported numerical limits."
        )

    st.divider()

    st.caption(
        "Finance Calculator | Educational mathematical "
        "modeling and deterministic scenario analysis"
    )


if __name__ == "__main__":
    main()