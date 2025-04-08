from pathlib import Path
import math, json
import pandas as pd
from .node_types import Producer, Consumer, Battery, Timesteps
from . import Utils
from . import model_input
from . import model as opt


class ScenarioResults:
    def __init__(self, instance):
        # A solved instace of the model!
        self._instance = instance

        # A dictionary of variables and their indexing sets
        # Not all vars are here, add as needed
        self._vars = {
            "Pg": ["H", "N", "T"],
            "Pd": ["H", "N", "T"],
            "nSPd": ["H", "N", "T"],
            "nSPg": ["H", "N", "T"],
            "Es": ["H", "N", "T"],
            "TOTEX": None,
            "EnergySupTot": None,
            "UnmetDemand": None,
            "Cg": ["H", "N"],
            "Ecap": ["H", "N"],
        }

        # NAme Constants
        self.STACK = "Order"
        self.VALUE = "Value"
        self.TYPE = "Type"
        self.SUPPLY, self.DEMAND = "Supply", "Demand"

    # Magic Methodds
    def __getitem__(self, variable_name):
        """
        Get the variable value from the instance
        """
        return self._get_variable(variable_name)

    # Private Methods
    def _get_variable(self, variable_name):
        """
        Get the variable value from the instance
        """
        # Check if the variable is indexed
        if self._vars[variable_name] is None:
            return opt.get_variable_value(self._instance, variable_name)[0]
        else:
            return opt.get_indexed_variable_value(
                self._instance, variable_name, self._vars[variable_name]
            )

    # Plot Methods
    def get_generation_conusmption_plot_data(self):
        """
        Get the generation and consumption data for plotting in a stacked bar chart as Data Frame
        """
        # Get the generation and consumption data

        generation = self["Pg"].rename(columns={"Pg": self.VALUE})
        generation[self.STACK] = 1  # Order of the stack in the plot
        generation[self.TYPE] = self.SUPPLY

        curt_gen = self["nSPg"].rename(columns={"nSPg": self.VALUE})
        curt_gen[self.STACK] = (
            100  # Order of the stack in the plot must be on top of the generation
        )
        curt_gen[self.TYPE] = self.SUPPLY

        consumption = self["Pd"].rename(columns={"Pd": self.VALUE})
        consumption[self.STACK] = -1  # Order of the stack in the plot
        consumption[self.TYPE] = self.DEMAND

        curt_demand = self["nSPd"].rename(columns={"nSPd": self.VALUE})
        curt_demand[self.STACK] = (
            -100
        )  # Order of the stack in the plot must be on top of the consumption
        curt_demand[self.TYPE] = self.DEMAND

        # Concatenate the dataframes into a single dataframe
        data = pd.concat([generation, consumption, curt_gen, curt_demand])

        return data

    def get_storage_level_plot_data(self):
        """
        Get the storage level data for plotting in a line chart as Data Frame
        """
        return self["Es"].rename(columns={"Es": self.VALUE})

    def get_heatmap_plot_data(self):
        """
        Get the number to put on the heatmap.
        It is the avarage cost electricity supply, if all demand is met.
        Otherwise this is inf.
        """
        total_costs = self["TOTEX"]
        energy_supplied = self["EnergySupTot"]
        unmet_demand = self["UnmetDemand"]

        if (
            unmet_demand < 1e-1
        ):  # All demand is met ( not zero because of floating point errors)
            return round(total_costs / energy_supplied, 4)  # Euro/kWh
        else:
            return float("inf")

    def get_capacities(self):
        """
        Get the capacities of the producers and batteries
        """
        generation = self["Cg"].rename(columns={"Cg": self.VALUE})
        storage = self["Ecap"].rename(columns={"Ecap": self.VALUE})

        return pd.concat([generation, storage])


