"""Bilingual exhibition copy and native chapter navigation."""
from html import escape

from content import PHASES
from project_gallery import render_project_gallery

ROOMS = (
    ("work", ("المشاريع", "Projects"), ("الأعمال وتجاربها", "The work in context")),
    ("about", ("كيف أعمل؟", "How I work"), ("من الفكرة إلى الاختبار", "From idea to test")),
    ("knowledge", ("المعرفة والأدوات", "Knowledge & tools"), ("مهارات متصلة بالممارسة", "Skills in practice")),
    ("experience", ("الخبرة", "Experience"), ("البحث والخبرة العملية", "Research and practice")),
    ("contact", ("تواصل", "Contact"), ("لنبدأ محادثة", "Start a conversation")),
)

BRANCHES = (
    ("design", ("التصميم", "Design"), ("أحوّل الاحتياجات إلى نماذج قابلة للتجربة. في أريس صمّمت صفحات رِواء عثمان في أكثر من جولة.", "I turn requirements into prototypes. At Arees I iterated on designs for the Rawaa Othman website."),
     ["Figma", "UX", "User research"], "experience", ("خبرتي في أريس", "My work at Arees")),
    ("engineering", ("هندسة البرمجيات", "Software engineering"), ("أبني تطبيقات وألعابًا تفاعلية. استخدم فريق مجرة نور Unity وC# لتحويل الدروس إلى تحديات قابلة للعب.", "I build interactive apps and games. My graduation team used Unity and C# to turn school lessons into playable challenges."),
     ["Unity", "C#", "Flutter", "Python"], "work/majarat-noor", ("استكشف مجرة نور", "Explore Majarat Noor")),
    ("research", ("الذكاء الاصطناعي والبحث", "AI & research"), ("أهتم بتقييم الأنظمة وتحويل نتائج التجارب إلى قرارات. في نسيج ساهمت في دراسة لأنظمة التعرّف الضوئي متعددة اللغات.", "I’m interested in evaluating systems and using experimental evidence to inform decisions. At Naseej I helped research multilingual OCR systems."),
     ["OCR", "LLMs", "Prompt engineering"], "experience", ("الخبرة والبحث", "Experience and research")),
)

PHASE_LINKS = (
    ("experience", ("تعرّف على عملي في أريس", "See my work at Arees")),
    ("knowledge/design", ("أدوات التصميم", "Explore design tools")),
    ("work/majarat-noor", ("استكشف مجرة نور", "Explore Majarat Noor")),
    ("experience", ("تعرّف على خبرتي في نسيج", "See my work at Naseej")),
)


