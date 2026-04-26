import pandas as pd
import matplotlib.pyplot as plt

def convert_time(t):
    h, m = map(int, t[:-2].split(":"))
    if "PM" in t and h != 12:
        h += 12
    if "AM" in t and h == 12:
        h = 0
    return h * 60 + m


def show_all_charts(bookings, complaints, assets):
    df_b = pd.DataFrame(bookings)
    df_c = pd.DataFrame(complaints)
    df_a = pd.DataFrame(assets)

    # ---------- 1. BOOKINGS: Most Used Facilities ----------
    if not df_b.empty:
        df_b["facility_id"].value_counts().plot(kind="bar")
        plt.title("Most Used Facilities")
        plt.xlabel("Facility")
        plt.ylabel("Bookings Count")
        plt.show()

    # ---------- LINE CHART: Bookings per Hour ----------
    if not df_b.empty:
        df_b["hour"] = df_b["start"].apply(lambda x: convert_time(x) // 60)

        hourly_counts = df_b["hour"].value_counts().sort_index()

        plt.plot(hourly_counts.index, hourly_counts.values, marker='o')
        plt.title("Bookings per Hour Trend")
        plt.xlabel("Hour of Day")
        plt.ylabel("Number of Bookings")
        plt.grid()
        plt.show()

    # ---------- 3. ASSETS: Health Status ----------
    if not df_a.empty:
        df_a["health"].value_counts().plot(kind="pie", autopct="%1.1f%%")
        plt.title("Asset Health Status")
        plt.ylabel("")
        plt.show()

    # ---------- 4. COMPLAINTS: Problematic Facilities ----------
    if not df_c.empty:
        df_c["facility_id"].value_counts().plot(kind="bar")
        plt.title("Most Problematic Facilities")
        plt.xlabel("Facility")
        plt.ylabel("Complaints Count")
        plt.show()