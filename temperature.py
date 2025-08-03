import pandas as pd


def get_max_temperatures(data: pd.DataFrame, periods: dict, days_per_period: int):
    """Extract the data from the X days from each period, fill missing days between the date period."""
    season_data = {}
    for label, (start_str, end_str) in periods.items():
        start = pd.to_datetime(start_str).date()
        end = pd.to_datetime(end_str).date()

        # Create full date range (as datetime.date)
        full_dates = pd.date_range(start, end, freq='D').date

        # Filter existing data from that period
        mask = (data['date'] >= start) & (data['date'] <= end)
        temp_df = data.loc[mask, ['date', 'temperature_max']].copy()

        # Create DataFrame with full dates and join with the data
        full_df = pd.DataFrame({'date': full_dates})
        merged = pd.merge(full_df, temp_df, on='date', how='left')

        # Save only the aligned temperature column
        season_data[label] = merged['temperature_max'].reset_index(drop=True)

        if len(merged) != days_per_period:
            print(f"⚠️  {label} has {len(merged)} days (expected: {days_per_period})")

    return pd.DataFrame(season_data)