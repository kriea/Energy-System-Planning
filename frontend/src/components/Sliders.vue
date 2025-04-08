<template>
  <Panel id="sliders" header="Sliders">
    <div id="only-sliders">
      <div id="only-sliders-for" v-for="(_, index) in sliderList" :key="index">
        <label id="slider-label">
          {{
            dataStore.selectedNodes[index] >= 0
              ? usedLang.getCurrentLabelTranslation(
                  dataStore.nodeInfo.get(dataStore.selectedNodes[index]).label
                )
              : ""
          }}
        </label>
        <Slider
          v-model="sliderList[index].value"
          :min="0"
          :max="5"
          :step="step"
          :disabled="isAutoSimulating || sliderList[index].nodeID === -1"
          class="w-56"
          :id="`slider${index}`"
          @change="(event) => startMoveOutline(event, index)"
          style="margin: 10px"
        ></Slider>
        <label id="slider-value">
          {{
            dataStore.selectedNodes[index] >= 0
              ? (
                  (sliderList[index].value / step / 5) *
                  dataStore.nodeInfo.get(dataStore.selectedNodes[index])?.max
                ).toString() +
                " " +
                dataStore.nodeInfo.get(dataStore.selectedNodes[index]).metric
              : ""
          }}
        </label>
      </div>
    </div>

    <div id="slider-buttons-container">
      <Button
        @click="postAndGet(true, false)"
        class="button"
        v-bind:label="usedLang.reset_text"
        :disabled="sliderList.some((node) => node.nodeID === -1)"
      ></Button>
      <Button
        @click="postAndGet(false, true)"
        class="button"
        v-bind:label="usedLang.auto"
        :disabled="
          isAutoSimulating || sliderList.some((node) => node.nodeID === -1)
        "
      >
      </Button>
      <Button
        @click="postAndGet(false, false)"
        class="button"
        v-bind:label="usedLang.simulate"
        :disabled="
          isAutoSimulating || sliderList.some((node) => node.nodeID === -1)
        "
      ></Button>
    </div>
  </Panel>
</template>

<script>
import Slider from "primevue/slider";
import Button from "primevue/button";
import Panel from "primevue/panel";
import axios from "axios";
import { ref, watch, inject } from "vue";
import { usedLanguage } from "../assets/stores/pageSettings";
import { useDataStore } from "../assets/stores/dataValues";
import { useScenarioStore } from "../assets/stores/scenarioStore";
import { backendURL } from "@/assets/urlExports";

export default {
  props: ["auto", "simulate", "reset_text"],
  setup(props, context) {
    const usedLang = usedLanguage(); // Get the current language settings
    const dataStore = useDataStore(); // Get the data store
    const url = backendURL + "api/save-slider-data/"; // API endpoint URL
    const scenarioStore = useScenarioStore(); // Get the scenario store

    let moveOutline = inject("moveOutline"); // Inject the moveOutline function
    let isAutoSimulating = inject("isAutoSimulating"); // Inject the isAutoSimulating flag

    const step = ref(1); // Step value for the sliders
    const sliderList = ref([
      { nodeID: -1, value: 0 },
      { nodeID: -1, value: 0 },
    ]); // List of sliders with node IDs and values

    // Function to send POST request and get simulation data
    async function postAndGet(reset, autoSimulate) {
      // Update the prodCapacities in dataStore
      sliderList.value.forEach((slider) => {
        if (autoSimulate) {
          dataStore.prodCapacities.set(slider.nodeID, 0);
        } else {
          dataStore.prodCapacities.set(slider.nodeID, slider.value);
        }
      });

      try {
        // Prepare the data to be sent
        const data = {
          nodes: scenarioStore.nodes,
          edges: scenarioStore.edges,
          sliderData: {
            reset: reset,
            autoSimulate: autoSimulate,
            prodCapacities: Array.from(dataStore.prodCapacities),
            sliderVals: sliderList.value,
          },
        };

        //turn ProgressSpinner on, if we autoSimulate
        dataStore.currentlyLoading = autoSimulate;

        // Send POST request and wait for the response
        const response = await axios.post(url, data, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        // Handle the response
        if (response && response.data) {
          const simData = response.data;

          const sliderVals = sliderList.value.map((slider) => {
            return slider.value;
          });

          const propagateChange = {
            simData: simData.mainData,
            reset: reset,
            autoSimulate: autoSimulate,
            sliderVals: sliderVals,
            bestIdx: simData.bestIdx,
          };
          // Emit the simulation data to parent component
          context.emit("getSimulationData", propagateChange);
        }
      } catch (error) {
        console.error("Error sending data to backend:", error);
        throw error;
      }
    }

    // Function to start moving the outline
    function startMoveOutline(event, index) {
      if (!isAutoSimulating.value) {
        moveOutline(event, index);
      }
    }

    // Function to change sliders based on selected nodes
    function changeSliders(newVal) {
      sliderList.value.forEach((slider, idx) => {
        slider.nodeID = newVal[idx];
        slider.value = dataStore.prodCapacities.has(
          dataStore.selectedNodes[idx]
        )
          ? dataStore.prodCapacities.get(dataStore.selectedNodes[idx])
          : 0;
      });
    }

    // Watch for changes in selectedNodes in dataStore
    watch(
      () => dataStore.selectedNodes,
      (newVal) => changeSliders(newVal),
      {
        deep: true,
      }
    );

    return {
      usedLang,
      sliderList,
      step,
      postAndGet,
      startMoveOutline,
      isAutoSimulating,
      dataStore,
    };
  },
  components: {
    Slider,
    Panel,
    Button,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
