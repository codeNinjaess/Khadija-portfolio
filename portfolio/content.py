# Pairs are ordered Arabic, English.
PROJECTS = [
    {
        "slug": "tamakkan",
        "name": ("تمكّن", "Tamakkan"),
        "type": ("إثبات مفهوم · مختبر الذكاء الاصطناعي في نسيج", "Proof of concept · Naseej AI Lab"),
        "tagline": ("من فجوة في التعلّم إلى خطوة واضحة", "From a learning gap to a clear next step"),
        "summary": ("مرشد أكاديمي يربط أدلة التعلّم بمتطلبات المنهج، ويبيّن للطالب ما يحتاج إلى مراجعته ولماذا.", "A curriculum-aware academic advisor that connects learner evidence to course prerequisites and explains what to review and why."),
        "tags": ["Knowledge graphs", "AI", "Bilingual UX"],
        "flow": [("المنهج والأدلة", "Curriculum & evidence"), ("كشف الفجوات", "Detect gaps"), ("ترتيب الأولويات", "Prioritize impact"), ("التدريب", "Practice"), ("التحقّق", "Verify")],
        "details": [
            ("قد يلاحظ الطالب ضعفًا في مقرر سابق من دون أن يعرف أي مفهوم يحتاج إليه الآن، أو كيف يؤثر ذلك في المقررات اللاحقة.", "Students may know they struggled in a prior course but still be unsure which concept to revisit or how it affects later courses."),
            ("طلاب الجامعة الذين يحتاجون إلى ترتيب مراجعتهم بناءً على متطلبات خطتهم الدراسية.", "University students deciding what to review in the context of their degree plan."),
            ("إثبات مفهوم لمرشد الفجوات الأكاديمية المرتبط بالمنهج (CAAGA)، طُوّر خلال التدريب في مختبر الذكاء الاصطناعي في نسيج.", "A proof of concept for a Curriculum-Aware Academic Gap Advisor (CAAGA), developed during my internship at Naseej AI Lab."),
            ("حدّدت المتطلبات وصمّمت الواجهة والمعمارية، وبنيت جزءًا من الرسم البياني المعرفي للمنهج ونموذج المتعلّم. طوّرت كشف الفجوات وترتيبها حسب أثرها الدراسي ومساري التدريب والتحقّق، وأعددت بنك أسئلة رياضيات ثنائي اللغة.", "I defined requirements, designed the interface and architecture, and built a slice of the curriculum knowledge graph and the learner model. I implemented gap detection, impact prioritization, practice and verification, and created a bilingual mathematics question bank."),
            ("ربطت الفجوات بمفاهيم محددة من المقررات السابقة. يجمع المسار أدلة مثل السجل الدراسي ونتائج التقييم، ويقارنها بعلاقات المنهج، ثم يوضّح أثر كل فجوة في المقررات التالية ويوجّه الطالب إلى تدريب مرتبط بها وأسئلة للتحقّق بصورة مستقلة.", "I modeled prerequisites at the concept level so a recommendation could explain why a specific topic matters. The flow compares evidence such as transcripts and assessment answers against curriculum relationships, explains the downstream impact of each gap, then routes students to targeted practice and separate verification questions."),
            ("راجعت إثبات المفهوم استعدادًا لاختبار الزملاء، وعرضته داخليًا. اختبرت إدخال سجل دراسي اصطناعي وملاءمة مواد التدريب للأسئلة، وأعددت حالات اختبار للمسار المعتاد والحالات الحدّية.", "I reviewed the proof of concept for a peer-testing release and presented it internally. I tested transcript input with synthetic data, checked that practice resources matched their questions, and wrote test suites for the normal flow and edge cases.")
        ]
    },
    {
        "slug": "majarat-noor",
        "name": ("مجرة نور", "Majarat Noor"),
        "type": ("مشروع تخرّج جماعي · جامعة الملك سعود", "Team graduation project · King Saud University"),
        "tagline": ("رحلة فضائية عبر المناهج الدراسية", "A space adventure through the school curriculum"),
        "summary": ("لعبة لطلاب الابتدائي تستكشف فيها مواد المنهج عبر كواكب وتحديات ومكافآت، مع تلميحات تُولَّد حسب أداء اللاعب.", "An elementary-school game that turns subjects into planets, with challenges, rewards and AI hints shaped by each player’s performance."),
        "tags": ["Unity", "C#", "AI hints"],
        "flow": [("استكشاف", "Explore"), ("تحدٍّ ومكافأة", "Challenge & reward"), ("تلميح عند الطلب", "On-demand hint")],
        "details": [
            ("كيف نجعل مراجعة الدروس تجربة تفاعلية تشجّع الطالب على الاستكشاف وتقدّم له المساعدة عند الحاجة؟", "How could reviewing school lessons become an interactive experience that invites exploration and offers help when needed?"),
            ("طلاب المرحلة الابتدائية.", "Elementary school students."),
            ("لعبة تعليمية جماعية أُنجزت في إطار مشروع التخرّج بجامعة الملك سعود باستخدام Unity وC#.", "A team graduation project at King Saud University, built in Unity and C#."),
            ("شاركت في المشروع ضمن فريق التخرّج. شمل عمل الفريق استخلاص المتطلبات ونمذجتها وتصميم اللعبة وتطويرها وهندسة الأوامر وبناء الخوارزميات.", "I was a member of the graduation team. The team’s work covered requirements elicitation and modeling, game design and development, prompt engineering, and algorithm design."),
            ("مثّل الفريق كل مادة بكوكب وكل موضوع بمنطقة. يجمع اللاعب مكافآت من التحديات لتخصيص شخصيته ومركبته، ويطلب عند الحاجة تلميحًا يولّده الذكاء الاصطناعي بناءً على أدائه وأخطائه في المستوى.", "The team gave each subject a planet and each topic a region. Players earn rewards from challenges to customize their character and ship, and can request an AI-generated hint informed by their performance and mistakes in the level."),
            ("اختتم الفريق المشروع بعرض اللعبة في معرض مشاريع التخرّج، مع فيديو تشويقي يوثّق فكرة اللعبة.", "The team showcased the game at the graduation project exhibition and produced a teaser.")
        ],
        "credits": ("الفريق: خديجة الأنصاري، Jood Al-Shehri، Fatema Maklad، Zinah Anbar، Nouf Alkathiri. الإشراف: الأستاذة منيرة الدليمي. تصميم وإخراج الفيديو التشويقي: Fatema Maklad.", "Team: Khadija Al-Ansari, Jood Al-Shehri, Fatema Maklad, Zinah Anbar and Nouf Alkathiri. Supervisor: Monira Aldelaimi. Teaser design and direction: Fatema Maklad.")
    },
    {
        "slug": "luqata",
        "name": ("Luqata", "Luqata"),
        "type": ("مشروع جوّال جماعي · جامعة الملك سعود", "Team mobile project · King Saud University"),
        "tagline": ("مسار أوضح لاستعادة المفقودات", "A clearer path to recovering lost items"),
        "summary": ("تطبيق جوّال يربط بلاغات الفقد والعثور باستخدام التعرّف على الصور لاقتراح مطابقات محتملة.", "A mobile app that connects lost and found reports, using image recognition to suggest possible matches."),
        "tags": ["Flutter", "Image recognition"],
        "flow": [("بلاغ", "Report"), ("مطابقة", "Match"), ("مطالبة", "Claim")],
        "details": [
            ("يصعب على من فقد غرضًا معرفة ما إذا كان شخص آخر قد عثر عليه، خصوصًا إذا اختلف وصف الغرض بين البلاغين.", "Someone who lost an item may struggle to find the corresponding report, especially when the two people describe the same item differently."),
            ("من فقد غرضًا ومن عثر على غرض ويريد إعادته.", "People who have lost an item and people who have found one."),
            ("مشروع تطبيق جوّال جماعي مرتبط بجامعة الملك سعود، طُوّر باستخدام Flutter.", "A team mobile application project associated with King Saud University, built with Flutter."),
            ("شاركت ضمن فريق المشروع. التحليل وتصميم الواجهات والتطوير أعمال موثقة على مستوى المشروع الجماعي.", "I contributed as a team member. Analysis, interface design, and development are documented at the project level."),
            ("استخدم الفريق التعرّف على الصور لاقتراح مطابقات. بعد رفع بلاغ فقد أو عثور، يراجع المستخدم النتائج ويستبعدها أو يقدّم مطالبة، ويمكن للطرفين التواصل عبر المحادثة.", "The team used image recognition to propose matches. After filing a lost or found report, users can review and dismiss suggestions or submit a claim. The two parties can communicate through chat."),
            ("خرج الفريق بتطبيق يجمع البلاغات والمطابقات المحتملة والمطالبة والمحادثة ضمن مسار واحد للمفقودات.", "The team built an app that brings reporting, suggested matches, claims, and chat into a single recovery flow.")
        ]
    }
]

