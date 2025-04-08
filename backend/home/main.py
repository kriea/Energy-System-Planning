from graph_Process import GraphProcessor
from scenario_processing import parse_json 
import os
import json
def main():
    # Your JSON input
    
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, '../slider_data/slider_data.json')


    # Load the JSON file
    with open(json_path, "r") as json_file:
        json_input = json.load(json_file)
    # Create an instance of GraphProcessor
    processor = GraphProcessor()

    # Load the JSON input
    processor.parse_and_load_graph(json_input)

    # Print summary of the graph
    print("\n--- Graph Summary ---")
    processor.print_summary()

    # Accessing specific details
    node_id = 'node_1'
    print(f"\nDetails for node {node_id}:")
    print(processor.get_node_details(node_id))

    # Get all producer nodes
    print("\n--- Producer Nodes ---")
    producer_nodes = processor.get_nodes_by_type("producer")
    for node in producer_nodes:
        print(node)

    # Get connected nodes to "node_3"
    print("\n--- Connected Nodes to node_3 ---")
    connected_nodes = processor.get_connected_nodes("node_3")
    print(connected_nodes)


if __name__ == "__main__":
    main()