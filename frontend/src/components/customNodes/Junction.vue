<template>
  <div
    class="custom-node"
    :class="{
      highlighted: isHighlighted,
    }"
    @mouseover="handleMouseOver"
    @mouseleave="handleMouseLeave"
  >
    <div class="junction-icon">
      <img :src="data.icon" alt="junction Icon" />
    </div>
    <div
      v-if="isHighlighted"
      class="node-name"
      style="color: black; background: rgba(255, 255, 255, 0.7)"
    >
      <!-- color of label -->
      {{ currLang.getCurrentLabelTranslation(data.label) || "junction" }}
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
import { usedLanguage } from "@/assets/stores/pageSettings";

export default defineComponent({
  name: "junctionNode",
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
    const currLang = usedLanguage();
    const selectedNodes = inject("selectedNodes");
    const isHighlighted = ref(false); // Tracks if the node is hovered
    const nodeID = context.attrs.id.slice(5);

    const handleMouseOver = () => {
      isHighlighted.value = true; // Show "Hello" on hover
    };

    const handleMouseLeave = () => {
      isHighlighted.value = false; // Hide "Hello" when hover ends
    };

    return {
      Position,
      isHighlighted,
      currLang,
      handleMouseOver,
      handleMouseLeave,
    };
  },
});
</script>

<style>
.custom-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.custom-node.highlighted {
  transform: scale(1.2);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.junction-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.junction-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.node-name {
  margin-top: 8px;
  font-size: 14px;
  color: #333;
  text-align: center;
}
</style>
