from pathlib import Path

import pytest

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def assert_app_healthy(app):
    assert len(app.exception) == 0
    assert len(app.error) == 0


def metric_value(app, label):
    for metric in app.metric:
        if metric.label == label:
            return metric.value

    pytest.fail(f"Metric not found: {label}")


def open_page(page="Overview"):
    app = AppTest.from_file(
        str(APP_PATH),
        default_timeout=30
    )

    app.run()

    if page != "Overview":
        app.sidebar.radio[0].set_value(page).run()

    assert_app_healthy(app)

    return app


# Page navigation


@pytest.mark.parametrize(
    "page,title",
    [
        (
            "Overview",
            "Financial Mathematics Laboratory"
        ),
        (
            "Growth Laboratory",
            "Combined Growth Projection"
        ),
        (
            "Financial Mathematics",
            "Time Value of Money"
        ),
        (
            "Scenario Analytics",
            "Growth and Inflation Sensitivity"
        ),
        (
            "Methodology",
            "Mathematical Foundations"
        )
    ]
)
def test_page_navigation(page, title):
    app = open_page(page)

    titles = [
        element.value
        for element in app.title
    ]

    assert title in titles


def test_overview_metrics():
    app = open_page()

    assert metric_value(
        app, "Mathematical models"
    ) == "7"

    assert metric_value(
        app, "CLI visualizations"
    ) == "8"

    assert metric_value(
        app, "Recorded core tests"
    ) == "191"

    assert metric_value(
        app, "Export formats"
    ) == "CSV / PNG"


# Growth laboratory


def test_growth_zero_rates():
    app = open_page("Growth Laboratory")

    app.number_input(
        key="growth_principal"
    ).set_value(1000.0)

    app.number_input(
        key="growth_monthly"
    ).set_value(100.0)

    app.number_input(
        key="growth_rate"
    ).set_value(0.0)

    app.number_input(
        key="growth_inflation"
    ).set_value(0.0)

    app.slider(
        key="growth_years"
    ).set_value(10)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Nominal balance"
    ) == "$13,000.00"

    assert metric_value(
        app, "Purchasing power"
    ) == "$13,000.00"

    assert metric_value(
        app, "Total principal"
    ) == "$13,000.00"

    assert metric_value(
        app, "Nominal growth or loss"
    ) == "$0.00"


def test_growth_without_contributions():
    app = open_page("Growth Laboratory")

    app.number_input(
        key="growth_principal"
    ).set_value(1000.0)

    app.number_input(
        key="growth_monthly"
    ).set_value(0.0)

    app.number_input(
        key="growth_rate"
    ).set_value(10.0)

    app.number_input(
        key="growth_inflation"
    ).set_value(0.0)

    app.slider(
        key="growth_years"
    ).set_value(2)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Nominal balance"
    ) == "$1,210.00"

    assert metric_value(
        app, "Nominal growth or loss"
    ) == "$210.00"


def test_growth_negative_returns():
    app = open_page("Growth Laboratory")

    app.number_input(
        key="growth_principal"
    ).set_value(1000.0)

    app.number_input(
        key="growth_monthly"
    ).set_value(0.0)

    app.number_input(
        key="growth_rate"
    ).set_value(-10.0)

    app.number_input(
        key="growth_inflation"
    ).set_value(0.0)

    app.slider(
        key="growth_years"
    ).set_value(2)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Nominal balance"
    ) == "$810.00"

    assert metric_value(
        app, "Nominal growth or loss"
    ) == "$-190.00"


def test_growth_zero_principal():
    app = open_page("Growth Laboratory")

    app.number_input(
        key="growth_principal"
    ).set_value(0.0)

    app.number_input(
        key="growth_monthly"
    ).set_value(0.0)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Nominal balance"
    ) == "$0.00"

    assert metric_value(
        app, "Purchasing power"
    ) == "$0.00"


