from utils import calculate_time

def is_color_valid(adjacency_list, current_node, current_color, assigned_colors):
    # Check if any neighboring nodes have the same color
    for adjacent_node in adjacency_list[current_node]:
        if assigned_colors.get(adjacent_node) == current_color:
            return False
    return True

def assign_colors(adjacency_list, total_colors, uncolored_nodes, assigned_colors, max_node_degree):
    if not uncolored_nodes:
        return True

    # Pick node with highest number of connections
    node_to_color = max(uncolored_nodes, key=lambda node: len(adjacency_list[node]))
    for color in range(total_colors):
        if color > max_node_degree:
            break  # Avoid coloring with more than max degree + 1
        if is_color_valid(adjacency_list, node_to_color, color, assigned_colors):
            assigned_colors[node_to_color] = color
            if assign_colors(adjacency_list, total_colors, uncolored_nodes - {node_to_color}, assigned_colors, max_node_degree):
                return True
            assigned_colors.pop(node_to_color)
    return False

@calculate_time
def find_chromatic_number(adjacency_list, graph_label):
    max_node_degree = max(len(adj_nodes) for adj_nodes in adjacency_list.values())
    total_colors = 1
    uncolored_nodes = set(adjacency_list.keys())
    assigned_colors = {}
    while not assign_colors(adjacency_list, total_colors, uncolored_nodes, assigned_colors, max_node_degree):
        total_colors += 1
        assigned_colors.clear()
    print(f"Minimum number of colors required for {graph_label} map:", total_colors)
    print(f"Computed Chromatic number for {graph_label} map ", end="")
    return total_colors
