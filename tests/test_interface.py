import pytest

import main
import history
import visualization


def run_session(monkeypatch, capsys, commands):
    responses = iter(commands)

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(responses)
    )

    main.main()

    return capsys.readouterr().out


@pytest.fixture(autouse=True)
def isolated_history(tmp_path, monkeypatch):
    history_file = tmp_path / "calculation_history.txt"

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        history,
        "HISTORY_FILE",
        str(history_file)
    )

    return history_file


# Application operations


@pytest.mark.parametrize(
    "commands,expected",
    [
        (
            ["1", "1000", "7", "10", "", "10"],
            "$1,967.15"
        ),
        (
            ["2", "100", "7", "10", "", "10"],
            "$17,308.48"
        ),
        (
            ["3", "50000", "7", "10", "", "10"],
            "$288.88"
        ),
        (
            ["4", "1000", "100", "0", "0", "10", "", "10"],
            "$13,000.00"
        ),
        (
            ["5", "1210", "10", "2", "", "10"],
            "$1,000.00"
        ),
        (
            ["6", "1210", "10", "2", "", "10"],
            "$1,000.00"
        ),
        (
            ["7", "0", "", "10"],
            "Equivalent monthly rate: 0.000000%"
        ),
        (
            ["8", "", "10"],
            "No calculations found."
        ),
        (
            ["10"],
            "Finance Calculator closed."
        )
    ]
)
def test_application_operations(
    monkeypatch,
    capsys,
    commands,
    expected
):
    output = run_session(
        monkeypatch,
        capsys,
        commands
    )

    assert expected in output


# Input validation


def test_invalid_menu_selection(
    monkeypatch,
    capsys
):
    output = run_session(
        monkeypatch,
        capsys,
        ["invalid", "10"]
    )

    assert "Select a valid operation." in output


@pytest.mark.parametrize(
    "invalid_amount",
    ["invalid", "-100", "nan", "inf", "-inf"]
)
def test_invalid_amount_recovery(
    monkeypatch,
    capsys,
    invalid_amount
):
    output = run_session(
        monkeypatch,
        capsys,
        [
            "1",
            invalid_amount,
            "1000",
            "0",
            "1",
            "",
            "10"
        ]
    )

    assert "Invalid input:" in output
    assert "$1,000.00" in output


@pytest.mark.parametrize(
    "invalid_rate",
    ["-100", "101", "nan", "inf", "invalid"]
)
def test_invalid_rate_recovery(
    monkeypatch,
    capsys,
    invalid_rate
):
    output = run_session(
        monkeypatch,
        capsys,
        [
            "1",
            "1000",
            invalid_rate,
            "0",
            "1",
            "",
            "10"
        ]
    )

    assert "Invalid input:" in output
    assert "$1,000.00" in output


@pytest.mark.parametrize(
    "invalid_years",
    ["0", "-1", "101", "1.5", "invalid"]
)
def test_invalid_duration_recovery(
    monkeypatch,
    capsys,
    invalid_years
):
    output = run_session(
        monkeypatch,
        capsys,
        [
            "1",
            "1000",
            "0",
            invalid_years,
            "1",
            "",
            "10"
        ]
    )

    assert (
        "Enter a whole number between 1 and 100."
        in output
    )

    assert "$1,000.00" in output


# Calculation history


def test_calculation_history(
    monkeypatch,
    capsys,
    isolated_history
):
    output = run_session(
        monkeypatch,
        capsys,
        [
            "1", "1000", "7", "10", "",
            "8", "",
            "10"
        ]
    )

    recorded = isolated_history.read_text()

    assert "Compound Growth Analysis" in recorded
    assert "Future value: $1,967.15" in recorded
    assert recorded.strip() in output


def test_history_multiple_calculations(
    monkeypatch,
    capsys,
    isolated_history
):
    output = run_session(
        monkeypatch,
        capsys,
        [
            "1", "1000", "0", "1", "",
            "5", "2000", "0", "1", "",
            "8", "",
            "10"
        ]
    )

    recorded = isolated_history.read_text()

    assert "Compound Growth Analysis" in recorded
    assert "Present Value Analysis" in recorded

    assert "Future value: $1,000.00" in recorded
    assert "Present value: $2,000.00" in recorded
    assert recorded.strip() in output


# Visualization navigation


@pytest.mark.parametrize(
    "choice,function_name,inputs,expected",
    [
        (
            "1",
            "create_growth_chart",
            ["1000", "7", "10"],
            (1000.0, 7.0, 10)
        ),
        (
            "2",
            "create_bar_chart",
            ["1000", "7", "10"],
            (1000.0, 7.0, 10)
        ),
        (
            "3",
            "create_return_comparison_chart",
            ["1000", "10"],
            (1000.0, 10)
        ),
        (
            "4",
            "create_combined_projection_chart",
            ["1000", "100", "7", "10", "2"],
            (1000.0, 100.0, 7.0, 10, 2.0)
        ),
        (
            "5",
            "create_contribution_breakdown_chart",
            ["1000", "100", "7", "10"],
            (1000.0, 100.0, 7.0, 10)
        ),
        (
            "6",
            "create_inflation_comparison_chart",
            ["1000", "100", "7", "10"],
            (1000.0, 100.0, 7.0, 10)
        )
    ]
)
def test_visualization_navigation(
    monkeypatch,
    capsys,
    choice,
    function_name,
    inputs,
    expected
):
    calls = []

    monkeypatch.setattr(
        visualization,
        function_name,
        lambda *args: calls.append(args)
    )

    run_session(
        monkeypatch,
        capsys,
        ["9", choice, *inputs, "", "10"]
    )

    assert calls == [expected]


def test_invalid_visualization_selection(
    monkeypatch,
    capsys
):
    output = run_session(
        monkeypatch,
        capsys,
        ["9", "invalid", "", "10"]
    )

    assert "Invalid visualization selection." in output


def test_return_from_visualizations(
    monkeypatch,
    capsys
):
    output = run_session(
        monkeypatch,
        capsys,
        ["9", "7", "", "10"]
    )

    assert "Finance Calculator closed." in output


# Application termination


@pytest.mark.parametrize(
    "error_type",
    [KeyboardInterrupt, EOFError]
)
def test_graceful_exit(
    monkeypatch,
    capsys,
    error_type
):
    def interrupt(prompt=""):
        raise error_type

    monkeypatch.setattr(
        "builtins.input",
        interrupt
    )

    main.main()

    assert (
        "Finance Calculator closed."
        in capsys.readouterr().out
    )