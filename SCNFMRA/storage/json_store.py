import json

def save_data(filename, data):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Error saving data:", e)


def load_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return []