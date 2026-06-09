import pandas as pd
import numpy as np
import plotly.express as px


def read_data ():
    df =  pd.read_csv("data\activities\activity.csv")
    df["time_in_seconds"] = np.arange(len(df))
    return df


meanmax_power = []
# windowsize ist Anzahl an rows als sekunde und ich muss sekunde rauskürzen
def find_best_power (df, windowsize_seconds, factor=1):
    windowsize_rows = windowsize_seconds*factor
    df.rolling(windowsize_rows).mean()
    meanmax_power = df.rolling(windowsize_rows).mean().max()
    return meanmax_power, windowsize_rows



def find_all_windows (df, window_list, factor=1):
    for windowsize_seconds in window_list:
        find_best_power(df, windowsize_seconds, factor)
    return df_power

def make_power_curve(df_power, time_step_seconds=None, total_duration_seconds=None):
    if isinstance(df_power, pd.DataFrame):
        if "PowerOriginal" in df_power.columns:
            power = df_power["PowerOriginal"]
        elif "power" in df_power.columns:
            power = df_power["power"]
        else:
            raise ValueError("DataFrame must contain 'PowerOriginal' or 'power'")
    else:
        power = pd.Series(df_power)

    power = power.dropna().astype(float)
    if power.empty:
        raise ValueError("Power data must not be empty")

    if time_step_seconds is not None:
        duration_seconds = np.arange(len(power)) * time_step_seconds
    elif total_duration_seconds is not None:
        duration_seconds = np.linspace(0, total_duration_seconds, len(power), endpoint=False)
    else:
        raise ValueError("Either time_step_seconds or total_duration_seconds must be provided")

    sorted_power = power.sort_values(ascending=False).reset_index(drop=True)
    df_curve = pd.DataFrame({
        "duration_seconds": duration_seconds,
        "power_watt": sorted_power.values,
    })

    fig = px.line(df_curve, x="duration_seconds", y="power_watt", title="Power Curve")
    fig.update_layout(
        xaxis_title="Duration (s)",
        yaxis_title="Power (W)",
    )
    return df_curve, fig


if __name__ ==  "__main__":
    window_list = [10, 20,30, 60, 120, 300, 1200, 1800, 3600, 7200]