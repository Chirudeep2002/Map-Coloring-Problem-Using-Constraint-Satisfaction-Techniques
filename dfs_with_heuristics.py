from utils import is_assignment_invalid, update_domains_on_assignment, singleton_domain_propagation, csp_common_decorator
import copy
from operator import attrgetter

# MRV heuristic selects the variable with the fewest remaining legal values.
def apply_mrv_heuristic(node_list, domain_map, adjacency_map):
    def priority_key(node):
        return (len(domain_map[node]), -len(adjacency_map[node]))
    node_list = sorted(node_list, key=priority_key)
    selected_node = node_list[0]
    return selected_node

# LCV heuristic prefers the color that rules out the fewest choices for neighboring variables.
def apply_lcv_heuristic(active_node, domain_map, adjacency_map):
    node_domain = domain_map[active_node]
    neighboring_nodes = adjacency_map[active_node]
    value_restrictions = {color: sum(color in domain_map[neighbor] for neighbor in neighboring_nodes) for color in node_domain}
    return sorted(value_restrictions.keys(), key=lambda color: value_restrictions[color])

# DFS with MRV & LCV
@csp_common_decorator
def dfs_graph_coloring_heuristic(node_list, adjacency_map, color_map, domain_map, total_nodes, backtrack_counter):
    current_node = apply_mrv_heuristic(node_list, domain_map, adjacency_map)
    adjacent_nodes = adjacency_map[current_node]
    neighbor_colors = [color_map.get(neighbor) for neighbor in adjacent_nodes]
    sorted_colors = apply_lcv_heuristic(current_node, domain_map, adjacency_map)
    
    for selected_color in sorted_colors:
        if selected_color not in neighbor_colors:
            color_map[current_node] = selected_color
            node_list.remove(current_node)
            solved, backtrack_counter = dfs_graph_coloring_heuristic(node_list, adjacency_map, color_map, domain_map, total_nodes, backtrack_counter)
            if solved:
                return True, backtrack_counter
            del color_map[current_node]
            node_list.append(current_node)
    return False, backtrack_counter + 1

# DFS with Forward Checking + Heuristics
@csp_common_decorator
def dfs_graph_coloring_fc_heuristic(node_list, adjacency_map, color_map, domain_map, total_nodes, backtrack_counter):
    current_node = apply_mrv_heuristic(node_list, domain_map, adjacency_map)
    adjacent_nodes = adjacency_map[current_node]
    neighbor_colors = [color_map.get(neighbor) for neighbor in adjacent_nodes]
    sorted_colors = apply_lcv_heuristic(current_node, domain_map, adjacency_map)
    
    for selected_color in sorted_colors:
        if selected_color not in neighbor_colors:
            color_map[current_node] = selected_color
            node_list.remove(current_node)
            constraint_violated = is_assignment_invalid(selected_color, adjacent_nodes, color_map, domain_map)
            if not constraint_violated:
                domain_snapshot = copy.deepcopy(domain_map)
                domain_map = update_domains_on_assignment(selected_color, adjacent_nodes, color_map, domain_map)
                solved, backtrack_counter = dfs_graph_coloring_fc_heuristic(node_list, adjacency_map, color_map, domain_map, total_nodes, backtrack_counter)
                if solved:
                    return True, backtrack_counter
                domain_map = domain_snapshot
            del color_map[current_node]
            node_list.append(current_node)
    return False, backtrack_counter + 1

# DFS with Forward Checking + Singleton Propagation + Heuristics
@csp_common_decorator
def dfs_graph_coloring_fc_sp_heuristic(node_list, adjacency_map, color_map, domain_map, total_nodes, backtrack_counter):
    current_node = apply_mrv_heuristic(node_list, domain_map, adjacency_map)
    adjacent_nodes = adjacency_map[current_node]
    neighbor_colors = [color_map.get(neighbor) for neighbor in adjacent_nodes]
    sorted_colors = apply_lcv_heuristic(current_node, domain_map, adjacency_map)
    
    for selected_color in sorted_colors:
        if selected_color not in neighbor_colors:
            color_map[current_node] = selected_color
            node_list.remove(current_node)
            constraint_violated = is_assignment_invalid(selected_color, adjacent_nodes, color_map, domain_map)
            if not constraint_violated:
                domain_snapshot = copy.deepcopy(domain_map)
                domain_map = update_domains_on_assignment(selected_color, adjacent_nodes, color_map, domain_map)
                propagated = singleton_domain_propagation(adjacent_nodes, adjacency_map, color_map, domain_map)
                if propagated:
                    solved, backtrack_counter = dfs_graph_coloring_fc_sp_heuristic(node_list, adjacency_map, color_map, domain_map, total_nodes, backtrack_counter)
                    if solved:
                        return True, backtrack_counter
                domain_map = domain_snapshot
            del color_map[current_node]
            node_list.append(current_node)
    return False, backtrack_counter + 1
