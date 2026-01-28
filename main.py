import copy
import time
import networkx as nx
import warnings

# Suppress a specific warning
warnings.filterwarnings("ignore", message="No data for colormapping provided via 'c'. Parameters 'cmap' will be ignored", category=UserWarning)

import matplotlib.pyplot as plt
from prettytable import PrettyTable

from constants import australia_states, australia_adjacency_list, usa_states, usa_adjacency_list
from chromatic_number_util import find_chromatic_number
from utils import create_initial_color_map, create_initial_domains

from dfs_without_heuristics import dfs_color_solver, dfs_color_solver_fc, dfs_color_solver_fc_sp
from dfs_with_heuristics import dfs_graph_coloring_heuristic,dfs_graph_coloring_fc_heuristic,dfs_graph_coloring_fc_sp_heuristic

algorithm_options = {
    1: {
        1: dfs_color_solver,
        2: dfs_color_solver_fc,
        3: dfs_color_solver_fc_sp
    },
    2: {
        1: dfs_graph_coloring_heuristic,
        2: dfs_graph_coloring_fc_heuristic,
        3: dfs_graph_coloring_fc_sp_heuristic
    }
}

regions_lookup = {
    1: "USA",
    2: "Australia"
}

def render_map(adj_list, state_color_map):
    graph_obj = nx.Graph(adj_list)
    layout = nx.spring_layout(graph_obj)
    plt.figure(figsize=(12, 8))
    nx.draw(graph_obj, layout, with_labels=True,
            node_color=[state_color_map[node] for node in graph_obj.nodes()],
            node_size=3000, cmap=plt.cm.Set1,
            font_size=10, font_weight='bold')
    plt.show()

def render_table(mapping_data):
    table = PrettyTable()
    table.field_names = ["Region", "Assigned Color"]
    for location, clr in mapping_data.items():
        table.add_row([location, clr])
    print(table)

def prepare_data(region_choice):
    locations = copy.deepcopy(usa_states if region_choice == 1 else australia_states)
    graph_data = copy.deepcopy(usa_adjacency_list if region_choice == 1 else australia_adjacency_list)
    min_colors = find_chromatic_number(graph_data, regions_lookup[region_choice])
    init_color_map = {}
    domains = create_initial_domains(locations, min_colors)
    return locations, graph_data, init_color_map, domains

def run_coloring(heuristic_mode, method_mode, region_mode):
    nodes, edges, color_mapping, domains = prepare_data(region_mode)
    selected_algo = algorithm_options[heuristic_mode][method_mode]
    backtrack_tally = 0
    node_count = len(nodes)
    start = time.perf_counter_ns()
    result, backtrack_tally = selected_algo(nodes, edges, color_mapping, domains, node_count, backtrack_tally)
    end = time.perf_counter_ns()
    duration = end - start

    if result:
        print('COLORING RESULT:')
        print(color_mapping)
        print('\n')
        print('--------------------- REGION COLOR TABLE ----------------------\n')
        render_table(color_mapping)
        print("--------------------------------------------------------------")
        print("TOTAL BACKTRACK COUNT: ", backtrack_tally)
        print(f"EXECUTION TIME: {duration} ns")
        print("--------------------------------------------------------------")
        render_map(edges, color_mapping)
    else:
        print("Coloring failed -- No valid assignment found")
        print(f"Execution Time: {duration} ns")

def main():
    print("Starting Map Coloring Application")
    print("SELECT A REGION:")
    print("1. USA")
    print("2. Australia")
    selected_region = int(input())
    print(f"---------------- {regions_lookup[selected_region]} SELECTED ---------------------\n")
    print("CHOOSE HEURISTIC MODE:")
    print("1. WITHOUT Heuristics")
    print("2. WITH Heuristics")
    heuristic_mode = int(input())
    print('\n')
    print(f'------------------- {"WITHOUT" if heuristic_mode == 1 else "WITH"} HEURISTICS SELECTED --------------------------\n')
    print("CHOOSE ALGORITHM:")
    print("1. DFS")
    print("2. DFS + Forward Checking")
    print("3. DFS + Forward Checking + Singleton Propagation")
    selected_method = int(input())
    run_coloring(heuristic_mode, selected_method, selected_region)

if __name__ == "__main__":
    main()
