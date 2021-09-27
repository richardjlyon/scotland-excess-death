__version__ = "0.1.0"
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.absolute()
DATA_DIR = ROOT_DIR / "data"
OUT_DIR = ROOT_DIR / "output"


from .chart_excess_deaths import chart_excess_deaths
from .chart_covid_vs_non_covid_excess_deaths import (
    chart_covid_vs_non_covid_excess_deaths,
)
from .chart_excess_death_by_cause_and_location import (
    chart_excess_death_by_cause_and_location,
)
from .chart_excess_death_by_cause_and_location_adjusted import (
    chart_excess_death_by_cause_and_location_adjusted,
)
