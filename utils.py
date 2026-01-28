import time
import copy
from constants import sample_colors
import functools

def calculate_time(func):
    """
    Decorator to calculate the execution time of a function.
    """
    def timer_wrapper(*args, **kwargs):
        start_ns = time.perf_counter_ns()
        outcome = func(*args, **kwargs)
        end_ns = time.perf_counter_ns()
        print(f"Runtime: {end_ns - start_ns} ns")
        return outcome
    return timer_wrapper


def csp_common_decorator(strategy_func):
    """
    Decorator to provide common logic for constraint satisfaction problem (CSP) algorithms.
    """
    @functools.wraps(strategy_func)
    def strategy_wrapper(state_queue, adjacency, color_map, domain_map, total_states, backtrack_counter):
        # Check if all nodes are assigned a color
        if len(color_map) == total_states:
            return True, backtrack_counter
        
        # Apply the specific CSP strategy
        result, backtrack_counter = strategy_func(state_queue, adjacency, color_map, domain_map, total_states, backtrack_counter)
        
        return result, backtrack_counter
    return strategy_wrapper


def is_assignment_invalid(selected_color, neighboring_nodes, current_colors, color_domains):
    """
    Check if assigning a selected_color to a node will cause any conflicts.
    """
    for adjacent in neighboring_nodes:
        if current_colors.get(adjacent) is None and selected_color in color_domains[adjacent]:
            if len(color_domains[adjacent]) == 1:
                return True
    return False


def update_domains_on_assignment(selected_color, neighboring_nodes, current_colors, domain_pool):
    """
    Update domains of neighbors by removing the assigned color from their possibilities.
    """
    for adjacent in neighboring_nodes:
        if current_colors.get(adjacent) is None and selected_color in domain_pool[adjacent]:
            domain_pool[adjacent].remove(selected_color)
    return domain_pool


def singleton_domain_propagation(current_neighbors, all_neighbors, current_colors, domain_pool):
    """
    Propagate constraints based on singleton domains in neighboring nodes.
    """
    queue_singletons = []
    for adjacent in current_neighbors:
        if len(domain_pool[adjacent]) == 1 and current_colors.get(adjacent) is None:
            queue_singletons.append(adjacent)

    while queue_singletons:
        current = queue_singletons.pop(0)
        for neighbor in all_neighbors[current]:
            if current_colors.get(neighbor) is None and domain_pool[current][0] in domain_pool[neighbor]:
                domain_pool[neighbor].remove(domain_pool[current][0])
                if len(domain_pool[neighbor]) == 0:
                    return False
                if len(domain_pool[neighbor]) == 1:
                    queue_singletons.append(neighbor)
    return True


def create_initial_color_map(nodes):
    """
    Initialize a color mapping with no color assigned.
    """
    initial_map = {node: 'NULL' for node in nodes}
    return initial_map


def create_initial_domains(nodes, chromatic_bound):
    """
    Create a domain map for each node using a slice of available sample colors.
    """
    available_palette = sample_colors[:chromatic_bound].copy()
    domain_map = {node: copy.deepcopy(available_palette) for node in nodes}
    return domain_map
