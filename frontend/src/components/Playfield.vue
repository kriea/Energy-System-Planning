<template>
  <Panel id="playfield">
    <!-- Image Box -->

    <!-- Vue Flow Container -->
    <div
      id="vueflow_container"
      ref="vueFlowContainer"
      :style="{
        backgroundImage: 'url(' + imgUrl + ')',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }"
      style="
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 72.5%;
        z-index: 2;
      "
    >
      <vue-flow
        ref="vueFlow"
        v-model:nodes="nodes"
        v-model:edges="edges"
        :fit-view="true"
        :zoomOnScroll="false"
        :zoomOnPinch="false"
        :panOnDrag="false"
        :pan-on-scroll="false"
        :preventScrolling="true"
        :snap-grid="snapGrid"
        :snap-to-grid="true"
        
        :connection-mode="connectionMode"
        :node-types="customNodeTypes"
        :auto-pan-on-node-drag="false"
        :nodes-draggable="!locked"
        :edges-connectable="edgeMode"
        :autoPanOnConnect="false"
        :zoomOnDoubleClick="false"
        @connect="onConnect"
      />
    </div>

    <canvas v-if="showGrid" ref="gridCanvas" id="grid_overlay"></canvas>

    <!-- Buttons at the Bottom -->
    <div id="buttons_container1">
      <!-- Dropdowns -->

      <!-- Scenario Management -->
      <div class="row">
        <Select
          v-model="selectedScenario"
          :options="scenarios"
          option-label=""
          :placeholder="currLang.choose_scenario"
        ></Select>
        <Button
          @click="loadRequest"
          type="submit"
          class="button"
          v-bind:label="currLang.load_scenario"
        ></Button>
        <Button
          @click="triggerJsonUpload"
          type="submit"
          class="button"
          v-bind:label="currLang.upload_json"
        ></Button>
        <Button
          @click="triggerImageUpload"
          type="submit"
          class="button"
          v-bind:label="currLang.upload_image"
        ></Button>

        <Button
          @click="toggleGridOverlay"
          type="submit"
          class="button"
          v-bind:label="currLang.toggle_grid"
        ></Button>
        <Button
          @click="clearNodes"
          type="submit"
          class="button"
          v-bind:label="currLang.clear_nodes"
        ></Button>
        <Button
          @click="saveData"
          type="submit"
          class="button"
          v-bind:label="currLang.save_text"
        ></Button>
      </div>
      <!-- Utilities -->
      <div class="row">
        <Button
          @click="toggleEdgeMode"
          type="submit"
          class="button"
          v-bind:label="currLang.add_edge"
        ></Button>

        <Button
          @click="addConsumerNode"
          type="submit"
          class="button"
          v-bind:label="currLang.add_consumer"
        ></Button>
        <Button
          @click="addBatteryNode"
          type="submit"
          class="button"
          v-bind:label="currLang.add_battery"
        ></Button>
        <Button
          @click="addJunctionNode"
          type="submit"
          class="button"
          v-bind:label="currLang.add_junction"
        ></Button>
        <Button
          @click="addEnergySourceNode"
          type="submit"
          class="button"
          v-bind:label="currLang.add_energy_source"
        ></Button>
      </div>
      <!-- Actions -->

      <div class="row">
        <!-- <Select v-model="selectedConsumer" :options="optionsConsumer"
          :placeholder="currLang.selector_text_consumer"></Select> -->
        <Select
          v-model="selectedConsumer"
          :options="currLang.consumer_types"
          option-label="label"
          option-value="value"
          :placeholder="currLang.selector_text_consumer"
        ></Select>
        <Select
          v-model="selectedProducer"
          :options="currLang.producer_types"
          option-label="label"
          option-value="value"
          :placeholder="currLang.selector_text_producer"
        ></Select>
      </div>
    </div>
    <input
      type="file"
      id="imageInput"
      ref="imageInput"
      @change="handleFileChange('image', $event)"
      accept="image/*"
      style="display: none"
    />
    <input
      type="file"
      id="jsonInput"
      ref="jsonInput"
      @change="handleFileChange('json', $event)"
      accept=".json"
      style="display: none"
    />
  </Panel>
