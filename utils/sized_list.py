class SizedList:
    def __init__(self, size):
        self.list = []
        self.size = size
    
    def __repr__(self):
        return str(self.list)

    def append(self, element):
        self.list.insert(0, element)
        return self.list.pop(-1) if len(self.list) > self.size else None
            
class PastBuffer(SizedList):
    def __init__(self, size):
        super().__init__(size)

    def find_closest_timestamp(self, timestamp):
        def get_closest_value(arr, target):
            abs_arr = [abs(i - target) for i in arr]
            return arr[abs_arr.index(min(abs_arr))]
        
        timestamp_list = [i['timestamp'] for i in self.list]

        closest_timestamp = get_closest_value(timestamp_list, timestamp)

        for past_snapshot in self.list:
            if past_snapshot['timestamp'] == closest_timestamp:
                return past_snapshot