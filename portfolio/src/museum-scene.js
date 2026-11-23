import {
  ACESFilmicToneMapping, AdditiveBlending, BoxGeometry, BufferGeometry, CanvasTexture,
  CatmullRomCurve3, Color, CylinderGeometry, Fog, Group, HemisphereLight,
  IcosahedronGeometry, Line, LineBasicMaterial, Mesh, MeshBasicMaterial, MeshStandardMaterial,
  OctahedronGeometry, PerspectiveCamera, PointLight, Scene, Sprite,
  SpriteMaterial, SRGBColorSpace, TorusGeometry, TubeGeometry, Vector3, WebGLRenderer
} from "three";
import { createProjectWalls } from "./project-walls.js";

const museum = document.querySelector("[data-museum]");
const canvas = museum?.querySelector("canvas");
if (canvas && museum.museumState) startScene();

function startScene() {
  const gl = canvas.getContext("webgl2", { alpha: false, antialias: true, powerPreference: "low-power" });
  if (!gl) return;

  let renderer;
  try {
    renderer = new WebGLRenderer({ canvas, context: gl });
  } catch {
    return;
  }

  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.24;
  const scene = new Scene();
  scene.background = new Color("#1b0611");
  scene.fog = new Fog("#1b0611", 16, 49);
  const camera = new PerspectiveCamera(40, 1, .12, 62);
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  const rtl = document.documentElement.dir === "rtl";
  const side = rtl ? -1 : 1;
  const V = (x, y, z) => new Vector3(x, y, z);
  const metal = (color, options) => new MeshStandardMaterial({ color, roughness: .42, metalness: .54, ...options });
  const emit = color => new MeshBasicMaterial({ color });
  const mat = {
    floor: metal("#42222e", { metalness: .26, roughness: .56 }),
    wall: metal("#3e192a", { metalness: .25 }),
    column: metal("#5b2439"),
    frame: metal("#91485b"),
    facet: metal("#7d253e", { metalness: .26, roughness: .42, flatShading: true }),
    warm: metal("#e9a183", { metalness: .4 }),
    black: metal("#21131e", { metalness: .21 }),
    ivory: emit("#ffd6b7"),
    coral: emit("#ff8b99"),
    neon: emit("#fa326c"),
    dim: emit("#803247"),
    gold: emit("#d88f75"),
  };

  const shell = new Group();
  scene.add(shell);
  scene.add(new HemisphereLight("#ffcfbb", "#602037", 1.7));
  const ambient = point("#ff6291", 140, 38, V(1, 6, 9), scene);
  point("#ffc4a8", 140, 31, V(-5, 5, 1), scene);
  point("#ed407c", 130, 30, V(8, 4, -5), scene);

  const atmos = document.createElement("canvas");
  atmos.width = atmos.height = 128;
  const ctx = atmos.getContext("2d");
  const gradient = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
  gradient.addColorStop(0, "rgba(255,255,255,.56)");
  gradient.addColorStop(.19, "rgba(255,255,255,.16)");
  gradient.addColorStop(.5, "rgba(255,255,255,.055)");
  gradient.addColorStop(1, "rgba(255,255,255,0)");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 128, 128);
  const glowTexture = new CanvasTexture(atmos);
  const glowMaterials = new Map();

  function mesh(geometry, material, parent, x = 0, y = 0, z = 0) {
    const object = new Mesh(geometry, material);
    object.position.set(x, y, z);
    parent.add(object);
    return object;
  }

  function group(parent, x = 0, y = 0, z = 0) {
    const object = new Group();
    object.position.set(x, y, z);
    parent.add(object);
    return object;
  }

  function box(parent, x, y, z, w, h, d, material) {
    return mesh(new BoxGeometry(w, h, d), material, parent, x, y, z);
  }

  function point(color, intensity, distance, position, parent) {
    const light = new PointLight(color, intensity, distance, 1.8);
    light.position.copy(position);
    parent.add(light);
    return light;
  }

  function glow(parent, x, y, z, size, color, opacity) {
    const key = color + opacity;
    if (!glowMaterials.has(key)) {
      glowMaterials.set(key, new SpriteMaterial({
        map: glowTexture, color, opacity, transparent: true,
        blending: AdditiveBlending, depthWrite: false, fog: true
      }));
    }
    const sprite = new Sprite(glowMaterials.get(key));
    sprite.position.set(x, y, z);
    sprite.scale.set(size, size, 1);
    parent.add(sprite);
    return sprite;
  }

  function stroke(parent, points, color) {
    const object = new Line(new BufferGeometry().setFromPoints(points), new LineBasicMaterial({ color }));
    parent.add(object);
    return object;
  }

  function tube(parent, points, radius, material, segments = 22) {
    const path = new CatmullRomCurve3(points, false, "centripetal");
    return mesh(new TubeGeometry(path, segments, radius, 7, false), material, parent);
  }

  function circle(parent, x, y, z, radius, thickness, material) {
    return mesh(new TorusGeometry(radius, thickness, 8, 64), material, parent, x, y, z);
  }

  function pedestal(parent, x, z, radius, height = .68) {
    const p = group(parent, x, 0, z);
    mesh(new CylinderGeometry(radius * .94, radius, height, 40), mat.black, p, 0, height / 2, 0);
    mesh(new CylinderGeometry(radius * .95, radius * .95, .055, 48), mat.frame, p, 0, height - .02, 0);
    const rim = circle(p, 0, .075, 0, radius * .985, .012, mat.coral);
    rim.rotation.x = Math.PI / 2;
    return p;
  }

  box(shell, 0, -.15, -5, 35, .29, 48, mat.floor);
  box(shell, 0, 5, -10, 33, 10, .7, mat.wall);
  for (const sign of [-1, 1]) {
    box(shell, sign * 13.7, 4.7, -2, .65, 9.4, 25, mat.wall);
    for (let z = -9; z <= 10; z += 4.7) {
      box(shell, sign * 12.9, 4.65, z, .51, 9.3, .62, mat.column);
      box(shell, sign * 12.58, 4.55, z + .22, .04, 8.95, .06, mat.dim);
    }
  }
  for (let x = -15; x <= 15; x += 1.7) {
    stroke(shell, [V(x, .005, -9.8), V(x, .005, 23)], "#744151");
  }
  for (let z = -8; z < 22; z += 2.45) stroke(shell, [V(-15, .008, z), V(15, .008, z)], "#643447");
  for (let x = -12.5; x <= 13; x += 2.5) {
    box(shell, x, 4.4, -9.53, .08, 8.8, .1, mat.column);
  }
  box(shell, 0, 5.75, -9.54, 25, .035, .09, mat.dim);
  box(shell, 0, 1.12, -9.53, 25, .022, .085, mat.dim);
  glow(shell, 0, 4.8, -8.9, 23, "#c22b58", .7);

  const roots = {};
  const clicks = {};
  const art = {};
  function stage(name) {
    roots[name] = group(scene);
    clicks[name] = [];
    return roots[name];
  }
  function hit(name, slug, object, radius = 48) {
    clicks[name].push({ slug, object, radius });
    return object;
  }

  function portal(parent, x, z, material) {
    const g = group(parent, x, .025, z);
    const line = (w, h, depth) => [
      V(-w, .05, depth), V(-w, h - .68, depth), V(-w * .68, h - .2, depth),
      V(0, h, depth), V(w * .68, h - .2, depth), V(w, h - .68, depth), V(w, .05, depth)
    ];
    tube(g, line(1.92, 4.55, -.28), .24, mat.column, 54);
    tube(g, line(1.79, 4.48, -.05), .09, mat.frame, 54);
    tube(g, line(1.7, 4.34, .08), .024, material, 48);
    tube(g, line(1.45, 3.98, -.39), .012, mat.dim, 46);
    box(g, 0, .08, -.13, 3.71, .12, 1.35, mat.black);
    box(g, 0, .15, .46, 3.48, .025, .035, material);
    glow(g, 0, 2.5, -.59, 5.9, "#f05082", .72);
    g.userData.leaves = [-1, 1].map(sign => {
      const leaf = group(g, sign * 1.61, .16, -.13);
      box(leaf, -sign * .8, 1.72, -.045, 1.59, 3.44, .15, mat.column);
      box(leaf, -sign * .8, 1.69, .042, 1.32, 2.96, .024, mat.black);
      box(leaf, -sign * 1.42, 1.4, .075, .066, .39, .065, mat.warm);
      return { leaf, sign };
    });
    return g;
  }

  const lobby = stage("lobby");
  const entrances = ["work", "about", "knowledge"];
  for (let i = 0; i < entrances.length; i++) {
    const name = entrances[i];
    const x = (i - 1) * 5.16 * side;
    const g = portal(lobby, x, i === 1 ? -3.26 : -2.14, i === 1 ? mat.ivory : mat.coral);
    const icon = hit("lobby", name, group(g, 0, 2.09, .21), 111);
    if (i === 0) {
      const object = mesh(new OctahedronGeometry(.72), mat.facet, icon);
      object.rotation.set(.4, .4, .45);
      circle(icon, 0, 0, .08, .93, .018, mat.ivory).rotation.y = -.26;
    } else if (i === 1) {
      circle(icon, 0, 0, 0, .83, .027, mat.ivory).rotation.set(.19, .22, .4);
      circle(icon, 0, 0, 0, .66, .022, mat.gold).rotation.set(-.5, -.58, .2);
      mesh(new IcosahedronGeometry(.3, 0), mat.warm, icon);
    } else {
      for (const sign of [-1, 0, 1]) {
        const endpoint = V(sign * .72, .63 - Math.abs(sign) * .19, .2);
        tube(icon, [V(0, -.72, 0), V(0, -.33, 0), V(sign * .11, -.04, .1), endpoint], .025, mat.ivory);
        mesh(new OctahedronGeometry(.13), mat.coral, icon, endpoint.x, endpoint.y, endpoint.z);
      }
    }
    const path = [V(x, .028, -1.65), V(x, .028, .4), V(x * .74, .028, 2.52), V(x * .74, .028, 11)];
    stroke(lobby, path, i === 1 ? "#fca289" : "#c35974");
    if (i !== 1) stroke(lobby, path.map(p => p.clone().add(V(.35, 0, 0))), "#78394e");
  }
  box(lobby, 0, 5.2, -4, 16.4, .05, .18, mat.frame);
  box(lobby, 0, 5.17, -3.88, 16.45, .026, .04, mat.gold);
  glow(lobby, 0, .34, 1.1, 14, "#c5356a", .66);

  const exhibition = createProjectWalls(stage("work"), museum, side, { group, box, pedestal, point, glow, stroke });

  const bench = stage("about");
  pedestal(bench, 0, -.48, 4.85, .53);
  for (let i = 0; i < 4; i++) {
    const holder = hit("about", String(i + 1), group(bench, (i - 1.5) * 2.28, .54, i === 1 || i === 2 ? -.64 : -.1), 57);
    box(holder, 0, .12, 0, 1.87, .24, 1.67, mat.column);
    box(holder, 0, .252, .85, 1.77, .025, .02, mat.gold);
    glow(holder, 0, .91, -.17, 3.1, "#e6536f", .57);
    if (i === 0) {
      for (let sheet = 0; sheet < 4; sheet++) {
        const paper = box(holder, .05 * sheet, .42 + .08 * sheet, 0, 1.31, .047, 1.22, sheet === 3 ? mat.warm : mat.frame);
        paper.rotation.y = .15 * sheet;
      }
      for (let line = 0; line < 3; line++) box(holder, -.11, .695, -.21 + .19 * line, .62, .012, .025, mat.column);
    } else if (i === 1) {
      const screen = group(holder, 0, .96, -.04);
      screen.rotation.x = -.17;
      box(screen, 0, 0, 0, 1.59, 1.02, .12, mat.warm);
      box(screen, 0, 0, .077, 1.44, .88, .045, mat.black);
      box(screen, -.45, -.05, .112, .36, .57, .02, mat.facet);
      for (let line = 0; line < 4; line++) box(screen, .18, .23 - .15 * line, .63, .019, .04, mat.gold);
    } else if (i === 2) {
      const gem = mesh(new OctahedronGeometry(.62), mat.facet, holder, 0, 1.04);
      gem.rotation.set(.4, .26, .7);
      const ring = circle(holder, 0, .85, 0, .77, .021, mat.ivory);
      ring.rotation.x = .9;
    } else {
      for (let ring = 0; ring < 3; ring++) {
        const halo = circle(holder, 0, 1.05, ring * .13, .62 - ring * .11, .021, ring === 2 ? mat.ivory : mat.gold);
        halo.rotation.y = -.28;
      }
      mesh(new IcosahedronGeometry(.19, 1), mat.coral, holder, 0, 1.05, .49);
    }
  }

  const tree = stage("knowledge");
  pedestal(tree, 0, -.74, 2.34, .52);
  tube(tree, [V(0, .48, -.52), V(-.45, 1.35, -.52), V(-.22, 2.15, -.65), V(.18, 2.85, -.63), V(.08, 3.68, -.62)], .13, mat.frame);
  tube(tree, [V(.26, .52, -.5), V(.1, 1.35, -.58), V(-.16, 2.13, -.62), V(.04, 2.93, -.58)], .055, mat.coral);
  const branches = [
    ["design", V(-3.22, 3.45, .01)],
    ["engineering", V(.15, 5.0, -.42)],
    ["research", V(3.1, 3.26, .13)]
  ];
  for (const [key, tip] of branches) {
    const fork = V(tip.x * .52, tip.y - .45, tip.z - .27);
    tube(tree, [V(.03, key === "engineering" ? 2.87 : 2.12, -.57), fork, tip], .071, mat.warm);
    const jewel = hit("knowledge", key, group(tree, tip.x, tip.y, tip.z), 63);
    mesh(new IcosahedronGeometry(.39, 0), mat.facet, jewel);
    circle(jewel, 0, 0, 0, .63, .016, mat.ivory).rotation.y = .29;
    glow(jewel, 0, 0, -.28, 3.8, "#f95180", .65);
    for (let i = 0; i < 4; i++) {
      const sign = i % 2 ? -1 : 1;
      const leaf = tip.clone().add(V(sign * (.53 + .13 * i), .42 + .21 * i, (i - 1.5) * .24));
      tube(tree, [fork, tip.clone().lerp(leaf, .65), leaf], .018, i % 2 ? mat.dim : mat.gold, 12);
      mesh(new OctahedronGeometry(.105 + .025 * i), i % 2 ? mat.coral : mat.ivory, tree, leaf.x, leaf.y, leaf.z);
    }
  }
  for (let i = -2; i <= 2; i++) {
    tube(tree, [V(-.15, .82, -.48), V(i * .46, .57, -.33), V(i * .74, .54, .29)], .027, mat.gold, 13);
  }
  glow(tree, 0, 3.2, -1.23, 9, "#ba335f", .54);

  const archive = stage("experience");
  pedestal(archive, 0, -.65, 3);
  for (let i = 0; i < 5; i++) {
    const shelf = group(archive, (i - 2) * 1.15, 1.65 + (i % 3) * .31, -.3 - Math.abs(i - 2) * .19);
    shelf.rotation.y = (i - 2) * -.13;
    box(shelf, 0, 0, 0, .91, 2.08, .31, mat.column);
    box(shelf, 0, 0, .18, .77, 1.87, .06, mat.black);
    box(shelf, 0, .61, .218, .48, .055, .012, mat.ivory);
    for (let n = 0; n < 5; n++) box(shelf, -.06, .29 - n * .17, .217, (n % 2 ? .42 : .57), .023, .02, mat.gold);
  }
  glow(archive, 0, 2.6, -1.6, 8, "#f24c74", .63);

  const contact = stage("contact");
  pedestal(contact, 0, -.6, 2.9, .62);
  const sculpture = group(contact, 0, 2.5, -.45);
  art.contact = sculpture;
  circle(sculpture, -.63, 0, 0, 1.29, .056, mat.ivory).rotation.set(.1, -.31, .34);
  circle(sculpture, .62, 0, .05, 1.29, .063, mat.coral).rotation.set(-.28, .57, -.28);
  circle(sculpture, 0, 0, -.14, 1.92, .015, mat.gold);
  glow(sculpture, 0, 0, -.52, 8, "#e84873", .75);

  const position = V(0, 4, 17);
  const aim = V(0, 2.8, -.4);
  const view = { position: position.clone(), aim: aim.clone(), shift: 0 };
  let state, previousRoom, frame = 0, lastFrame = 0, previousTime = 0;
  let transition = 0;
  let currentWall, opening;
  let onScreen = true;
  let pointerX = 0;
  let fieldWidth = 0;
  let fieldHeight = 0;
  const world = V();
  const projected = V();

  function adjustCamera(immediate = false) {
    if (!state) return;
    const desktop = innerWidth >= 800;
    const aspect = fieldHeight ? fieldWidth / fieldHeight : 1.6;
    const portrait = aspect < 1;
    const narrowLobby = aspect < .75;
    if (state.room === "lobby") {
      lobby.scale.x = narrowLobby ? .79 : 1;
      const distance = narrowLobby ? Math.max(25, 6.25 / (Math.tan(Math.PI / 9) * aspect)) : portrait ? 24 : 16;
      position.set(pointerX * .38, narrowLobby ? 3.85 : 4.55, distance);
      aim.set(pointerX * .25, narrowLobby ? 3.64 : 4.02, -1.98);
      view.goalShift = 0;
    } else if (state.room === "work") {
      const narrow = aspect < .82;
      currentWall.layout(narrow);
      const fixture = state.exhibit && currentWall.fixtures.get(state.item);
      const target = fixture ? currentWall.wall.worldToLocal(fixture.object.getWorldPosition(world)) : V(0, 2.42, -4.25);
      const span = (state.wall === "galleries" ? 6.9 : 9.6) * (narrow ? .81 : 1);
      const dist = fixture ? (narrow ? 9 : 8) : Math.max(13.5, span / (Math.tan(Math.PI / 9) * aspect) - 4.1);
      position.copy(currentWall.wall.localToWorld(V(target.x + pointerX * .27, fixture ? target.y + .9 : 4.4, dist)));
      aim.copy(currentWall.wall.localToWorld(V(target.x + pointerX * .19, target.y, target.z)));
      view.goalShift = fixture && desktop ? -side * 5 : 0;
    } else {
      const selected = clicks[state.room].find(pick => pick.slug === state.item);
      const focus = selected && state.focused;
      const x = focus ? selected.object.getWorldPosition(world).x : 0;
      const y = focus ? Math.max(1.75, world.y) : (state.room === "knowledge" ? 2.92 : 1.95);
      const dist = focus ? (portrait ? 9.3 : 8.65) : (portrait ? 14.2 : 12.5);
      position.set(x + pointerX * .39, y + 1.65, dist);
      aim.set(x + pointerX * .23, y, -.45);
      view.goalShift = desktop ? -side * Math.min(10.2, 8.4 + fieldWidth / 750) : 0;
    }
    if (immediate) {
      view.position.copy(position);
      view.aim.copy(aim);
      view.shift = view.goalShift;
    }
  }

  function resize() {
    const { clientWidth, clientHeight } = canvas;
    if (clientWidth < 2 || clientHeight < 2) return;
    fieldWidth = clientWidth;
    fieldHeight = clientHeight;
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, fieldWidth < 820 ? 1.3 : 1.65));
    renderer.setSize(clientWidth, clientHeight, false);
    camera.aspect = clientWidth / clientHeight;
    adjustCamera(true);
    draw(performance.now(), true);
  }

  function draw(time, force = false) {
    const dt = Math.min(64, time - previousTime || 16);
    previousTime = time;
    const easing = force || motion.matches ? 1 : 1 - Math.exp(-dt / 145);
    view.position.lerp(position, easing);
    view.aim.lerp(aim, easing);
    view.shift += (view.goalShift - view.shift) * easing;
    camera.position.copy(view.position);
    camera.filmOffset = view.shift;
    camera.lookAt(view.aim);
    camera.updateProjectionMatrix();

    const t = motion.matches ? 0 : time * .001;
    ambient.intensity = 139 + 16 * Math.sin(t * .84);
    for (const { object } of clicks.lobby) {
      const gate = object.parent;
      for (const { leaf, sign } of gate.userData.leaves) {
        const angle = gate === opening ? sign * 1.24 : 0;
        leaf.rotation.y += (angle - leaf.rotation.y) * (force || motion.matches ? 1 : .18);
      }
    }
    art.contact.rotation.y = t * .16;
    for (const pick of clicks.knowledge) {
      const emph = state.room === "knowledge" && state.item === pick.slug;
      pick.object.rotation.y = t * .23 * (emph ? 1.5 : .7);
      pick.object.scale.setScalar(emph ? 1.14 : 1);
    }
    for (const pick of clicks.about) {
      const emph = state.room === "about" && state.item === pick.slug;
      pick.object.position.y = .54 + (emph ? .15 + .045 * Math.sin(t * 1.6) : 0);
    }
    renderer.render(scene, camera);
  }

  function loop(time) {
    frame = 0;
    if (!onScreen || document.hidden || motion.matches) return;
    if (time - lastFrame > 30) {
      draw(time);
      lastFrame = time;
    }
    frame = requestAnimationFrame(loop);
  }

  function resume() {
    if (motion.matches) {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      draw(performance.now(), true);
    } else if (!frame && onScreen && !document.hidden) {
      frame = requestAnimationFrame(loop);
    }
  }

  function present(detail) {
    const changed = detail.room !== previousRoom || (detail.room === "work" && state?.wall !== detail.wall);
    state = detail;
    opening = undefined;
    shell.visible = state.room !== "work";
    scene.fog.near = state.room === "work" ? 27 : 16;
    scene.fog.far = state.room === "work" ? 75 : 49;
    if (state.room === "work") currentWall = exhibition.show(state.wall || "devices");
    for (const [name, root] of Object.entries(roots)) root.visible = state.room === name;
    if (changed && previousRoom && !motion.matches) {
      canvas.getAnimations().forEach(animation => animation.cancel());
      canvas.animate([{ opacity: .34 }, { opacity: 1 }], { duration: 460, easing: "ease-out" });
    }
    previousRoom = state.room;
    adjustCamera(!fieldWidth || motion.matches);
    resume();
  }

  function update(detail) {
    clearTimeout(transition);
    const entrance = previousRoom === "lobby" && clicks.lobby.find(item => item.slug === detail.room);
    if (entrance && !motion.matches && onScreen) {
      opening = entrance.object.parent;
      const door = entrance.object.getWorldPosition(world);
      position.set(door.x * .77, 3.2, view.position.z * .66);
      aim.set(door.x, door.y, door.z);
      canvas.getAnimations().forEach(animation => animation.cancel());
      canvas.animate([{ opacity: 1 }, { opacity: .34 }], { duration: 265, fill: "forwards" });
      transition = setTimeout(() => {
        transition = 0;
        present(detail);
      }, 250);
    } else {
      transition = 0;
      canvas.getAnimations().forEach(animation => animation.cancel());
      present(detail);
    }
  }

  function pick(event) {
    if (!state || !fieldWidth || transition || (state.room === "work" && state.exhibit)) return null;
    const box = canvas.getBoundingClientRect();
    let result = null;
    let nearest = Infinity;
    const picks = state.room === "work" ? currentWall.fixtures.values() : clicks[state.room];
    for (const item of picks) {
      item.object.getWorldPosition(projected).project(camera);
      const x = box.left + (projected.x + 1) * box.width / 2;
      const y = box.top + (1 - projected.y) * box.height / 2;
      const distance = Math.hypot(event.clientX - x, event.clientY - y);
      if (distance < item.radius && distance < nearest) {
        result = item;
        nearest = distance;
      }
    }
    return result;
  }

  canvas.addEventListener("pointermove", event => {
    const rect = canvas.getBoundingClientRect();
    if (!transition && !motion.matches && event.pointerType === "mouse") {
      pointerX = (event.clientX - rect.left) / rect.width * 2 - 1;
      adjustCamera();
    }
    canvas.style.cursor = pick(event) ? "pointer" : "";
  });
  canvas.addEventListener("pointerleave", () => {
    pointerX = 0;
    if (!transition) adjustCamera();
  });
  canvas.addEventListener("click", event => {
    const item = pick(event);
    if (item) museum.dispatchEvent(new CustomEvent("museum:pick", {
      detail: state.room === "lobby" ? item.slug : state.room + "/" + item.slug
    }));
  });
  canvas.addEventListener("webglcontextlost", event => {
    event.preventDefault();
    museum.classList.remove("has-scene");
    onScreen = false;
  });
  canvas.addEventListener("webglcontextrestored", () => {
    museum.classList.add("has-scene");
    onScreen = true;
    resize();
    resume();
  });

  museum.addEventListener("museum:state", event => update(event.detail));
  museum.addEventListener("museum:surface", resume);
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(([entry]) => {
    onScreen = entry.isIntersecting;
    if (onScreen) resume();
  }).observe(canvas);
  document.addEventListener("visibilitychange", resume);
  motion.addEventListener("change", () => { adjustCamera(true); resume(); });
  update(museum.museumState());
  resize();
  museum.classList.add("has-scene");
}
