import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import ScenarioCreator from "./views/ScenarioCreator.vue";
import About from "./views/About.vue";
import Home from "./views/Home.vue"; //main page
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura/";
import VueApexCharts from "vue3-apexcharts";
import "./assets/main.css";
import { createPinia } from "pinia";

// Hardcoded password
const PASSWORD = "password";

//creates link for root aka / ehich opens home.vue and /admin opens admin.vue
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home }, //route to main page
    {
      path: "/scenario",
      component: ScenarioCreator, //route to password protected scenario creator
      beforeEnter: (to, from, next) => {
        const userPassword = prompt("Enter the password:");
        if (userPassword === PASSWORD) {
          next(); // Allow access
        } else {
          alert("Incorrect password!");
          next("/"); // Redirect to landing page
        }
      },
    }, //route to scenario creator
    {
      path: "/about",
      component: About
    },
    // all others route to home
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});

const app = createApp(App);

app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      prefix: "p",
      darkModeSelector: ".dark-theme",
      cssLayer: false,
    },
  },
});
app.use(VueApexCharts);

// Creates a pinia instance for us so that stores can be used
app.use(createPinia());
app.use(router);
app.mount("#app");
