import { defineStore } from "pinia";
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

/**
 * Global store used to change the settings of the web application. Changes the following settings:
 * - Theme
 * - Langugage
 * - Colorblindness filter
 */
export const usedTheme = defineStore("usedTheme", {
  state: () => {
    let themeSymbol = "☀️"; // Symbol representing the current theme
    let currentTheme = "LIGHT"; // Current theme (LIGHT or DARK)
    let matrixTheme = {
      backgroundColor: "white",
      gridColor: "black",
    }; // Theme settings for the matrix
    let body = document.body; // Reference to the document body
    return {
      themeSymbol,
      currentTheme,
      body,
      matrixTheme,
    };
  },
  actions: {
    /**
     * Toggles between themes.
     */
    toggleTheme() {
      if (this.currentTheme == "LIGHT") {
        this.currentTheme = "DARK";
        this.themeSymbol = "🌑";
        this.matrixTheme = {
          backgroundColor: "rgb(39, 39, 39)",
          gridColor: "white",
        };
      } else {
        this.currentTheme = "LIGHT";
        this.themeSymbol = "☀️";
        this.matrixTheme = {
          backgroundColor: "white",
          gridColor: "black",
        };
      }
      this.body.classList.toggle("dark-theme");
    },
  },
});

/**
 * Global store for the web application's language.
 */
