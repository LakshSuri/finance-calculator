import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

from calculator import (
    future_value,
    projection_breakdown,
    validate_amount,
    validate_rate,
    validate_years
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


def create_figure(title, xlabel, ylabel):
    figure, axis = plt.subplots(
        figsize=(11, 6),
        facecolor=COLORS["background"]
    )

    axis.set_facecolor(COLORS["surface"])

    axis.set_title(
        title,
        color=COLORS["text"],
        fontsize=17,
        fontweight="bold",
        pad=20
    )

    axis.set_xlabel(xlabel, color=COLORS["muted"])
    axis.set_ylabel(ylabel, color=COLORS["muted"])

    axis.tick_params(colors=COLORS["muted"])

    axis.grid(
        True,
        color=COLORS["grid"],
        alpha=0.6,
        linewidth=0.7
    )

    axis.set_axisbelow(True)

    for spine in axis.spines.values():
        spine.set_color(COLORS["grid"])

    axis.yaxis.set_major_formatter(
        StrMethodFormatter("${x:,.0f}")
    )

    return figure, axis


def finish_figure(figure, axis, legend=False):
    if legend:
        axis.legend(
            facecolor=COLORS["surface"],
            edgecolor=COLORS["grid"],
            labelcolor=COLORS["text"]
        )

    figure.tight_layout()

    plt.show()
    plt.close(figure)


def calculate_yearly_growth(
    starting_amount,
    return_rate,
    years
):
    starting_amount = validate_amount(
        starting_amount,
        "Starting amount"
    )

    validate_rate(return_rate)

    years = validate_years(years)

    yearly_values = list(range(years + 1))

    values = [
        future_value(
            starting_amount,
            return_rate,
            year
        )
        for year in yearly_values
    ]

    return yearly_values, values


def calculate_projection_data(
    starting_amount,
    monthly_amount,
    annual_rate,
    years,
    inflation_rate=0
):
    years = validate_years(years)

    return [
        projection_breakdown(
            starting_amount,
            monthly_amount,
            annual_rate,
            year,
            inflation_rate
        )
        for year in range(years + 1)
    ]


def create_growth_chart(
    starting_amount,
    return_rate,
    years
):
    yearly_values, values = calculate_yearly_growth(
        starting_amount,
        return_rate,
        years
    )

    figure, axis = create_figure(
        "Compound Growth Projection",
        "Years",
        "Calculated balance"
    )

    axis.plot(
        yearly_values,
        values,
        color=COLORS["primary"],
        linewidth=2.5,
        marker="o",
        markersize=4
    )

    axis.fill_between(
        yearly_values,
        values,
        alpha=0.12,
        color=COLORS["primary"]
    )

    axis.axhline(
        starting_amount,
        color=COLORS["muted"],
        linestyle="--",
        label="Initial principal"
    )

    finish_figure(figure, axis, legend=True)


def create_bar_chart(
    starting_amount,
    return_rate,
    years
):
    yearly_values, values = calculate_yearly_growth(
        starting_amount,
        return_rate,
        years
    )

    figure, axis = create_figure(
        "Annual Balance Analysis",
        "Years",
        "Calculated balance"
    )

    axis.bar(
        yearly_values,
        values,
        color=COLORS["secondary"],
        alpha=0.85,
        edgecolor=COLORS["background"]
    )

    finish_figure(figure, axis)


def create_return_comparison_chart(
    starting_amount,
    years,
    rates=(-5, 0, 5, 10)
):
    figure, axis = create_figure(
        "Hypothetical Growth Rate Comparison",
        "Years",
        "Calculated balance"
    )

    palette = [
        COLORS["accent"],
        COLORS["muted"],
        COLORS["secondary"],
        COLORS["primary"]
    ]

    for index, rate in enumerate(rates):
        yearly_values, values = calculate_yearly_growth(
            starting_amount,
            rate,
            years
        )

        axis.plot(
            yearly_values,
            values,
            linewidth=2.2,
            color=palette[index % len(palette)],
            label=f"{rate:g}% annual rate"
        )

    finish_figure(figure, axis, legend=True)


def create_combined_projection_chart(
    starting_amount,
    monthly_amount,
    annual_rate,
    years,
    inflation_rate=0
):
    records = calculate_projection_data(
        starting_amount,
        monthly_amount,
        annual_rate,
        years,
        inflation_rate
    )

    timeline = [row["years"] for row in records]

    principal = [
        row["total_principal"]
        for row in records
    ]

    nominal = [
        row["nominal_future_value"]
        for row in records
    ]

    real = [
        row["inflation_adjusted_value"]
        for row in records
    ]

    figure, axis = create_figure(
        "Principal, Growth and Purchasing Power",
        "Years",
        "Calculated value"
    )

    axis.plot(
        timeline,
        principal,
        color=COLORS["muted"],
        linestyle="--",
        linewidth=2,
        label="Total principal"
    )

    axis.plot(
        timeline,
        nominal,
        color=COLORS["primary"],
        linewidth=2.5,
        label="Nominal balance"
    )

    axis.plot(
        timeline,
        real,
        color=COLORS["secondary"],
        linewidth=2.5,
        label="Inflation-adjusted balance"
    )

    axis.fill_between(
        timeline,
        principal,
        nominal,
        alpha=0.12,
        color=COLORS["primary"]
    )

    finish_figure(figure, axis, legend=True)


def create_contribution_breakdown_chart(
    starting_amount,
    monthly_amount,
    annual_rate,
    years
):
    records = calculate_projection_data(
        starting_amount,
        monthly_amount,
        annual_rate,
        years
    )

    timeline = [row["years"] for row in records]

    initial = [
        row["starting_amount"]
        for row in records
    ]

    contributions = [
        row["total_contributions"]
        for row in records
    ]

    principal = [
        row["total_principal"]
        for row in records
    ]

    growth = [
        row["nominal_growth"]
        for row in records
    ]

    figure, axis = create_figure(
        "Contribution and Growth Decomposition",
        "Years",
        "Calculated value"
    )

    axis.bar(
        timeline,
        initial,
        color=COLORS["secondary"],
        label="Initial principal"
    )

    axis.bar(
        timeline,
        contributions,
        bottom=initial,
        color=COLORS["muted"],
        label="Monthly contributions"
    )

    axis.bar(
        timeline,
        growth,
        bottom=principal,
        color=COLORS["primary"],
        label="Growth or loss",
        alpha=0.85
    )

    finish_figure(figure, axis, legend=True)


def create_inflation_comparison_chart(
    starting_amount,
    monthly_amount,
    annual_rate,
    years,
    inflation_rates=(0, 2, 4, 6)
):
    figure, axis = create_figure(
        "Purchasing Power Sensitivity",
        "Years",
        "Inflation-adjusted value"
    )

    palette = [
        COLORS["primary"],
        COLORS["secondary"],
        COLORS["accent"],
        COLORS["muted"]
    ]

    for index, inflation_rate in enumerate(
        inflation_rates
    ):
        records = calculate_projection_data(
            starting_amount,
            monthly_amount,
            annual_rate,
            years,
            inflation_rate
        )

        axis.plot(
            [row["years"] for row in records],
            [
                row["inflation_adjusted_value"]
                for row in records
            ],
            color=palette[index % len(palette)],
            linewidth=2.2,
            label=f"{inflation_rate:g}% inflation"
        )

    finish_figure(figure, axis, legend=True)