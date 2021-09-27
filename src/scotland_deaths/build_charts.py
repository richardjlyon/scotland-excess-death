from scotland_deaths import (
    chart_excess_deaths,
    chart_covid_vs_non_covid_excess_deaths,
    chart_excess_death_by_cause_and_location,
    chart_excess_death_by_cause_and_location_adjusted,
)

if __name__ == "__main__":
    chart_excess_deaths()
    chart_covid_vs_non_covid_excess_deaths()
    chart_excess_death_by_cause_and_location()
    chart_excess_death_by_cause_and_location_adjusted()
