from models.facility import Facility
from models.booking import Booking
from models.complaint import Complaint
from models.asset import SmartAsset

from utils.navigation import bfs_path
from analysis.analytics import facility_usage_analysis
from visual.charts import show_all_charts

import pandas as pd

# ----------- CSV STORAGE -----------
def load_csv(filename):
    try:
        df = pd.read_csv(filename)
        return df.to_dict(orient="records")
    except:
        return []

def save_csv(filename, data):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# ----------- DATA -----------

facilities = [
    Facility("F101", "Classroom A", 60),
    Facility("F102", "Lab B", 30),
    Facility("F103", "Seminar Hall", 100),
    Facility("F104", "Auditorium", 200),
    Facility("F105", "Conference Room", 40),
    Facility("F106", "Computer Lab", 35),
    Facility("F107", "Library Hall", 120)
]
bookings = load_csv("bookings.csv")
complaints = load_csv("complaints.csv")
assets = load_csv("assets.csv")

# ----------- CAMPUS MAP -----------

campus_map = {
    "MainGate": [("Security", "Enter gate", 20)],

    "Security": [
        ("MainGate", "Exit", 20),
        ("AcademicBlock", "Go straight", 50),
        ("Parking", "Turn right", 30)
    ],

    "Parking": [("Security", "Go back", 30)],

    "AcademicBlock": [
        ("Security", "Go back", 50),
        ("Library", "Go straight", 30),
        ("Canteen", "Turn left", 25),
        ("AdminBlock", "Turn right", 20),
        ("Floor1", "Go upstairs", 10),
        ("Floor2", "Go upstairs", 15)
    ],

    "AdminBlock": [
        ("AcademicBlock", "Go back", 20),
        ("Office", "Enter office", 10)
    ],

    "Office": [("AdminBlock", "Exit", 10)],

    "Library": [("AcademicBlock", "Go back", 30)],
    "Canteen": [("AcademicBlock", "Go back", 25)],

    "Floor1": [
        ("AcademicBlock", "Go downstairs", 10),
        ("F101", "Left", 5),
        ("F102", "Right", 5),
        ("F106", "Computer Lab", 6),
        ("Lab1", "Straight", 8)
    ],

    "Floor2": [
        ("AcademicBlock", "Go downstairs", 15),
        ("F103", "Seminar Hall", 5),
        ("F104", "Auditorium", 6),
        ("F105", "Conference Room", 5)
    ],

    "F101": [("Floor1", "Exit", 5)],
    "F102": [("Floor1", "Exit", 5)],
    "F106": [("Floor1", "Exit", 6)],
    "Lab1": [("Floor1", "Exit", 8)],

    "F103": [("Floor2", "Exit", 5)],
    "F104": [("Floor2", "Exit", 6)],
    "F105": [("Floor2", "Exit", 5)]
}

# ----------- UTIL -----------

def convert_time(t):
    time_part = t[:-2]
    period = t[-2:]

    hours, minutes = map(int, time_part.split(":"))

    if period == "PM" and hours != 12:
        hours += 12
    if period == "AM" and hours == 12:
        hours = 0

    return hours * 60 + minutes

# ----------- FUNCTIONS -----------

def show_facilities():
    print("\n--- Facilities ---")
    for f in facilities:
        print(f.display())

def add_booking():
    try:
        bid = input("Booking ID: ")
        fid = input("Facility ID: ")
        purpose = input("Purpose: ")
        start = input("Start Time (7:10AM): ")
        end = input("End Time (8:50AM): ")

        start_time = convert_time(start)
        end_time = convert_time(end)

        if start_time >= end_time:
            print("Invalid time range")
            return

        # TIME CLASH CHECK
        for b in bookings:
            if b["facility_id"] == fid:
                existing_start = convert_time(b["start"])
                existing_end = convert_time(b["end"])

                if not (end_time <= existing_start or start_time >= existing_end):
                    print("Time clash! Already booked.")
                    return

        b = Booking(bid, fid, purpose, start, end)
        bookings.append(vars(b))
        save_csv("bookings.csv", bookings)
        print("Booking Saved to CSV")

    except Exception as e:
        print("Error:", e)

