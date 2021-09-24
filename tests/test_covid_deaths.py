from scotland_deaths.covid_deaths import CovidDeaths


def test_covid_deaths():
    cd = CovidDeaths(week_no=37)
    assert cd.all_death_df["Total deaths from all causes"].iloc[0] == 1720


def test_get_row_list():
    cd = CovidDeaths(week_no=37)

    skiprows = cd.get_row_list(start_row=6)
    assert skiprows[:6] == [0, 1, 2, 3, 5, 12]

    skiprows = cd.get_row_list(start_row=14)

    print()
    for row in skiprows:
        print(row + 1)


def test_get_excess_deaths():
    cd = CovidDeaths(week_no=37)
    df = cd.get_excess_deaths()

    assert cd.excess_death_df["Care Homes"]["Cancer"]["2021"]["2021-01-04"] == 68
    assert (
        cd.excess_death_df["Other Institution"]["Other"]["(2015-2019)"]["2021-09-13"]
        == 1
    )
