import plotly.graph_objects as go
import networkx as nx
import numpy as np

class GraphBasedVisualiser:
    def __init__(self):
        self.G = nx.Graph()
        self.minWeight = float("inf")
        self.maxWeight = 0

    def add_vertex(self, node, color):
        self.G.add_node(node["AIRPORT_ID"], pos=(node['LONGITUDE'], node['LATITUDE']), name=node["AIRPORT"])

    def add_edge(self, node1, node2, weight):
        self.G.add_edge(node1["AIRPORT_ID"], node2["AIRPORT_ID"], weight=weight)
        if weight < self.minWeight:
            self.minWeight = weight
        if weight > self.maxWeight:
            self.maxWeight = weight

    def open_display(self):
        pos = nx.spring_layout(self.G, iterations=50, weight='weight')
        for keys, values in pos.items():
            self.G.nodes[keys]['pos'] = (values[0], values[1])

        node_x = []
        node_y = []
        for node in self.G.nodes():
            x, y = self.G.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)

        edge_trace = []
        edge_x = []
        edge_y = []

        for edge in self.G.edges(data=True):
            x0, y0 = self.G.nodes[edge[0]]['pos']
            x1, y1 = self.G.nodes[edge[1]]['pos']
            weight = self.G.get_edge_data(edge[0], edge[1])['weight']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
            color = -1 * ((((weight - self.minWeight) * 255) / (self.maxWeight-self.minWeight)) - 255)
            width = 1 + (((weight - self.minWeight) * 5) / (self.maxWeight - self.minWeight))
            edge_trace.append(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=dict(
                    width=width,
                    color='rgb(255,'+str(int(color))+',0)',
                ),
                hoverinfo='none',
                mode='lines'
            ))

        node_x = []
        node_y = []
        for node in self.G.nodes():
            x, y = self.G.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='Reds',
                reversescale=False,
                color=[],
                size=10,
                # colorbar=dict(
                #     thickness=15,
                #     title='Node Connections',
                #     xanchor='left',
                #     titleside='right'
                # ),
                line_width=2))

        node_adjacencies = []
        node_text = []

        for node in self.G.nodes():
            node_text.append(self.G.nodes[node]['name'])

        for node, adjacencies in enumerate(self.G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text[node] = (node_text[node] + ' [ # of connections: ' + str(len(adjacencies[1])) + ' ]')

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        dataToShow = edge_trace
        dataToShow.append(node_trace)

        fig = go.Figure(data=dataToShow,
                        layout=go.Layout(
                            title='Network graph',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.show()