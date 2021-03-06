from scotland_deaths.covid_deaths import CovidDeaths

cd = CovidDeaths(week_no=37)


class TestMethods:
    def test_excess_deaths_df(self):
        excess_deaths_df = cd.deaths_by_cause_and_location()
        assert excess_deaths_df["2021"]["Cancer"]["Care Homes"]["2021-01-04"] == 68
        assert (
            excess_deaths_df["(2015-2019)"]["Other"]["Other Institution"]["2021-09-13"]
            == 1
        )

    def test_get_covid_non_covid_excess_deaths(self):
        df = cd.covid_non_covid_excess_deaths()
        total = df["Covid"] + df["non-Covid"]
        assert df["Covid"]["2021-01-04"] == 332
        assert df["non-Covid"]["2021-09-13"] == 126  # Note: some minor rounding errors
        assert (
            total["2021-01-04"] == 446
        )  # Note: some minor rounding errors, actual = 444


class TestHelpers:
    def test_get_row_list(self):
        skiprows = cd.get_row_list(start_row=6)
        assert skiprows[:6] == [0, 1, 2, 3, 5, 12]

        skiprows = cd.get_row_list(start_row=14)

        print()
        for row in skiprows:
            print(row + 1)
