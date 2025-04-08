<template>
  <div id="drawerbox">
    <Drawerbox @changeLanguage="updateLanguage"></Drawerbox>
  </div>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox1" class="grid-column">
        <Playfield></Playfield>
      </div> 
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="attention-box">
        <img src="@/assets/tuda_logo.png" alt="TUDA Logo" id="tuda-logo" />
        <h2>Attention</h2>
        <ul>
          <li>Welcome to the scenario creator. Here you can create a scenario using your own image or one from the default scenarios.</li>
          <li>To create a custom scenario from default scenarios, load a default scenario and click "Clear Nodes" before starting. Warning: Do not create a scenario without clicking "Clear Nodes."</li>
          <li>Choose the type of consumer or energy source before clicking the button to add nodes. Once all nodes are added, click on "Add Edge" to connect the nodes. Trying to connect edges without clicking "Add Edge" will not work.</li>
          <li>For battery and junction nodes: They both take inputs and outputs. Inputs are on the top and left, and outputs are on the bottom and right side of the node.</li>
          <li>You can only have a total of 5 energy + battery nodes (e.g., 3 energy source nodes and 2 battery nodes). If you try to add more and save, an error will occur.</li>
          <li>Ensure that the graph created is connected, meaning all nodes should be reachable directly or indirectly.</li>
          <li>Once done creating a graph, click "Save" to download the custom-created graph file.</li>
          <li>To use this on the student website, you can load a scenario or upload your own image and directly upload the JSON.</li>
        </ul>
        <h2>Achtung</h2>
        <ul>
          <li>Willkommen beim Szenario-Ersteller. Hier können Sie ein Szenario mit Ihrem eigenen Bild oder einem der Standard-Szenarien erstellen.</li>
          <li>Um ein benutzerdefiniertes Szenario aus den Standardszenarien zu erstellen, laden Sie ein Standardszenario und klicken Sie auf "Knoten löschen", bevor Sie beginnen. Warnung: Erstellen Sie kein Szenario, ohne "Knoten löschen" zu klicken.</li>
          <li>Wählen Sie die Art des Verbrauchers oder der Energiequelle, bevor Sie auf die Schaltfläche klicken, um Knoten hinzuzufügen. Sobald alle Knoten hinzugefügt wurden, klicken Sie auf "Kante hinzufügen", um die Knoten zu verbinden. Das Verbinden von Kanten ohne vorheriges Klicken auf "Kante hinzufügen" funktioniert nicht.</li>
          <li>Für Batterie- und Verzweigungsknoten: Sie nehmen sowohl Eingaben als auch Ausgaben entgegen. Eingaben befinden sich oben und links, Ausgaben unten und rechts.</li>
          <li>Sie können insgesamt nur 5 Energie- + Batterieknoten haben (z. B. 3 Energiequellen und 2 Batterieknoten). Wenn Sie mehr hinzufügen und speichern, tritt ein Fehler auf.</li>
          <li>Stellen Sie sicher, dass der erstellte Graph verbunden ist, d. h. alle Knoten sollten direkt oder indirekt erreichbar sein.</li>
          <li>Wenn Sie die Graphenerstellung abgeschlossen haben, klicken Sie auf "Speichern", um die erstellte Graph-Datei herunterzuladen.</li>
          <li>Um dies auf der Studenten-Website zu verwenden, können Sie ein Szenario laden oder Ihr eigenes Bild hochladen und die JSON-Datei direkt hochladen.</li>
        </ul> 
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import Playfield from "../components/Playfield.vue";
import NodeSelector from "@/components/NodeSelector.vue";
import Drawerbox from "@/components/Drawerbox.vue";
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

export default {
  setup() {
    return {};
  },
  components: {
    Playfield,
    NodeSelector,
    Drawerbox,
  },
  methods: {

  },
};
</script>

<style>
@import "../assets/main.css";


#attention-box {
  padding: 2%;
  background-color: #f8f9fa;
  border: 1% solid #ccc;
  border-radius: 2%;
  margin: 1.5%;
}

#attention-box h2 {
  color: #d9534f;
  font-size: 1.5em;
}

#tuda-logo {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 5rem;
  height: auto;
}


#attention-box ul {
  list-style-type: disc;
  padding-left: 10px;
}
</style>
