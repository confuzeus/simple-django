import { Alert, Collapse } from "bootstrap";

window.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll(".alert")
    .forEach((alertNode) => new Alert(alertNode));

  document
    .querySelectorAll(".collapse")
    .forEach((collapseNode) => new Collapse(collapseNode));
});
