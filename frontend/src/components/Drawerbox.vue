<template>
  <Drawer id="drawer" v-model:visible="visible" position="top">
    <!-- Button to navigate to the About page, visible only on the home page -->
    <Button
      @click="goToAbout"
      class="button"
      :label="currLang.about_header"
      v-if="route.fullPath === '/'"
    ></Button>
    <!-- Button to navigate to the Home page, visible only on the About page -->
    <Button
      @click="gotToHome"
      class="button"
      :label="currLang.home"
      v-if="route.fullPath === '/about'"
    ></Button>
    <!-- Button to toggle the theme -->
    <Button @click="currTheme.toggleTheme" class="button">
      {{ currTheme.themeSymbol }}
    </Button>
    <!-- Button to change the language to English -->
    <Button @click="currLang.changeLang('EN')" class="button"
      ><img src="../assets/en.png" style="width: 30px; height: 20px" />
    </Button>
    <!-- Button to change the language to German -->
    <Button @click="currLang.changeLang('DE')" class="button"
      ><img src="../assets/de.png" style="width: 30px; height: 20px" />
    </Button>

    <!-- Select component for color blindness filter -->
    <Select
      v-model="newColorFilter"
      :options="currColorBlindnessTheme.colorBlindnessTypes"
      option-label="label"
      option-group-label="label"
      option-group-children="items"
      :placeholder="
        currColorBlindnessTheme.colorBlindnessTypes[0].items[0].label
      "
      @change="currColorBlindnessTheme.setColorBlindness(newColorFilter)"
    ></Select>
  </Drawer>
  <!-- Button to toggle the visibility of the drawer -->
  <Button id="drawer-button" @click="visible = !visible">
    <div class="hamburger-menu">
      <div class="line"></div>
      <div class="line"></div>
      <div class="line"></div>
    </div>
  </Button>
</template>

<script>
import { ref } from "vue";
import { Select, Button, Drawer } from "primevue";
import {
  usedLanguage,
  usedTheme,
  usedColorBlindnessTheme,
} from "../assets/stores/pageSettings";
import { useDataStore } from "../assets/stores/dataValues";
import { useRouter, useRoute } from "vue-router";
import { useMatrixDesignStore } from "@/assets/stores/matrixDesign";

export default {
  setup(prop, context) {
    const currLang = usedLanguage(); // Get the current language settings
    const currTheme = usedTheme(); // Get the current theme settings
    const matrixStore = useMatrixDesignStore(); // Get the matrix design store
    const dataStore = useDataStore(); // Get the data store
    const currColorBlindnessTheme = usedColorBlindnessTheme(); // Get the color blindness theme settings
    const visible = ref(false); // Visibility state of the drawer
    const newColorFilter = ref(currColorBlindnessTheme); // Selected color blindness filter
    const router = useRouter(); // Router instance
    const route = useRoute(); // Route instance

    // Function to navigate to the About page
    function goToAbout() {
      router.push("/about");
    }

    /**
     * Navigates to the home page.
     * Resets the datastore values.
     */
    function gotToHome() {
      dataStore.prodCapacities = new Map();
      dataStore.nodeInfo = new Map();
      dataStore.selectedNodes = [];
      router.push("/");
    }

    return {
      visible,
      currLang,
      currTheme,
      newColorFilter,
      currColorBlindnessTheme,
      goToAbout,
      gotToHome,
      route,
    };
  },
  components: {
    Drawer,
    Button,
    Select,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
