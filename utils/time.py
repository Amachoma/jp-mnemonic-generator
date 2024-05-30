class AvgRemainingTime:
    def __init__(self, total):
        self.total_count = total
        self.time_elapsed = 0
        self.processed_count = 0
        self.approx_remaining_sec = None
        self.percent = 0

    def add_item(self, time_elapsed):
        self.processed_count += 1
        self.time_elapsed += time_elapsed

        avg_processing_time = self.time_elapsed / self.processed_count
        self.approx_remaining_sec = int((self.total_count - self.processed_count) * avg_processing_time)
        self.percent = self.processed_count / self.total_count

    def __str__(self):
        seconds = self.approx_remaining_sec
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return f"Approximately remains {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"
