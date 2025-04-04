import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import random


def visualize(
        data: pd.DataFrame,
        index: str,
        columns: str,
        values: str = 'level',
        title: str = '',
        show_values: bool = True,
        figsize: tuple = (12, 8)) -> None:

    vertices = []
    for _, row in data.iterrows():
        origin = row[index]
        destination = row[columns]
        if (origin, destination) not in vertices:
            vertices.append((origin, destination))

    origins = sorted(list(set([v[0] for v in vertices])))
    destinations = sorted(list(set([v[1] for v in vertices])))

    G = nx.DiGraph()

    for o in origins:
        G.add_node(o, bipartite=0)

    for d in destinations:
        G.add_node(d, bipartite=1)

    origin_color = '#3498db'
    destination_color = '#e74c3c'

    for _, row in data.iterrows():
        origin = row[index]
        destination = row[columns]
        value = row[values]

        if value <= 0:
            continue

        edge_attrs = {'weight': value}

        if 'marginal' in data.columns:
            edge_attrs['marginal'] = row['marginal']

        G.add_edge(origin, destination, **edge_attrs)

    fig, ax = plt.subplots(figsize=figsize)

    pos = {}

    pos_origins = {node: (0, i) for i, node in enumerate(origins)}
    pos_destinations = {node: (1, i) for i, node in enumerate(destinations)}

    pos.update(pos_origins)
    pos.update(pos_destinations)

    nx.draw_networkx_nodes(G=G, pos=pos, nodelist=origins,
                           node_color=origin_color, node_size=700, alpha=0.8, ax=ax)

    nx.draw_networkx_nodes(G=G, pos=pos, nodelist=destinations,
                           node_color=destination_color, node_size=700, alpha=0.8, ax=ax)

    nx.draw_networkx_labels(G=G, pos=pos, font_size=10,
                            font_weight='bold', ax=ax)

    edge_widths = []
    edge_colors = []

    max_value = data[values].max() if len(data) > 0 else 1

    for (u, _, d) in G.edges(data=True):
        min_width = 1
        max_width = 3

        if max_value > 0:
            width = min_width + (d['weight'] / max_value) * \
                (max_width - min_width)
        else:
            width = min_width

        edge_widths.append(width)

        r, g, b = random.random(), random.random(), random.random()
        edge_colors.append((r, g, b, 0.7))

    nx.draw_networkx_edges(G=G, pos=pos,
                           width=edge_widths,
                           edge_color=edge_colors,
                           arrowsize=15,
                           connectionstyle='arc3,rad=0.1',
                           ax=ax)

    if show_values:
        used_positions = {}
        edge_labels = {}

        for u, v, d in G.edges(data=True):
            label = ""
            if show_values:
                label += f"value: {d['weight']:.1f}"

            x_origin, y_origin = pos[u]
            x_dest, y_dest = pos[v]

            label_pos_x = x_origin + 0.25 * (x_dest - x_origin)
            label_pos_y = y_origin + 0.25 * (y_dest - y_origin)

            offset_y = 0
            key = (u, label_pos_x)
            if key in used_positions:
                offset_y = 0.05 * len(used_positions[key])
                used_positions[key].append((label_pos_x, label_pos_y))
            else:
                used_positions[key] = [(label_pos_x, label_pos_y)]

            label_pos = (label_pos_x, label_pos_y + offset_y)

            edge_labels[(u, v)] = (label, label_pos)

        for (u, v), (label_text, label_pos) in edge_labels.items():
            plt.text(label_pos[0], label_pos[1], label_text,
                     fontsize=8, bbox=dict(facecolor='white', alpha=0.7),
                     horizontalalignment='center', verticalalignment='center')

    plt.title(title, fontsize=15)
    plt.axis('off')
    plt.tight_layout()

    return fig, ax
