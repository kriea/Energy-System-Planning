<template>
  <div class="node-selector">
    <!-- Buttons to handle different actions -->
    <Button @click="handleButtonClick('Button 1')" :label="button1"></Button>
    <Button @click="handleButtonClick('Button 2')" :label="button2"></Button>
    <Button @click="handleButtonClick('Button 3')" :label="button3"></Button>
    <!-- Select component to choose an option -->
    <Select
      v-model="selectedOption"
      :options="options"
      placeholder="Please select one"
    >
    </Select>
  </div>
</template>

<script>
import { Button, Select } from "primevue";

export default {
  components: {
    Button,
    Select,
  },
  name: "NodeSelector",
  setup() {
    let button1 = "Button 1";
    let button2 = "Button 2";
    let button3 = "Button 3";

    // Function to handle button clicks
    function handleButtonClick(buttonName) {
      console.log(`${buttonName} clicked`);
    }

    return {
      selectedOption: "",
      options: ["Option 1", "Option 2", "Option 3"],
      handleButtonClick,
      button1,
      button2,
      button3,
    };
  },
};
</script>

<style scoped>
@import "../assets/main.css";
.node-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
}

button {
  margin: 5px;
}

select {
  margin: 10px;
}
</style>
