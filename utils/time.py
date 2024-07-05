import datetime


class AvgRemainingTime:
    def __init__(self, total, finished=0):
        self.total_count = total
        self.finished_count = finished

        self.time_elapsed = 0
        self.processed_count = 0

        self.approx_remaining_sec = None
        self.percent = self.finished_count / self.total_count

    def add_item(self, time_elapsed, item_count=1):
        self.processed_count += item_count
        self.time_elapsed += time_elapsed

        avg_processing_time_per_item = self.time_elapsed / self.processed_count
        self.approx_remaining_sec = int(
            (self.total_count - self.finished_count - self.processed_count) * avg_processing_time_per_item)

        self.percent = (self.finished_count + self.processed_count) / self.total_count

    def __str__(self):
        return f"Approximately remains {datetime.timedelta(self.approx_remaining_sec)}"
