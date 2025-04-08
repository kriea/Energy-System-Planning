import { defineStore } from "pinia";
import { ref } from "vue";
import { useDataStore } from "./dataValues";
import { usedTheme, usedLanguage } from "./pageSettings";

// Define a store for matrix design settings
export const useMatrixDesignStore = defineStore("useMatrixDesignStore", () => {
  // State variables
  const outLinePosition = ref(null); // Position of the outline
  const layout = ref(null); // Layout configuration for the heatmap
  const gridSize = ref(6); // Size of the grid
  const gridColor = ref("black"); // Color of the grid lines
  const gridLines = ref([]); // Array to store grid lines
  const axisDimension = ref(Array.from({ length: 6 }, (_, i) => i)); // Axis dimensions
  const currTheme = usedTheme(); // Current theme
  const usedLang = usedLanguage(); // Current language

  const dataStore = useDataStore(); // Data store

  // Function to initialize the heatmap
  function initHeatmap() {
    var currentLineColor =
      currTheme.currentTheme === "DARK" ? "white" : "black";
    var currentGridColor =
      currTheme.currentTheme === "DARK" ? "white" : "black";
    var currentHeatMapBGColor =
      currTheme.currentTheme === "DARK" ? "rgb(39, 39, 39)" : "white";
    for (let i = 0; i <= gridSize.value; i++) {
      // Horizontal lines
      gridLines.value.push({
        type: "line",
        x0: -0.5,
        x1: gridSize.value - 0.5,
        y0: i - 0.5,
        y1: i - 0.5,
        line: {
          color: currentLineColor,
          width: 1,
        },
      });

      // Vertical lines
      gridLines.value.push({
        type: "line",
        x0: i - 0.5,
        x1: i - 0.5,
        y0: -0.5,
        y1: gridSize.value - 0.5,
        line: {
          color: currentLineColor,
          width: 1,
        },
      });
    }

    layout.value = {
      coloraxis: {
        colorbar: {
          title: "Colorbar Title", // Title for the colorbar
          tickfont: {
            color: "blue", // Change the label color to blue
          },
        },
      },
      margin: {
        l: 80,

        r: 50,

        b: 50,

        t: 50,
      },
      xaxis: {
        title: {
          text: "",
        },
        range: [-0.55, gridSize.value - 0.45], // -0.5 to 5.5 in order to display the cells with their axis values centered
        tickmode: "array",
        ticks: "", //for the - at the numbers at the axis baselines
        color: currentGridColor,
        showgrid: false, //for the grid lines inside the coordinate system
        zeroline: false, //for the baseline of an x axis (the thick one)
        fixedrange: true,
        tickvals: Array.from({ length: 6 }, (_, i) => i), //values where the ticks should be located
        ticktext: Array.from({ length: 6 }, () => ""),
      },
      yaxis: {
        title: {
          text: "",
        },
        range: [-0.55, gridSize.value - 0.45], //-0.5 to 5.5 in order to display the cells with their axis values centered
        tickmode: "array",
        ticks: "", //for the - at the numbers at the axis baselines
        color: currentGridColor,
        showgrid: false, //for the grid lines inside the coordinate system
        zeroline: false, //for the baseline of an x axis (the thick one)
        fixedrange: true,
        tickvals: Array.from({ length: 6 }, (_, i) => i), //values where the ticks should be located
        ticktext: Array.from({ length: 6 }, () => ""),
      },
      paper_bgcolor: currentHeatMapBGColor, // Background color outside the plotting area
      plot_bgcolor: currentHeatMapBGColor,
      shapes: [
        ...gridLines.value,
        {
          type: "rect",
          x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
          x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
          y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
          y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
          xref: "x",
          yref: "y",
          line: {
            color: "green", // Outline color
            width: 3, // Outline width
          },
          fillcolor: "rgba(0,0,0,0)", // Transparent fill
        },
      ],
    };
  }

  // Function to update matrix labels
  function updateMatrixLabels() {
    var currentThemeMode =
      currTheme.currentTheme === "DARK" ? "white" : "black";
    const prodCapacitiesKeys = Array.from(dataStore.prodCapacities.keys());

    const hasFirstNode = prodCapacitiesKeys.some(
      (el) => el === dataStore.selectedNodes[0]
    );
    const hasSecondNode = prodCapacitiesKeys.some(
      (el) => el === dataStore.selectedNodes[1]
    );

    const newLayout = {
      ...layout.value,
      xaxis: {
        title: {
          text: hasFirstNode
            ? usedLang.getCurrentLabelTranslation(
                dataStore.nodeInfo.get(dataStore.selectedNodes[0]).label
              ) +
              ` (${dataStore.nodeInfo.get(dataStore.selectedNodes[0]).metric})`
            : "",
        },
        range: [-0.55, gridSize.value - 0.45], // -0.5 to 5.5 in order to display the cells with their axis values centered
        tickmode: "array",
        ticks: "", // for the - at the numbers at the axis baselines
        color: currentThemeMode,
        showgrid: false, // for the grid lines inside the coordinate system
        zeroline: false, // for the baseline of an x axis (the thick one)
        fixedrange: true,
        tickvals: Array.from({ length: 6 }, (_, i) => i),
        ticktext: hasFirstNode
          ? Array.from(
              { length: 6 },
              (_, i) =>
                (i / 5) * dataStore.nodeInfo.get(dataStore.selectedNodes[0]).max
            )
          : Array.from({ length: 6 }, () => ""),
      },
      yaxis: {
        title: {
          text: hasSecondNode
            ? usedLang.getCurrentLabelTranslation(
                dataStore.nodeInfo.get(dataStore.selectedNodes[1]).label
              ) +
              ` (${dataStore.nodeInfo.get(dataStore.selectedNodes[1]).metric})`
            : "",
        },
        range: [-0.55, gridSize.value - 0.45], //-0.5 to 5.5 in order to display the cells with their axis values centered
        tickmode: "array",
        ticks: "", //for the - at the numbers at the axis baselines
        color: currentThemeMode,
        showgrid: false, //for the grid lines inside the coordinate system
        zeroline: false, //for the baseline of an x axis (the thick one)
        fixedrange: true,
        tickvals: Array.from({ length: 6 }, (_, i) => i), //values where the ticks should be located
        ticktext: hasSecondNode
          ? Array.from(
              { length: 6 },
              (_, i) =>
                (i / 5) * dataStore.nodeInfo.get(dataStore.selectedNodes[1]).max
            )
          : Array.from({ length: 6 }, () => ""),
      },
    };
    layout.value = newLayout;
  }

  // Function to handle slider values
  function handleSliderVals(newVal) {
    outLinePosition.value = newVal;
    layout.value = {
      ...layout.value,
      shapes: [
        ...gridLines.value,
        {
          type: "rect",
          x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
          x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
          y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
          y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
          xref: "x",
          yref: "y",
          line: {
            color: "green",
            width: 3,
          },
          fillcolor: "rgba(0,0,0,0)",
        },
      ],
    };
  }

  // Function to handle matrix theme
  function handleMatrixTheme(newVal) {
    gridColor.value = newVal.gridColor;
    gridLines.value = [];
    for (let i = 0; i <= gridSize.value; i++) {
      // Horizontal lines
      gridLines.value.push({
        type: "line",
        x0: -0.5,
        x1: gridSize.value - 0.5,
        y0: i - 0.5,
        y1: i - 0.5,
        line: {
          color: newVal.gridColor,
          width: 1,
        },
      });

      // Vertical lines
      gridLines.value.push({
        type: "line",
        x0: i - 0.5,
        x1: i - 0.5,
        y0: -0.5,
        y1: gridSize.value - 0.5,
        line: {
          color: newVal.gridColor,
          width: 1,
        },
      });
    }
    layout.value = {
      ...layout.value,
      paper_bgcolor: newVal.backgroundColor,
      plot_bgcolor: newVal.backgroundColor,
      xaxis: {
        title: {
          text: "",
        },
        range: [-0.55, gridSize.value - 0.45],
        tickmode: "array",
        ticks: "",
        color: newVal.gridColor,
        showgrid: false,
        zeroline: false,
        fixedrange: true,
        tickvals: [0, 1, 2, 3, 4, 5],
      },
      yaxis: {
        title: {
          text: "",
        },
        range: [-0.55, gridSize.value - 0.45], //-0.5 to 5.5 in order to display the cells with their axis values centered
        tickmode: "array",
        ticks: "", //for the - at the numbers at the axis baselines
        color: newVal.gridColor,
        showgrid: false, //for the grid lines inside the coordinate system
        zeroline: false, //for the baseline of an x axis (the thick one)
        fixedrange: true,
        tickvals: [0, 1, 2, 3, 4, 5], //values where the ticks should be located
      },
      shapes: [
        ...gridLines.value,
        {
          type: "rect",
          x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
          x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
          y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
          y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
          xref: "x",
          yref: "y",
          line: {
            color: "green",
            width: 3,
          },
          fillcolor: "rgba(0,0,0,0)",
        },
      ],
    };
  }

  // Return the state variables and functions
  return {
    layout,
    outLinePosition,
    axisDimension,
    gridSize,
    initHeatmap,
    handleSliderVals,
    handleMatrixTheme,
    updateMatrixLabels,
  };
});
