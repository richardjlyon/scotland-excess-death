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

        self.all_death_df = self.get_all_deaths()
        self.excess_death_df = self.get_excess_deaths()

    def get_file(self):
        filename = f"covid-deaths-21-data-week-{self.week_no}.xlsx"
        if not Path(self.datafile_path).is_file():
            url = f"https://www.nrscotland.gov.uk/files//statistics/covid19/{filename}"
            r = requests.get(url, allow_redirects=True)
            open(self.datafile_path, "wb").write(r.content)

    def get_all_deaths(self) -> pd.DataFrame:
        """Retrieve total deaths, 2021 and average (2015-2019)."""
        df = pd.read_excel(
            self.datafile_path,
            sheet_name="Table 2 (2021)",
            usecols=[0] + list(range(2, 2 + self.week_no)),
            index_col=0,
            skiprows=[0, 1, 2, 4, 5, 7, 8],
            skipfooter=103,
        ).T
        return df

    def get_row_list(self, start_row):
        """Get a list of rows suitable for passing to skiprows."""
        rows_to_keep = [4] + list(range(start_row, start_row + 6))
        all_rows = list(range(150))
        skiprows = [row for row in all_rows if row not in rows_to_keep]
        return skiprows

    def get_excess_deaths(self) -> pd.DataFrame:
        """
        Retrieve excess deaths, 2021 and average (2015-2019) organised by location.

        example
        -------
        deaths = df["Care Homes"]["Cancer"]["(2015-2019)"]

        :return: Dataframe with multiindex [location, cause, period] of deaths by week date
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

        return df_data

    @property
    def datafile_name(self):
        return f"covid-deaths-21-data-week-{self.week_no}.xlsx"

    @property
    def datafile_path(self):
        return DATA_DIR / self.datafile_name
