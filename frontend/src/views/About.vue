<template>
    <div id="drawerbox">
        <Drawerbox></Drawerbox>
    </div>
    <div id="about-page-container">
        <Fieldset :legend="currLang.about_header">
            <div class="about">
                <p class="about-text" v-html="currLang.about_text"></p>
                <div class="logo-contact">
                    <div>
                        <img id="about-logo" src="../assets/tuda_logo.png">
                    </div>
                    <div>
                        <h1 class="contact-header">Product Owner</h1>
                        <h3 class="contact-header">
                            <li>Julia Barbosa</li>
                            <li>Florian Steinke</li>
                        </h3>
                        <h1 class="contact-header">Developers</h1>
                        <h3 class="contact-header">
                            <li>Kartikeya Chaudhary</li>
                            <li>Dennis Dias Fernandes</li>
                            <li>Akshat Gupta</li>
                            <li>Khush Makhija</li>
                            <li>Paul Plath</li>
                        </h3>


                    </div>
                </div>
            </div>
        </Fieldset>
    </div>

</template>

<script>
import { Panel, Fieldset, Button } from "primevue";
import Drawerbox from "@/components/Drawerbox.vue";
import { usedLanguage } from "../assets/stores/pageSettings";

export default {
    components: {
        Panel,
        Drawerbox,
        Fieldset,
        Button
    },
    setup() {
        const currLang = usedLanguage();
        return {
            currLang,
        }
    }
}
</script>
<style>
@import "../assets/main.css";
</style>