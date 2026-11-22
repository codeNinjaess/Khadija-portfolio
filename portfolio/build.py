"""Generate the Arabic and English static pages into dist."""
from html import escape
from os import environ
from pathlib import Path
from posixpath import relpath
import re

from content import ADDITIONAL, EXPERIENCE, PAPER, PHASES, PROJECTS, RECOGNITION

OUT = Path(__file__).resolve().parent / "dist"
BASE_URL = environ.get("PORTFOLIO_BASE_URL", "").rstrip("/")
LINKEDIN = "https://www.linkedin.com/in/khaditheeng/"
GITHUB = "https://github.com/codeNinjaess"
NAV = [
    ("work", ("الأعمال", "Work")), ("experience", ("الخبرة", "Experience")),
    ("about", ("عنّي", "About")), ("contact", ("تواصل", "Contact"))
]
FIELDS = [
    ("المشكلة", "Problem"), ("الجمهور", "Audience"), ("حالة المشروع", "Project status"),
    ("مساهمتي", "My contribution"), ("قرار في التصميم", "A design decision"), ("النتيجة", "Documented outcome")
]


class Page:
    def __init__(self, language, project=None):
        self.language = language
        self.en = int(language == "en")
        self.project = project
        self.stem = "en/" if self.en else ""
        self.path = self.stem + (f"work/{project['slug']}/" if project else "")
        self.home = self.url(self.stem)

    def t(self, arabic, english):
        return self.copy((arabic, english))

    def copy(self, pair):
        value = escape(pair[self.en])
        if self.en:
            return value
        return re.sub(r"[A-Za-z][A-Za-z0-9#+'-]*(?:[ .-][A-Za-z][A-Za-z0-9#+'-]*)*",
                      lambda match: f'<bdi lang="en" dir="ltr">{match[0]}</bdi>', value)

    def url(self, path):
        target = path + "index.html" if not path or path.endswith("/") else path
        return relpath(target, self.path or ".")

    def asset(self, name):
        return self.url("assets/" + name)

    def project_url(self, project):
        return self.url(self.stem + "work/" + project["slug"] + "/")

    def logo(self, cream=True):
        color = "cream" if cream else "burgundy"
        return f'<img src="{self.asset(f"logo-{color}-300.webp")}" alt="{self.t("خديجة الأنصاري", "Khadija Al-Ansari")}" width="300" height="111">'

    def header(self):
        switch = ("en/" if not self.en else "") + self.path.removeprefix(self.stem)
        label = "العربية" if self.en else "English"
        other = "ar" if self.en else "en"
        nav = "".join(f'<a href="{self.home}#{anchor}">{self.copy(label)}</a>' for anchor, label in NAV)
        return f"""
<a class="skip" href="#main">{self.t("انتقل إلى المحتوى", "Skip to content")}</a>
<header class="masthead dark">
  <div class="wrap masthead-inner">
    <a class="brand" href="{self.home}">{self.logo()}</a>
    <nav aria-label="{self.t("التنقّل الرئيسي", "Main navigation")}">{nav}</nav>
    <a class="language" data-language href="{self.url(switch)}" lang="{other}" hreflang="{other}" dir="auto">{label}</a>
  </div>
</header>"""

    def footer(self):
        return f"""
<footer class="contact dark" id="contact">
  <div class="wrap contact-inner">
    <div>
      <p class="eyebrow">{self.t("تواصل", "Contact")}</p>
      <h2>{self.t("لنبنِ شيئًا معًا.", "Let’s build something.")}</h2>
      <p>{self.t("للفرص المهنية والتعاون، يسعدني التواصل عبر لينكدإن.", "For roles and collaborations, reach out on LinkedIn.")}</p>
      <div class="contact-links">
        <a class="button" href="{LINKEDIN}" lang="en" dir="ltr">LinkedIn</a>
        <a class="button outline" href="{GITHUB}" lang="en" dir="ltr">GitHub</a>
      </div>
    </div>
    <a class="footer-logo" href="{self.home}">{self.logo()}</a>
  </div>
  <div class="wrap footer-line"><span>{self.t("خديجة الأنصاري", "Khadija Al-Ansari")}</span><span>{self.t("الرياض، السعودية", "Riyadh, Saudi Arabia")}</span></div>
</footer>"""

    def hero(self):
        mobile = f'{self.asset("hero-mobile-560.webp")} 560w, {self.asset("hero-mobile-1122.webp")} 1122w'
        desktop = f'{self.asset("hero-desktop-960.webp")} 960w, {self.asset("hero-desktop-1672.webp")} 1672w'
        return f"""
<section class="hero dark" aria-labelledby="hero-title">
  <picture class="hero-art">
    <source media="(max-width: 799px)" width="1122" height="1402" srcset="{mobile}" sizes="100vw">
    <img src="{self.asset("hero-desktop-1672.webp")}" srcset="{desktop}" sizes="(min-width: 1500px) 1500px, 100vw"
         width="1672" height="941" alt="" fetchpriority="high">
  </picture>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="eyebrow location"><span aria-hidden="true"></span>{self.t("الرياض، السعودية", "Riyadh, Saudi Arabia")}</p>
      <h1 id="hero-title">{self.t("خديجة الأنصاري", "Khadija Al‑Ansari")}</h1>
      <p class="role">{self.t("مهندسة برمجيات | تطبيقات الذكاء الاصطناعي وتجربة المستخدم", "Software Engineer | AI Applications & User Experience")}</p>
      <p class="hero-description">{self.t("أطوّر تطبيقات برمجية توظّف الذكاء الاصطناعي وتحول الأفكار إلى تجارب تفاعلية.", "I build software that puts AI to work and turns ideas into interactive experiences.")}</p>
      <a class="button" href="#work">{self.t("مشاهدة المشاريع", "View projects")}</a>
    </div>
  </div>
</section>"""

    def diagram(self, project):
        slug = project["slug"]
        flow = "".join(f'<li>{self.copy(item)}</li>' for item in project["flow"])
        motif = {
            "majarat-noor": '<div class="orbit"><i></i><i></i><i></i></div>',
            "luqata": '<div class="match"><i></i><i></i><i></i></div>'
        }[slug]
        return f"""
<figure class="diagram {slug}">
  <div class="motif" aria-hidden="true">{motif}</div>
  <figcaption>{self.t("مخطط مفاهيمي", "Concept diagram")}</figcaption>
  <ol>{flow}</ol>
</figure>"""

    def tags(self, project):
        items = "".join(f'<li lang="en" dir="ltr">{escape(tag)}</li>' for tag in project["tags"])
        return f'<ul class="tags">{items}</ul>'

    def work(self):
        cards = "".join(f"""
<article class="project-card">
  {self.diagram(project)}
  <div class="project-copy">
    <p class="eyebrow">{self.copy(project["type"])}</p>
    <h3>{self.copy(project["name"])}</h3>
    <p class="project-tagline">{self.copy(project["tagline"])}</p>
    <p>{self.copy(project["summary"])}</p>
    {self.tags(project)}
    <a class="text-link" href="{self.project_url(project)}">{self.t("دراسة الحالة", "Read case study")}<span class="sr-only"> · {self.copy(project["name"])}</span></a>
  </div>
</article>""" for project in PROJECTS)
        more = "".join(f'<li><h4>{self.copy(name)}</h4><p class="eyebrow">{self.copy(kind)}</p><p>{self.copy(summary)}</p></li>'
                       for name, kind, summary in ADDITIONAL)
        return f"""
<section id="work" class="section wrap">
  <div class="section-title"><h2>{self.t("أعمال مختارة", "Selected work")}</h2></div>
  <div class="projects">
    <article class="project-card locked">
      <h3>{self.t("تمكّن", "Tamakkan")}</h3>
      <p class="coming-soon"><span class="lock-icon" aria-hidden="true"></span>{self.t("قريبًا", "Coming soon")}</p>
    </article>{cards}
  </div>
  <div class="additional"><h3>{self.t("أعمال أخرى", "More work")}</h3><ul>{more}</ul></div>
</section>"""

    def experience(self):
        jobs = "".join(f"""
<article class="job">
  <div><p class="eyebrow">{self.copy(date)}</p><h3>{self.copy(name)}</h3><p class="job-role">{self.copy(role)}</p></div>
  <p>{self.copy(summary)}</p>
</article>""" for name, role, date, summary in EXPERIENCE)
        honors = "".join(f'<li><h4>{self.copy(name)}</h4><p>{self.copy(summary)}</p>' +
                         (f'<a class="text-link" href="{url}">{self.t("عن الفعالية", "Event details") if "hackathon" in url else self.t("عن البرنامج", "Program details")}<span class="sr-only"> · {self.copy(name)}</span></a>' if url else "") +
                         '</li>' for name, summary, url in RECOGNITION)
        return f"""
<section id="experience" class="section experience">
  <div class="wrap">
    <div class="section-title"><h2>{self.t("الخبرة", "Experience")}</h2></div>
    <div class="jobs">{jobs}</div>
    <div class="research">
      <p class="eyebrow">{self.t("بحث · نسخة أولية على arXiv", "Research · arXiv preprint")}</p>
      <h3 lang="en" dir="ltr">{escape(PAPER)}</h3>
      <p>{self.t("مؤلفة مشاركة في دراسة تقارن أنظمة التعرّف الضوئي على الحروف في الوثائق العربية والإنجليزية والفرنسية. ساهمت في كتابة المسودة ودمج نتائج التجارب.", "I co-authored a study comparing OCR systems for Arabic, English, and French documents. I contributed to drafting and incorporating experimental results.")}</p>
      <a class="text-link" href="https://arxiv.org/abs/2610.25235">{self.t("قراءة البحث على arXiv", "Read the preprint")}</a>
    </div>
    <div class="recognition"><h3>{self.t("التعليم والتكريم", "Education & recognition")}</h3><ul>{honors}</ul></div>
  </div>
</section>"""

    def about(self):
        phases = "".join(f"""
<li class="phase" id="phase-{i + 1}">
  <span class="phase-index" aria-hidden="true">{i + 1:02}</span>
  <div><h3>{self.copy(title)}</h3><p>{self.copy(example)}</p></div>
</li>""" for i, (title, example) in enumerate(PHASES))
        nodes = "".join(f'<a href="#phase-{i + 1}" data-phase="{i}" aria-label="{self.copy(title) if self.en else escape(title[0])}">{i + 1:02}</a>'
                        for i, (title, _) in enumerate(PHASES))
        return f"""
<section id="about" class="section wrap">
  <div class="section-title"><h2>{self.t("كيف أعمل", "How I work")}</h2><p>{self.t("أربع مراحل من دورة حياة تطوير البرمجيات، مع مثال من عملي في كل مرحلة.", "Four phases of the software development lifecycle, each with an example from my work.")}</p></div>
  <div class="process">
    <div class="process-art dark">
      <img src="{self.asset("hero-desktop-960.webp")}" width="960" height="540" loading="lazy" alt="">
      <nav class="phase-map" aria-label="{self.t("خريطة مراحل التطوير", "Development phase map")}"><div class="map-plane">{nodes}</div></nav>
    </div>
    <ol class="phases">{phases}</ol>
  </div>
  <div class="about-grid">
    <article><h3>{self.t("عنّي خارج التقنية", "Beyond tech")}</h3>
      <p>{self.t("أحب الألعاب والتصميم ثلاثي الأبعاد والروبوتات. وفي أوقات الهدوء أقرأ الروايات، وأكتب القصص، وأستمتع بالإعراب.", "I enjoy games, 3D design, and robotics. In quieter moments I read novels, write stories, and enjoy working through Arabic grammar.")}</p>
    </article>
    <article><h3>{self.t("ما أتعلمه", "What I’m learning")}</h3>
      <p>{self.t("أكملت دورات في مهارات الوكلاء وتصميم الأنظمة الوكيلة باستخدام LangChain وهندسة الأوامر.", "I completed courses in agent skills, agentic system design with LangChain, and prompt engineering.")}</p>
      <p>{self.t("أستكشف التوليد المعزَّز بالاسترجاع (RAG) وبروتوكول سياق النموذج (MCP)، وأواصل برنامج الذكاء الاصطناعي في أكاديمية كاوست.", "I’m exploring retrieval-augmented generation (RAG) and the Model Context Protocol (MCP), and continuing KAUST Academy’s AI program.")}</p>
    </article>
    <article><h3>{self.t("أدوات أستخدمها", "Tools I use")}</h3>
      <p>{self.t("أستخدم Figma للتصميم، وFlutter وUnity للتطوير، وPython وNeo4j لتطبيقات الذكاء الاصطناعي والبيانات.", "I use Figma for design, Flutter and Unity for development, and Python and Neo4j for AI and data work.")}</p>
    </article>
  </div>
</section>"""

    def case_study(self):
        project = self.project
        fields = "".join(f'<div><dt>{self.copy(label)}</dt><dd>{self.copy(value)}</dd></div>'
                         for label, value in zip(FIELDS, project["details"], strict=True))
        credits = f'<p class="credits">{self.copy(project["credits"])}</p>' if "credits" in project else ""
        alternate = "".join(f'<a class="text-link" href="{self.project_url(other)}">{self.copy(other["name"])}</a>'
                            for other in PROJECTS if other is not project)
        return f"""
<article class="wrap section case-study">
  <div class="case-intro">
    <a class="case-back text-link" href="{self.home}#work">{self.t("جميع الأعمال", "All work")}</a>
    <p class="eyebrow">{self.copy(project["type"])}</p>
    <h1>{self.copy(project["name"])}</h1>
    <p class="case-tagline">{self.copy(project["tagline"])}</p>
    {self.tags(project)}
  </div>
  {self.diagram(project)}
  <dl class="case-fields">{fields}</dl>
  {credits}
  <div class="related"><h2>{self.t("دراسات حالة أخرى", "More case studies")}</h2>{alternate}</div>
  <div class="case-signature">{self.logo(cream=False)}</div>
</article>"""

    def render(self):
        name = ("خديجة الأنصاري", "Khadija Al-Ansari")[self.en]
        title = f"{self.project['name'][self.en]} · {name}" if self.project else name
        description = (self.project["summary"] if self.project else (
            "خديجة الأنصاري، مهندسة برمجيات في الرياض تعمل على تطبيقات الذكاء الاصطناعي وتطوير البرمجيات وتجربة المستخدم.",
            "Khadija Al-Ansari is a software engineer in Riyadh working across AI applications, software development, and user experience."
        ))[self.en]
        main = self.case_study() if self.project else self.hero() + self.work() + self.experience() + self.about()
        social_image = f"{BASE_URL}/assets/social-preview.jpg" if BASE_URL else self.asset("social-preview.jpg")
        return f"""<!doctype html>
<html lang="{self.language}" dir="{"ltr" if self.en else "rtl"}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#180006">
  <meta name="description" content="{escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{escape(social_image)}">
  <meta property="og:image:width" content="1000">
  <meta property="og:image:height" content="525">
  <meta name="twitter:card" content="summary_large_image">
  <title>{escape(title)}</title>
  <link rel="icon" href="{self.asset("logo-burgundy-300.webp")}" type="image/webp">
  <link rel="stylesheet" href="{self.asset("site.css")}">
  <script defer src="{self.asset("site.js")}"></script>
</head>
<body>
{self.header()}
<main id="main" tabindex="-1">{main}</main>
{self.footer()}
</body>
</html>
"""

    def save(self):
        target = OUT / self.path / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.render(), encoding="utf-8")


if __name__ == "__main__":
    for language in ("ar", "en"):
        for project in (None, *PROJECTS):
            Page(language, project).save()