export const usedLanguage = defineStore("usedLanguage", {
  state: () => {
    const colorBlindnessStore = usedColorBlindnessTheme(); // Reference to the color blindness theme store
    let currLang = "EN"; // Current language (EN or DE)
    let currLangFile = ENLang; // Current language file
    let capacity = currLangFile.capacity;
    let battery_supply = currLangFile.battery_supply;
    let cost = currLangFile.cost;
    let battery_demand = currLangFile.battery_demand;
    let wind_curtailment = currLangFile.wind_curtailment;
    let solar_curtailment = currLangFile.solar_curtailment;
    let city_non_supplied_demand = currLangFile.city_non_supplied_demand;
    let industry_non_supplied_demand =
      currLangFile.industry_non_supplied_demand;
    let house_non_supplied_demand = currLangFile.house_non_supplied_demand;
    let pv = currLangFile.pv;
    let pv_production = currLangFile.pv_production;
    let curtailment = currLangFile.curtailment;
    let non_supplied_demand = currLangFile.non_supplied_demand;
    let demand = currLangFile.demand;
    let purchased_power = currLangFile.purchased_power;
    let storage_text = currLangFile.storage_text;
    let storage_charge = currLangFile.storage_charge;
    let storage_discharge = currLangFile.storage_discharge;
    let storage_level = currLangFile.storage_level;
    let simulate = currLangFile.simulate;
    let reset_text = currLangFile.reset_text;
    let auto = currLangFile.auto;
    let title_upper_plot = currLangFile.title_upper_plot;
    let title_middle_plot = currLangFile.title_middle_plot;
    let title_lower_plot = currLangFile.title_lower_plot;
    let load_scenario = currLangFile.load_scenario;
    let upload_scenario = currLangFile.upload_scenario;
    let upload_image = currLangFile.upload_image;
    let toggle_grid = currLangFile.toggle_grid;
    let add_consumer = currLangFile.add_consumer;
    let add_energy_source = currLangFile.add_energy_source;
    let add_battery = currLangFile.add_battery;
    let add_junction = currLangFile.add_junction;
    let clear_nodes = currLangFile.clear_nodes;
    let save_text = currLangFile.save_text;
    let lock_text = currLangFile.lock_text;
    let unlock_text = currLangFile.unlock_text;
    let add_edge = currLangFile.add_edge;
    let upload_json = currLangFile.upload_json;
    let selector_text_consumer = currLangFile.selector_text_consumer;
    let selector_text_producer = currLangFile.selector_text_producer;
    let group_no_color_blindness = currLangFile.group_no_color_blindness;
    let group_monochrome = currLangFile.group_monochrome;
    let group_red_green = currLangFile.group_red_green;
    let group_blue_yellow = currLangFile.group_blue_yellow;
    let noColorBlindness = currLangFile.noColorBlindness;
    let achromatopsia = currLangFile.achromatopsia;
    let tritanopia = currLangFile.tritanopia;
    let tritanomaly = currLangFile.tritanomaly;
    let protanopia = currLangFile.protanopia;
    let protanomaly = currLangFile.protanomaly;
    let deuteranopia = currLangFile.deuteranopia;
    let deuteranomaly = currLangFile.deuteranomaly;
    let nuclear = currLangFile.nuclear;
    let nuclear_power = currLangFile.nuclear_power;
    let nuclear_desc = currLangFile.nuclear_desc;
    let coal = currLangFile.coal;
    let coal_power = currLangFile.coal_power;
    let coal_desc = currLangFile.coal_desc;
    let solar = currLangFile.solar;
    let solar_power = currLangFile.solar_power;
    let solar_desc = currLangFile.solar_desc;
    let wind = currLangFile.wind;
    let wind_power = currLangFile.wind_power;
    let wind_desc = currLangFile.wind_desc;
    let gas = currLangFile.gas;
    let commercial = currLangFile.commercial;
    let junction = currLangFile.junction;
    let battery = currLangFile.battery;
    let residential_small = currLangFile.residential_small;
    let residential_large = currLangFile.residential_large;
    let choose_scenario = currLangFile.choose_scenario;
    let scene_1 = currLangFile.scene_1;
    let scene_2 = currLangFile.scene_2;
    let scene_3 = currLangFile.scene_3;
    let unknown_label = currLangFile.unknown_label;
    let error_parsing_json = currLangFile.error_parsing_json;
    let files_loaded_locally = currLangFile.files_loaded_locally;
    let error_saving_data = currLangFile.error_saving_data;
    let invalid_json_struc_node = currLangFile.invalid_json_struc_node;
    let invalid_json_struc_edge = currLangFile.invalid_json_struc_edge;
    let invalid_json = currLangFile.invalid_json;
    let consumer_types = currLangFile.consumer_types;
    let producer_types = currLangFile.producer_types;
    let home = currLangFile.home;
    let about_contact = currLangFile.about_contact;
    let about_header = currLangFile.about_header;
    let about_text = currLangFile.about_text;
    let about_contact_text = currLangFile.about_contact_text;

    return {
      currLang,
      currLangFile,
      capacity,
      battery_demand,
      battery_supply,
      cost,
      battery_demand,
      wind_curtailment,
      solar_curtailment,
      city_non_supplied_demand,
      industry_non_supplied_demand,
      house_non_supplied_demand,
      pv,
      pv_production,
      curtailment,
      non_supplied_demand,
      demand,
      purchased_power,
      storage_charge,
      storage_discharge,
      storage_level,
      simulate,
      reset_text,
      auto,
      title_upper_plot,
      title_middle_plot,
      title_lower_plot,
      load_scenario,
      upload_scenario,
      upload_image,
      toggle_grid,
      add_consumer,
      add_energy_source,
      add_battery,
      add_junction,
      clear_nodes,
      save_text,
      lock_text,
      unlock_text,
      add_edge,
      upload_json,
      selector_text_consumer,
      selector_text_producer,
      storage_text,
      noColorBlindness,
      achromatopsia,
      tritanopia,
      tritanomaly,
      protanopia,
      protanomaly,
      deuteranopia,
      deuteranomaly,
      colorBlindnessStore,
      nuclear,
      nuclear_power,
      nuclear_desc,
      coal,
      coal_power,
      coal_desc,
      solar,
      solar_power,
      solar_desc,
      wind,
      wind_power,
      wind_desc,
      gas,
      commercial,
      junction,
      battery,
      residential_small,
      residential_large,
      choose_scenario,
      scene_1,
      scene_2,
      scene_3,
      unknown_label,
      error_parsing_json,
      files_loaded_locally,
      error_saving_data,
      invalid_json_struc_node,
      invalid_json_struc_edge,
      invalid_json,
      group_no_color_blindness,
      group_monochrome,
      group_red_green,
      group_blue_yellow,
      consumer_types,
      producer_types,
      home,
      about_contact,
      about_contact_text,
      about_header,
      about_text,
    };
  },
  actions: {
    /**
     * Changes the language of the web application.
     * @param {*} language
     * @returns nothing
     */
    changeLang(language) {
      if (this.currLang == language) {
        return;
      }
      if (language == "EN") {
        this.currLang = "EN";
        this.currLangFile = ENLang;
      } else if (language == "DE") {
        this.currLang = "DE";
        this.currLangFile = DELang;
      } else {
        return;
      }
      this.capacity = this.currLangFile.capacity;
      this.cost = this.currLangFile.cost;
      this.battery_supply = this.currLangFile.battery_supply;
      this.battery_demand = this.currLangFile.battery_demand;
      this.wind_curtailment = this.currLangFile.wind_curtailment;
      this.solar_curtailment = this.currLangFile.solar_curtailment;
      this.city_non_supplied_demand =
        this.currLangFile.city_non_supplied_demand;
      this.industry_non_supplied_demand =
        this.currLangFile.industry_non_supplied_demand;
      this.house_non_supplied_demand =
        this.currLangFile.house_non_supplied_demand;
      this.pv = this.currLangFile.pv;
      this.pv_production = this.currLangFile.pv_production;
      this.curtailment = this.currLangFile.curtailment;
      this.non_supplied_demand = this.currLangFile.non_supplied_demand;
      this.demand = this.currLangFile.demand;
      this.purchased_power = this.currLangFile.purchased_power;
      this.storage_text = this.currLangFile.storage_text;
      this.storage_charge = this.currLangFile.storage_charge;
      this.storage_discharge = this.currLangFile.storage_discharge;
      this.storage_level = this.currLangFile.storage_level;
      this.simulate = this.currLangFile.simulate;
      this.reset_text = this.currLangFile.reset_text;
      this.auto = this.currLangFile.auto;
      this.title_upper_plot = this.currLangFile.title_upper_plot;
      this.title_middle_plot = this.currLangFile.title_middle_plot;
      this.title_lower_plot = this.currLangFile.title_lower_plot;
      this.load_scenario = this.currLangFile.load_scenario;
      this.upload_scenario = this.currLangFile.upload_scenario;
      this.upload_image = this.currLangFile.upload_image;
      this.toggle_grid = this.currLangFile.toggle_grid;
      this.add_consumer = this.currLangFile.add_consumer;
      this.add_energy_source = this.currLangFile.add_energy_source;
      this.add_battery = this.currLangFile.add_battery;
      this.add_junction = this.currLangFile.add_junction;
      this.clear_nodes = this.currLangFile.clear_nodes;
      this.save_text = this.currLangFile.save_text;
      this.lock_text = this.currLangFile.lock_text;
      this.unlock_text = this.currLangFile.unlock_text;
      this.add_edge = this.currLangFile.add_edge;
      this.upload_json = this.currLangFile.upload_json;
      this.selector_text_consumer = this.currLangFile.selector_text_consumer;
      this.selector_text_producer = this.currLangFile.selector_text_producer;
      this.group_no_color_blindness =
        this.currLangFile.group_no_color_blindness;
      this.group_monochrome = this.currLangFile.group_monochrome;
      this.group_red_green = this.currLangFile.group_red_green;
      this.group_blue_yellow = this.currLangFile.group_blue_yellow;
      this.noColorBlindness = this.currLangFile.noColorBlindness;
      this.achromatopsia = this.currLangFile.achromatopsia;
      this.tritanopia = this.currLangFile.tritanopia;
      this.tritanomaly = this.currLangFile.tritanomaly;
      this.protanopia = this.currLangFile.protanopia;
      this.protanomaly = this.currLangFile.protanomaly;
      this.deuteranopia = this.currLangFile.deuteranopia;
      this.deuteranomaly = this.currLangFile.deuteranomaly;
      this.nuclear = this.currLangFile.nuclear;
      this.nuclear_power = this.currLangFile.nuclear_power;
      this.nuclear_desc = this.currLangFile.nuclear_desc;
      this.coal = this.currLangFile.coal;
      this.coal_power = this.currLangFile.coal_power;
      this.coal_desc = this.currLangFile.coal_desc;
      this.solar = this.currLangFile.solar;
      this.solar_power = this.currLangFile.solar_power;
      this.solar_desc = this.currLangFile.solar_desc;
      this.wind = this.currLangFile.wind;
      this.wind_power = this.currLangFile.wind_power;
      this.wind_desc = this.currLangFile.wind_desc;
      this.gas = this.currLangFile.gas;
      this.commercial = this.currLangFile.commercial;
      this.junction = this.currLangFile.junction;
      this.battery = this.currLangFile.battery;
      this.residential_small = this.currLangFile.residential_small;
      this.residential_large = this.currLangFile.residential_large;
      this.choose_scenario = this.currLangFile.choose_scenario;
      this.scene_1 = this.currLangFile.scene_1;
      this.scene_2 = this.currLangFile.scene_2;
      this.scene_3 = this.currLangFile.scene_3;
      this.unknown_label = this.currLangFile.unknown_label;
      this.error_parsing_json = this.currLangFile.error_parsing_json;
      this.files_loaded_locally = this.currLangFile.files_loaded_locally;
      this.error_saving_data = this.currLangFile.error_saving_data;
      this.invalid_json_struc_node = this.currLangFile.invalid_json_struc_node;
      this.invalid_json_struc_edge = this.currLangFile.invalid_json_struc_edge;
      this.invalid_json = this.currLangFile.invalid_json;
      this.consumer_types = this.currLangFile.consumer_types;
      this.producer_types = this.currLangFile.producer_types;
      this.home = this.currLangFile.home;
      this.about_contact = this.currLangFile.about_contact;
      this.about_header = this.currLangFile.about_header;
      this.about_text = this.currLangFile.about_text;
      this.about_contact_text = this.currLangFile.about_contact_text;
      this.colorBlindnessStore.updateColorBlindnessLang(this);
    },
    /**
     * Returns the translation of the current label.
     * @param {*} label
     * @returns a string containing the translation of the current label.
     */
    getCurrentLabelTranslation(label) {
      switch (label) {
        case "Gas":
          return this.gas;
        case "Coal":
        case "Kohle":
          return this.coal;
        case "Solar":
          return this.solar;
        case "Wind":
          return this.wind;
        case "Industry":
        case "Industrie":
          return this.consumer_types[0].label;
        case "City":
        case "Stadt":
          return this.consumer_types[1].label;
        case "House":
        case "Haus":
          return this.consumer_types[2].label;
        case "Batterie":
        case "Battery":
          return this.battery;
        case "Kreuzung":
        case "Junction":
          return this.junction;
        case "Verbrauch":
        case "Demand":
          return this.demand;
        case "Curtailment":
        case "Abregelung":
          return this.curtailment;
        case "Non-Supplied Demand":
        case "nicht-gedeckte Nachfrage":
          return this.curtailment;
        case "Supply":
        case "nicht-gedeckte Nachfrage":
          return this.curtailment;
        case "Battery Supply":
        case "Batterie Versorgung":
          return this.battery_supply;
        case "Battery Demand":
        case "Batterie Nachfrage":
          return this.battery_demand;
        case "Industrie nicht-gedeckte Nachfrage":
        case "Industry Non-Supplied Demand":
          return this.industry_non_supplied_demand;
        case "Stadt nicht-gedeckte Nachfrage":
        case "City Non-Supplied Demand":
          return this.city_non_supplied_demand;
        case "Haus nicht-gedeckte Nachfrage":
        case "House Non-Supplied Demand":
          return this.house_non_supplied_demand;
        case "Solar Curtailment":
        case "Solar Kürzung":
          return this.solar_curtailment;
        case "Wind Curtailment":
        case "Wind Kürzung":
          return this.wind_curtailment;
      }
    },
    /**
     * Changes the language of the chart's labels
     * @param {*} dataset
     */
    updateChartLanguage(dataset) {
      for (let i = 0; i < dataset.length; i++) {
        switch (dataset[i].label) {
          case "Gas":
            dataset.dataset[i].label = this.producer_types[0].label;
            continue;
          case "Kohle":
          case "Coal":
            dataset[i].label = this.producer_types[1].label;
            continue;
          case "Solar":
            dataset[i].label = this.producer_types[2].label;
            continue;
          case "Solar Curtailment":
          case "Solar Kürzung":
            dataset[i].label = this.solar_curtailment;
            continue;
          case "Wind":
            dataset[i].label = this.producer_types[3].label;
            continue;
          case "Wind Curtailment":
          case "Wind Kürzung":
            dataset[i].label = this.wind_curtailment;
            continue;
          case "Industrie":
          case "Industry":
            dataset[i].label = this.consumer_types[0].label;
            continue;
          case "Industrie nicht-gedeckte Nachfrage":
          case "Industry Non-Supplied Demand":
            dataset[i].label = this.industry_non_supplied_demand;
            continue;
          case "Stadt":
          case "City":
            dataset[i].label = this.consumer_types[1].label;
            continue;
          case "Stadt nicht-gedeckte Nachfrage":
          case "City Non-Supplied Demand":
            dataset[i].label = this.city_non_supplied_demand;
          case "Haus":
          case "House":
            dataset[i].label = this.consumer_types[2].label;
            continue;
          case "Haus nicht-gedeckte Nachfrage":
          case "House Non-Supplied Demand":
            dataset[i].label = this.house_non_supplied_demand;
            continue;
          case "Batterie":
          case "Battery":
            dataset[i].label = this.battery;
            continue;
          case "Battery Supply":
          case "Batterie Versorgung":
            dataset[i].label = this.battery_supply;
            continue;
          case "Battery Demand":
          case "Batterie Nachfrage":
            dataset[i].label = this.battery_demand;
            continue;
        }
      }
    },
  },
});

