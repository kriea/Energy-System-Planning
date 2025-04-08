// src/utils/nodeUtils.js

import Industry from "@/assets/node_images/consumer/Industry.png";
import City from "@/assets/node_images/consumer/City.png";
import House from "@/assets/node_images/consumer/House.png";

import Battery from "@/assets/node_images/misc/battery.png";
import Junction from "@/assets/node_images/misc/junction.png";

import Gas from "@/assets/node_images/producer/Gas.png";
import Coal from "@/assets/node_images/producer/Coal.png";
import Solar from "@/assets/node_images/producer/Solar.png";
import Wind from "@/assets/node_images/producer/Wind.png";

import { usedLanguage } from "@/assets/stores/pageSettings";

export function getNodeData(label) {

  const currLang = usedLanguage(); 
  switch (label) {
    case "Industrie":
    case "Industry":
      return {
        label: currLang.consumer_types[0].label,
        icon: Industry,
        inputs: [0, 1, 2, 3],
      };
    case "Stadt":
    case "City":
      return {
        label: currLang.consumer_types[1].label,
        icon: City,
        inputs: [0, 1, 2, 3],
      };
    case "Haus":
    case "House":
      return {
        label: currLang.consumer_types[2].label,
        icon: House,
        inputs: [0, 1, 2, 3],
      };
    case "Batterie":
    case "Battery":
      return {
        label: currLang.battery,
        icon: Battery,
        inputs: [0, 1],
        outputs: [2, 3],
        description: "Stores excess energy and releases it when needed.",
      };
    case "Kreuzung":
    case "Junction":
      return {
        label: currLang.junction,
        icon: Junction,
        inputs: [0, 1],
        outputs: [2, 3],
        description: "Connects multiple energy sources and consumers.",
      };

    case "Gas":
      return {
        label: currLang.producer_types[0].label,
        icon: Gas,
        outputs: [0, 1, 2, 3],
        description:
          "Provides large-scale base power with low carbon emissions.",
      };
    case "Kohle":
    case "Coal":
      return {
        label: currLang.producer_types[1].label,
        icon: Coal,
        outputs: [0, 1, 2, 3],
        description: "Traditional fossil fuel energy source.",
      };

    case "Solar":
      return {
        label: currLang.producer_types[2].label,
        icon: Solar,
        outputs: [0, 1, 2, 3],
        description: "Generates renewable energy from sunlight.",
      };

    case "Wind":
      return {
        label: currLang.producer_types[3].label,
        icon: Wind,
        outputs: [0, 1, 2, 3],
        description: "Generates renewable energy from wind.",
      };

    default:
      console.warn(`Unknown node type: ${label}`);
      return null;
  }
}

export function getNodeIcon(label) {
  switch (label) {
    case "Batterie":
    case "Battery":
      return Battery;
      
    case "Gas":
      return Gas;

    case "Kohle":
    case "Coal":
      return Coal;

    case "Solar":
      return Solar;

    case "Wind":
      return Wind;
    default:
      console.warn(`Unknown node type: ${label}`);
      return null;
  }
}
