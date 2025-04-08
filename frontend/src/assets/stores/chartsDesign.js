import { defineStore } from "pinia";
import { ref, shallowRef } from "vue";
import { usedTheme } from "./pageSettings";

// Define a store for chart design settings
export const useChartsDesignStore = defineStore("useChartsDesignStore", () => {
  // Get the current theme
  const currTheme = usedTheme();
    // Set grid and label colors based on the current theme

  let gridColor =
    currTheme.currentTheme === "DARK" ? "rgba(255,255,255,0.2)" : "lightgrey";
  let labelColor = currTheme.currentTheme === "DARK" ? "white" : "black";
  
  // Define options for bar charts
  const barChartOptions = shallowRef({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "bottom",
        labels: {
          color: labelColor,
        },
      },
    },
    scales: {
      x: {
        display: true,
        stacked: true,
        grid: {
          color: gridColor,
        },
        ticks: {
          color: labelColor,
        },
      },
      y: {
        display: true,
        stacked: true,
        grid: {
          color: gridColor,
        },
        ticks: {
          color: labelColor,
        },
        title: {
          display: true,
          text: "in kW",
          color: labelColor,
        },
      },
    },
  });

  // Define options for line charts
  const lineChartOptions = shallowRef({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "bottom",
        labels: {
          color: labelColor,
        },
      },
    },
    scales: {
      x: {
        display: true,
        grid: {
          color: gridColor,
        },
        ticks: {
          color: labelColor,
        },
      },
      y: {
        display: true,
        grid: {
          color: gridColor,
        },
        ticks: {
          color: labelColor,
        },
        title: {
          display: true,
          text: "in kWh",
          color: labelColor,
        },
      },
    },
  });

  // Define color values for chart elements
  const colorValues = shallowRef({
    background: [
      "rgba(153, 102, 255, 0.2)",
      "rgba(75, 192, 192, 0.2)",
      "rgba(255, 99, 132, 0.2)",
      "rgba(34, 139, 34, 0.2)",
      "rgba(255, 255, 0, 0.2)",
      "rgba(255, 165, 0, 0.2)",
      "rgba(138, 43, 226, 0.2)",
    ],
    border: [
      "rgba(153, 102, 255, 1)",
      "rgba(75, 192, 192, 1)",
      "rgba(255, 99, 132, 1)",
      "rgba(34, 139, 34, 1)",
      "rgba(204, 204, 0, 1)",
      "rgba(255, 140, 0, 1)",
      "rgba(75, 0, 130, 1)",
    ],
  });

  // Function to toggle chart theme
  function toggleChartTheme() {
    let gridColor =
      currTheme.currentTheme === "DARK" ? "rgba(255,255,255,0.2)" : "lightgrey";
    let labelColor = currTheme.currentTheme === "DARK" ? "white" : "black";
    barChartOptions.value.plugins.legend.labels.color = labelColor;
    barChartOptions.value.scales.x.grid.color = gridColor;
    barChartOptions.value.scales.y.grid.color = gridColor;
    barChartOptions.value.scales.x.ticks.color = labelColor;
    barChartOptions.value.scales.y.ticks.color = labelColor;
    barChartOptions.value.scales.y.title.color = labelColor;
    lineChartOptions.value.plugins.legend.labels.color = labelColor;
    lineChartOptions.value.scales.y.grid.color = gridColor;
    lineChartOptions.value.scales.x.grid.color = gridColor;
    lineChartOptions.value.scales.x.ticks.color = labelColor;
    lineChartOptions.value.scales.y.ticks.color = labelColor;
    lineChartOptions.value.scales.y.title.color = labelColor;
  }
  // Return the chart options and toggle function
  return { lineChartOptions, barChartOptions, colorValues, toggleChartTheme };
});
