import { defineStore } from "pinia";

// Define a store for scenario data
export const useScenarioStore = defineStore("scenario", {
  // State variables
  state: () => ({
    nodes: [], // Array to store nodes
    edges: [], // Array to store edges
    sliderData: {}, // Object to store slider data
  }),

  // Actions to manipulate the state
  actions: {
    // Action to save the scenario data
    saveScenario(nodes, edges) {
      this.nodes = nodes; // Save nodes to the state
      this.edges = edges; // Save edges to the state
      console.log("Nodes and edges saved in store!"); // Log a message to the console
    },

 
    

    // Action to load the scenario data
    loadScenario() {
      return {
        nodes: this.nodes, // Return nodes from the state
        edges: this.edges, // Return edges from the state
        sliderData: this.sliderData, // Return slider data from the state
      };
    },
  },
});

