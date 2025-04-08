<template>
  <div id="drawerbox">
    <Drawerbox></Drawerbox>
  </div>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <Playfield @keydown.stop></Playfield>
      </div>
      <div id="slider-box">
        <Sliders @getSimulationData="handleSimulationData"> </Sliders>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="matrix-box" class="grid-column">
        <Matrix
          ref="matrixComp"
          :matrixData="matrixData"
          :matrixTheme="currTheme.matrixTheme"
          :sliderVals="sliderVals"
        ></Matrix>
      </div>
      <div id="charts-box" class="grid-column">
        <Charts
          ref="chartsComp"
          :chartsData="chartsData"
          :sliderVals="sliderVals"
        ></Charts>
      </div>
    </div>
    <div
      v-if="dataStore.currentlyLoading"
      style="
        position: absolute;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
      "
    >
      <ProgressSpinner />
    </div>
  </div>
</template>

<script>
import {
  ref,
  provide,
  onMounted,
  onUnmounted,
  useTemplateRef,
} from "vue";
import Chart from "primevue/chart";
import ProgressSpinner from "primevue/progressspinner";
import Sliders from "../components/Sliders.vue";
import Playfield from "../components/PlayfieldStudent.vue";
import Matrix from "../components/Matrix.vue";
import Charts from "../components/Charts.vue";
import Drawerbox from "../components/Drawerbox.vue";
import { usedTheme } from "../assets/stores/pageSettings";
import { useDataStore } from "../assets/stores/dataValues";