</template>

<script>
import { Button, Select } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";
import { VueFlow, MarkerType, useVueFlow } from "@vue-flow/core";
import "@vue-flow/core/dist/style.css";
import ConsumerNode from "./customNodes/Consumer.vue";
import BatteryNode from "./customNodes/Battery.vue";
import JunctionNode from "./customNodes/Junction.vue";
import ProducerNode from "./customNodes/Producer.vue";
import { usedLanguage } from "../assets/stores/pageSettings";
import {  ref, reactive, watch } from "vue";
import { getNodeData } from "@/utils/nodeUtils.js";
import { onMounted, onBeforeUnmount } from "vue";
import { backendURL } from "@/assets/urlExports";

export default {
  components: {
    Panel,
    Button,
    Select,
    VueFlow,
  },
  setup() {
    const currLang = usedLanguage();
    //Playfield variables
    const imgUrl = ref(null); // URL for the image
    const showGrid = ref(false); // Flag for showing grid
    const gridSize = ref(15); // Grid size (number of cells per row/column)
    const snapGrid = ref([50, 50]);
    const nodes = ref([]); // Nodes for Vue Flow
    const edges = ref([]); // Edges for Vue Flow
    const nodeIdCounter = ref(1); // Counter for unique IDs
    const connectionMode = ref("strict"); // Connection mode for the graph
    const edgeMode = ref(false); // Flag for edge creation mode
    const selectedNodeId = ref(null); // Track the selected node for edge creation
    const locked = ref(false); // Lock flag
    const jsonUrl = ref(null); // JSON file URL

    // Reactive object for edge properties
    const edgeProps = reactive({
      color: "#FA0404", // Edge color
      animated: true, // Edge animation
      style: { stroke: "#FA0404", strokeWidth: 3, opacity: 0.8 }, // Edge style
      type: "bezier",

      markerEnd: { type: MarkerType.Arrow, width: 6, height: 6, color: "#000" },
    });


    // Reactive object for custom node types
    const customNodeTypes = reactive({
      consumer: ConsumerNode,
      producer: ProducerNode,
      battery: BatteryNode,
      junction: JunctionNode,
    });

    // Reactive state for selected consumer/producer and their options
    const selectedConsumer = ref(""); // Selected value for consumers
    const selectedProducer = ref(""); // Selected value for producers
    const scenarios = ref([
      currLang.scene_1,
      currLang.scene_2,
      currLang.scene_3,
    ]); // Scenario options
    const selectedScenario = ref();

    watch(
      () => currLang.currLang,
      () => {
        scenarios.value[0] = currLang.scene_1;
        scenarios.value[1] = currLang.scene_2;
        scenarios.value[2] = currLang.scene_3;
      }
    );

    const vueFlowContainer = ref(null); // Ref for the container
    const vueFlow = ref(null); // Ref for the VueFlow instance

    onMounted(() => {
      const resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const { width, height } = entry.contentRect;
          // Update node positions based on normalized data
          nodes.value = nodes.value.map((node) => {
            if (!node.data.normalizedX || !node.data.normalizedY) {
              return node; // Skip if normalized data is missing
            }
            return {
              ...node,
              position: {
                x: node.data.normalizedX * width,
                y: node.data.normalizedY * height,
              },
            };
          });
          // Adjust the view after resizing
          if (vueFlow.value) {
            vueFlow.value.fitView({ padding: 0.1 });
          }
        }
      });

      if (vueFlowContainer.value) {
        resizeObserver.observe(vueFlowContainer.value);
      }

      onBeforeUnmount(() => {
        resizeObserver.disconnect();
      });
    });

    return {
      currLang,
      //playfield variables
      imgUrl,
      showGrid,
      gridSize,
      snapGrid,
      nodes,
      edges,
      customNodeTypes,
      nodeIdCounter,
      connectionMode,
      edgeMode,
      selectedNodeId,
      edgeProps,
      locked,
      jsonUrl,
      selectedConsumer,
      selectedProducer,
      scenarios,
      selectedScenario,
      VueFlow,
      vueFlowContainer,
    };
  },

  methods: {
    toggleLock() {
      this.locked = !this.locked;
    },

    async loadRequest() {
      try {
        const url = backendURL + "api/process-scenario/";
        let id = null;
        if (
          this.selectedScenario.charAt(this.selectedScenario.length - 1) == "1"
        ) {
          id = 1;
        } else if (
          this.selectedScenario.charAt(this.selectedScenario.length - 1) == "2"
        ) {
          id = 2;
        } else if (
          this.selectedScenario.charAt(this.selectedScenario.length - 1) == "3"
        ) {
          id = 3;
        }

        const imgResponse = await axios.get(url, {
          params: { id: id, filetype: "png" },
          responseType: "blob",
        });

        if (this.imgUrl) {
          URL.revokeObjectURL(this.imgUrl);
        }

        this.imgUrl = URL.createObjectURL(imgResponse.data);

        const graphResponse = await axios.get(url, {
          params: { id: id, filetype: "json" },
          responseType: "json",
        });

        const { nodes, edges } = graphResponse.data;

        this.nodes = nodes.map((node) => {
          return {
            ...node,
            data: {
              ...getNodeData(node.label),
              normalizedX: node.position.x, // Store normalized X (0-1)
              normalizedY: node.position.y, // Store normalized Y (0-1)
            },
            position: {
              x: node.position.x * this.$refs.vueFlowContainer.offsetWidth,
              y: node.position.y * this.$refs.vueFlowContainer.offsetHeight,
            },
          };
        });

        this.edges = edges.map((edge) => ({
          ...edge,
          animated: this.edgeProps.animated,
          style: this.edgeProps.style,
          color: this.edgeProps.color,

          markerEnd: { type: MarkerType.Arrow, width: 6, height: 6, color: "#000" },
        }));
      } catch (error) {
        console.error("Error fetching data:", error);
        alert(`Error: ${error.message}`);
      }
    },

    toggleGridOverlay() {
      this.showGrid = !this.showGrid;
      if (this.showGrid) {
        this.$nextTick(() => {
          this.drawGrid();
        });
      }
    },

    drawGrid() {
      const canvas = this.$refs.gridCanvas;
      const vueFlowContainer = this.$refs.vueFlowContainer;

      if (!canvas || !vueFlowContainer) return;

      // Match canvas dimensions to the VueFlow container
      const width = vueFlowContainer.offsetWidth;
      const height = vueFlowContainer.offsetHeight;

      canvas.width = width;
      canvas.height = height;

      const cellWidth = width / this.gridSize;
      const cellHeight = height / this.gridSize;

      // Set the snapGrid based on cell width/height
      this.snapGrid = [cellWidth, cellHeight]; // Update snapGrid

      const context = canvas.getContext("2d");
      context.clearRect(0, 0, width, height); // Clear the canvas
      context.strokeStyle = "#000000"; // Set grid line color
      context.lineWidth = 1; // Set grid line width

      // Draw vertical lines
      for (let x = 0; x <= width; x += cellWidth) {
        context.beginPath();
        context.moveTo(x, 0);
        context.lineTo(x, height);
        context.stroke();
      }

      // Draw horizontal lines
      for (let y = 0; y <= height; y += cellHeight) {
        context.beginPath();
        context.moveTo(0, y);
        context.lineTo(width, y);
        context.stroke();
      }
    },

    addBatteryNode() {
      const vueFlowContainer = this.$refs.vueFlowContainer;
      if (!vueFlowContainer) return;

      const width = vueFlowContainer.offsetWidth / this.gridSize;
      const height = vueFlowContainer.offsetHeight / this.gridSize;

      const nodeData = getNodeData("Battery");
      if (!nodeData) return;

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "battery",
        position: { x: width * 5, y: height * 3 },
        data: nodeData,
      };
      this.nodes.push(newNode);
    },

    addJunctionNode() {
      const vueFlowContainer = this.$refs.vueFlowContainer;
      if (!vueFlowContainer) return;

      const width = vueFlowContainer.offsetWidth / this.gridSize;
      const height = vueFlowContainer.offsetHeight / this.gridSize;
      const nodeData = getNodeData("Junction");
      if (!nodeData) return;

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "junction",
        position: { x: width * 7, y: height * 3 },
        data: nodeData,
      };
      this.nodes.push(newNode);
    },

    addEnergySourceNode() {
      const vueFlowContainer = this.$refs.vueFlowContainer;
      if (!vueFlowContainer) return;

      const width = vueFlowContainer.offsetWidth / this.gridSize;
      const height = vueFlowContainer.offsetHeight / this.gridSize;

      if (!this.selectedProducer) {
        alert("Please select an energy source type before adding a node.");
        return;
      }
      const nodeData = getNodeData(this.selectedProducer);
      if (!nodeData) {
        alert("Unknown producer type selected.");
        return;
      }

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "producer",
        position: { x: width * 5, y: height * 4 },
        data: nodeData,
        targetPosition: "left",
        sourcePosition: "right",
      };

      this.nodes.push(newNode);
    },

    addConsumerNode() {
      if (!this.selectedConsumer) {
        alert("Please select an option before adding a node.");
        return;
      }

      const vueFlowContainer = this.$refs.vueFlowContainer;
      if (!vueFlowContainer) return;

      const width = vueFlowContainer.offsetWidth;
      const height = vueFlowContainer.offsetHeight;

      const nodeData = getNodeData(this.selectedConsumer);
      if (!nodeData) {
        alert("Unknown Consumer type selected.");
        return;
      }

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "consumer",
        position: { x: (2 * width) / 3, y: (2 * height) / 3 },
        data: nodeData,
      };

      this.nodes.push(newNode);
    },

    toggleEdgeMode() {
      // Toggle edge creation mode
      this.locked = !this.locked;
      this.edgeMode = !this.edgeMode;
      if (this.edgeMode) {
        this.selectedNodeId = null;
        this.connectionMode = "loose"; // Allow loose connections for edge creation
      } else {
        this.connectionMode = "strict"; // Return to strict mode
      }
    },
    clearNodes() {
      this.nodes = [];
      this.edges = [];
    },

    onConnect(connection) {
      if (this.edgeMode) {
        const newEdge = {
          id: `edge_${this.edges.length + 1}`,
          source: connection.source,
          target: connection.target,
          sourceHandle: connection.sourceHandle, // Ensure correct handle connection
          targetHandle: connection.targetHandle, // Ensure correct handle connection
          type: "default",
          animated: this.edgeProps.animated,
          style: this.edgeProps.style,
          color: this.edgeProps.color,
        };
        this.edges.push(newEdge);
      }
    },

    saveData() {
      try {
        // Check if the graph is fully connected
        const nodesConnected = this.depthFirstSearch();
        if (!nodesConnected) {
          alert("Error: Graph is not fully connected");
          return;
        }

        // Check if the total number of producers and batteries exceeds 5
        const producerAndBatteryCount = this.countProducersAndBatteries();
        if (producerAndBatteryCount > 5) {
          alert(
            "Error: The total number of producers and batteries cannot exceed 5."
          );
          return;
        }

        // Get the container dimensions
        const container = this.$refs.vueFlowContainer;
        if (!container) {
          throw new Error(
            "Container not found. Unable to normalize node positions."
          );
        }

        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;

        if (containerWidth === 0 || containerHeight === 0) {
          throw new Error(
            "Container dimensions are invalid. Unable to normalize node positions."
          );
        }

        // Normalize node positions and prepare data for saving
        const dataToSave = {
          nodes: this.nodes.map((node) => ({
            id: node.id,
            position: {
              x: node.position.x / containerWidth, // Normalize x
              y: node.position.y / containerHeight, // Normalize y
            },
            type: node.type,
            label: node.data.label,
          })),
          edges: this.edges.map((edge) => ({
            id: edge.id,
            source: edge.source,
            target: edge.target,
            sourceHandle: edge.sourceHandle,
            targetHandle: edge.targetHandle,
          })),
        };

        // Convert the data to a JSON string
        const jsonString = JSON.stringify(dataToSave, null, 2); // Pretty-print JSON

        // Create a Blob and trigger download
        const jsonBlob = new Blob([jsonString], { type: "application/json" });
        const jsonLink = document.createElement("a");
        jsonLink.href = URL.createObjectURL(jsonBlob);
        jsonLink.download = "scenario_graph.json";
        jsonLink.click();

        // Clean up the URL object
        URL.revokeObjectURL(jsonLink.href);
      } catch (error) {
        console.error("Error saving data:", error);
        alert(`Error: ${error.message}`);
      }
    },
    depthFirstSearch() {
      const visited = new Set();

      const dfs = (nodeId) => {
        if (visited.has(nodeId)) return;
        visited.add(nodeId);

        this.edges.forEach((edge) => {
          if (edge.source === nodeId && !visited.has(edge.target)) {
            dfs(edge.target);
          } else if (edge.target === nodeId && !visited.has(edge.source)) {
            dfs(edge.source);
          }
        });
      };

      if (this.nodes.length > 0) {
        dfs(this.nodes[0].id);
      }

      return this.nodes.every((node) => visited.has(node.id));
    },

    countProducersAndBatteries() {
      let count = 0;

      this.nodes.forEach((node) => {
        if (node.type === "producer" || node.type === "battery") {
          count++;
        }
      });

      return count;
    },

    triggerImageUpload() {
      this.$refs.imageInput.click(); // Trigger image upload
    },

    // Trigger the JSON file input
    triggerJsonUpload() {
      this.$refs.jsonInput.click(); // Trigger JSON upload
    },

    handleFileChange(type, event) {
      const file = event.target.files[0];
      if (type === "image") {
        this.imageFile = file;
        if (this.imgUrl) URL.revokeObjectURL(this.imgUrl);
        this.imgUrl = URL.createObjectURL(file);

        // Show alert for JSON upload
        alert("Please upload the corresponding JSON file.");
      } else if (type === "json") {
        this.jsonFile = file;
        this.loadScenarioData(); // Handle JSON after image upload
      }
    },
    // Load and parse the JSON file
    loadScenarioData() {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target.result);

          // Check for both JSON structures
          const nodes = json.nodes || json.data.nodes;
          const edges = json.edges || json.data.edges;

          if (!nodes || !Array.isArray(nodes)) {
            throw new Error(
              "Invalid JSON structure: 'nodes' must be an array."
            );
          }

          if (!edges || !Array.isArray(edges)) {
            throw new Error(
              "Invalid JSON structure: 'edges' must be an array."
            );
          }

          this.nodes = nodes.map((node) => {
            const newNode = {
              ...node,
              data: {
                ...getNodeData(node.label),
                normalizedX: node.position.x,
                normalizedY: node.position.y,
              },
              position: {
                x: node.position.x * this.$refs.vueFlowContainer.offsetWidth,
                y: node.position.y * this.$refs.vueFlowContainer.offsetHeight,
              },
            };
            return newNode;
          });

          this.edges = edges.map((edge) => ({
            ...edge,
            animated: this.edgeProps.animated,
            style: this.edgeProps.style,
            color: this.edgeProps.color,

            markerEnd: { type: MarkerType.Arrow, width: 6, height: 6, color: "#000" },
          }));

          console.log("Nodes processed:", this.nodes);
          console.log("Edges processed:", this.edges);
        } catch (error) {
          console.error("Error parsing JSON:", error);
          alert(`Invalid JSON file: ${error.message}`);
        }
      };

      reader.readAsText(this.jsonFile);
    },
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