def test_growth_duration_update():
    app = open_page("Growth Laboratory")

    app.number_input(
        key="growth_principal"
    ).set_value(1000.0)

    app.number_input(
        key="growth_monthly"
    ).set_value(100.0)

    app.number_input(
        key="growth_rate"
    ).set_value(0.0)

    app.number_input(
        key="growth_inflation"
    ).set_value(0.0)

    app.slider(
        key="growth_years"
    ).set_value(5)

    app.run()

    assert metric_value(
        app, "Nominal balance"
    ) == "$7,000.00"

    app.slider(
        key="growth_years"
    ).set_value(10).run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Nominal balance"
    ) == "$13,000.00"


def test_growth_projection_table():
    app = open_page("Growth Laboratory")

    app.slider(
        key="growth_years"
    ).set_value(5).run()

    assert_app_healthy(app)

    assert len(app.dataframe) == 1

    frame = app.dataframe[0].value

    assert len(frame) == 6
    assert list(frame["years"]) == list(range(6))

    assert "nominal_future_value" in frame.columns
    assert "inflation_adjusted_value" in frame.columns


# Financial mathematics


@pytest.mark.parametrize(
    "operation,metric",
    [
        (
            "Compound future value",
            "Calculated future value"
        ),
        (
            "Monthly contribution accumulation",
            "Accumulated value"
        ),
        (
            "Hypothetical goal calculation",
            "Calculated periodic contribution"
        ),
        (
            "Present value",
            "Calculated present value"
        ),
        (
            "Inflation adjustment",
            "Inflation-adjusted value"
        ),
        (
            "Interest-rate conversion",
            "Equivalent monthly rate"
        )
    ]
)
def test_mathematical_operations(operation, metric):
    app = open_page("Financial Mathematics")

    app.selectbox[0].set_value(operation).run()

    assert_app_healthy(app)

    assert metric_value(app, metric)


def test_future_value_accuracy():
    app = open_page("Financial Mathematics")

    app.number_input(
        key="fv_amount"
    ).set_value(1000.0)

    app.number_input(
        key="fv_rate"
    ).set_value(7.0)

    app.slider(
        key="fv_years"
    ).set_value(10)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Calculated future value"
    ) == "$1,967.15"


def test_monthly_contribution_accuracy():
    app = open_page("Financial Mathematics")

    app.selectbox[0].set_value(
        "Monthly contribution accumulation"
    ).run()

    app.number_input(
        key="monthly_amount"
    ).set_value(100.0)

    app.number_input(
        key="monthly_rate"
    ).set_value(7.0)

    app.slider(
        key="monthly_years"
    ).set_value(10)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Accumulated value"
    ) == "$17,308.48"


def test_goal_calculation_accuracy():
    app = open_page("Financial Mathematics")

    app.selectbox[0].set_value(
        "Hypothetical goal calculation"
    ).run()

    app.number_input(
        key="goal_amount"
    ).set_value(50000.0)

    app.number_input(
        key="goal_rate"
    ).set_value(7.0)

    app.slider(
        key="goal_years"
    ).set_value(10)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Calculated periodic contribution"
    ) == "$288.88"


def test_present_value_accuracy():
    app = open_page("Financial Mathematics")

    app.selectbox[0].set_value(
        "Present value"
    ).run()

    app.number_input(
        key="pv_amount"
    ).set_value(1210.0)

    app.number_input(
        key="pv_rate"
    ).set_value(10.0)

    app.slider(
        key="pv_years"
    ).set_value(2)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Calculated present value"
    ) == "$1,000.00"


def test_inflation_adjustment_accuracy():
    app = open_page("Financial Mathematics")

    app.selectbox[0].set_value(
        "Inflation adjustment"
    ).run()

    app.number_input(
        key="inflation_amount"
    ).set_value(1210.0)

    app.number_input(
        key="inflation_rate"
    ).set_value(10.0)

    app.slider(
        key="inflation_years"
    ).set_value(2)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Inflation-adjusted value"
    ) == "$1,000.00"


