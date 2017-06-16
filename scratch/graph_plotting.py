import networkx as nx
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.offline as po


DATA = {
    "foo": {"links": ["bar", "bar", "woo"]},
    "bar": {"links": ["woo"]},
    "woo": {"links": ["zoo", "NA"]},
    "zoo": {"links": []}
}


def main():

    G = nx.MultiDiGraph()

    for node, details in DATA.items():
        G.add_node(node)
        for link in details["links"]:
            G.add_edge(node, link)

    print("Nodes: {}".format(G.number_of_nodes()))
    print("Edges: {}".format(G.number_of_edges()))
    pos = nx.fruchterman_reingold_layout(G)

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
        line=Line(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines+markers')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

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
            colorscale='YIGnBu',
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

    for node, adjacencies in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        node_info = '# of connections: ' + str(len(adjacencies))
        node_trace['text'].append(node_info)

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

    po.plot(fig, filename='networkx.html')

if __name__ == "__main__":
    main()