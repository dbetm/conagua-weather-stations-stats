import re
from http import HTTPStatus

import pandas as pd
import requests

from utils import get_date, get_numerical_value



class Station:
    HEADER_DATA = "FECHA		PRECIP	EVAP	TMAX	TMIN"

    def __init__(self, source_url: str):
        self.url = source_url
        lines = self.__download_data()

        cursor = self.__load_metadata(lines)
        print("Done metadata...")
        self.daily_historic: pd.DataFrame = self.__get_historic(lines, cursor)
        print("Done daily historic!")

    def __download_data(self) -> list:
        response = requests.get(url=self.url, stream=True)

        if response.status_code != HTTPStatus.OK:
            raise Exception(
                f"Error trying to download data file from: {self.url}. Status: {HTTPStatus.OK.value}"
            )

        return response.text.splitlines()

    def __load_metadata(self, lines: list) -> int:
        lines_before_data = 0

        for line in lines:
            line = line.strip()
            lines_before_data += 1
            if not line: # skip empty lines
                continue

            numerical_pattern = r"[-+]?\d*\.\d+|\d+"

            if line.startswith("NOMBRE"):
                self.name = line.split(":")[1].strip()
            elif line.startswith("LATITUD"):
                self.latitude = float(re.search(numerical_pattern, line).group())
            elif line.startswith("LONGITUD"):
                self.longitude = float(re.search(numerical_pattern, line).group())
            elif line.startswith("ALTITUD"):
                self.altitude = float(re.search(numerical_pattern, line).group())

            if line == self.HEADER_DATA:
                break

        return lines_before_data

    def __get_historic(self, lines: list, cursor: int) -> pd.DataFrame:
        historic = list()

        for idx, line in enumerate(lines):
            line = line.strip()

            if not line or idx <= cursor:
                continue

            fields = line.split("\t")
            historic.append({
                "date": get_date(fields[0]),
                "precipitation": get_numerical_value(fields[1]),
                "evaporation": get_numerical_value(fields[2]),
                "temperature_max": get_numerical_value(fields[3]),
                "temperature_min": get_numerical_value(fields[4])
            })

        return pd.DataFrame(historic)