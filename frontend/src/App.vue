/** * App.vue contains all the pages and sets the routes which are set in
main.js * Home.vue is loaded as root and /scenario loads the Scenario creator
page * All routes are set in main.js and vue pages are in frontend\src\views
folder */

<template>
  <div id="app">
    <div class="aspect-ratio-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    document.addEventListener("wheel", this.preventZoom, { passive: false });
    document.addEventListener("keydown", this.preventKeyboardZoom);
  },
  beforeUnmount() {
    document.removeEventListener("wheel", this.preventZoom);
    document.removeEventListener("keydown", this.preventKeyboardZoom);
  },
  methods: {
    preventZoom(event) {
      if (event.ctrlKey) {
        event.preventDefault();
      }
    },
    preventKeyboardZoom(event) {
      if (event.ctrlKey && (event.key === "=" || event.key === "-" || event.key === "0")) {
        event.preventDefault();
      }
      window.onload = function () {
  document.body.style.zoom = "100%";
};

window.addEventListener("resize", function () {
  document.body.style.zoom = "100%";
});

    }
  }
};
</script>



