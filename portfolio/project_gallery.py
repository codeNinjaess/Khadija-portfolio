"""Render the exhibition walls and their bilingual media viewers."""
from base64 import b64encode
from pathlib import Path

from content import ADDITIONAL, PROJECTS

ASSETS = Path(__file__).resolve().parent / "dist" / "assets" / "projects"
EXHIBITS = {
    project["slug"]: (project["name"], project["type"], project["summary"], project)
    for project in PROJECTS
}
EXHIBITS.update({slug: (name, kind, summary, None) for slug, name, kind, summary in ADDITIONAL})

WALLS = (
    ("devices", ("أجهزة العرض", "Device wall"), ("tamassak", "luqata", "majarat-noor", "tamakkan")),
    ("galleries", ("لوحات النماذج", "Prototype wall"), ("rehlati", "unibites")),
    ("stands", ("أجنحة المشاريع", "Project stands"), ("movie-cave", "clothing-advice", "robolux", "rawaa-othman", "talaqa")),
)

MODELS = {
    "tamassak": "desktop",
    "luqata": "phone",
    "majarat-noor": "tablet",
    "rehlati": "board",
    "unibites": "board",
}

# Each resource is a video with its poster, or a set of individual images.
RESOURCES = {
    "tamassak": (
        ("gameplay", ("لقطات من اللعبة", "Gameplay footage"), "video", "gameplay.mp4"),
    ),
    "luqata": (
        ("screens", ("شاشات التطبيق", "App screenshots"), "gallery", "screen-*.webp"),
    ),
    "majarat-noor": (
        ("part-1", ("الفيديو · الجزء الأول", "Video · Part one"), "video", "part-1.mp4"),
        ("part-2", ("الفيديو · الجزء الثاني", "Video · Part two"), "video", "part-2.mp4"),
    ),
    "rehlati": (
        ("walkthrough", ("جولة في النموذج الرقمي", "Digital prototype walkthrough"), "video", "walkthrough.mp4"),
        ("handmade", ("صور النموذج اليدوي", "Handmade prototype photos"), "gallery", "handmade-*.webp"),
    ),
    "unibites": (
        ("cover", ("صورة المشروع", "Project image"), "gallery", "cover.webp"),
        ("trailer", ("الفيديو التشويقي", "Trailer"), "video", "trailer.mp4"),
    ),
}


def local_asset(page, path):
    return page.asset("projects/" + path.relative_to(ASSETS).as_posix())


def asset_list(slug, pattern):
    return sorted((ASSETS / slug).glob(pattern))


def cover_for(slug):
    for _, _, kind, pattern in RESOURCES.get(slug, ()):
        if kind == "video":
            pattern = Path(pattern).stem + "-poster.webp"
        images = asset_list(slug, pattern)
        if images:
            return images[0]
    return None


def gallery(page, images, label):
    figures = "".join(
        f'<figure data-slide><img src="{local_asset(page, path)}" alt="{label} {index}" loading="lazy" decoding="async"></figure>'
        for index, path in enumerate(images, 1)
    )
    if len(images) < 2:
        return f'<div class="resource-slides">{figures}</div>'
    t = page.t
    return f"""
<div class="resource-carousel" data-carousel>
  <div class="resource-slides">{figures}</div>
  <div class="resource-arrows">
    <button type="button" data-slide-step="-1" aria-label="{t("الصورة السابقة", "Previous image")}"><span aria-hidden="true">←</span></button>
    <span data-slide-count aria-live="polite" dir="ltr">1 / {len(images)}</span>
    <button type="button" data-slide-step="1" aria-label="{t("الصورة التالية", "Next image")}"><span aria-hidden="true">→</span></button>
  </div>
</div>"""


