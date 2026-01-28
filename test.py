""" This code tests the days dict pickle created in organize_data.py
and it just tests that the data is there, that it's a dict, and that each day's DataFrame has the expected columns and types.
It also checks that the timestamps are in order and belong to the correct day, and prints a quick preveiw.
"""
import pickle
import pandas as pd

def test_loaded_days_dict():
    # Load the saved days object (dict[str, DataFrame])
    with open("days_file.pkl", "rb") as f:
        days = pickle.load(f)

    # 1) Check it's a dict and not empty
    assert isinstance(days, dict), f"Expected dict, got {type(days)}"
    assert len(days) > 0, "Days dict is empty"

    # 2) Check keys are date-like strings and values are DataFrames
    expected_columns = {"open", "low", "close"}

    for day_key, day_df in days.items():
        assert isinstance(day_key, str), f"Day key is not a str: {type(day_key)}"
        # simple sanity: YYYY-MM-DD length
        assert len(day_key) == 10, f"Day key not YYYY-MM-DD-like: {day_key}"

        assert isinstance(day_df, pd.DataFrame), f"Value for {day_key} is not a DataFrame: {type(day_df)}"
        assert not day_df.empty, f"Day DataFrame is empty for {day_key}"
        assert expected_columns.issubset(day_df.columns), (
            f"{day_key} missing expected columns: {expected_columns - set(day_df.columns)}"
        )
        assert isinstance(day_df.index, pd.DatetimeIndex), f"{day_key} index is not a DateTimeIndex"
        assert not day_df.isnull().values.any(), f"{day_key} contains NaN values"

        # 3) Check intra-day ordering (chronological)
        assert day_df.index.is_monotonic_increasing, f"{day_key} is not sorted chronologically"

        # 4) Check all timestamps belong to that day (based on index date)
        unique_dates = set(day_df.index.date)
        assert len(unique_dates) == 1, f"{day_key} contains multiple dates: {unique_dates}"

    return "All tests passed!"

print(test_loaded_days_dict())

# Print a quick preview of the first day
with open("days_file.pkl", "rb") as f:
    days = pickle.load(f)

first_key = sorted(days.keys())[0]
print("First day key:", first_key)
print(days[first_key].head())