def add_complaint():
    cid = input("Complaint ID: ")
    fid = input("Facility ID: ")
    issue = input("Issue: ")

    c = Complaint(cid, fid, issue)
    complaints.append(vars(c))

    save_csv("complaints.csv", complaints)

    print("Complaint Saved to CSV")


def add_asset():
    aid = input("Asset ID: ")
    category = input("Category: ")
    location = input("Location: ")
    health = input("Health Status: ")

    a = SmartAsset(aid, category, location, health)
    assets.append(vars(a))

    save_csv("assets.csv", assets)

    print("Asset Saved to CSV")


def analytics():
    facility_usage_analysis(bookings)

def charts():
    show_all_charts(bookings, complaints, assets)

def navigate():
    print("\n====== CAMPUS NAVIGATION SYSTEM ======")

    # Show available locations clearly
    print("\nAvailable Locations:")
    for loc in campus_map.keys():
        print("•", loc)

    start = input("\nEnter Start Location: ").strip()
    end = input("Enter Destination: ").strip()

    # ✅ Validation
    if start not in campus_map or end not in campus_map:
        print("\n❌ Invalid location entered. Please try again.")
        return

    if start == end:
        print("\n⚠️ You are already at the destination.")
        return

    # ✅ Find path
    path, total_dist = bfs_path(campus_map, start, end)

    if path:
        print("\n📍 Navigation Path:\n")

        step_no = 1
        for src, dest, direction, dist in path:
            print(f"Step {step_no}: {src} → {dest}")
            print(f"   Direction : {direction}")
            print(f"   Distance  : {dist} meters\n")
            step_no += 1

        print("✅ Destination Reached!")
        print(f"📏 Total Distance: {total_dist} meters")

    else:
        print("\n❌ No path found between locations.")


import networkx as nx
import matplotlib.pyplot as plt

def show_visual_map():
    G = nx.Graph()

    # Add edges
    for node in campus_map:
        for neighbor, direction, dist in campus_map[node]:
            G.add_edge(node, neighbor, weight=dist)

    # ✅ MANUAL POSITIONS (REAL MAP STRUCTURE)
    pos = {
        "MainGate": (0, 0),
        "Security": (0, 1),
        "Parking": (2, 1),

        "AcademicBlock": (0, 3),
        "AdminBlock": (2, 3),
        "Office": (3, 3),

        "Library": (-2, 4),
        "Canteen": (-2, 2),

        "Floor1": (-1, 5),
        "Floor2": (1, 5),

        "F101": (-2, 6),
        "F102": (-1, 6),
        "F106": (0, 6),
        "Lab1": (-1, 7),

        "F103": (1, 6),
        "F104": (2, 6),
        "F105": (3, 6)
    }

    plt.figure(figsize=(14, 10))

    # 🎨 Node coloring (meaningful)
    node_colors = []
    for node in G.nodes():
        if node.startswith("F"):
            node_colors.append("lightgreen")   # rooms
        elif "Floor" in node:
            node_colors.append("pink")         # floors
        elif node in ["Library", "Canteen"]:
            node_colors.append("orange")       # facilities
        elif node in ["AdminBlock", "Office"]:
            node_colors.append("violet")       # admin
        else:
            node_colors.append("skyblue")      # general

    # Draw graph
    nx.draw_networkx_nodes(G, pos, node_size=2200, node_color=node_colors)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Distance labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("SMART CAMPUS MAP (REALISTIC VIEW)", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# ----------- MENU -----------

def main():
    while True:
        print("\n====== SMART CAMPUS SYSTEM ======")
        print("1. Show Facilities")
        print("2. Add Booking")
        print("3. Add Complaint")
        print("4. Add Asset")
        print("5. Analytics")
        print("6. Charts")
        print("7. Navigation")
        print("8. Visual Campus Map")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            show_facilities()
        elif choice == "2":
            add_booking()

        elif choice == "3":
            add_complaint()
        elif choice == "4":
            add_asset()
        elif choice == "5":
            analytics()
        elif choice == "6":
            charts()
        elif choice == "7":
            navigate()
        elif choice == "8":
            show_visual_map()
        elif choice == "9":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()