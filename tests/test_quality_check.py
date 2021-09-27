import pytest

from scotland_deaths.covid_deaths import CovidDeaths

covid_deaths = CovidDeaths(week_no=37)


class TestChartExcessDeaths:
    def test_weekly_totals_are_correct(self):
        df = covid_deaths.deaths_by_cause_and_location(daily=False)

        # Note: All Locations total (cell AO13) is 41051, and is probably a summing error. \
        # We compute the sum directly from the individual locations, hence the difference
        total_all_locations_all_causes = df["(2015-2019)"].sum(axis=1).sum()
        assert total_all_locations_all_causes == 41043

        total_all_locations_all_causes = df["2021"].sum(axis=1).sum()
        assert total_all_locations_all_causes == 44057

    def test_daily_totals_are_correct(self):
        df = covid_deaths.deaths_by_cause_and_location(daily=True)

        # Note: All Locations total (cell AO13) is 41051, and is probably a summing error. \
        # We compute the sum directly from the individual locations, hence the difference
        total_all_locations_all_causes = df["(2015-2019)"].sum(axis=1).sum()
        assert total_all_locations_all_causes == pytest.approx(41043)

        total = df["2021"].sum(axis=1).sum()
        assert total == pytest.approx(44057)


class TestChartCovidVsNonCovidExcessDeaths:
    def test_weekly_covid_totals_are_correct(self):
        df = covid_deaths.deaths_by_cause_and_location(daily=False)
        covid_deaths_on_1_4_2021 = df["2021"]["COVID-19"].sum(axis=1)["2021-01-04"]
        assert covid_deaths_on_1_4_2021 == 332  # cell C27

    def test_daily_covid_totals_are_correct(self):
        df = covid_deaths.deaths_by_cause_and_location(daily=True)
        covid_deaths_on_1_4_2021 = df["2021"]["COVID-19"].sum(axis=1)["2021-01-04"]

        assert covid_deaths_on_1_4_2021 == pytest.approx(332 / 7, 1)  # cell C27

    def test_weekly_non_covid_totals_are_correct(self):
        df = covid_deaths.deaths_by_cause_and_location(daily=False)
        all_deaths_on_1_4_2021 = df["2021"].sum(axis=1)["2021-01-04"]
        covid_deaths_on_1_4_2021 = df["2021"]["COVID-19"].sum(axis=1)["2021-01-04"]
        non_covid_deaths_on_1_4_2021 = all_deaths_on_1_4_2021 - covid_deaths_on_1_4_2021

        assert non_covid_deaths_on_1_4_2021 == 1720 - 332  # cell C21 - C19


class TestChartExcessDeathByCauseAndLocation:
    @pytest.mark.parametrize(
        "cause, location, expected",
        [
            ("COVID-19", "Care Homes", 623),
            ("Cancer", "Hospital", -751),
        ],
    )
    def test_totals_are_correct(self, cause, location, expected):
        df = covid_deaths.deaths_by_cause_and_location(daily=False)
        df = df["2021"] - df["(2015-2019)"]
        assert df[cause][location].sum() == expected