export default {
  setup(props, context) {
    // Disable keyboard input to prevent unwanted interactions
    const disableKeyboardInput = (e) => {
      e.preventDefault();
      e.stopPropagation();
    };

    onMounted(() => {
      // Add event listeners to disable keyboard input on mount
      window.addEventListener("keydown", disableKeyboardInput);
      window.addEventListener("keypress", disableKeyboardInput);
      window.addEventListener("keyup", disableKeyboardInput);
    });

    // Remove event listeners on unmount
    onUnmounted(() => {
      window.removeEventListener("keydown", disableKeyboardInput);
      window.removeEventListener("keypress", disableKeyboardInput);
      window.removeEventListener("keyup", disableKeyboardInput);
    });

    const first = ref(true);
    const currTheme = usedTheme();

    const dataStore = useDataStore();

    const sliderVals = ref([0, 0]);
    const matrixData = ref(undefined);
    const chartsData = ref(undefined);

    const isAutoSimulating = ref(false);
    const stopAutoSimulate = ref(false);
    const newScenarioLoaded = ref(false);

    const matrixComp = useTemplateRef("matrixComp");
    const chartsComp = useTemplateRef("chartsComp");

    let numberProducers = 0;
    let numberConsumers = 0;

    provide("isAutoSimulating", isAutoSimulating);
    provide("newScenarioLoaded", newScenarioLoaded);
    provide("sliderVals", sliderVals);

    const matrixTheme = ref({ backgroundColor: "white", gridColor: "black" });

    // Handle simulation data received from the Sliders component
    function handleSimulationData(propagateChange) {
      if (
        dataStore.selectedNodes[0] === -1 ||
        dataStore.selectedNodes[1] === -1
      )
        return;

      if (propagateChange.reset) {
        if (isAutoSimulating.value) {
          stopAutoSimulate.value = true;
          isAutoSimulating.value = false;
        }
        prepareNewScenario(numberProducers, numberConsumers);
        console.log(isAutoSimulating);
      } else {
        if (!isAutoSimulating.value) {
          if (propagateChange.autoSimulate) {
            dataStore.currentlyLoading = false;
            isAutoSimulating.value = true;
            //dataStore.dataValues = propagateChange.simData;
            dataStore.insertDataValuesCell(
              propagateChange.simData,
              dataStore.dataValues
            );
            console.log(dataStore.dataValues);
            autoSimulateData(propagateChange);
          } else {
            dataStore.updateDataValuesCell(
              dataStore.dataValues,
              propagateChange
            );
            simulateData(propagateChange, propagateChange.sliderVals);
          }
        }
      }
    }

    // Automatically simulate data
    async function autoSimulateData(propagateChange) {
      const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

      const bestIdxMap = new Map(propagateChange.bestIdx);
      for (const [key, _] of dataStore.prodCapacities) {
        if (dataStore.selectedNodes.some((el) => el === key)) {
          dataStore.prodCapacities.set(key, 0);
        }
      }

      for (let rowIndex = 0; rowIndex < 6; rowIndex++) {
        for (let colIndex = 0; colIndex < 6; colIndex++) {
          if (stopAutoSimulate.value) {
            stopAutoSimulate.value = false;
            return;
          }
          //Extract desired values from propagateChange.simData or dataValues
          dataStore.prodCapacities.set(dataStore.selectedNodes[1], rowIndex);
          dataStore.prodCapacities.set(dataStore.selectedNodes[0], colIndex);
          let currentSliderVals = [colIndex, rowIndex];
          let cell = {
            simData: propagateChange.simData[colIndex][rowIndex],
            reset: propagateChange.reset,
            autoSimulate: propagateChange.autoSimulate,
            sliderVals: propagateChange.sliderVals,
            bestIdx: propagateChange.bestIdx,
          };
          simulateData(cell, currentSliderVals);
          await sleep(100);
        }
      }
      processBestIndex(bestIdxMap);
      isAutoSimulating.value = false;
    }

    // Process the best index for simulation
    function processBestIndex(bestIdxMap) {
      dataStore.prodCapacities.set(
        dataStore.selectedNodes[0],
        bestIdxMap.get(dataStore.selectedNodes[0])
      );
      dataStore.prodCapacities.set(
        dataStore.selectedNodes[1],
        bestIdxMap.get(dataStore.selectedNodes[1])
      );
      sliderVals.value = [
        bestIdxMap.get(dataStore.selectedNodes[0]),
        bestIdxMap.get(dataStore.selectedNodes[1]),
      ];
    }

    // Simulate data based on the provided change
    function simulateData(propagateChange, currentSliderVals) {
      sliderVals.value = currentSliderVals;
      matrixData.value = {
        reset: propagateChange.reset,
        matrixValue: propagateChange.simData.matrixData,
      };
      chartsData.value = {
        reset: propagateChange.reset,
        chartsValues: propagateChange.simData.chartsData,
      };
    }

    // Handle node selection
    function handleNodeSelection(newNode) {
      if (!isAutoSimulating.value) {
        //LIFO-wise selection -> 0 first, 1 subsequently
        const idx = dataStore.selectedNodes.findIndex((el) => {
          return el === newNode;
        });
        //if idx >= 0, that means that the node is supposed to be de-highlighted (shifted with idx = 0, popped with idx = 1). Otherwise, it is going to be highlighted (pushed)
        if (idx >= 0) {
          idx === 0
            ? (dataStore.selectedNodes = [dataStore.selectedNodes[1], -1])
            : (dataStore.selectedNodes = [dataStore.selectedNodes[0], -1]);
        } else {
          if (dataStore.selectedNodes[0] === -1) {
            dataStore.selectedNodes = [newNode, -1];
          } else {
            dataStore.selectedNodes = [dataStore.selectedNodes[0], newNode];
          }
        }
      }
    }
    provide("handleNodeSelection", handleNodeSelection);

    // Move the outline based on the new value
    function moveOutline(newVal, idx) {
      dataStore.prodCapacities.set(dataStore.selectedNodes[idx], newVal);
      sliderVals.value[idx] = newVal;
    }
    provide("moveOutline", moveOutline);

    // Prepare a new scenario
    function prepareNewScenario() {
      dataStore.selectedNodes = [-1, -1];

      matrixComp.value?.initMatrix();
      chartsComp.value?.initCharts();

      const initializeNDarray = (nProds) => {
        return nProds === 0
          ? { matrixData: null, chartsData: null }
          : Array.from({ length: 6 }, () => initializeNDarray(nProds - 1));
      };

      dataStore.dataValues = initializeNDarray(dataStore.prodCapacities.size);
    }

    provide("prepareNewScenario", prepareNewScenario);

    return {
      handleSimulationData,
      matrixTheme,
      sliderVals,
      matrixData,
      chartsData,
      currTheme,
      handleNodeSelection,
      dataStore,
      first,
    };
  },
  components: {
    Sliders,
    Chart,
    Playfield,
    Matrix,
    Charts,
    Drawerbox,
    ProgressSpinner,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
