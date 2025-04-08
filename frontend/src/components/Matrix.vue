<template>
  <Panel id="matrix-container" :header="null">
    <div id="label-container">
      <label class="custom-label" :class="{
        selectedFirst: dataStore.isSelectedFirst(key),
        selectedSecond: dataStore.isSelectedSecond(key),
      }" v-for="[key, value] in Array.from(dataStore.prodCapacities)" :key="key">
        <img width="2rem" height="2rem" style="width: 2rem; height: 2rem;"
          :src="getNodeIcon(dataStore.nodeInfo.get(key).label)"></img>
        <label id="slider-value"></label>
        {{ usedLang.getCurrentLabelTranslation(dataStore.nodeInfo.get(key).label) }}: {{ (value / 5) *
          dataStore.nodeInfo.get(key).max }}
      </label>
    </div>
    <VuePlotly :data="[
      {
        z: z,
        x: matrixDesignStore.axisDimension,
        y: matrixDesignStore.axisDimension,
        type: 'heatmap',
        text:
          z !== null
            ? z.map((row) => row.map((cell) => (cell === null ? '-' : cell === 9999 ? 'Infinite' : cell)))
            : z,
        texttemplate: '%{text}',
        hoverongaps: false,
        colorscale: 'RdBu',
        zmin: 0,
        zmax: 1,
        colorbar: {
          tickfont: {
            color: currTheme.currentTheme === 'DARK' ? 'white' : 'black'
          }
        }
      },
    ]" :layout="matrixDesignStore.layout" :display-mode-bar="true" :config="{
        displayModeBar: false,
      }" class="matrix-plotly"></VuePlotly>
  </Panel>
</template>

<script>
import { Panel } from "primevue";
import { ref, watch, onMounted } from "vue";
import { VuePlotly } from "vue3-plotly";
import { useDataStore } from "../assets/stores/dataValues";
import { usedLanguage, usedTheme } from "@/assets/stores/pageSettings";
import { useMatrixDesignStore } from "../assets/stores/matrixDesign";
import { getNodeIcon } from "@/utils/nodeUtils";

export default {
  props: {
    matrixData: {
      type: Object,
      required: false,
      default: () => {
        return {
          reset: false,
          matrixValue: null,
        };
      },
    },
    matrixTheme: {
      type: Object,
      required: false,
      default: { backgroundColor: "white", gridColor: "black" },
    },
    sliderVals: {
      type: Array,
      required: false,
      default: [0, 0],
    },
  },
  setup(props) {
    const usedLang = usedLanguage();
    const dataStore = useDataStore();
    const currTheme = usedTheme();
    const matrixDesignStore = useMatrixDesignStore();
    const z = ref(null);

    /**
     * Updates the heatmap with the calculated values corresponding to the row and column given.
     * If the value equals 9999, then the string "inf" is inserted into the cell instead of a value.
     * @param newVal Value to be inserted.
     * @param colIndex Column index.
     * @param rowIndex Row index.
     */
    function updateHeatmap(newVal, colIndex, rowIndex) {
      z.value[rowIndex][colIndex] = newVal === "inf" ? 9999 : newVal;
    }

    // Initialize the matrix with default values
    const initMatrix = () => {
      z.value = Array.from({ length: matrixDesignStore.gridSize }, () =>
        Array.from({ length: matrixDesignStore.gridSize }, () => null)
      );
    };

    // On component mount, initialize the matrix and heatmap
    onMounted(() => {
      z.value = Array.from(
        { length: matrixDesignStore.gridSize },
        (_, rowIndex) =>
          Array.from({ length: matrixDesignStore.gridSize }, () => null)
      );
      matrixDesignStore.outLinePosition = props.sliderVals;
      matrixDesignStore.initHeatmap();
    });

    /**
     * Updates the matrix value and labels based on the selected nodes.
     * @param newVal Selected nodes.
     */
    function changeMatrix(newVal) {
      if (newVal[0] === -1 || newVal[1] === -1) {
        z.value = Array.from({ length: matrixDesignStore.gridSize }, () =>
          Array.from({ length: matrixDesignStore.gridSize }, () => null)
        );
        matrixDesignStore.updateMatrixLabels()
        return;
      }

      let rowID = dataStore.selectedNodes[1];
      let colID = dataStore.selectedNodes[0];
      const newZ = Array.from({ length: matrixDesignStore.gridSize }, () =>
        Array.from({ length: matrixDesignStore.gridSize }, () => null)
      );

      dataStore.extractDataValuesCell(
        newZ,
        dataStore.dataValues,
        colID,
        rowID,
        true,
        false
      );

      z.value = newZ.map((row) => row.map((cell) => cell === "inf" ? 9999 : cell));

      matrixDesignStore.updateMatrixLabels()


      matrixDesignStore.handleSliderVals([
        dataStore.prodCapacities.get(dataStore.selectedNodes[0]),
        dataStore.prodCapacities.get(dataStore.selectedNodes[1]),
      ]);
    }

    /**
     * Updates the matrix with the given values based on the given indicies.
     * @param newVal New data to be added.
     */
    function handleMatrixData(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        if (!newVal.reset) {
          const colIndex = props.sliderVals[0];
          const rowIndex = props.sliderVals[1];
          updateHeatmap(newVal.matrixValue, colIndex, rowIndex);
        } else {
          initMatrix();
        }
      } else {
        console.error("Not good, matrix is not receiving data");
      }
    }

    /**
     * Watcher that updates the matrix, when new data exists.
     */
    watch(
      () => props.matrixData,
      (newVal) => handleMatrixData(newVal),
      { deep: true }
    );

    /**
     * Watcher that updates the slider values, when new data exists.
     */
    watch(
      () => props.sliderVals,
      (newVal) => matrixDesignStore.handleSliderVals(newVal),
      { deep: true }
    );

    /**
     * Watcher that updates the matrix theme, when a new theme is selected.
     */
    watch(
      () => props.matrixTheme,
      (newVal) => {
        matrixDesignStore.handleMatrixTheme(newVal);
        matrixDesignStore.updateMatrixLabels(true);
      },
      { deep: true }
    );

    /**
     * Watcher that updates the matrix with new values based on nodes selected.
     */
    watch(
      () => dataStore.selectedNodes,
      (newVal) => changeMatrix(newVal),
      {
        deep: true,
      }
    );

    /**
     * Watcher that updates the current language of the labels of the matrix.
     */
    watch(
      () => usedLang.currLang,
      () => {
        if (dataStore.selectedNodes[0] === -1 || dataStore.selectedNodes[1] === -1) {
          matrixDesignStore.updateMatrixLabels(false)
        } else {
          matrixDesignStore.updateMatrixLabels(true)
        }
      }
    )

    return {
      z,
      initMatrix,
      matrixDesignStore,
      dataStore,
      getNodeIcon,
      usedLang,
      currTheme
    };
  },
  components: {
    Panel,
    VuePlotly,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
