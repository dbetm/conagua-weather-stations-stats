import pandas as pd


from contants import MONTH_TO_MONTH_NAME



def get_accumulated_precipitation(df: pd.DataFrame, years: list, months: list):
    data = df.copy()

    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month

    data_filtered = data[data['month'].isin(months)]
    data_filtered = data[data['year'].isin(years)]

    monthly_sum = data_filtered.groupby(['year', 'month'])['precipitation'].sum().reset_index()

    pivot = monthly_sum.pivot(index='month', columns='year', values='precipitation')

    # reorder months
    pivot = pivot.reindex(months)
    pivot.index = pivot.index.map(MONTH_TO_MONTH_NAME)

    return pivot


def get_data_coverage(df: pd.DataFrame, years: list, months: list) -> list:
    """Get data coverage for accumulated precipitation"""
    data = df.copy()

    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month

    df_precip = data[['date', 'precipitation']]
    df_precip = df_precip.dropna(subset=['precipitation'])

    def get_full_date_range(year: int, month_start: int, month_end: int):
        last_day_start = pd.Period(f'{year}-{month_start:02d}').days_in_month
        last_day_end = pd.Period(f'{year}-{month_end:02d}').days_in_month

        return pd.date_range(
            start=f"{year}-{month_start}-{last_day_start}",
            end=f"{year}-{month_end}-{last_day_end}",
            freq='D',
        )

    completeness = {}
    for year in years:
        expected_dates = get_full_date_range(year, months[0], months[-1])
        actual_dates = df_precip[df_precip['date'].dt.year == year]['date'].dt.floor('D')
        present_dates = actual_dates[actual_dates.between(expected_dates.min(), expected_dates.max())]
        percent = present_dates.nunique() / len(expected_dates) * 100
        completeness[year] = percent


    data_filtered = data[data['month'].isin(months)]
    data_filtered = data[data['year'].isin(years)]
    totals = data_filtered.groupby('year')['precipitation'].sum()

    # Create text for year and completeness
    completeness_py_year = []
    for year in sorted(totals.index):
        total_mm = totals[year]
        percent = completeness.get(year, 0)
        line = f"{year}: {total_mm:.1f} mm, datos: {percent:.1f}%"
        completeness_py_year.append(line)

    return completeness_py_year