def test_interest_rate_conversion():
    app = open_page("Financial Mathematics")

    app.selectbox[0].set_value(
        "Interest-rate conversion"
    ).run()

    app.number_input(
        key="conversion_rate"
    ).set_value(12.0).run()

    assert_app_healthy(app)

    expected = (
        (1.12 ** (1 / 12) - 1) * 100
    )

    assert metric_value(
        app, "Equivalent monthly rate"
    ) == f"{expected:.6f}%"


def test_zero_interest_rate_conversion():
    app = open_page("Financial Mathematics")

    app.selectbox[0].set_value(
        "Interest-rate conversion"
    ).run()

    app.number_input(
        key="conversion_rate"
    ).set_value(0.0).run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Equivalent monthly rate"
    ) == "0.000000%"

    assert metric_value(
        app, "Equivalent nominal annual rate"
    ) == "0.000000%"


# Scenario analytics


def test_default_scenario_count():
    app = open_page("Scenario Analytics")

    assert metric_value(
        app, "Scenarios"
    ) == "12"


def test_custom_scenario_count():
    app = open_page("Scenario Analytics")

    app.multiselect[0].set_value(
        [0, 5, 10]
    )

    app.multiselect[1].set_value(
        [0, 2]
    )

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Scenarios"
    ) == "6"


def test_single_zero_rate_scenario():
    app = open_page("Scenario Analytics")

    app.multiselect[0].set_value([0])
    app.multiselect[1].set_value([0])

    app.number_input(
        key="scenario_principal"
    ).set_value(1000.0)

    app.number_input(
        key="scenario_monthly"
    ).set_value(100.0)

    app.slider(
        key="scenario_years"
    ).set_value(10)

    app.run()

    assert_app_healthy(app)

    assert metric_value(
        app, "Scenarios"
    ) == "1"

    assert metric_value(
        app, "Minimum modeled value"
    ) == "$13,000.00"

    assert metric_value(
        app, "Maximum modeled value"
    ) == "$13,000.00"

    assert metric_value(
        app, "Modeled value range"
    ) == "$0.00"


@pytest.mark.parametrize(
    "selection_index",
    [0, 1]
)
def test_empty_scenario_selection(selection_index):
    app = open_page("Scenario Analytics")

    app.multiselect[
        selection_index
    ].set_value([]).run()

    assert_app_healthy(app)

    assert len(app.warning) == 1

    assert "Select at least one" in (
        app.warning[0].value
    )


def test_scenario_selection_recovery():
    app = open_page("Scenario Analytics")

    app.multiselect[0].set_value([]).run()

    assert len(app.warning) == 1

    app.multiselect[0].set_value(
        [0, 5]
    ).run()

    assert_app_healthy(app)

    assert len(app.warning) == 0

    assert metric_value(
        app, "Scenarios"
    ) == "6"


def test_scenario_data_table():
    app = open_page("Scenario Analytics")

    assert len(app.dataframe) == 1

    frame = app.dataframe[0].value

    assert len(frame) == 12

    assert "annual_rate" in frame.columns
    assert "inflation_rate" in frame.columns

    assert (
        "real_value_change_from_baseline"
        in frame.columns
    )

    baseline = frame[
        (frame["annual_rate"] == 5)
        & (frame["inflation_rate"] == 2)
    ]

    assert len(baseline) == 1

    assert baseline[
        "real_value_change_from_baseline"
    ].iloc[0] == pytest.approx(0)


# Methodology


def test_methodology_sections():
    app = open_page("Methodology")

    sections = [
        element.value
        for element in app.subheader
    ]

    assert "1. Compound accumulation" in sections
    assert "2. Ordinary annuity" in sections
    assert "3. Rate conventions" in sections
    assert "6. Numerical stability" in sections
    assert "8. Model limitations" in sections
    assert "9. Software validation" in sections


# Navigation stability


def test_complete_navigation_cycle():
    app = open_page()

    pages = [
        "Growth Laboratory",
        "Financial Mathematics",
        "Scenario Analytics",
        "Methodology",
        "Overview"
    ]

    for page in pages:
        app.sidebar.radio[0].set_value(page).run()

        assert_app_healthy(app)
        assert app.sidebar.radio[0].value == page