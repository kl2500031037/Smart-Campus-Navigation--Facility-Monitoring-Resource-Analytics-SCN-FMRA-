class Asset:
    def __init__(self, asset_id, category, location):
        self.asset_id = asset_id
        self.category = category
        self.location = location


class SmartAsset(Asset):
    def __init__(self, asset_id, category, location, health):
        super().__init__(asset_id, category, location)
        self.health = health