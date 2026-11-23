(() => {
  const gallery = document.querySelector(".project-gallery");
  if (!gallery) return;

  for (const device of gallery.querySelectorAll("[data-device]")) {
    const menu = device.querySelector("[data-resource-menu]");
    if (menu) {
      for (const pane of device.querySelectorAll("[data-resource]")) pane.hidden = true;
    }
  }

  function showSlide(carousel, next) {
    const slides = [...carousel.querySelectorAll("[data-slide]")];
    const index = (next + slides.length) % slides.length;
    carousel.dataset.activeSlide = String(index);
    slides.forEach((slide, i) => { slide.hidden = i !== index; });
    slides[index].querySelector("img").loading = "eager";
    carousel.querySelector("[data-slide-count]").textContent = (index + 1) + " / " + slides.length;
  }

  for (const carousel of gallery.querySelectorAll("[data-carousel]")) showSlide(carousel, 0);

  gallery.addEventListener("click", event => {
    const action = event.target.closest("button");
    if (!action) return;
    const device = action.closest("[data-device]");
    if (!device) return;

    if (action.hasAttribute("data-open-resource")) {
      const key = action.dataset.openResource;
      const panel = [...device.querySelectorAll("[data-resource]")].find(pane => pane.dataset.resource === key);
      if (!panel) return;
      device.querySelector("[data-resource-menu]").hidden = true;
      panel.hidden = false;
      panel.querySelector("[data-resource-back]").focus({ preventScroll: true });
    } else if (action.hasAttribute("data-resource-back")) {
      const panel = action.closest("[data-resource]");
      panel.querySelector("video")?.pause();
      panel.hidden = true;
      const menu = device.querySelector("[data-resource-menu]");
      menu.hidden = false;
      [...menu.querySelectorAll("button")].find(button => button.dataset.openResource === panel.dataset.resource)
        ?.focus({ preventScroll: true });
    } else if (action.hasAttribute("data-slide-step")) {
      const carousel = action.closest("[data-carousel]");
      showSlide(carousel, Number(carousel.dataset.activeSlide) + Number(action.dataset.slideStep));
    }
  });

  gallery.closest("[data-museum]").addEventListener("museum:state", ({ detail }) => {
    for (const exhibit of gallery.querySelectorAll("[data-exhibit]")) {
      if (detail.room !== "work" || detail.item !== exhibit.dataset.detail) {
        for (const video of exhibit.querySelectorAll("video")) video.pause();
      }
    }
  });
})();
