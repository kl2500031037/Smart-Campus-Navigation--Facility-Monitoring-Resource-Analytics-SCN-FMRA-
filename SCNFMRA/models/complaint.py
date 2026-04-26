class Complaint:
    def __init__(self, complaint_id, facility_id, issue, status="Open"):
        self.complaint_id = complaint_id
        self.facility_id = facility_id
        self.issue = issue
        self.status = status