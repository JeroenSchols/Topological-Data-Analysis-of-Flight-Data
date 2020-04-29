import csv


class Visualizer:
    def __init__(self, files):
        self.data = []
        for file in files:
            with open("../Dataset/"+file) as csvfile:
                reader = csv.DictReader(csvfile)
                print(list(reader))

    def select_time(self, start, end):
        pass

    def add_edge(self, source, target):
        pass

    def add_vertex(self, airport, value):
        pass

    def open_display(self):
        pass

    def close_display(self):
        pass

    def update_display(self):
        pass
