import argparse
import csv
import io
from pathlib import Path

from calculator import (
    projection_breakdown,
    validate_number
)


SCENARIO_COLUMNS = (
    "starting_amount",
    "monthly_contribution",
    "years",
    "annual_rate",
    "inflation_rate",
    "total_principal",
    "nominal_growth",
    "nominal_future_value",
    "inflation_adjusted_value",
    "baseline_annual_rate",
    "baseline_inflation_rate",
    "real_value_change_from_baseline"
)


def normalize_rates(rates):
    values = [
        validate_number(rate, "Scenario rate")
        for rate in rates
    ]

    if not values:
        raise ValueError(
            "At least one scenario rate is required."
        )

    return sorted(set(values))


def compare_scenarios(
    starting_amount,
    monthly_amount,
    years,
    annual_rates,
    inflation_rates,
    baseline_annual_rate=5,
    baseline_inflation_rate=2
):
    annual_rates = normalize_rates(annual_rates)
    inflation_rates = normalize_rates(inflation_rates)

    baseline_annual_rate = validate_number(
        baseline_annual_rate,
        "Baseline annual rate"
    )

    baseline_inflation_rate = validate_number(
        baseline_inflation_rate,
        "Baseline inflation rate"
    )

    baseline = projection_breakdown(
        starting_amount,
        monthly_amount,
        baseline_annual_rate,
        years,
        baseline_inflation_rate
    )

    baseline_real_value = baseline[
        "inflation_adjusted_value"
    ]

    results = []

    for annual_rate in annual_rates:
        for inflation_rate in inflation_rates:
            projection = projection_breakdown(
                starting_amount,
                monthly_amount,
                annual_rate,
                years,
                inflation_rate
            )

            real_value = projection[
                "inflation_adjusted_value"
            ]

            results.append({
                "starting_amount": projection[
                    "starting_amount"
                ],
                "monthly_contribution": float(
                    monthly_amount
                ),
                "years": projection["years"],
                "annual_rate": annual_rate,
                "inflation_rate": inflation_rate,
                "total_principal": projection[
                    "total_principal"
                ],
                "nominal_growth": projection[
                    "nominal_growth"
                ],
                "nominal_future_value": projection[
                    "nominal_future_value"
                ],
                "inflation_adjusted_value": real_value,
                "baseline_annual_rate": baseline_annual_rate,
                "baseline_inflation_rate": baseline_inflation_rate,
                "real_value_change_from_baseline": (
                    real_value - baseline_real_value
                )
            })

    return results


def summarize_scenarios(records):
    if not records:
        raise ValueError(
            "Scenario records cannot be empty."
        )

    ordered = sorted(
        records,
        key=lambda record: record[
            "inflation_adjusted_value"
        ]
    )

    minimum = ordered[0]
    maximum = ordered[-1]

    return {
        "scenario_count": len(records),
        "minimum_real_value": minimum[
            "inflation_adjusted_value"
        ],
        "maximum_real_value": maximum[
            "inflation_adjusted_value"
        ],
        "real_value_range": (
            maximum["inflation_adjusted_value"]
            - minimum["inflation_adjusted_value"]
        ),
        "minimum_scenario": minimum.copy(),
        "maximum_scenario": maximum.copy()
    }


def scenarios_to_csv(records):
    if not records:
        raise ValueError(
            "No scenario records to export."
        )

    buffer = io.StringIO(newline="")

    writer = csv.DictWriter(
        buffer,
        fieldnames=SCENARIO_COLUMNS
    )

    writer.writeheader()
    writer.writerows(records)

    return buffer.getvalue()


def export_scenarios(records, destination):
    destination = Path(destination)

    content = scenarios_to_csv(records)

    with destination.open(
        "x",
        encoding="utf-8",
        newline=""
    ) as file:
        file.write(content)

    return destination


def demonstration():
    return compare_scenarios(
        starting_amount=1000,
        monthly_amount=100,
        years=10,
        annual_rates=(-5, 0, 5, 10),
        inflation_rates=(0, 2, 4),
        baseline_annual_rate=5,
        baseline_inflation_rate=2
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Compare synthetic growth and inflation scenarios."
        )
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Export scenarios to a new CSV file."
    )

    arguments = parser.parse_args(argv)

    records = demonstration()
    summary = summarize_scenarios(records)

    print("Financial Scenario Analysis")
    print("-" * 40)

    print(
        f"Scenarios evaluated: "
        f"{summary['scenario_count']}"
    )

    print(
        f"Minimum calculated real value: "
        f"${summary['minimum_real_value']:,.2f}"
    )

    print(
        f"Maximum calculated real value: "
        f"${summary['maximum_real_value']:,.2f}"
    )

    print(
        f"Calculated value range: "
        f"${summary['real_value_range']:,.2f}"
    )

    print(
        "\nAll scenarios use hypothetical assumptions."
    )

    if arguments.output is not None:
        try:
            destination = export_scenarios(
                records,
                arguments.output
            )
        except OSError as error:
            parser.error(str(error))

        print(f"Exported results to: {destination}")


if __name__ == "__main__":
    main()