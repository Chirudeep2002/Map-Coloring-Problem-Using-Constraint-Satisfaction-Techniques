from utils import is_assignment_invalid,update_domains_on_assignment, singleton_domain_propagation, csp_common_decorator

import copy

# Basic DFS-based backtracking algorithm for coloring nodes in a graph.
@csp_common_decorator
def dfs_color_solver(node_list, adjacency_map, color_assignment, domain_map, total_nodes, backtrack_counter):
    active_node = node_list[0]
    neighbors = adjacency_map[active_node]
    restricted_colors = [color_assignment.get(neighbor) for neighbor in neighbors]
    
    for available_color in domain_map[active_node]:
        if available_color not in restricted_colors:
            color_assignment[active_node] = available_color
            node_list.remove(active_node)
            success, backtrack_counter = dfs_color_solver(node_list, adjacency_map, color_assignment, domain_map, total_nodes, backtrack_counter)
            if success:
                return True, backtrack_counter
            del color_assignment[active_node]
            node_list.append(active_node)
    
    return False, backtrack_counter + 1

# DFS with Forward Checking to avoid invalid paths earlier in the recursion.
@csp_common_decorator
def dfs_color_solver_fc(node_list, adjacency_map, color_assignment, domain_map, total_nodes, backtrack_counter):
    active_node = node_list[0]
    neighbors = adjacency_map[active_node]
    restricted_colors = [color_assignment.get(neighbor) for neighbor in neighbors]
    
    for available_color in domain_map[active_node]:
        if available_color not in restricted_colors:
            color_assignment[active_node] = available_color
            node_list.remove(active_node)
            violates_constraints = is_assignment_invalid(available_color, neighbors, color_assignment, domain_map)
            if not violates_constraints:
                saved_domain = copy.deepcopy(domain_map)
                domain_map = update_domains_on_assignment(available_color, neighbors, color_assignment, saved_domain)
                success, backtrack_counter = dfs_color_solver_fc(node_list, adjacency_map, color_assignment, domain_map, total_nodes, backtrack_counter)
                if success:
                    return True, backtrack_counter
                domain_map = saved_domain
            del color_assignment[active_node]
            node_list.append(active_node)
    
    return False, backtrack_counter + 1

# DFS with Forward Checking and Singleton Propagation for enhanced constraint pruning.
@csp_common_decorator
def dfs_color_solver_fc_sp(node_list, adjacency_map, color_assignment, domain_map, total_nodes, backtrack_counter):
    active_node = node_list[0]
    neighbors = adjacency_map[active_node]
    restricted_colors = [color_assignment.get(neighbor) for neighbor in neighbors]
    
    for available_color in domain_map[active_node]:
        if available_color not in restricted_colors:
            color_assignment[active_node] = available_color
            node_list.remove(active_node)
            violates_constraints = is_assignment_invalid(available_color, neighbors, color_assignment, domain_map)
            if not violates_constraints:
                saved_domain = copy.deepcopy(domain_map)
                update_domains_on_assignment(available_color, neighbors, color_assignment, domain_map)
                propagated = update_domains_on_assignment(neighbors, adjacency_map, color_assignment, domain_map)
                if propagated:
                    success, backtrack_counter = dfs_color_solver_fc_sp(node_list, adjacency_map, color_assignment, domain_map, total_nodes, backtrack_counter)
                    if success:
                        return True, backtrack_counter
                domain_map = saved_domain
            del color_assignment[active_node]
            node_list.append(active_node)
    
    return False, backtrack_counter + 1
