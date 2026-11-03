"""Plotting helper for the lab: draws a sequence similarity network with NetworkX + matplotlib.

You don't need to edit this file. Import it in a notebook with:

    from ssn_plot import draw_ssn
"""

import math

import matplotlib.pyplot as plt
import networkx as nx

# Each protein type gets a color AND a marker shape, so the plot still reads
# for colorblind viewers or when printed in grayscale.
STYLES = {
    "hemoglobin_alpha": ("#2a78d6", "o"),
    "hemoglobin_beta": ("#eb6834", "s"),
    "myoglobin": ("#1baf7a", "^"),
    "neuroglobin": ("#eda100", "D"),
    "cytoglobin": ("#e87ba4", "v"),
    "leghemoglobin": ("#008300", "p"),
    "unknown": ("#0b0b0b", "*"),
}
OTHER_STYLE = ("#8a8984", "o")


def cluster_layout(G, seed=274):
    """Lay out each connected component on its own, then tile them in a grid.

    Big clusters come first; nodes with no edges (singletons) go in a row at the bottom.
    This is roughly how Cytoscape displays SSNs.
    """
    components = sorted(nx.connected_components(G), key=lambda c: (-len(c), sorted(c)))
    clusters = [c for c in components if len(c) > 1]
    singletons = [next(iter(c)) for c in components if len(c) == 1]

    pos = {}
    n_cols = max(1, math.ceil(math.sqrt(len(clusters))))
    for i, cluster in enumerate(clusters):
        row, col = divmod(i, n_cols)
        # Add nodes in sorted order: a set's order changes between runs, and so would the layout.
        subgraph = nx.Graph()
        subgraph.add_nodes_from(sorted(cluster))
        subgraph.add_edges_from(G.subgraph(cluster).edges)
        sub_pos = nx.spring_layout(subgraph, seed=seed, weight=None)
        for node, (x, y) in sub_pos.items():
            pos[node] = (col * 2.6 + x, -row * 2.6 + y)

    # Singletons: one row (or more) at the bottom, spaced so their labels don't collide.
    n_rows = math.ceil(len(clusters) / n_cols)
    spacing = 1.1
    per_row = max(int(n_cols * 2.6 / spacing), 1)
    for i, node in enumerate(sorted(singletons)):
        row, col = divmod(i, per_row)
        pos[node] = (-1 + col * spacing, -n_rows * 2.6 - row * 0.8)
    return pos


def draw_ssn(G, title="", seed=274, ax=None):
    """Draw graph G, coloring nodes by their 'protein_type' attribute.

    Parameters
    ----------
    G : networkx.Graph
        Nodes should have a 'protein_type' attribute.
    title : str
        Title shown above the plot.
    seed : int
        Random seed for the layout, so the picture is the same each time you run it.
    ax : matplotlib Axes, optional
        Draw on an existing set of axes (useful for side-by-side plots).
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 8))

    pos = cluster_layout(G, seed=seed)

    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.2, width=0.6, edge_color="#52514e")

    types = sorted({G.nodes[n].get("protein_type", "other") for n in G})
    for ptype in types:
        nodes = [n for n in G if G.nodes[n].get("protein_type", "other") == ptype]
        color, marker = STYLES.get(ptype, OTHER_STYLE)
        nx.draw_networkx_nodes(
            G, pos, nodelist=nodes, ax=ax, node_color=color, node_shape=marker,
            node_size=200 if ptype == "unknown" else 80,
            edgecolors="white", linewidths=0.8, label=ptype.replace("_", " "),
        )

    # Label the mystery sequences so they're easy to find.
    unknown = {n: n for n in G if G.nodes[n].get("protein_type") == "unknown"}
    # Singletons sit close together, so alternate their labels at two heights above the point.
    # (Labels below a point could land on the next row of singletons.)
    label_pos = {}
    for i, n in enumerate(sorted(unknown)):
        x, y = pos[n]
        raised = G.degree(n) == 0 and i % 2 == 1
        label_pos[n] = (x, y + 0.3) if raised else (x, y + 0.15)
    nx.draw_networkx_labels(G, label_pos, labels=unknown, ax=ax, font_size=9)

    ax.set_title(title)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=4, frameon=False,
              markerscale=1.0, fontsize=9)
    ax.axis("off")
    ax.margins(0.08)
    return ax