/**
 * Global store controlling the colorblindness filters.
 */
export const usedColorBlindnessTheme = defineStore("usedColorBlindnessTheme", {
  state: () => {
    let colorBlindnessTypes = [
      {
        label: "NO COLOR BLINDNESS",
        items: [
          { label: "Color blindness filter off", value: "noColorBlindness" },
        ],
      },
      {
        label: "MONOCHROME",
        items: [{ label: "Achromatopsia", value: "achromatopsia" }],
      },
      {
        label: "RED-GREEN",
        items: [
          { label: "Protanopia", value: "protanopia" },
          { label: "Protanomaly", value: "protanomaly" },
          { label: "Deuteranopia", value: "deuteranopia" },
          { label: "Deuteranomaly", value: "deuteranomaly" },
        ],
      },
      {
        label: "BLUE-YELLOW",
        items: [
          { label: "Tritanopia", value: "tritanopia" },
          { label: "Tritanomaly", value: "tritanomaly" },
        ],
      },
    ];

    var currentColorSettings = colorBlindnessTypes[0];
    document.body.classList.toggle(currentColorSettings.value);

    return {
      colorBlindnessTypes,
      currentColorSettings,
    };
  },
  actions: {
    /**
     * Changes the theme.
     * @param {*} colorBlindnessType
     * @returns nothing
     */
    setColorBlindness(colorBlindnessType) {
      if (colorBlindnessType.value == this.currentColorSettings.value) {
        return;
      }
      document.body.classList.toggle(this.currentColorSettings.value);
      document.body.classList.toggle(colorBlindnessType.value);
      this.currentColorSettings = colorBlindnessType;
    },
    /**
     * Changes the language of the colorblindness labels.
     * @param {*} langStore
     */
    updateColorBlindnessLang(langStore) {
      this.colorBlindnessTypes[0].label = langStore.group_no_color_blindness;
      this.colorBlindnessTypes[1].label = langStore.group_monochrome;
      this.colorBlindnessTypes[2].label = langStore.group_red_green;
      this.colorBlindnessTypes[3].label = langStore.group_blue_yellow;
      this.colorBlindnessTypes[0].items[0].label = langStore.noColorBlindness;
      this.colorBlindnessTypes[1].items[0].label = langStore.achromatopsia;
      this.colorBlindnessTypes[2].items[0].label = langStore.tritanopia;
      this.colorBlindnessTypes[2].items[1].label = langStore.tritanomaly;
      this.colorBlindnessTypes[2].items[2].label = langStore.protanopia;
      this.colorBlindnessTypes[2].items[3].label = langStore.protanomaly;
      this.colorBlindnessTypes[3].items[0].label = langStore.deuteranopia;
      this.colorBlindnessTypes[3].items[1].label = langStore.deuteranomaly;
    },
  },
});
