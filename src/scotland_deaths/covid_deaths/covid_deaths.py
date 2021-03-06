"""
    covid-deaths.py
    Richard Lyon, 24 Sep 2021
"""
from pathlib import Path

import pandas as pd
import requests

from scotland_deaths import DATA_DIR


class CovidDeaths:
    """
    A class for processing the National Records of Scotland covid death data speadsheet
    https://www.nrscotland.gov.uk/covid19stats
    """

    def __init__(self, week_no: int):
        """
        Initialise an instance using the data spread sheet for the specified week.
        :param week_no: Week number to process
        """
        self.week_no = week_no

        self.get_file()

    def get_file(self):
        """Check file exists or download it from NRS."""
        filename = f"covid-deaths-21-data-week-{self.week_no}.xlsx"
        if not Path(self.datafile_path).is_file():
            url = f"https://www.nrscotland.gov.uk/files//statistics/covid19/{filename}"
            r = requests.get(url, allow_redirects=True)
            open(self.datafile_path, "wb").write(r.content)

    def deaths_by_cause_and_location(self, daily: bool = False) -> pd.DataFrame:
        """
        Extract excess deaths, 2021 and average (2015-2019) from spreadsheet 'Table 2 (2021)',
        and organise by period, cause, and location.

        example
        -------
        df = cd.deaths_by_cause_and_location()
        df["(2015-2019)"]["Cancer"]["Care Homes"].plot()

        :param: daily If true, resample as daily
        :return: Dataframe with multi-index [period, cause, and location] of deaths by week date
        """

        # Excel row numbers corresponding to the header of each sub-table
        data_structure = {
            "Care Homes": {"(2015-2019)": 30, "2021": 38},
            "Home/Non-institution": {"(2015-2019)": 54, "2021": 62},
            "Hospital": {"(2015-2019)": 78, "2021": 86},
            "Other Institution": {"(2015-2019)": 102, "2021": 110},
        }

        df_data = pd.DataFrame(
            columns=[
                "Cancer",
                "Dementia / Alzheimers",
                "Circulatory (heart disease and stroke)",
                "Respiratory",
                "COVID-19",
                "Other",
                "Location",
                "Period",
            ]
        )

        for location, data in data_structure.items():
            for period, start_row in data.items():
                skiprows = self.get_row_list(start_row)
                df = pd.read_excel(
                    self.datafile_path,
                    sheet_name="Table 3  (2021)",
                    usecols=list(range(self.week_no + 2)),
                    index_col=1,
                    skiprows=skiprows,
                )
                df = df.drop("Week beginning", axis=1).T
                df["Location"] = location
                df["Period"] = period

                df_data = pd.concat([df_data, df])

        df_data = pd.pivot_table(
            df_data, index=df_data.index, columns=["Period", "Location"]
        )

        # -> period, cause, location
        df_data = df_data.swaplevel(0, 1, axis=1)

        if daily:
            # Spreadsheet gives weekly totals: resample to compute daily
            # Resampling alters the totals, so normalise to preserve

            total_before_2021 = df_data["2021"].sum(axis=1).sum()
            total_before_2015_2019 = df_data["(2015-2019)"].sum(axis=1).sum()

            df_data = df_data / 7.0
            df_data = df_data.resample("D").interpolate(method="quadratic")

            total_after_2021 = df_data["2021"].sum(axis=1).sum()
            total_after_2015_2019 = df_data["(2015-2019)"].sum(axis=1).sum()

            df_data["2021"] = df_data["2021"] * total_before_2021 / total_after_2021
            df_data["(2015-2019)"] = (
                df_data["(2015-2019)"] * total_before_2015_2019 / total_after_2015_2019
            )

        return df_data

    def covid_non_covid_excess_deaths(self, daily: bool = False) -> pd.DataFrame:
        """
        Reprocess the excess deaths dataframe to compute excess deaths grouped into "Covid" and "all other causes".
        :param daily: Resample to daily data if True (useful for area fills)

        Example
        -------
        df_data["Covid"].plot()
        df_data["non Covid"].plot()

        :return: dataframe, columns=["Covid", "non-Covid"]
        """

        # Sum deaths by location i.e. ('(2015-2019)', 'COVID-19', 'Care Homes') ->  ('(2015-2019)', 'COVID-19')
        df = self.deaths_by_cause_and_location()
        df = df.groupby(level=[0, 1], axis=1).sum()

        causes = list(df["2021"].columns)
        non_covid_causes = [c for c in causes if c != "COVID-19"]

        df_data = pd.DataFrame(columns=["Covid", "non-Covid"])

        # Compute excess deaths in each category
        df_data["Covid"] = df["2021"]["COVID-19"] - df["(2015-2019)"]["COVID-19"]
        df_data["non-Covid"] = df["2021"][non_covid_causes].sum(axis=1) - df[
            "(2015-2019)"
        ][non_covid_causes].sum(axis=1)

        if daily:
            # spreadsheet gives weekly totals: compute daily
            df_data = df_data / 7.0
            df_data = df_data.resample("D").interpolate(method="quadratic")

        return df_data

    def get_row_list(self, start_row):
        """Get a list of rows suitable for passing to skiprows."""
        rows_to_keep = [4] + list(range(start_row, start_row + 6))
        all_rows = list(range(150))
        skiprows = [row for row in all_rows if row not in rows_to_keep]
        return skiprows

    @property
    def datafile_name(self):
        return f"covid-deaths-21-data-week-{self.week_no}.xlsx"

    @property
    def datafile_path(self):
        return DATA_DIR / self.datafile_name
