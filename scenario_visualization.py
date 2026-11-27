import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

from scenario_analysis import demonstration
from visualization import COLORS


def build_sensitivity_matrix(records):
    if not records:
        raise ValueError("Scenario records cannot be empty.")

    annual_rates = sorted({
        row["annual_rate"]
        for row in records
    })

    inflation_rates = sorted({
        row["inflation_rate"]
        for row in records
    })

    lookup = {}

    for row in records:
        key = (
            row["annual_rate"],
            row["inflation_rate"]
        )

        if key in lookup:
            raise ValueError(
                "Duplicate scenario combination."
            )

        value = row["inflation_adjusted_value"]

        if not math.isfinite(value):
            raise ValueError(
                "Scenario values must be finite."
            )

        lookup[key] = value

    matrix = []

    for annual_rate in annual_rates:
        values = []

        for inflation_rate in inflation_rates:
            key = (
                annual_rate,
                inflation_rate
            )

            if key not in lookup:
                raise ValueError(
                    "Scenario matrix is incomplete."
                )

            values.append(lookup[key])

        matrix.append(values)

    return annual_rates, inflation_rates, matrix


def create_sensitivity_heatmap(records):
    annual_rates, inflation_rates, matrix = (
        build_sensitivity_matrix(records)
    )

    figure, axis = plt.subplots(
        figsize=(11, 7),
        facecolor=COLORS["background"]
    )

    axis.set_facecolor(COLORS["surface"])

    image = axis.imshow(
        matrix,
        cmap="viridis",
        aspect="auto",
        origin="lower"
    )

    axis.set_title(
        "Growth and Inflation Sensitivity",
        color=COLORS["text"],
        fontsize=17,
        fontweight="bold",
        pad=22
    )

    axis.set_xlabel(
        "Annual inflation assumption",
        color=COLORS["muted"],
        labelpad=12
    )

    axis.set_ylabel(
        "Effective annual growth assumption",
        color=COLORS["muted"],
        labelpad=12
    )

    axis.set_xticks(
        range(len(inflation_rates)),
        labels=[
            f"{rate:g}%"
            for rate in inflation_rates
        ]
    )

    axis.set_yticks(
        range(len(annual_rates)),
        labels=[
            f"{rate:g}%"
            for rate in annual_rates
        ]
    )

    axis.tick_params(
        colors=COLORS["muted"]
    )

    for spine in axis.spines.values():
        spine.set_color(COLORS["grid"])

    if len(annual_rates) * len(inflation_rates) <= 100:
        for row_index, row in enumerate(matrix):
            for column_index, value in enumerate(row):
                normalized = image.norm(value)

                red, green, blue, _ = image.cmap(
                    normalized
                )

                brightness = (
                    0.299 * red
                    + 0.587 * green
                    + 0.114 * blue
                )

                text_color = (
                    "#101820"
                    if brightness > 0.55
                    else "#FFFFFF"
                )

                axis.text(
                    column_index,
                    row_index,
                    f"${value:,.0f}",
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=10,
                    fontweight="medium"
                )

    colorbar = figure.colorbar(
        image,
        ax=axis,
        pad=0.03
    )

    colorbar.set_label(
        "Inflation-adjusted value",
        color=COLORS["muted"]
    )

    colorbar.ax.tick_params(
        colors=COLORS["muted"]
    )

    colorbar.ax.yaxis.set_major_formatter(
        StrMethodFormatter("${x:,.0f}")
    )

    colorbar.outline.set_edgecolor(
        COLORS["grid"]
    )

    figure.text(
        0.5,
        0.025,
        "Deterministic scenarios using hypothetical assumptions.",
        color=COLORS["muted"],
        fontsize=10,
        ha="center"
    )

    figure.tight_layout(
        rect=(0, 0.06, 1, 1)
    )

    return figure, axis


def create_baseline_comparison_chart(records):
    if not records:
        raise ValueError("Scenario records cannot be empty.")

    baseline_pairs = {
        (
            row["baseline_annual_rate"],
            row["baseline_inflation_rate"]
        )
        for row in records
    }

    if len(baseline_pairs) != 1:
        raise ValueError(
            "All scenarios must share the same baseline."
        )

    ordered = sorted(
        records,
        key=lambda row: row[
            "real_value_change_from_baseline"
        ]
    )

    baseline_rate, baseline_inflation = (
        next(iter(baseline_pairs))
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

    if not all(math.isfinite(value) for value in values):
        raise ValueError(
            "Scenario differences must be finite."
        )

    colors = [
        COLORS["primary"]
        if value >= 0
        else COLORS["accent"]
        for value in values
    ]

    figure, axis = plt.subplots(
        figsize=(12, max(6, len(records) * 0.4)),
        facecolor=COLORS["background"]
    )

    axis.set_facecolor(COLORS["surface"])

    axis.barh(
        labels,
        values,
        color=colors,
        alpha=0.9
    )

    axis.axvline(
        0,
        color=COLORS["muted"],
        linewidth=1.2
    )

    axis.set_title(
        "Scenario Differences from Baseline",
        fontsize=17,
        fontweight="bold",
        color=COLORS["text"],
        pad=20
    )

    axis.set_xlabel(
        "Change in inflation-adjusted value",
        color=COLORS["muted"]
    )

    axis.tick_params(
        colors=COLORS["muted"]
    )

    axis.xaxis.set_major_formatter(
        StrMethodFormatter("${x:,.0f}")
    )

    axis.grid(
        axis="x",
        color=COLORS["grid"],
        alpha=0.6
    )

    axis.set_axisbelow(True)

    for spine in axis.spines.values():
        spine.set_color(COLORS["grid"])

    figure.text(
        0.5,
        0.025,
        (
            f"Baseline: {baseline_rate:g}% growth, "
            f"{baseline_inflation:g}% inflation. "
            "Hypothetical assumptions."
        ),
        color=COLORS["muted"],
        fontsize=10,
        ha="center"
    )

    figure.tight_layout(
        rect=(0, 0.06, 1, 1)
    )

    return figure, axis


def save_chart(figure, destination):
    destination = Path(destination)

    if destination.suffix.lower() != ".png":
        raise ValueError(
            "Chart destination must use the .png extension."
        )

    with destination.open("xb") as file:
        figure.savefig(
            file,
            format="png",
            dpi=200,
            bbox_inches="tight",
            facecolor=figure.get_facecolor()
        )

    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Visualize hypothetical financial scenarios."
        )
    )

    parser.add_argument(
        "--chart",
        choices=("heatmap", "baseline"),
        default="heatmap"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Save the chart to a new PNG file."
    )

    arguments = parser.parse_args(argv)

    records = demonstration()

    if arguments.chart == "heatmap":
        figure, _ = create_sensitivity_heatmap(
            records
        )
    else:
        figure, _ = create_baseline_comparison_chart(
            records
        )

    try:
        if arguments.output is not None:
            destination = save_chart(
                figure,
                arguments.output
            )

            print(f"Chart saved to: {destination}")

        else:
            plt.show()

    except (ValueError, OSError) as error:
        parser.error(str(error))

    finally:
        plt.close(figure)


if __name__ == "__main__":
    main()