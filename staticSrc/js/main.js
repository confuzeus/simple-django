function initToasts() {
  const toastEls = document.querySelectorAll(".toast");
  toastEls.forEach((el) => {
    const toast = window.bootstrap.Toast.getOrCreateInstance(el);
    toast.show();
    el.addEventListener("hidden.bs.toast", () => {
      el.remove();
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initToasts();
});

document.addEventListener("initToasts", () => {
  initToasts();
});
