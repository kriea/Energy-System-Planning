import { defineStore } from "pinia";
import { ref, shallowRef } from "vue";

// Define a store for data values
export const useDataStore = defineStore("useDataStore", () => {
  // State variables
  const selectedNodes = ref([-1, -1]); // Array to store selected node IDs
  const dataValues = ref(null); // Data values
  const prodCapacities = shallowRef(new Map()); // Map to store production capacities
  const nodeInfo = shallowRef(new Map()); // Map to store node information
  const maxInstalledCapacity = shallowRef(
    new Map([
      ["Solar", 300],
      ["Wind", 8000],
      ["Gas", 10000],
      ["Coal", 10000],
      ["Battery", 10000],
    ])
  );
  // Map to store maximum installed capacities for different technologies
  const currentlyLoading = ref(false); // Flag to indicate if data is currently loading

  // Function to check if a node is selected as the first node
  const isSelectedFirst = (nodeID) => {
    return selectedNodes.value ? selectedNodes.value[0] === nodeID : false;
  };
  // Function to check if a node is selected as the second node
  const isSelectedSecond = (nodeID) => {
    return selectedNodes.value ? selectedNodes.value[1] === nodeID : false;
  };

  // Function to get data values for a specific cell
  function getDataValuesCell(pointer) {
    const prodCapacitiesArr = Array.from(prodCapacities.value);
    for (let i = 0; i < prodCapacitiesArr.length; i++) {
      if (i === prodCapacitiesArr.length - 1) {
        return pointer[prodCapacitiesArr[i][1]];
      }

      if (!pointer) {
        console.error("prodCapacities length is not equal to dataValues depth");
        throw new Error(
          "prodCapacities length is not equal to dataValues depth"
        );
      }

      pointer = pointer[prodCapacitiesArr[i][1]];
    }
  }

  // Function to insert data values into a specific cell
  function insertDataValuesCell(valueMatrix, pointer) {
    const colID = selectedNodes.value[0];
    const rowID = selectedNodes.value[1];

    const insertInDataStructure = (value, pointer) => {
      const prodCapacitiesArr = Array.from(prodCapacities.value);

      const recInsertInDataStructure = (value, pointer, rec_depth) => {
        if (rec_depth === prodCapacitiesArr.length - 1) {
          pointer[prodCapacitiesArr[rec_depth][1]] = value;
        } else {
          recInsertInDataStructure(
            value,
            pointer[prodCapacitiesArr[rec_depth][1]],
            rec_depth + 1
          );
        }
      };

      recInsertInDataStructure(value, pointer, 0);
    };

    for (let col = 0; col < 6; col++) {
      prodCapacities.value.set(colID, col);
      for (let row = 0; row < 6; row++) {
        prodCapacities.value.set(rowID, row);
        let value = valueMatrix[col][row];
        insertInDataStructure(value, pointer);
      }
    }
  }

  // Function to extract data values from a specific cell
  function extractDataValuesCell(
    matrixToWhichIsAssigned,
    pointer,
    colID,
    rowID,
    forMatrix,
    forCharts
  ) {
    const prodCapacitiesArr = Array.from(prodCapacities.value);
    function recExtractDataValuesCell(pointer, rec_depth, colIndex, rowIndex) {
      if (rec_depth == prodCapacitiesArr.length) {
        return forMatrix
          ? pointer.matrixData
          : forCharts
          ? pointer.chartsData
          : console.error("data cannot be assigned to visualization component");
      } else {
        if (
          selectedNodes.value.some(
            (el) => el === prodCapacitiesArr[rec_depth][0]
          )
        ) {
          if (prodCapacitiesArr[rec_depth][0] == colID) {
            for (let currColIndex = 0; currColIndex <= 5; currColIndex++) {
              let tmp = recExtractDataValuesCell(
                pointer[currColIndex],
                rec_depth + 1,
                currColIndex,
                rowIndex
              );
              matrixToWhichIsAssigned[rowIndex][currColIndex] =
                tmp !== null && tmp !== undefined
                  ? tmp
                  : matrixToWhichIsAssigned[rowIndex][currColIndex];
            }
          } else if (prodCapacitiesArr[rec_depth][0] == rowID) {
            for (let currRowIndex = 0; currRowIndex <= 5; currRowIndex++) {
              let tmp = recExtractDataValuesCell(
                pointer[currRowIndex],
                rec_depth + 1,
                colIndex,
                currRowIndex
              );
              matrixToWhichIsAssigned[currRowIndex][colIndex] =
                tmp !== null && tmp !== undefined
                  ? tmp
                  : matrixToWhichIsAssigned[currRowIndex][colIndex];
            }
          } else {
            console.error("rec_depth does not equal any selected node ID");
          }
        } else {
          return recExtractDataValuesCell(
            pointer[prodCapacitiesArr[rec_depth][1]],
            rec_depth + 1,
            colIndex,
            rowIndex
          );
        }
      }
    }

    return recExtractDataValuesCell(pointer, 0, 0, 0);
  }

  // Function to update data values in a specific cell
  function updateDataValuesCell(pointer, propagateChange) {
    const prodCapacitiesArr = Array.from(prodCapacities.value);
    for (let i = 0; i < prodCapacitiesArr.length; i++) {
      if (i === prodCapacitiesArr.length - 1) {
        pointer[prodCapacitiesArr[i][1]] = propagateChange.simData;

        return;
      }

      if (!pointer) {
        console.error("prodCapacities length is not equal to dataValues depth");
        throw new Error(
          "prodCapacities length is not equal to dataValues depth"
        );
      }

      pointer = pointer[prodCapacitiesArr[i][1]];
    }
  }

  // Return the state variables and functions
  return {
    dataValues,
    prodCapacities,
    selectedNodes,
    nodeInfo,
    maxInstalledCapacity,
    currentlyLoading,
    isSelectedFirst,
    isSelectedSecond,
    getDataValuesCell,
    updateDataValuesCell,
    extractDataValuesCell,
    insertDataValuesCell,
  };
});
