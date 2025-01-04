import Alpine from 'alpinejs';
import { Toast } from 'bootstrap';

window.Alpine = Alpine;

document.addEventListener("DOMContentLoaded", () => {
  Alpine.start()
});

document.addEventListener("alpine:init", () => {
  Alpine.data("toast", () => ({
    init() {
      const bsToast = new Toast(this.$el);
      bsToast.show();
    }
  }))
})
