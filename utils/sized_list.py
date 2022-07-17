class SizedList:
    def __init__(self, size):
        self.list = []
        self.size = size
    
    def __repr__(self):
        return str(self.list)

    def append(self, element):
        self.list.insert(0, element)
        return self.list.pop(-1) if len(self.list) > self.size else None
    
    def index(self, element):
        return self.list.index(element)
            
class PastBuffer(SizedList):
    def __init__(self, size):
        super().__init__(size)

    def find_timestamps(self, current_timestamp):
        timestamp_list = [i['timestamp'] for i in self.list]

        for timestamp in timestamp_list:
            if current_timestamp > timestamp:
                timestamps = timestamp
                break

        snapshots = []
        for past_snapshot in self.list:
            snapshots.append(past_snapshot)
            if past_snapshot['timestamp'] == timestamps:
                break

        snapshots.reverse()
            
        return snapshots