import App from "./widget/App.vue";
import { createApp } from "vue";
import VueAxios from "vue-axios";
import axios from "axios";
import qs from "qs";
import i18n from "./widget/i18n.js";

function axiosInstance() {
  const instance = axios.create({
    paramsSerializer: (params) =>
      qs.stringify(params, { arrayFormat: "repeat" }),
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      Prefer: "return=representation",
    },
  });
  return instance;
}

function initReferenceWidget() {
  document.querySelectorAll(".reference-widget-app").forEach((element) => {
    if (element.classList.contains("initialized")) {
      return;
    }

    const app = createApp(App);
    app.use(VueAxios, {
      axios: axiosInstance(),
    });

    const messages = JSON.parse(element.getAttribute("data-translations"));
    app.use(i18n, messages);
    app.mount(element);
    element.classList.add("initialized");
  });
}

initReferenceWidget();
window.initReferenceWidget = initReferenceWidget;
