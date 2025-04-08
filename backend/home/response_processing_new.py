import json, math, random, os, copy
from graph_to_scenario.scenario import Scenario


class OptimizerResultProcessor:
    def __init__(self, json_data):
        self.json_data = json_data
        self.prodCapacities = []
        self.autoSimulate = None
        self.reset = None
        self.node_data = None
        self.bestIdx = []
        self.sliderVals = []
        self.combined_json = (
            None  # final JSON containing heatmap, linechart, and barchart data
        )

    def process_response(self):
        """Process the incoming JSON data and save it for debugging."""

        # Extracting data from the JSON
        self.node_data = self.json_data.get("nodes")
        slider_data = self.json_data.get("sliderData")

        self.prodCapacities = [
            capacity for capacity in slider_data.get("prodCapacities")
        ]
        self.sliderVals = [obj for obj in slider_data.get("sliderVals")]
        self.autoSimulate = slider_data.get("autoSimulate")
        self.reset = slider_data.get("reset")

        # Check for reset state
        if not self.reset:
            if self.autoSimulate:
                mainData = self.fillMatrixOfCells(
                    self.prodCapacities,
                )
                data = {"mainData": mainData, "bestIdx": self.bestIdx}
            else:
                data = {
                    "mainData": self.fill_cell(
                        self.prodCapacities,
                    ),
                    "bestIdx": self.bestIdx,
                }
        else:
            data = {
                "mainData": None,
                "bestIdx": self.bestIdx,
            }

        return data
    
    def run_optimizer_return_results(self, prodCapacities):
        """
        Runs the optimizer and returns a combined JSON containing heatmap, linechart,
        and barchart data.
        """
        self.json_data["sliderData"]["prodCapacities"] = prodCapacities

        optimizer = Scenario(self.json_data)
        optimizer_result = optimizer.get_final_instance()

        # Heatmap (single float value)
        heatmap_data = optimizer_result.get_heatmap_plot_data()  # single value
        if heatmap_data == float("inf"):  # Handle float("inf") for JSON compatibility
            heatmap_data = '"inf"'  #'"Inf"' #in case value is infinite return 9999, change this later to Inf and integrate in matrix to display string
        ##########Important, change ^the above line later ^^##################

        # Line chart (DataFrame to JSON)
        linechart_data = (optimizer_result.get_storage_level_plot_data()).to_json(
            orient="records"
        )

        # Bar chart (DataFrame to JSON)
        barchart_data = (
            optimizer_result.get_generation_conusmption_plot_data()
        ).to_json(orient="records")

        # Create a combined JSON string with different keys
        combined_json = f"""
        {{
            "heatmap": {heatmap_data},
            "linechart": {linechart_data},
            "barchart": {barchart_data}
        }}
        """
        self.combined_json = json.loads(
            combined_json
        )  # Save the combined JSON for later use

    def fill_cell(self, prodCapacities):
        """Fills a cell with calculated values and saves combined data."""
        self.run_optimizer_return_results(prodCapacities)

        # Extract DataFrames from the optimizer output
        matrixData = JSONExtractor.extract_items(self.combined_json, "heatmap")

        tmpLine = JSONExtractor.extract_items(self.combined_json, "linechart")
        tmpBar = JSONExtractor.extract_items(self.combined_json, "barchart")

        lineChartData = {}
        barChartData = {}
        timestep = max(barItem.get("T") for barItem in tmpBar)

        for node in self.node_data:

            if node.get("type") != "junction": #if the node is not a junction, then it produces data for the barchart and possibly linechart
                currentNodeID = node.get("id")[5:]

                for bardata in tmpBar: # barData is something like this: {'H': 'Solar', 'N': 'node_1', 'T': 1, 'Value': 0.0, 'Order': 1, 'Type': 'Supply'}
                    currentBarDataID = bardata.get("N", -1)[5:]
                    if currentBarDataID == currentNodeID:
                        if barChartData.get(currentBarDataID) is None:
                            barChartData.update({currentBarDataID:{}})
                        currentOrder = bardata.get("Order")
                        if barChartData.get(currentBarDataID).get(currentOrder) is None:
                            barChartData.get(currentBarDataID).update({currentOrder:[]})
                        barChartData.get(currentBarDataID).get(currentOrder).append({**bardata,  "Value": math.copysign(bardata["Value"], bardata["Order"])}) #create a dict with all Values being multiplied by either 1 or -1 depending on the sign of Order (Goal: For nodes with type Demand to have negative Value)
    
                if node.get("type") == "battery":#if node is a battery, then it additionally produces data for linechart
                    lineChartData.update(## group all objects for linechart data together by node id
                        {
                            currentNodeID: [
                                linedata
                                for linedata in tmpLine
                                if linedata.get("N", -1)[5:] == currentNodeID
                            ]
                        }
                    )
        return {
            "matrixData": matrixData,
            "chartsData": {
                "lineChartData": lineChartData,
                "barChartData": barChartData,
                "timestep": timestep,
            },
        }

    def fillMatrixOfCells(self, prodCapacities):
        """Fills the result matrix for all slider value combinations."""
        bestMatrixVal = [float("inf")]
        resultMatrix = [[0 for _ in range(6)] for _ in range(6)]
        indexCol = -1
        indexRow = -1

        # Identify index of nodes in prodCapacities
        if self.sliderVals[0]["nodeID"] in [entry[0] for entry in prodCapacities]:
            indexCol = next(
                (
                    i
                    for i, entry in enumerate(prodCapacities)
                    if entry[0] == self.sliderVals[0]["nodeID"]
                ),
                -1,
            )

        if self.sliderVals[1]["nodeID"] in [entry[0] for entry in prodCapacities]:
            indexRow = next(
                (
                    i
                    for i, entry in enumerate(prodCapacities)
                    if entry[0] == self.sliderVals[1]["nodeID"]
                ),
                -1,
            )
        

        if indexCol == -1 or indexRow == -1:
            raise Exception("IDs of selectedNodes are not in prodCapacities")

        # Fill the result matrix
        for col in range(6):
            prodCapacities[indexCol][1] = col
            for row in range(6):
                prodCapacities[indexRow][1] = row
                value = self.fill_cell(prodCapacities)
                resultMatrix[col][row] = value

                if not isinstance(value["matrixData"], str) and bestMatrixVal[0] > value["matrixData"]:
                    bestMatrixVal[0] = value["matrixData"]
                    self.bestIdx[:] = copy.deepcopy(prodCapacities)

        if bestMatrixVal == [float("inf")]:
            self.bestIdx[:] = [[x[0], 0] for x in prodCapacities]

        return resultMatrix


class JSONExtractor:
    @staticmethod
    def extract_items(json_data, key, **filters):
        """
        Extracts items from the JSON data based on the specified key and filters.
        :param json_data: The JSON object to search within.
        :param key: The top-level key to search within ('heatmap', 'linechart', or 'barchart').
        :param filters: Key-value pairs to filter the items.
                        Example: H='Battery', Type='Demand'
        :return: List of items that match the filters.
        """
        # Check if the key exists in the JSON data
        if key not in json_data:
            print(f"Key '{key}' not found in JSON data.")
            return []

        # If the key is 'heatmap', return the value directly
        if key == "heatmap":
            return json_data[key]

        # For 'linechart' and 'barchart', filter the list of dictionaries
        items = json_data[key]
        result = []

        # Apply all filters
        for item in items:
            if all(item.get(k) == v for k, v in filters.items()):
                result.append(item)

        return result

    @staticmethod
    def save_json(json_file, filename: str):
        dict = json.loads(json_file)
        # Write JSON to processed_data folder, for debugging, remove later
        folder_path = os.path.join(os.getcwd(), "processed_results")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "w") as json_file:
            json.dump(dict, json_file, indent=4)