ADDITIONAL = [
    (("تمسّك", "Tamassak"), ("لعبة جماعية · Unity وC#", "Team game · Unity and C#"), ("لعبة أركيد ثلاثية الأبعاد عن التوازن في مترو الرياض. أحرز الفريق المركز الثاني في معسكر AtharTech.", "A 3D arcade game about keeping your balance on the Riyadh Metro. The team placed second at the AtharTech bootcamp.")),
    (("رحلتي", "Rehlati"), ("تصميم تجربة مستخدم جماعي · Figma", "Team UX project · Figma"), ("تصميم لتنسيق الرحلات المدرسية إلى إكسبو 2030، يشمل التصويت على الأجنحة والتواصل والتنبيه عند الابتعاد عن المجموعة.", "A school-trip design for Expo 2030 with pavilion voting, communication, and alerts when a student leaves the group.")),
    (("UniBites", "UniBites"), ("مشروع جماعي · معمارية البرمجيات", "Team project · Software architecture"), ("تصميم لطلب الطعام داخل الحرم الجامعي واستلامه من خزائن ذكية تُخصَّص حسب الطلب.", "A design for ordering campus meals and collecting them from dynamically assigned smart lockers.")),
    (("Movie Cave", "Movie Cave"), ("تطبيق ويب متكامل", "Full-stack web application"), ("تطبيق ويب يستخدم Angular وSpring Boot وواجهات REST.", "A web application using Angular, Spring Boot, and REST APIs.")),
    (("Clothing Advice System", "Clothing Advice System"), ("نظام توصية · تعلّم آلي", "Recommender · Machine learning"), ("نظام توصية بالملابس باستخدام Python وscikit-learn ونماذج لغوية كبيرة.", "A clothing recommender using Python, scikit-learn, and large language models.")),
]

