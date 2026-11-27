import csv
import io
import math

import pytest

from calculator import projection_breakdown

from scenario_analysis import (
    SCENARIO_COLUMNS,
    normalize_rates,
    compare_scenarios,
    summarize_scenarios,
    scenarios_to_csv,
    export_scenarios,
    demonstration,
    main
)


@pytest.fixture
def scenarios():
    return compare_scenarios(
        starting_amount=1000,
        monthly_amount=100,
        years=10,
        annual_rates=(-5, 0, 5, 10),
        inflation_rates=(0, 2, 4),
        baseline_annual_rate=5,
        baseline_inflation_rate=2
    )


def test_scenario_count(scenarios):
    assert len(scenarios) == 12


def test_unique_scenario_combinations(scenarios):
    combinations = {
        (
            row["annual_rate"],
            row["inflation_rate"]
        )
        for row in scenarios
    }

    assert len(combinations) == 12


def test_rate_normalization():
    assert normalize_rates(
        [10, 5, 0, 5, -5]
    ) == [-5, 0, 5, 10]


@pytest.mark.parametrize(
    "rates",
    [
        [],
        [math.nan],
        [math.inf],
        [-math.inf],
        ["invalid"]
    ]
)
def test_invalid_scenario_rates(rates):
    with pytest.raises(ValueError):
        normalize_rates(rates)


def test_scenario_matches_calculator(scenarios):
    for row in scenarios:
        expected = projection_breakdown(
            row["starting_amount"],
            row["monthly_contribution"],
            row["annual_rate"],
            row["years"],
            row["inflation_rate"]
        )

        assert row[
            "nominal_future_value"
        ] == pytest.approx(
            expected["nominal_future_value"]
        )

        assert row[
            "inflation_adjusted_value"
        ] == pytest.approx(
            expected["inflation_adjusted_value"]
        )


def test_baseline_difference(scenarios):
    baseline = next(
        row for row in scenarios
        if row["annual_rate"] == 5
        and row["inflation_rate"] == 2
    )

    assert baseline[
        "real_value_change_from_baseline"
    ] == pytest.approx(0)


def test_growth_rate_sensitivity(scenarios):
    selected = [
        row for row in scenarios
        if row["inflation_rate"] == 2
    ]

    values = [
        row["inflation_adjusted_value"]
        for row in selected
    ]

    assert values == sorted(values)


def test_inflation_sensitivity(scenarios):
    selected = [
        row for row in scenarios
        if row["annual_rate"] == 5
    ]

    values = [
        row["inflation_adjusted_value"]
        for row in selected
    ]

    assert values == sorted(
        values,
        reverse=True
    )


def test_zero_rate_scenario():
    records = compare_scenarios(
        1000,
        100,
        10,
        annual_rates=(0,),
        inflation_rates=(0,)
    )

    assert records[0][
        "nominal_future_value"
    ] == pytest.approx(13000)

    assert records[0][
        "inflation_adjusted_value"
    ] == pytest.approx(13000)


def test_scenario_summary(scenarios):
    summary = summarize_scenarios(
        scenarios
    )

    values = [
        row["inflation_adjusted_value"]
        for row in scenarios
    ]

    assert summary["scenario_count"] == 12

    assert summary[
        "minimum_real_value"
    ] == min(values)

    assert summary[
        "maximum_real_value"
    ] == max(values)

    assert summary[
        "real_value_range"
    ] == pytest.approx(
        max(values) - min(values)
    )


def test_empty_scenario_summary():
    with pytest.raises(ValueError):
        summarize_scenarios([])


def test_csv_column_order(scenarios):
    content = scenarios_to_csv(scenarios)

    reader = csv.DictReader(
        io.StringIO(content)
    )

    assert tuple(
        reader.fieldnames
    ) == SCENARIO_COLUMNS


def test_csv_record_count(scenarios):
    content = scenarios_to_csv(scenarios)

    records = list(
        csv.DictReader(io.StringIO(content))
    )

    assert len(records) == 12


def test_csv_numerical_accuracy(scenarios):
    content = scenarios_to_csv(scenarios)

    records = list(
        csv.DictReader(io.StringIO(content))
    )

    for actual, expected in zip(
        records,
        scenarios
    ):
        assert float(
            actual["nominal_future_value"]
        ) == pytest.approx(
            expected["nominal_future_value"]
        )

        assert float(
            actual["inflation_adjusted_value"]
        ) == pytest.approx(
            expected["inflation_adjusted_value"]
        )


def test_empty_csv_export():
    with pytest.raises(ValueError):
        scenarios_to_csv([])


def test_export_file(scenarios, tmp_path):
    destination = tmp_path / "scenarios.csv"

    result = export_scenarios(
        scenarios,
        destination
    )

    assert result == destination
    assert destination.exists()

    with destination.open(
        encoding="utf-8",
        newline=""
    ) as file:
        records = list(csv.DictReader(file))

    assert len(records) == 12


def test_export_prevents_overwriting(
    scenarios,
    tmp_path
):
    destination = tmp_path / "scenarios.csv"

    destination.write_text(
        "Existing data",
        encoding="utf-8"
    )

    with pytest.raises(FileExistsError):
        export_scenarios(
            scenarios,
            destination
        )

    assert destination.read_text(
        encoding="utf-8"
    ) == "Existing data"


def test_demonstration():
    records = demonstration()

    assert len(records) == 12


def test_command_line_summary(capsys):
    main([])

    output = capsys.readouterr().out

    assert "Financial Scenario Analysis" in output
    assert "Scenarios evaluated: 12" in output


def test_command_line_export(tmp_path):
    destination = tmp_path / "scenarios.csv"

    main([
        "--output",
        str(destination)
    ])

    assert destination.exists()