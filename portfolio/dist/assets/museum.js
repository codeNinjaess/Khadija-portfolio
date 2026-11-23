(() => {
  const museum = document.querySelector("[data-museum]");
  const rooms = new Map([...museum.querySelectorAll("[data-room]")].map(room => [room.dataset.room, room]));
  const map = museum.querySelector(".museum-map");
  const language = museum.querySelector("[data-language]");
  const languageTarget = language.getAttribute("href");
  const back = museum.querySelector("[data-back]");
  const main = museum.querySelector("main");
  const header = museum.querySelector(".museum-header");
  let active;
  let previousRoom;

  function parse(hash) {
    const value = hash.slice(1);
    const legacy = value.match(/^phase-([1-4])$/);
    const [roomSlug, item] = legacy ? ["about", legacy[1]] : value.split("/");
    const room = rooms.get(roomSlug) || rooms.get("lobby");
    const key = room.dataset.room;
    const items = [...room.querySelectorAll("[data-detail]")];
    const selected = items.find(node => node.dataset.detail === item) || items[0];
    const wall = selected?.dataset.wall;
    const exhibit = selected?.hasAttribute("data-exhibit") ?? false;
    return { key, room, items, item: selected?.dataset.detail, wall, exhibit, explicit: item === selected?.dataset.detail };
  }

  function render({ focus = false, resetScroll = false } = {}) {
    active = parse(location.hash);
    const changedRoom = previousRoom !== active.key;
    museum.dataset.active = active.key;
    museum.dataset.workView = active.exhibit ? "exhibit" : "wall";
    museum.dataset.workWall = active.wall || "";
    for (const room of rooms.values()) room.hidden = room !== active.room;
    for (const item of active.items) item.hidden = item.dataset.detail !== active.item;
    back.hidden = active.key === "lobby";

    for (const link of museum.querySelectorAll("a[data-route]")) {
      const [room, item] = link.getAttribute("href").slice(1).split("/");
      if (room === active.key && (!item || item === active.item || (room === "work" && item === active.wall))) {
        link.setAttribute("aria-current", item ? "true" : "location");
      } else {
        link.removeAttribute("aria-current");
      }
    }

    language.href = languageTarget + (active.key === "lobby" ? "" : location.hash);
    if (focus && changedRoom) active.room.querySelector("h1, h2").focus({ preventScroll: true });
    if (resetScroll || changedRoom) window.scrollTo({ top: 0, behavior: "instant" });
    previousRoom = active.key;
    museum.dispatchEvent(new CustomEvent("museum:state", {
      detail: sceneState()
    }));
  }

  function navigate(hash, overlay = false) {
    const current = parse(location.hash);
    const destination = parse(hash);
    if (hash !== location.hash) history.pushState({ museumTrail: true }, "", hash);
    if (map.open) map.open = false;
    render({ focus: true });
    if (destination.exhibit && destination.item !== current.item) {
      document.getElementById("focus-" + destination.item)?.focus({ preventScroll: true });
    } else if (current.exhibit && destination.key === "work" && !destination.exhibit) {
      const exhibit = destination.room.querySelector('.project-overview[data-wall="' + destination.wall + '"] [href="#work/' + current.item + '"]');
      const wall = destination.room.querySelector('.project-wall-picker [aria-current="true"]');
      (exhibit || wall)?.focus({ preventScroll: true });
    } else if (overlay && current.key === destination.key) {
      const link = destination.room.querySelector('[aria-current="true"]');
      link?.focus({ preventScroll: true });
    }
  }

  museum.addEventListener("click", event => {
    const link = event.target.closest("a[data-route]");
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    navigate(link.getAttribute("href"));
  });
  museum.addEventListener("museum:pick", event => navigate("#" + event.detail, true));
  window.addEventListener("popstate", () => render({ focus: true }));
  window.addEventListener("hashchange", () => render({ focus: true }));

  back.addEventListener("click", () => {
    if (history.state?.museumTrail) {
      history.back();
    } else {
      history.replaceState(null, "", "#lobby");
      render({ focus: true, resetScroll: true });
    }
  });
  document.querySelector(".skip").addEventListener("click", event => {
    event.preventDefault();
    main.focus({ preventScroll: true });
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && map.open) {
      map.open = false;
      map.querySelector("summary").focus();
    }
  });
  document.addEventListener("click", event => {
    if (map.open && !map.contains(event.target)) map.open = false;
  });

  museum.classList.add("museum-ready");
  if ("ResizeObserver" in window) {
    new ResizeObserver(() => {
      museum.style.setProperty("--museum-gallery-header", header.getBoundingClientRect().height + "px");
    }).observe(header);
  }
  render();
  if (location.hash) {
    window.addEventListener("load", () => requestAnimationFrame(() => {
      window.scrollTo({ top: 0, behavior: "instant" });
    }), { once: true });
  }
  // The scene is optional. The semantic exhibit links work before it loads.
  function sceneState() {
    return { room: active.key, item: active.item, wall: active.wall, exhibit: active.exhibit, focused: active.explicit };
  }
  museum.museumState = sceneState;
})();