def render_museum(page, linkedin, github):
    t, copy = page.t, page.copy
    other = "ar" if page.en else "en"
    switch = page.url("" if page.en else "en/")
    lobby_name = t("المدخل", "Entrance")
    index_items = "".join(f'<a href="#{slug}" data-route><strong>{copy(title)}</strong><span>{copy(line)}</span></a>'
                          for slug, title, line in ROOMS)
    entrances = "".join(f'<a class="door door-{slug}" href="#{slug}" data-route><span class="door-light" aria-hidden="true"></span><strong>{copy(title)}</strong></a>'
                        for slug, title, _ in ROOMS[:3])

    phase_tabs = "".join(f'<a href="#about/{i}" data-route>{copy(title)}</a>'
                         for i, (title, _) in enumerate(PHASES, 1))
    phase_panels = "".join(f"""
<div class="exhibit-detail" data-detail="{i}" id="about/{i}">
  <h3>{copy(title)}</h3>
  <p>{copy(example)}</p>
  <a class="museum-cta" href="#{route}" data-route>{copy(label)}</a>
</div>""" for i, ((title, example), (route, label)) in enumerate(zip(PHASES, PHASE_LINKS, strict=True), 1))

    branch_tabs = "".join(f'<a href="#knowledge/{slug}" data-route>{copy(title)}</a>' for slug, title, *_ in BRANCHES)
    branch_panels = "".join(f"""
<div class="exhibit-detail" data-detail="{slug}" id="knowledge/{slug}">
  <h3>{copy(title)}</h3>
  <p>{copy(text)}</p>
  <ul class="museum-tools">{''.join(f'<li lang="en" dir="ltr">{escape(tool)}</li>' for tool in tools)}</ul>
  <a class="museum-cta" href="#{route}" data-route>{copy(label)}</a>
</div>""" for slug, title, text, tools, route, label in BRANCHES)

    return f"""
<a class="skip" href="#main">{t("انتقل إلى المحتوى", "Skip to content")}</a>
<div class="museum" data-museum>
  <header class="museum-header">
    <a class="museum-brand" href="#lobby" data-route>{page.logo()}</a>
    <div class="museum-header-actions">
      <button class="museum-back" type="button" data-back hidden>{t("العودة", "Back")}</button>
      <details class="museum-map">
        <summary><span class="map-icon" aria-hidden="true"><i></i><i></i><i></i><i></i></span>{t("خريطة المعرض", "Gallery map")}</summary>
        <nav aria-label="{t("خريطة المعرض", "Gallery map")}">
          <a href="#lobby" data-route><strong>{lobby_name}</strong></a>{index_items}
        </nav>
      </details>
      <a class="museum-language" data-language href="{switch}" lang="{other}" hreflang="{other}" dir="auto">{"العربية" if page.en else "English"}</a>
    </div>
  </header>
  <main id="main" tabindex="-1" class="museum-main">
    <div class="museum-visual" aria-hidden="true"><div class="museum-haze"></div><canvas class="museum-canvas"></canvas></div>
    <section class="lobby" id="lobby" data-room="lobby" aria-labelledby="lobby-title">
      <div class="lobby-copy">
        <p class="museum-kicker"><span></span>{t("معرض الأعمال · الرياض", "Portfolio gallery · Riyadh")}</p>
        <h1 id="lobby-title" class="museum-title" tabindex="-1">{t("خديجة الأنصاري", "Khadija Al-Ansari")}</h1>
        <p class="lobby-role">{t("مهندسة برمجيات · تطبيقات الذكاء الاصطناعي وتجربة المستخدم", "Software engineer · AI applications & user experience")}</p>
      </div>
      <nav class="lobby-doors" aria-label="{t("مداخل المعرض", "Gallery entrances")}">{entrances}</nav>
      <div class="lobby-footer">
        <span>{t("اختر جناحًا لاستكشافه", "Choose an exhibit to explore")}</span>
        <a href="#experience" data-route>{t("الخبرة", "Experience")}</a>
        <a href="#contact" data-route>{t("تواصل", "Contact")}</a>
      </div>
    </section>
{render_project_gallery(page)}
    <section id="about" class="museum-room" data-room="about" aria-labelledby="about-title">
      <div class="museum-panel">
        <p class="museum-kicker">{t("طاولة العمل", "The workbench")}</p>
        <h2 id="about-title" class="museum-title" tabindex="-1">{t("كيف أعمل؟", "How I work")}</h2>
        <p class="room-intro">{t("أربع مراحل من دورة تطوير البرمجيات، مع مثال من عملي في كل مرحلة.", "Four phases of software development, each with an example from my work.")}</p>
        <nav class="exhibit-choices step-choices" aria-label="{t("مراحل التطوير", "Development phases")}">{phase_tabs}</nav>
{phase_panels}
      </div>
    </section>
    <section id="knowledge" class="museum-room" data-room="knowledge" aria-labelledby="knowledge-title">
      <div class="museum-panel">
        <p class="museum-kicker">{t("شجرة المعرفة", "The knowledge tree")}</p>
        <h2 id="knowledge-title" class="museum-title" tabindex="-1">{t("المعرفة والأدوات", "Knowledge & tools")}</h2>
        <p class="room-intro">{t("اقترب من أي فرع لترى أين أستخدم أدواته.", "Focus a branch to see where I put its tools to work.")}</p>
        <nav class="exhibit-choices branch-choices" aria-label="{t("فروع شجرة المعرفة", "Knowledge tree branches")}">{branch_tabs}</nav>
{branch_panels}
        <details class="museum-drawer"><summary>{t("ما أتعلمه", "What I’m learning")}</summary>
          <p>{t("أكملت دورات في مهارات الوكلاء، وتصميم الأنظمة باستخدام LangChain، وهندسة الأوامر.", "I completed courses in agent skills, agentic system design with LangChain, and prompt engineering.")}</p>
          <p>{t("أستكشف التوليد المعزَّز بالاسترجاع وبروتوكول سياق النموذج، وأواصل برنامج الذكاء الاصطناعي في أكاديمية كاوست.", "I’m exploring retrieval-augmented generation and the Model Context Protocol, and continuing KAUST Academy’s AI program.")}</p>
        </details>
      </div>
    </section>
    <section class="museum-room museum-archive" data-room="experience" aria-labelledby="experience-title">
      <div class="museum-panel">
        <p class="museum-kicker">{t("الأرشيف", "The archive")}</p>
        <h2 id="experience-title" class="museum-title" tabindex="-1">{t("الخبرة", "Experience")}</h2>
{page.experience()}
      </div>
    </section>
    <section id="contact" class="museum-room" data-room="contact" aria-labelledby="contact-title">
      <div class="museum-panel">
        <p class="museum-kicker">{t("تواصل · الرياض", "Contact · Riyadh")}</p>
        <h2 id="contact-title" class="museum-title" tabindex="-1">{t("لنبنِ شيئًا معًا.", "Let’s build something.")}</h2>
        <p class="room-intro">{t("للفرص المهنية والتعاون، يسعدني التواصل عبر لينكدإن.", "For professional opportunities and collaborations, reach out on LinkedIn.")}</p>
        <div class="museum-contact">
          <a class="museum-cta" href="{linkedin}" lang="en" dir="ltr">LinkedIn</a>
          <a class="museum-cta" href="{github}" lang="en" dir="ltr">GitHub</a>
        </div>
        <details class="museum-drawer"><summary>{t("عنّي خارج التقنية", "Beyond tech")}</summary>
          <p>{t("أحب الألعاب والتصميم ثلاثي الأبعاد والروبوتات. وفي أوقات الهدوء أقرأ الروايات، وأكتب القصص، وأستمتع بالإعراب.", "I enjoy games, 3D design, and robotics. In quieter moments, I read novels, write stories, and enjoy working through Arabic grammar.")}</p>
        </details>
      </div>
    </section>
  </main>
</div>"""