PHASES = [
    (("المتطلبات", "Requirements"), ("حدّدت نطاق تمكّن واحتياجاته وقصص المستخدم قبل تصميم الحل.", "I defined Tamakkan’s scope, requirements, and user stories before designing the solution.")),
    (("التصميم", "Design"), ("في أريس، صمّمت صفحات رِواء عثمان على Figma وطوّرت نماذجها عبر أكثر من جولة.", "At Arees, I designed Rawaa Othman pages in Figma and iterated on the prototypes.")),
    (("التطوير", "Development"), ("ربطت نموذج المتعلّم في تمكّن بالرسم البياني للمنهج لدعم كشف الفجوات.", "I connected Tamakkan’s learner model to the curriculum graph to support gap detection.")),
    (("الاختبار", "Testing"), ("أعددت اختبارات لرحلة الطالب في تمكّن تغطّي المسار المعتاد والحالات الحدّية.", "I wrote tests for Tamakkan’s student journey covering the typical flow and edge cases.")),
]

EXPERIENCE = [
    (("مختبر الذكاء الاصطناعي في نسيج", "Naseej AI Lab"), ("متدربة ذكاء اصطناعي", "AI Engineering Intern"), ("من سبتمبر ٢٠٢٦ · الرياض", "Since September 2026 · Riyadh"),
     ("طوّرت إثبات مفهوم تمكّن، وساهمت في صياغة بحث عن التعرّف الضوئي متعدد اللغات وتحديثه بنتائج التجارب. قدّمت ورشتين عن الاستعانة بالنماذج اللغوية في كتابة الأبحاث وعن إعداد العروض التقديمية.", "I built the Tamakkan proof of concept, helped draft a multilingual OCR study and incorporated experimental results. I delivered workshops on using language models to support research writing and on preparing presentations.")),
    (("أريس", "Arees"), ("متدربة هندسة برمجيات", "Software Engineering Intern"), ("يونيو – أغسطس ٢٠٢٦ · المدينة المنورة", "June–August 2026 · Medina"),
     ("ساهمت في تصميم وتطوير موقع رِواء عثمان لمشروع بئر عثمان، باستخدام Figma للتصميم وWordPress للتطوير. قارنت أدوات البناء، وبحثت في تاريخ البئر، وأعددت مسودة متطلبات وواجهات لصفحات التاريخ والرؤية والرسالة وغيرها. درست أفكار المساعد الذكي والجولة بزاوية ٣٦٠° ضمن التصوّر الأولي.", "I helped design and develop the Rawaa Othman website for the Bir Othman project using Figma and WordPress. I compared site-building tools, researched the well’s history, drafted requirements, and designed pages including History and Vision & Mission. An AI assistant and a 360° tour were explored as concepts."))
]

RECOGNITION = [
    (("جامعة الملك سعود", "King Saud University"), ("بكالوريوس هندسة البرمجيات مع مرتبة الشرف · ٢٠٢٦", "BSc in Software Engineering with honors · 2026"), None),
    (("المركز الثاني · AtharTech", "Second place · AtharTech"), ("فريق تمسّك في معسكر تطوير الألعاب باستخدام Unity.", "Team Tamassak, Unity game development bootcamp."), None),
    (("المركز الثالث · RoboRumble", "Third place · RoboRumble"), ("فريق RoboLux في هاكاثون الروبوتات، بتجربة في التصميم ثلاثي الأبعاد وتجميع الدوائر وبرمجة Arduino.", "Team RoboLux, a robotics hackathon involving 3D design, circuit assembly, and Arduino programming."), None),
    (("هاكاثون الحلول المبتكرة لجودة الحياة", "Innovative Solutions for Quality of Life Hackathon"), ("مثّلت نسيج في فعالية جامعة الأميرة نورة بنت عبدالرحمن.", "I represented Naseej at the Princess Nourah bint Abdulrahman University event."), "https://pnuhackathon.com/"),
    (("أكاديمية كاوست", "KAUST Academy"), ("مشاركة جارية في برنامج التخصص في الذكاء الاصطناعي.", "Ongoing participation in the Artificial Intelligence Specialization."), "https://academy.kaust.edu.sa/programs/ai-specialization/"),
]

PAPER = "Evaluating Cloud and Self-Hosted OCR Systems for Arabic, English, and French Documents: Bounding Box Detection, Text Recognition, and Mathematical Expression Recognition"

