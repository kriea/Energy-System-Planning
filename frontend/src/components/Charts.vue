<template>
  <Panel id="charts-container">
    <Chart
      ref="lineKey"
      type="line"
      :data="lineChartSet"
      :options="chartsDesignStore.lineChartOptions"
      class="h-[30rem]"
      style="height: 25vh; width: 45vw"
    />
    <Chart
      ref="barKey"
      type="bar"
      :data="barChartSet"
      :options="chartsDesignStore.barChartOptions"
      class="h-[30rem]"
      style="height: 25vh; width: 45vw"
    />
  </Panel>
</template>

<script>
import Chart from "primevue/chart";
import Panel from "primevue/panel";
import { ref, watch, onMounted, nextTick } from "vue";
import { usedLanguage, usedTheme } from "../assets/stores/pageSettings";
import { useDataStore } from "../assets/stores/dataValues";
import { useChartsDesignStore } from "../assets/stores/chartsDesign";
export default {
  props: {
    chartsData: {
      type: Object,
      required: true,
      default: () => {
        return {
          reset: false,
          chartsValues: null,
        };
      },
    },
    sliderVals: {
      type: Array,
      required: true,
      default: [0, 0],
    },
    dispatch: {
      type: String,
      required: false,
    },
    time: {
      type: String,
      required: false,
    },
    pv_prodcution: {
      type: String,
      required: false,
    },
    pv_curtailment: {
      type: String,
      required: false,
    },
    purchased_power: {
      type: String,
      required: false,
    },
    demand: {
      type: String,
      required: false,
    },
    storage_charge: {
      type: String,
      required: false,
    },
    storage_discharge: {
      type: String,
      required: false,
    },
  },
  setup(props) {
    const usedLang = usedLanguage();
    const dataStore = useDataStore();
    const currTheme = usedTheme();
    const chartsDesignStore = useChartsDesignStore();
    const barKey = ref(null);
    const lineKey = ref(null);
    const gridSize = ref(6);

    // Cache for storing chart data
    const chartsCache = ref(
      Array.from({ length: gridSize.value }, (_, rowIndex) =>
        Array.from({ length: gridSize.value }, () => null)
      )
    );
    // Data for line chart
    const lineChartSet = ref({
      labels: Array.from({ length: 0 }, (_, i) => i),
      datasets: [],
    });

    // Data for bar chart
    const barChartSet = ref({
      labels: Array.from({ length: 0 }, (_, i) => i),
      datasets: [],
    });

    /**
     * Initializes the charts.
     * Adds the corresponding label and with translation to the nodes.
     */
    const initCharts = () => {
      chartsCache.value = Array.from(
        { length: gridSize.value },
        (_, rowIndex) => Array.from({ length: gridSize.value }, () => null)
      );

      barChartSet.value.datasets = [];
      lineChartSet.value.datasets = [];
      Array.from(dataStore.nodeInfo)?.forEach((node, idx) => {
        if (node[1].type !== "junction") {
          barChartSet.value.datasets.push({
            label:
              node[1].type === "battery"
                ? usedLang.getCurrentLabelTranslation(node[1].label + " Supply")
                : usedLang.getCurrentLabelTranslation(node[1].label),
            id: node[0],
            backgroundColor:
              chartsDesignStore.colorValues.background[
                idx % chartsDesignStore.colorValues.background.length
              ],
            borderColor:
              chartsDesignStore.colorValues.border[
                idx % chartsDesignStore.colorValues.border.length
              ],
            borderWidth: 1,
            data: null,
          });
          if (
            node[1].type === "consumer" ||
            node[1].type === "battery" ||
            node[1].label === "Solar" ||
            node[1].label === "Wind"
          ) {
            barChartSet.value.datasets.push({
              label:
                node[1].type === "battery"
                  ? usedLang.getCurrentLabelTranslation(
                      node[1].label + " Demand"
                    )
                  : node[1].type === "consumer"
                  ? usedLang.getCurrentLabelTranslation(
                      node[1].label + " Non-Supplied Demand"
                    )
                  : node[1].label === "Solar" || node[1].label === "Wind"
                  ? usedLang.getCurrentLabelTranslation(
                      node[1].label + " Curtailment"
                    )
                  : "",
              id: parseInt(node[0]) + dataStore.nodeInfo.size, //1 Solar ,2 Coal ,3 Battery, 4 City || 5 (1 + 4) Solar Curtailment, 6 Coal Curtailment, 7 Battery Curtailment, 8 City Non Supplied Demand
              backgroundColor:
                chartsDesignStore.colorValues.background[
                  idx % chartsDesignStore.colorValues.background.length
                ],
              borderColor:
                chartsDesignStore.colorValues.border[
                  idx % chartsDesignStore.colorValues.border.length
                ],
              borderWidth: 1,
              data: null,
            });
          }
          if (node[1].type === "battery")
            lineChartSet.value.datasets.push({
              label: usedLang.getCurrentLabelTranslation(node[1].label),
              id: node[0],
              backgroundColor: "rgba(153, 102, 255, 0.2)",
              borderColor: "rgba(153, 102, 255, 1)",
              borderWidth: 1,
              data: null,
            });
        }
      });

      assignAllData(null);
    };

    /**
     * Updates the chart with values if two nodes have been selected.
     * Chart does not update if less than two nodes have been selected.
     * @param newVal Array containing values if two nodes have been selected.
     */
    function changeCharts(newVal) {
      console.log("Change Charts called!");

      if (newVal[0] === -1 || newVal[1] === -1) {
        assignAllData(null);
        chartsCache.value = Array.from(
          { length: gridSize.value },
          (_, rowIndex) => Array.from({ length: gridSize.value }, () => null)
        );
        return;
      }

      let rowID = dataStore.selectedNodes[1];
      let colID = dataStore.selectedNodes[0];
      const newChartsCache = Array.from({ length: gridSize.value }, () =>
        Array.from({ length: gridSize.value }, () => null)
      );

      dataStore.extractDataValuesCell(
        newChartsCache,
        dataStore.dataValues,
        colID,
        rowID,
        false,
        true
      );

      chartsCache.value = newChartsCache;
      assignAllData(
        chartsCache.value[
          dataStore.prodCapacities.get(dataStore.selectedNodes[1])
        ][dataStore.prodCapacities.get(dataStore.selectedNodes[0])]
      );
    }

    /**
     * Updates the values at a given timestep.
     * @param timestep Given timestep.
     */
    function updateTimestep(timestep) {
      lineChartSet.value.labels = Array.from({ length: timestep }, (_, i) => i);
      barChartSet.value.labels = Array.from({ length: timestep }, (_, i) => i);
    }

    /**
     * Updates the charts with new data after simulation.
     * @param newVal Object containing chart data and flags.
     */
    function assignAllData(newVal) {
      if (!newVal) return;

      updateTimestep(newVal.timestep);

      Array.from(dataStore.nodeInfo).forEach((node) => {
        if (node[1].type !== "junction") {
          const currentValues = newVal?.barChartData[node[0]];

          let idxOne = barChartSet.value.datasets.findIndex(
            (dataset) => dataset.id === node[0]
          ); //For Order 1 and -1 and Battery Supply

          const firstValues =
            node[1].type === "consumer"
              ? currentValues["-1"]
              : node[1].type === "producer" || node[1].type === "battery"
              ? currentValues["1"]
              : console.error("No valid node type");

          barChartSet.value.datasets[idxOne].data = firstValues.map(
            (el) => el.Value
          );

          if (
            node[1].type === "consumer" ||
            node[1].type === "battery" ||
            node[1].label === "Solar" ||
            node[1].label === "Wind"
          ) {
            let idxTwo = barChartSet.value.datasets.findIndex(
              (dataset) =>
                dataset.id === parseInt(node[0]) + dataStore.nodeInfo.size
            ); //For Order 100 and -100 and Battery Demand

            const secondValues =
              node[1].type === "consumer"
                ? currentValues["-100"]
                : node[1].type === "producer"
                ? currentValues["100"]
                : node[1].type === "battery"
                ? currentValues["-1"]
                : console.error("No valid node type");

            barChartSet.value.datasets[idxTwo].data = secondValues.map(
              (el) => el.Value
            );
          }
          if (node[1].type === "battery") {
            let idx = lineChartSet.value.datasets.findIndex(
              (dataset) => dataset.id === node[0]
            );
            lineChartSet.value.datasets[idx].data = newVal?.lineChartData[
              node[0]
            ].map((el) => el.Value);
          }
        }
      });
    }

    /**
     * Updates charts with new values.
     * Resets chart if reset flag is true.
     * @param newVal Object containing chart data and flags.
     */
    function handleChartsData(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        if (!newVal.reset) {
          const colIndex = props.sliderVals[0];
          const rowIndex = props.sliderVals[1];
          updateChart(newVal.chartsValues, colIndex, rowIndex);
        } else {
          resetCharts();
        }
      }
    }

    /**
     * Updates the chart with the current selected slider values.
     * @param newVal Value to be added based on the slider value combination.
     */
    function handleSliderVals(newVal) {
      const rowIndex = newVal[1];
      const colIndex = newVal[0];
      assignAllData(chartsCache.value[rowIndex][colIndex]);
    }

    /**
     * Updates the chart with new values in the corresponding column and row.
     * @param newVal Value to be inserted into the chart-
     * @param colIndex Column index.
     * @param rowIndex Row index.
     */
    function updateChart(newVal, colIndex, rowIndex) {
      chartsCache.value[rowIndex][colIndex] = newVal;
      assignAllData(newVal);
    }

    /**
     * Resets the chart.
     */
    function resetCharts() {
      assignAllData(null);
      chartsCache.value = Array.from({ length: gridSize.value }, () =>
        Array.from({ length: gridSize.value }, () => null)
      );
    }

    /**
     * Watcher to update charts when new data exist.
     */
    watch(
      () => props.chartsData,
      (newVal) => handleChartsData(newVal),
      { deep: true }
    );

    /**
     * Watcher to update slider values when new data exists.
     */
    watch(
      () => props.sliderVals,
      (newVal) => handleSliderVals(newVal),
      { deep: true }
    );

    /**
     * Watcher to update the chart based on selected nodes.
     */
    watch(
      () => dataStore.selectedNodes,
      (newVal) => changeCharts(newVal),
      {
        deep: true,
      }
    );

    /**
     * Watcher to update the charts language with the selected language.
     */
    watch(
      () => usedLang.currLang,
      () => {
        usedLang.updateChartLanguage(lineChartSet.value.datasets);
        usedLang.updateChartLanguage(barChartSet.value.datasets);
      }
    );

    /**
     * Watchter to update the chart's theme with the current selected theme.
     */
    watch(
      () => currTheme.currentTheme,
      async () => {
        chartsDesignStore.toggleChartTheme();
        chartsDesignStore.toggleChartTheme();
        await nextTick();
        barKey.value.chart.update();
        lineKey.value.chart.update();
      }
    );

    return {
      lineChartSet,
      barChartSet,
      chartsDesignStore,
      usedLang,
      initCharts,
      barKey,
      lineKey,
    };
  },
  components: {
    Chart,
    Panel,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