def viewer(page, slug):
    t, copy = page.t, page.copy
    options, panes = [], []
    for key, title, kind, pattern in RESOURCES.get(slug, ()):
        files = asset_list(slug, pattern)
        if not files:
            continue
        label = copy(title)
        options.append(f'<button type="button" data-open-resource="{key}">{label}</button>')
        if kind == "video":
            source = files[0]
            poster = source.with_name(source.stem + "-poster.webp")
            poster_attr = f' poster="{local_asset(page, poster)}"' if poster.is_file() else ""
            body = f'<video controls playsinline preload="none"{poster_attr} src="{local_asset(page, source)}" aria-label="{label}"></video>'
        else:
            body = gallery(page, files, label)
        panes.append((key, label, body))

    if not panes:
        return ""
    multiple = len(panes) > 1
    menu = f'<div class="screen-menu" data-resource-menu>{"".join(options)}</div>' if multiple else ""
    back = f'\n  <button class="screen-back" type="button" data-resource-back>{t("العودة إلى الموارد", "Back to resources")}</button>' if multiple else ""
    resources = "".join(f"""
<section class="screen-resource" data-resource="{key}" aria-label="{label}">{back}
  <div class="screen-content">{body}</div>
</section>""" for key, label, body in panes)
    return f"""
<div class="device-viewer device-{MODELS[slug]}" data-device>
  <div class="device-chassis">
    <div class="device-screen">{menu}{resources}
    </div>
  </div>
</div>"""


def exhibit(page, wall, slug):
    t, copy = page.t, page.copy
    name, kind, summary, case = EXHIBITS[slug]
    media = viewer(page, slug)
    case_link = (
        f' <a class="project-case-link" href="{page.project_url(case)}">{t("قراءة دراسة الحالة", "Read case study")}</a>'
        if case else ""
    )
    return f"""
<article class="project-focus{" text-exhibit" if not media else ""}" data-detail="{slug}" data-wall="{wall}" data-exhibit id="work/{slug}" aria-labelledby="focus-{slug}">
  <div class="project-caption">
    <p class="project-kind">{copy(kind)}</p>
    <h3 id="focus-{slug}" tabindex="-1">{copy(name)}</h3>
    <p class="project-summary">{copy(summary)}</p>
    <a class="project-case-link exhibit-wall-back" href="#work/{wall}" data-route>{t("العودة إلى الجدار", "Back to wall")}</a>{case_link}
  </div>{media}
</article>"""


def wall_overview(page, wall, slugs):
    t, copy = page.t, page.copy
    panels = []
    for slug in slugs:
        if slug == "tamakkan":
            panels.append(f"""
<div class="project-plaque exhibit-locked">
  <strong>{t("تمكّن", "Tamakkan")}</strong><small><i class="lock-icon" aria-hidden="true"></i>{t("قريبًا", "Coming soon")}</small>
</div>""")
            continue
        image = cover_for(slug)
        thumb = image.with_name("thumb.webp") if image else None
        has_thumb = thumb is not None and thumb.is_file()
        thumbnail = f'<img src="{local_asset(page, thumb if has_thumb else image)}" alt="" loading="lazy" decoding="async">' if image else ""
        surface = f' data-surface="data:image/webp;base64,{b64encode(thumb.read_bytes()).decode()}"' if has_thumb else ""
        panels.append(f"""
<a class="project-plaque" href="#work/{slug}" data-route{surface}>{thumbnail}<strong>{copy(EXHIBITS[slug][0])}</strong></a>""")
    return f"""
<div class="project-overview" data-detail="{wall}" data-wall="{wall}" id="work/{wall}">
  <nav class="project-wall" aria-label="{t("معروضات الجدار", "Wall exhibits")}">{"".join(panels)}
  </nav>
</div>"""


def render_project_gallery(page):
    t, copy = page.t, page.copy
    nav = "".join(f'<a href="#work/{wall}" data-route>{copy(name)}</a>' for wall, name, _ in WALLS)
    displays = "".join(
        wall_overview(page, wall, slugs)
        + "".join(exhibit(page, wall, slug) for slug in slugs if slug != "tamakkan")
        for wall, _, slugs in WALLS
    )
    return f"""
<section id="work" class="museum-room project-gallery" data-room="work" aria-labelledby="work-title">
  <div class="project-heading">
    <h2 id="work-title" class="museum-title projects-title" tabindex="-1">{t("المشاريع", "Projects")}</h2>
    <nav class="project-wall-picker" aria-label="{t("جدران المتحف", "Museum walls")}">{nav}</nav>
  </div>
  <div class="project-showcase">{displays}
  </div>
</section>"""
