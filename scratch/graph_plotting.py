import networkx as nx
from plotly.graph_objs import *
import plotly.figure_factory as ff
import plotly.offline as po
from collections import defaultdict


DATA = {
    "foo": {"level": 1, "links": ["bar", "bar", "woo"]},
    "bar": {"level": 2, "links": ["woo"]},
    "woo": {"level": 2, "links": ["zoo", "NA"]},
    "zoo": {"level": 3, "links": ["foo"]},
    "NA": {"level": 4, "links": []}
}


def main():

    G = nx.MultiDiGraph()
    shells = defaultdict(list)

    for node, details in DATA.items():
        G.add_node(node)
        shells[details["level"]].append(node)

        for link in details["links"]:
            G.add_edge(node, link)

    shell_list = []
    for k in sorted(shells.keys()):
        shell_list.append(shells[k])

    print(shell_list)
    print("Nodes: {}".format(G.number_of_nodes()))
    print("Edges: {}".format(G.number_of_edges()))
    pos = nx.fruchterman_reingold_layout(G)
    pos = nx.shell_layout(G, shell_list)

    print(pos)
    """
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) **2
        if d < dmin:
            ncenter = n
            dmin = d

    p = nx.single_source_shortest_path_length(G, ncenter)
    """

    edge_trace = Scatter(
        x=[],
        y=[],
        text=[],
        line=Line(width=0.5, color='#888'),
        hoverinfo='text',
        mode='lines+markers'
        )

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1]
        edge_trace['y'] += [y0, y1]
        edge_trace["text"].append("TODO")

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='Electric',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace["text"].append(node)

    for node, adjacencies in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = '# of connections: ' + str(len(adjacencies))
        node_trace['text'][node] += "\n{}".format(node_info)

    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                     title='Example Directed Node Graph',
                     titlefont=dict(size=16),
                     showlegend=True,
                     hovermode='closest',
                     margin=dict(b=20, l=5, r=5, t=40),
                     annotations=[],
                     xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                     yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False))
                    )

    data_matrix = [['Country', 'Year', 'Population'],
                   ['United States', 2000, 282200000],
                   ['Canada', 2000, 27790000],
                   ['United States', 2005, 295500000],
                   ['Canada', 2005, 32310000],
                   ['United States', 2010, 309000000],
                   ['Canada', 2010, 34000000]]

    table = ff.create_table(data_matrix)


    po.plot(fig, table, filename='networkx.html')

if __name__ == "__main__":
    main()