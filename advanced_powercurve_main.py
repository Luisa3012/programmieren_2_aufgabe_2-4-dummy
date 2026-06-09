import pandas as pd
from advanced_power_curve import make_power_curve


def main():
    df = pd.read_csv("data/activities/activity.csv")
    power = df["PowerOriginal"]

    df_curve, fig = make_power_curve(power, time_step_seconds=1)
    print(df_curve.head())
    fig.show()

    try:
        fig.write_image("screenshot.png")
    except ValueError as exc:
        if "Kaleido" in str(exc):
            print("Kaleido ist nicht installiert. Screenshot wird nicht gespeichert.")
            print("Installiere Kaleido mit: pip install kaleido")
        else:
            raise


if __name__ == "__main__":
    main()