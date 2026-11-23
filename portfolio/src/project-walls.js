import {
  BoxGeometry, CylinderGeometry, Mesh, MeshBasicMaterial, MeshStandardMaterial,
  PlaneGeometry, SphereGeometry, SRGBColorSpace, TextureLoader, TorusGeometry, Vector3
} from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

const WALLS = {
  devices: { angle: 0, slugs: ["tamassak", "luqata", "majarat-noor", "tamakkan"] },
  galleries: { angle: -Math.PI / 2, slugs: ["rehlati", "unibites"] },
  stands: { angle: Math.PI / 2, slugs: ["movie-cave", "clothing-advice", "robolux", "rawaa-othman", "talaqa"] }
};

export function createProjectWalls(root, museum, side, { group, box, pedestal, point, glow, stroke }) {
  const vec = (x, y, z) => new Vector3(x, y, z);
  const steel = new MeshStandardMaterial({ color: "#b2aeb6", roughness: .28, metalness: .76 });
  const edge = new MeshStandardMaterial({ color: "#6a5666", roughness: .31, metalness: .75 });
  const graphite = new MeshStandardMaterial({ color: "#17151d", roughness: .37, metalness: .57 });
  const keycap = new MeshStandardMaterial({ color: "#3b3542", roughness: .62 });
  const glass = new MeshBasicMaterial({ color: "#1b1422" });
  const rose = new MeshStandardMaterial({ color: "#552238", roughness: .45, metalness: .28 });
  const wallFloor = new MeshStandardMaterial({ color: "#42212d", roughness: .61, metalness: .23 });
  const light = new MeshBasicMaterial({ color: "#ffc2a2" });
  const sign = new MeshStandardMaterial({ color: "#b67d7b", roughness: .5, metalness: .45 });
  const loader = new TextureLoader();

  function object(parent, geometry, material, x, y, z) {
    const mesh = new Mesh(geometry, material);
    mesh.position.set(x, y, z);
    parent.add(mesh);
    return mesh;
  }

  function rounded(parent, x, y, z, width, height, depth, radius, material) {
    return object(parent, new RoundedBoxGeometry(width, height, depth, 3, radius), material, x, y, z);
  }

  function screen(parent, slug, width, height, depth) {
    object(parent, new PlaneGeometry(width, height), glass, 0, 0, depth);
    const poster = museum.querySelector('[href="#work/' + slug + '"]')?.dataset.surface;
    if (!poster) return;
    loader.load(poster, texture => {
      texture.colorSpace = SRGBColorSpace;
      const imageRatio = texture.image.width / texture.image.height;
      const visibleWidth = Math.min(width * .99, height * imageRatio);
      const visibleHeight = visibleWidth / imageRatio;
      const material = new MeshBasicMaterial({ map: texture, toneMapped: false });
      object(parent, new PlaneGeometry(visibleWidth, visibleHeight), material, 0, 0, depth + .004);
      museum.dispatchEvent(new Event("museum:surface"));
    });
  }

  function desktop(parent, slug) {
    rounded(parent, 0, .64, -.19, .31, .82, .22, .065, steel);
    rounded(parent, 0, .19, -.15, 1.17, .12, .66, .056, steel);
    const display = group(parent, 0, 1.65, -.24);
    rounded(display, 0, 0, 0, 3.53, 2.16, .22, .084, edge);
    rounded(display, 0, .03, .105, 3.41, 2.02, .043, .02, graphite);
    screen(display, slug, 3.24, 1.85, .132);
    box(display, 0, -1.015, .13, .15, .022, .009, light);
    const keyboard = group(parent, -.34, .145, .75);
    rounded(keyboard, 0, 0, 0, 1.71, .09, .51, .041, steel);
    const key = new BoxGeometry(.112, .032, .083);
    for (let row = 0; row < 4; row++) {
      for (let col = 0; col < 12; col++) object(keyboard, key, keycap, (col - 5.5) * .127, .053, (row - 1.5) * .103);
    }
    object(parent, new SphereGeometry(.15, 18, 12), graphite, .82, .17, .73).scale.set(.78, .53, 1.26);
    return display;
  }

  function mobile(parent, slug, tablet) {
    const width = tablet ? 3.12 : 1.32;
    const height = tablet ? 2.27 : 2.59;
    const body = group(parent, 0, height / 2 + .19, -.05);
    body.rotation.x = -.11;
    rounded(body, 0, 0, 0, width, height, .18, tablet ? .082 : .087, steel);
    rounded(body, 0, 0, .087, width - .067, height - .065, .035, .017, graphite);
    screen(body, slug, width - (tablet ? .2 : .13), height - .19, .111);
    if (tablet) box(body, 0, height / 2 - .046, .112, .035, .035, .009, glass);
    else rounded(body, 0, height / 2 - .123, .122, .24, .061, .018, .008, graphite);
    box(body, width / 2, .42, 0, .04, .23, .06, edge);
    rounded(parent, 0, .11, .24, width * .58, .13, .49, .06, steel);
    return body;
  }

  function board(parent, slug) {
    for (const x of [-1.61, 1.61]) box(parent, x, .82, -.19, .1, 1.67, .16, steel);
    const display = group(parent, 0, 2.38, -.09);
    rounded(display, 0, 0, 0, 4.4, 2.66, .18, .075, edge);
    rounded(display, 0, 0, .085, 4.22, 2.51, .038, .018, graphite);
    screen(display, slug, 4.03, 2.34, .111);
    return display;
  }

  function plinthStand(parent) {
    rounded(parent, 0, .08, .15, 1.51, .14, .89, .055, graphite);
    object(parent, new CylinderGeometry(.073, .11, 1.34, 14), steel, 0, .77, .04);
    const lectern = group(parent, 0, 1.53, .06);
    lectern.rotation.x = -.42;
    rounded(lectern, 0, 0, 0, 1.65, 1.1, .12, .052, edge);
    box(lectern, 0, 0, .065, 1.49, .94, .02, sign);
    for (let i = 0; i < 4; i++) box(lectern, 0, .26 - i * .154, .08, i === 3 ? .67 : 1, .013, .012, graphite);
    return lectern;
  }

  function closed(parent) {
    rounded(parent, 0, .83, -.06, 2.51, 1.51, 1.61, .075, graphite);
    box(parent, 0, .3, .76, 2.46, .025, .025, edge);
    const loop = object(parent, new TorusGeometry(.136, .025, 8, 26, Math.PI), steel, 0, .85, .763);
    loop.rotation.z = 0;
    rounded(parent, 0, .733, .782, .34, .23, .06, .029, steel);
  }

  box(root, 0, -.15, 0, 43, .28, 43, wallFloor);
  for (let x = -15; x <= 15; x += 2.6) {
    stroke(root, [vec(x, .002, -16), vec(x, .002, 16)], "#74364b");
    stroke(root, [vec(-16, .002, x), vec(16, .002, x)], "#64324a");
  }

  const walls = new Map();
  for (const [key, { angle, slugs }] of Object.entries(WALLS)) {
    const wall = group(root);
    wall.rotation.y = angle;
    const displays = group(wall, 0, 0, -4.25);
    const fixtures = new Map();
    const positions = [];
    box(wall, 0, 3.4, -6.1, 22, 6.8, .22, rose);
    box(wall, 0, .15, -5.94, 21.9, .06, .105, light);
    box(wall, 0, 5.6, -5.94, 21.9, .045, .105, light);
    for (let x = -10.5; x <= 10.5; x += 3.5) {
      box(wall, x, 3.05, -5.95, .085, 6.1, .11, edge);
    }
    const spot = point("#ff87a5", 155, 24, vec(0, 5.8, .65), wall);
    spot.intensity = key === "stands" ? 108 : 178;
    const spacing = key === "devices" ? 4.48 : key === "galleries" ? 5.65 : 3.05;
    slugs.forEach((slug, i) => {
      const position = (i - (slugs.length - 1) / 2) * spacing * side;
      const base = group(displays, position, 0, 0);
      positions.push({ base, position });
      const p = key === "stands" ? base : group(pedestal(base, 0, 0, key === "galleries" ? 1.85 : 1.47, .65), 0, .65, 0);
      glow(base, 0, 1.8, -.42, 4.4, "#db386b", .48);
      let target;
      switch (slug) {
        case "tamassak": target = desktop(p, slug); break;
        case "luqata": target = mobile(p, slug, false); break;
        case "majarat-noor": target = mobile(p, slug, true); break;
        case "tamakkan": closed(p); return;
        default: target = key === "galleries" ? board(p, slug) : plinthStand(p); break;
      }
      fixtures.set(slug, { slug, object: target, radius: key === "galleries" ? 83 : 64 });
    });
    walls.set(key, {
      wall, fixtures, angle,
      layout(narrow) {
        for (const entry of positions) entry.base.position.x = entry.position * (narrow ? .76 : 1);
      }
    });
  }

  return {
    show(key) {
      for (const [name, state] of walls) state.wall.visible = name === key;
      return walls.get(key) || walls.get("devices");
    }
  };
}
