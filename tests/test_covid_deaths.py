from scotland_deaths.covid_deaths import CovidDeaths

cd = CovidDeaths(week_no=37)


class TestMethods:
    def test_get_all_deaths(self):
        all_deaths_df = cd.get_all_deaths()
        assert all_deaths_df["Total deaths (2021)"].iloc[0] == 1720
        assert all_deaths_df["Average total deaths (2015-2019)"].iloc[0] == 1276

    def test_excess_deaths_df(self):
        excess_deaths_df = cd.get_excess_deaths()
        assert excess_deaths_df["2021"]["Cancer"]["Care Homes"]["2021-01-04"] == 68
        assert (
            excess_deaths_df["(2015-2019)"]["Other"]["Other Institution"]["2021-09-13"]
            == 1
        )

    def test_get_covid_non_covid_excess_deaths(self):
        pass


class TestHelpers:
    def test_get_row_list(self):
        skiprows = cd.get_row_list(start_row=6)
        assert skiprows[:6] == [0, 1, 2, 3, 5, 12]

        skiprows = cd.get_row_list(start_row=14)

        print()
        for row in skiprows:
            print(row + 1)
