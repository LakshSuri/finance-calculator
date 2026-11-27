import math

import matplotlib.pyplot as plt
import pytest

from scenario_analysis import (
    demonstration,
    compare_scenarios
)

from scenario_visualization import (
    build_sensitivity_matrix,
    create_sensitivity_heatmap,
    create_baseline_comparison_chart,
    save_chart,
    main
)


@pytest.fixture
def scenarios():
    return demonstration()


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


# Sensitivity matrix


def test_matrix_dimensions(scenarios):
    annual_rates, inflation_rates, matrix = (
        build_sensitivity_matrix(scenarios)
    )

    assert len(annual_rates) == 4
    assert len(inflation_rates) == 3
    assert len(matrix) == 4

    assert all(
        len(row) == 3
        for row in matrix
    )


def test_matrix_rate_order(scenarios):
    annual_rates, inflation_rates, _ = (
        build_sensitivity_matrix(scenarios)
    )

    assert annual_rates == [-5, 0, 5, 10]
    assert inflation_rates == [0, 2, 4]


def test_matrix_values(scenarios):
    annual_rates, inflation_rates, matrix = (
        build_sensitivity_matrix(scenarios)
    )

    for row in scenarios:
        row_index = annual_rates.index(
            row["annual_rate"]
        )

        column_index = inflation_rates.index(
            row["inflation_rate"]
        )

        assert matrix[
            row_index
        ][
            column_index
        ] == pytest.approx(
            row["inflation_adjusted_value"]
        )


def test_matrix_independent_of_input_order(scenarios):
    original = build_sensitivity_matrix(
        scenarios
    )

    reversed_matrix = build_sensitivity_matrix(
        list(reversed(scenarios))
    )

    assert original == reversed_matrix


def test_matrix_single_scenario():
    records = compare_scenarios(
        1000,
        100,
        10,
        annual_rates=(0,),
        inflation_rates=(0,)
    )

    annual_rates, inflation_rates, matrix = (
        build_sensitivity_matrix(records)
    )

    assert annual_rates == [0]
    assert inflation_rates == [0]
    assert matrix == [[13000]]


def test_empty_matrix():
    with pytest.raises(ValueError):
        build_sensitivity_matrix([])


def test_duplicate_scenarios(scenarios):
    records = scenarios + [
        scenarios[0].copy()
    ]

    with pytest.raises(ValueError):
        build_sensitivity_matrix(records)


def test_incomplete_matrix(scenarios):
    with pytest.raises(ValueError):
        build_sensitivity_matrix(
            scenarios[:-1]
        )


@pytest.mark.parametrize(
    "value",
    [math.nan, math.inf, -math.inf]
)
def test_nonfinite_matrix_value(
    scenarios,
    value
):
    scenarios[0][
        "inflation_adjusted_value"
    ] = value

    with pytest.raises(ValueError):
        build_sensitivity_matrix(
            scenarios
        )


# Heatmap generation


def test_heatmap_generation(scenarios):
    figure, axis = (
        create_sensitivity_heatmap(scenarios)
    )

    figure.canvas.draw()

    assert axis.get_title() == (
        "Growth and Inflation Sensitivity"
    )

    assert len(axis.images) == 1
    assert len(axis.texts) == 12


def test_heatmap_axis_labels(scenarios):
    _, axis = create_sensitivity_heatmap(
        scenarios
    )

    xlabels = [
        label.get_text()
        for label in axis.get_xticklabels()
    ]

    ylabels = [
        label.get_text()
        for label in axis.get_yticklabels()
    ]

    assert xlabels == ["0%", "2%", "4%"]

    assert ylabels == [
        "-5%",
        "0%",
        "5%",
        "10%"
    ]


def test_heatmap_data_accuracy(scenarios):
    _, _, matrix = build_sensitivity_matrix(
        scenarios
    )

    _, axis = create_sensitivity_heatmap(
        scenarios
    )

    plotted = axis.images[0].get_array()

    assert plotted.tolist() == matrix


def test_single_scenario_heatmap():
    records = compare_scenarios(
        1000,
        100,
        10,
        annual_rates=(0,),
        inflation_rates=(0,)
    )

    figure, axis = (
        create_sensitivity_heatmap(records)
    )

    figure.canvas.draw()

    assert len(axis.texts) == 1


# Baseline comparison


def test_baseline_chart_generation(scenarios):
    figure, axis = (
        create_baseline_comparison_chart(
            scenarios
        )
    )

    figure.canvas.draw()

    assert len(axis.patches) == 12

    assert axis.get_title() == (
        "Scenario Differences from Baseline"
    )


def test_baseline_chart_values(scenarios):
    _, axis = create_baseline_comparison_chart(
        scenarios
    )

    expected = sorted([
        row["real_value_change_from_baseline"]
        for row in scenarios
    ])

    actual = [
        bar.get_width()
        for bar in axis.patches
    ]

    assert actual == pytest.approx(expected)


def test_baseline_chart_empty_records():
    with pytest.raises(ValueError):
        create_baseline_comparison_chart([])


def test_inconsistent_baseline(scenarios):
    scenarios[0]["baseline_annual_rate"] = 3

    with pytest.raises(ValueError):
        create_baseline_comparison_chart(
            scenarios
        )


# PNG export


def test_save_heatmap(scenarios, tmp_path):
    figure, _ = create_sensitivity_heatmap(
        scenarios
    )

    destination = tmp_path / "heatmap.png"

    result = save_chart(
        figure,
        destination
    )

    assert result == destination
    assert destination.exists()

    assert destination.read_bytes().startswith(
        b"\x89PNG\r\n\x1a\n"
    )


def test_save_baseline_chart(
    scenarios,
    tmp_path
):
    figure, _ = create_baseline_comparison_chart(
        scenarios
    )

    destination = tmp_path / "baseline.png"

    save_chart(
        figure,
        destination
    )

    assert destination.stat().st_size > 0


def test_prevent_chart_overwrite(
    scenarios,
    tmp_path
):
    figure, _ = create_sensitivity_heatmap(
        scenarios
    )

    destination = tmp_path / "heatmap.png"

    destination.write_bytes(
        b"Existing file"
    )

    with pytest.raises(FileExistsError):
        save_chart(
            figure,
            destination
        )

    assert destination.read_bytes() == (
        b"Existing file"
    )


def test_invalid_chart_extension(
    scenarios,
    tmp_path
):
    figure, _ = create_sensitivity_heatmap(
        scenarios
    )

    with pytest.raises(ValueError):
        save_chart(
            figure,
            tmp_path / "chart.txt"
        )


# Command-line integration


@pytest.mark.parametrize(
    "chart",
    ["heatmap", "baseline"]
)
def test_command_line_chart_export(
    tmp_path,
    chart
):
    destination = tmp_path / f"{chart}.png"

    existing_figures = set(
        plt.get_fignums()
    )

    main([
        "--chart",
        chart,
        "--output",
        str(destination)
    ])

    assert destination.exists()

    assert set(
        plt.get_fignums()
    ) == existing_figures


def test_command_line_chart_display(monkeypatch):
    calls = []

    monkeypatch.setattr(
        plt,
        "show",
        lambda: calls.append(True)
    )

    main(["--chart", "heatmap"])

    assert calls == [True]