import geopandas as gpd
import matplotlib.pyplot as plt
from src.Visualizer import Visualizer
from shapely.geometry import Point, LineString


class MapVisualizer(Visualizer):
    def __init__(self):
        plt.rcParams['figure.dpi'] = 900
        self.points = {'geometry': [], 'color': []}
        self.edges = {'geometry': [], 'color': []}

    def add_vertex(self, airport, color):
        self.points['geometry'].append(Point(airport['LONGITUDE'], airport['LATITUDE']))
        self.points['color'].append(color)

    def clear_vertices(self):
        self.points = {'geometry': [], 'color': []}

    def add_edge(self, source, target, color):
        self.edges['geometry'].append(LineString([Point(source['LONGITUDE'], source['LATITUDE']), Point(target['LONGITUDE'], target['LATITUDE'])]))
        self.edges['color'].append(color)

    def clear_edges(self):
        self.edges = {'geometry': [], 'color': []}

    def open_display(self):
        self.update_display()

    def update_display(self):
        plt.clf()
        world_df = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        point_df = gpd.GeoDataFrame(self.points['color'], geometry=self.points['geometry'])
        edge_df = gpd.GeoDataFrame(self.edges['color'], geometry=self.edges['geometry'])
        ax = world_df.boundary.plot(linewidth=0.2, color='gray')
        ax = world_df.plot(ax=ax, color='teal')
        ax = point_df.plot(ax=ax, marker='o', column=0, markersize=0.05, cmap='brg')
        edge_df.plot(ax=ax, column=0, linewidth=0.1, cmap='viridis')
        plt.axis('off')
        plt.show()

    def close_display(self):
        plt.close()
