<template>
  <div
    class="custom-node"
    :class="{
      highlighted: isHighlighted,
      selectedFirst: dataStore.isSelectedFirst(nodeID),
      selectedSecond: dataStore.isSelectedSecond(nodeID),
    }"
    @mouseover="handleMouseOver"
    @mouseleave="handleMouseLeave"
    @click="handleClick"
  >
    <div class="battery-icon">
      <img :src="data.icon" alt="Battery Icon" />
    </div>
    <div
      v-if="isHighlighted"
      class="node-name"
      style="color: black; background: rgba(255, 255, 255, 0.7)"
    >
      <!-- color of label -->
      {{ currLang.getCurrentLabelTranslation(data.label) || "Battery" }}
    </div>
    <div class="handles">
      <!-- Handles for inputs -->
      <div v-for="(input, index) in data.inputs" :key="'input_' + index">
        <Handle
          type="target"
          :position="'left'"
          :id="'input_' + index"
          style="background: #555"
        />
        <Handle
          type="target"
          :position="'top'"
          :id="'input_top_' + index"
          style="background: #555"
        />
      </div>

      <!-- Handles for outputs -->
      <div v-for="(output, index) in data.outputs" :key="'output_' + index">
        <Handle
          type="source"
          :position="'right'"
          :id="'output_' + index"
          style="background: #555"
        />
        <Handle
          type="source"
          :position="'bottom'"
          :id="'output_bottom_' + index"
          style="background: #555"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, inject, defineComponent, computed } from "vue";
import { Handle, Position } from "@vue-flow/core";
import { useDataStore } from "../../assets/stores/dataValues";
import { usedLanguage } from "@/assets/stores/pageSettings";

export default defineComponent({
  name: "BatteryNode",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  components: {
    Handle,
  },
  setup(props, context) {
    let handleNodeSelection = inject("handleNodeSelection");
    const dataStore = useDataStore();
    const isHighlighted = ref(false); // Tracks if the node is hovered
    const nodeID = context.attrs.id.slice(5);
    const currLang = usedLanguage();

    const handleMouseOver = () => {
      isHighlighted.value = true; // Show "Hello" on hover
    };

    const handleMouseLeave = () => {
      isHighlighted.value = false; // Hide "Hello" when hover ends
    };

    const handleClick = () => {
      if (handleNodeSelection) handleNodeSelection(nodeID);
    };

    return {
      Position,
      isHighlighted,
      dataStore,
      nodeID,
      currLang,
      handleMouseOver,
      handleMouseLeave,
      handleClick,
    };
  },
});
</script>

<style>
@import "../../assets/main.css";
</style>
