import pytest
from growth_api import projection
import calculator


def query(**changes):
    values = {"principal": "1000", "monthly": "100", "rate": "5", "years": "20", "inflation": "2"}
    values.update(changes)
    return {k: [v] for k, v in values.items()}


def test_matches_engine():
    rows = projection(query())["rows"]
    assert len(rows) == 21
    for year, row in enumerate(rows):
        assert row == calculator.projection_breakdown(1000, 100, 5, year, 2)


def test_zero_rate():
    row = projection(query(rate="0", inflation="0"))["rows"][-1]
    assert row["nominal_future_value"] == pytest.approx(25000)
    assert row["inflation_adjusted_value"] == pytest.approx(25000)


@pytest.mark.parametrize("changes", [{"years":"51"},{"years":"1.5"},{"rate":"nan"},{"rate":"-100"},{"principal":"-1"},{"monthly":"inf"},{"inflation":"-100"}])
def test_invalid_assumptions(changes):
    with pytest.raises(ValueError):
        projection(query(**changes))


def test_invalid_query_shape():
    with pytest.raises(ValueError):
        projection({})
    with pytest.raises(ValueError):
        projection({**query(), "rate": ["5", "7"]})
