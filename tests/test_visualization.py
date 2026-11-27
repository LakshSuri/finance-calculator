import matplotlib.pyplot as plt
import pytest

import calculator
import visualization


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


@pytest.mark.parametrize(
    "rate,expected",
    [
        (10, [1000, 1100, 1210, 1331]),
        (0, [1000, 1000, 1000, 1000]),
        (-10, [1000, 900, 810, 729])
    ]
)
def test_yearly_growth(rate, expected):
    years, values = visualization.calculate_yearly_growth(
        1000, rate, 3
    )

    assert years == [0, 1, 2, 3]
    assert values == pytest.approx(expected)


def test_yearly_growth_zero_duration():
    years, values = visualization.calculate_yearly_growth(
        1000, 7, 0
    )

    assert years == [0]
    assert values == [1000]


@pytest.mark.parametrize(
    "rate",
    [-10, 0, 5, 10, 20]
)
def test_yearly_growth_matches_calculator(rate):
    years, values = visualization.calculate_yearly_growth(
        1000, rate, 10
    )

    for year, value in zip(years, values):
        assert value == pytest.approx(
            calculator.future_value(
                1000, rate, year
            )
        )


def test_projection_timeline():
    records = visualization.calculate_projection_data(
        1000, 100, 7, 10, 2
    )

    assert len(records) == 11

    assert [
        row["years"] for row in records
    ] == list(range(11))


def test_projection_initial_balance():
    records = visualization.calculate_projection_data(
        1000, 100, 7, 10, 2
    )

    initial = records[0]

    assert initial["nominal_future_value"] == 1000
    assert initial["total_contributions"] == 0
    assert initial["nominal_growth"] == 0


def test_projection_final_balance():
    records = visualization.calculate_projection_data(
        1000, 100, 7, 10, 2
    )

    expected = calculator.projection_breakdown(
        1000, 100, 7, 10, 2
    )

    assert records[-1] == expected


def test_projection_accounting():
    records = visualization.calculate_projection_data(
        1000, 100, 7, 10
    )

    for row in records:
        assert (
            row["starting_amount"]
            + row["total_contributions"]
            + row["nominal_growth"]
        ) == pytest.approx(
            row["nominal_future_value"]
        )


def test_projection_zero_rate():
    records = visualization.calculate_projection_data(
        1000, 100, 0, 10
    )

    for row in records:
        expected = 1000 + 1200 * row["years"]

        assert row["nominal_future_value"] == pytest.approx(
            expected
        )


def test_projection_zero_inflation():
    records = visualization.calculate_projection_data(
        1000, 100, 7, 10, 0
    )

    for row in records:
        assert row[
            "inflation_adjusted_value"
        ] == pytest.approx(
            row["nominal_future_value"]
        )


def test_projection_positive_inflation():
    records = visualization.calculate_projection_data(
        1000, 100, 7, 10, 2
    )

    for row in records[1:]:
        assert (
            row["inflation_adjusted_value"]
            < row["nominal_future_value"]
        )


@pytest.mark.parametrize(
    "function,args",
    [
        (
            visualization.create_growth_chart,
            (1000, 7, 10)
        ),
        (
            visualization.create_bar_chart,
            (1000, 7, 10)
        ),
        (
            visualization.create_return_comparison_chart,
            (1000, 10)
        ),
        (
            visualization.create_combined_projection_chart,
            (1000, 100, 7, 10, 2)
        ),
        (
            visualization.create_contribution_breakdown_chart,
            (1000, 100, 7, 10)
        ),
        (
            visualization.create_inflation_comparison_chart,
            (1000, 100, 7, 10)
        )
    ]
)
def test_chart_generation(monkeypatch, function, args):
    rendered = []

    def capture_figure():
        figure = plt.gcf()
        figure.canvas.draw()

        rendered.append({
            "title": figure.axes[0].get_title(),
            "xlabel": figure.axes[0].get_xlabel(),
            "ylabel": figure.axes[0].get_ylabel()
        })

    monkeypatch.setattr(
        plt,
        "show",
        capture_figure
    )

    existing_figures = set(plt.get_fignums())

    function(*args)

    assert len(rendered) == 1
    assert rendered[0]["title"]
    assert rendered[0]["xlabel"]
    assert rendered[0]["ylabel"]

    assert set(plt.get_fignums()) == existing_figures


@pytest.mark.parametrize(
    "rate",
    [-10, 0, 10]
)
def test_combined_chart_scenarios(monkeypatch, rate):
    monkeypatch.setattr(
        plt,
        "show",
        lambda: plt.gcf().canvas.draw()
    )

    visualization.create_combined_projection_chart(
        1000, 100, rate, 10, 2
    )


@pytest.mark.parametrize(
    "amount,rate,years",
    [
        (-100, 7, 10),
        (1000, -100, 10),
        (1000, 7, -1),
        (1000, 7, 1.5)
    ]
)
def test_invalid_growth_inputs(amount, rate, years):
    with pytest.raises(ValueError):
        visualization.calculate_yearly_growth(
            amount, rate, years
        )