class Scenario:
    """
    A class to represent a Scenario in the energy system.

    Attributes:
    ----------
    nodes : list
        Contains nodes parsed from JSON sent from frontend.
    edges : list
        Contains edges parsed from JSON sent from frontend.
    timestepfile_chosen : str
        The timestep from the excel file.
    timesteps : list
        List of timesteps.
    graph_data : dict
        The scenario and slider JSON from frontend.
    reset_flag : bool
        Flag to indicate if the scenario should be reset.
    auto_simulate_flag : bool
        Flag to indicate if the scenario should be auto-simulated.
    prodCapacities : list
        List of producer capacities.
    modified_slider_values : list
        List of modified slider values.
    final_instance : ScenarioResults
        The final instance of the scenario results.
    current_dir : Path
        The current directory path.
    excel_file_path : Path
        The path to the excel file containing technology defaults.
    volume_data_folder : Path
        The path to the volume data folder.
    """
    def __init__(self, graph_data):
        """
        Constructs all the necessary attributes for the Scenario object.

        Parameters:
        ----------
        graph_data : dict
            The scenario and slider JSON from frontend.
        """
        self.nodes = []  # contains nodes parsed from json sent from frontend
        self.edges = []  # contains edges parsed from json sent from frontend
        self.timestepfile_chosen = None  # the timestep from the excel file
        self.timesteps = []
        self.graph_data = graph_data  # the scenario+slider json from frontend
        self.reset_flag = False
        self.auto_simulate_flag = False
        self.prodCapacities = []
        self.modified_slider_values = []
        self.final_instance = None
        # folder paths
        self.current_dir = Path(__file__).parent
        self.excel_file_path = (
            self.current_dir / "volume_data" / "Technology_defaults.xlsx"
        )
        self.volume_data_folder = self.current_dir / "volume_data"
        self.initialize()

    def initialize(self):
        """
        Initializes the Scenario class by processing the graph data and getting the default node values.
        """
        
        self.get_time_steps()
        self.get_default_node_values()
        self.get_slider_data()
        self.process_graph_data()
        self.get_edges()
        self.optimize()
        #self.print_nodes()

    def process_graph_data(self):
        """
        Processes the raw graph data to initialize nodes and assign default values.

        This method iterates over the nodes in the graph data, validates their types, and creates
        corresponding Producer, Consumer, or Battery instances with default values and positions.
        """
        # Define the valid node types
        VALID_TYPES = {"producer", "consumer", "battery", "junction"}

        try:
            # Loop through each node in the graph data
            for node in self.graph_data.get("nodes", []) or self.graph_data.get(
                "data", {}
            ).get("nodes", []):
                # Check that each node contains the required keys
                if not all(key in node for key in ["id", "type", "label"]):
                    raise ValueError(f"Missing keys in node: {node}")

                # Extract and validate the node type
                node_type = node["type"].lower()
                if node_type not in VALID_TYPES:
                    raise ValueError(f"Invalid type in node: {node['type']}")

                # Retrieve technology defaults
                technology = node["label"].lower()
                tech_defaults = self.defaults.get(technology)
                if not tech_defaults:
                    raise ValueError(f"No defaults found for technology: {technology}")

                # Process availability_profile_name or demand_profile
                processed_availability_profile = None
                processed_demand_profile = None

                if (
                    "availability_profile_name" in tech_defaults
                    and tech_defaults["availability_profile_name"] != None
                ):
                    processed_availability_profile = self.process_profile(
                        tech_defaults["availability_profile_name"],
                        profile_type="availability",
                    )

                if (
                    "demand_profile_name" in tech_defaults
                    and tech_defaults["demand_profile_name"] != None
                ):
                    processed_demand_profile = self.process_profile(
                        tech_defaults["demand_profile_name"], profile_type="demand"
                    )
                # Create the appropriate node based on type
                if node_type == "producer":
                    self.nodes.append(
                        Producer(
                            node_id=node["id"],
                            technology=node["label"],
                            capacity_cost=tech_defaults.get("capacity_cost"),
                            operational_cost=tech_defaults.get("operational_cost"),
                            operational_lifetime=tech_defaults.get(
                                "operational_lifetime"
                            ),
                            availability_profile=processed_availability_profile,
                            installed_capacity=self.installed_capacity_adjuster(
                                node["label"], node["id"]
                            ),  # gets slider value for a node
                            record_curtailment=tech_defaults.get("record_curtailment"),
                        )
                    )
                elif node_type == "consumer":
                    self.nodes.append(
                        Consumer(
                            node_id=node["id"],
                            technology=node["label"],
                            yearly_demand=tech_defaults.get("yearly_demand"),
                            demand_profile=processed_demand_profile,
                        )
                    )
                elif node_type == "battery":
                    self.nodes.append(
                        Battery(
                            node_id=node["id"],
                            technology=node["label"],
                            energy_capacity=tech_defaults.get("energy_capacity"),
                            installed_capacity=self.installed_capacity_adjuster(
                                node["label"], node["id"]
                            ),  # gets slider value for a node
                        )
                    )
            self.nodes.append(
                Timesteps(timesteplist=self.timesteps)
            )  # at end append timestep list
        except Exception as e:
            print(f"Error processing graph data: {e}")

    def get_default_node_values(self):
        """Gets the default values for the nodes from the excel file
        and stores as a dictionary in self.defaults"""
        self.defaults = Utils.load_default_technology_data(self.excel_file_path)

    def get_time_steps(self, scenario_name="default"):
        """
        Gets the timestep for a specific scenario name from excel file and saves it to self.timestepfile_chosen.

        Parameters:
            scenario_name (str): The name of the scenario to fetch the timestep for (default is "default").
        """
        self.timestepfile_chosen = Utils.get_timestep(
            self.excel_file_path, scenario_name
        )


    def get_edges(self):
        """
        Gets the edges from the graph data and stores them in self.edges.
        """
        self.edges = self.graph_data.get("edges", []) or self.graph_data.get(
            "data", {}
        ).get("edges", [])

    def get_slider_data(self):
        """Gets slider data from json and saves it to respective"""
        slider_data = self.graph_data.get("sliderData")
        self.reset_flag = slider_data.get("reset")
        self.autoSimulate_flag = slider_data.get("autoSimulate")
        self.prodCapacities = [
            (id, value) for id, value in slider_data.get("prodCapacities")
        ]
        self.modified_slider_values = [
            [f"node_{item[0]}", item[1]] for item in self.prodCapacities
        ]  # adds node Id to slider data

    def print_nodes(self):
        """
        Gets the nodes from the graph data and stores them in self.nodes.
        """
        print("Nodes in the scenario:")
        for node in self.nodes:
            print(node)


    def installed_capacity_adjuster(self, node_name, node_id):
        """
        Adjusts the installed capacity based on the slider value and node type.

        Parameters:
        ----------
        node_name : str
            The name of the node.
        node_id : str
            The unique identifier of the node.

        Returns:
        -------
        float
            The adjusted installed capacity.
        """
        try:
            slider_value = None
            for node in self.modified_slider_values:
                if node[0] == node_id:
                    slider_value = node[1]

            # Get the default values for the node from excel
            tech_defaults = self.defaults.get(node_name.lower()) #also use lowercase to match excel sheet

            # Get the max capacity for the node
            max_capacity = tech_defaults.get("max_installed_capacity")

            # Calculate the multiplier and adjusted capacity
            multiplier = max_capacity / 5
            adjusted_capacity = multiplier * slider_value

            return adjusted_capacity

        except Exception as e:
            # Handle any error (e.g., missing max_capacity or tech_defaults is None)
            print(
                f"Error: Could not calculate installed capacity for node '{node_name}'. Reason: {e}"
            )
            return 0

    def process_profile(self, profile_name, profile_type):
        """
        Processes the profile file based on the given profile name and selected timesteps. Availability profiles are processed differently from demand profiles. Demand profiles must be normalized to sum 1, otherwise model renders infeasible.

        Args:
            profile_name (str): The name of the profile file to process.
            profile_type (str): The type of profile to process (availability or demand).

        Returns:
            list: Processed and formatted array or data structure.
        """
        try:
            # Handle empty or NaN profile_name
            if not profile_name or (
                isinstance(profile_name, float) and math.isnan(profile_name)
            ):
                # print(f"Skipping invalid profile_name: {profile_name}")
                return []

            # Construct paths using pathlib
            profile_file_path = self.volume_data_folder / profile_name
            indices_file_path = self.volume_data_folder / self.timestepfile_chosen

            # Read and process the profile data
            with open(profile_file_path, "r") as profile_file:
                profile_data = [float(value) for value in profile_file.read().split()]

            # Read and process the indices data
            with open(indices_file_path, "r") as indices_file:
                indices = [int(index.strip()) for index in indices_file.readlines()]
                self.timesteps = indices  # assign timesteps from file to list

            # Extract the corresponding values
            selected_data = [
                profile_data[i - 1] for i in indices
            ]  # timesteps are not 0 index

            # Normalize the demand profile if necessary
            if profile_type.lower() == "demand":
                # Normalize the demand profile to sum to 1
                sum_values = sum(selected_data)
                if sum_values == 0:
                    raise ValueError("Sum of demand profile values is zero.")
                selected_data = [value / sum_values for value in selected_data]
            elif profile_type.lower() == "availability":
                # Availability profiles are not normalized
                pass
            else:
                raise ValueError(
                    f"Invalid profile type: {profile_type}. Must be 'demand' or 'availability'."
                )

            # Format the values to six decimal places
            formatted_data = [f"{value:.6f}" for value in selected_data]

            return formatted_data

        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return []
        except ValueError as e:
            print(f"Value error: {e}")
            return []
        except IndexError as e:
            print(f"Index error: {e}")
            return []
        except Exception as e:
            print(f"Error processing profile {profile_name}: {e}")
            return []

    def optimize(self):
        """
        Optimizes the scenario using the model input and solver.
        """
        m = model_input.OptNetworkInput()
        m.populate_from_scenario_list(self.nodes, self.timesteps)
        temp_file_path = m.save_to_temp_file() #saves file temporarily for multiple users
        #m.write("test.dat")  # save file to folder

        optimizer = opt.get_abstract_pyomo_model(
            fix_capacities=True
        )  # true to use slider values
        #instance = opt.load_input(optimizer)
        instance = opt.load_input_from_temp_file(optimizer, temp_file_path)
        instance = opt.solve_instance(instance)
        self.final_instance = ScenarioResults(instance)

    def get_final_instance(self):
        """
        Returns the final instance of the scenario results.

        Returns:
        -------
        ScenarioResults
            The final instance of the scenario results.
        """
        return self.final_instance


def main(): #for testing
    current_dir = Path(__file__).parent
    scenario_json_file = current_dir.parent / "slider_data" / "slider_data.json"
    graph_data = Utils.load_json(scenario_json_file)

    # Initialize the Scenario class
    scenario = Scenario(graph_data)
    scenario.optimize()

    results = scenario.get_final_instance()
    # Example of how to get the data for plotting
    print(results.get_generation_conusmption_plot_data())
    print(results.get_storage_level_plot_data())
    print(results.get_capacities())


if __name__ == "__main__":
    #main()
    pass
