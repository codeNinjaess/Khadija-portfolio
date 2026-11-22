const language = document.querySelector("[data-language]");
const languageTarget = language.getAttribute("href");
const keepFragment = () => {
  language.setAttribute("href", languageTarget + location.hash);
};
keepFragment();
window.addEventListener("hashchange", keepFragment);

const copy = document.querySelector(".hero-copy");
if (copy && "ResizeObserver" in window) {
  const mobile = matchMedia("(max-width: 799px)");
  const checkCopy = () => {
    const heading = copy.querySelector("h1");
    const singleLine = heading.getBoundingClientRect().height <=
      parseFloat(getComputedStyle(heading).lineHeight) * 1.1;
    const compact = copy.getBoundingClientRect().height <= 295 ||
      (window.innerWidth >= 430 && copy.getBoundingClientRect().height <= 335);
    copy.closest(".hero").classList.toggle("copy-above", mobile.matches && (!singleLine || !compact));
  };
  new ResizeObserver(checkCopy).observe(copy);
  mobile.addEventListener("change", checkCopy);
}

const phases = [...document.querySelectorAll(".phase")];
const nodes = [...document.querySelectorAll("[data-phase]")];
if (phases.length) {
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  let active;
  let pending = false;

  const highlight = (index) => {
    if (active === index) return;
    active = index;
    phases.forEach((phase, i) => phase.classList.toggle("is-current", index === i));
    nodes.forEach((node, i) => {
      if (index === i) node.setAttribute("aria-current", "step");
      else node.removeAttribute("aria-current");
    });
  };

  const updateProgress = () => {
    pending = false;
    if (reducedMotion.matches) {
      highlight(phases.findIndex((phase) => "#" + phase.id === location.hash));
      return;
    }
    const readingLine = window.innerHeight * .62;
    const index = phases.findLastIndex((phase) => phase.getBoundingClientRect().top <= readingLine);
    highlight(Math.max(0, index));
  };

  const onScroll = () => {
    if (reducedMotion.matches || pending) return;
    pending = true;
    requestAnimationFrame(updateProgress);
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  window.addEventListener("hashchange", updateProgress);
  reducedMotion.addEventListener("change", updateProgress);
  updateProgress();
}

