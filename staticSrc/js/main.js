import Alpine from "alpinejs";

window.Alpine = Alpine;

document.addEventListener("DOMContentLoaded", () => {
  Alpine.start();
});

document.addEventListener("alpine:init", () => {});
