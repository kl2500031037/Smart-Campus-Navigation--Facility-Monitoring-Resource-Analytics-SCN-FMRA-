class Facility:
    def __init__(self, facility_id, name, capacity):
        self.facility_id = facility_id
        self.name = name
        self.capacity = capacity

    def display(self):
        return f"{self.facility_id} - {self.name} (Capacity: {self.capacity})"