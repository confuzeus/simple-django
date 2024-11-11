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
  console.log("ready");
  initToasts();
});

document.addEventListener("htmx:afterRequest", (evt) => {
  if (!evt.detail.requestConfig.path.includes("toasts")) {
    document.querySelector("body").dispatchEvent(new Event("fetchToasts"));
  }
});

document.addEventListener("initToasts", () => {
  initToasts();
});
