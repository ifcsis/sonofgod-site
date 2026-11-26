#!/usr/bin/env python3
"""Build sonofgod.love as a static site for GitHub Pages.

src/  holds the four pages exported from the old GoDaddy site (home, chart,
survey, glossary). This script adds SEO metadata and a Library link to them,
and generates the Library, the paper briefs, Understanding, sitemap and robots.

Run:  python3 build.py   -> writes site/   (copy site/* to the repo root)
"""
import html, json, os, re, shutil

SITE = "https://sonofgod.love"
OUT = "site"
EMAIL = "steele@sonofgod.love"
ORCID = "https://orcid.org/0009-0004-3600-4115"
UPDATED = "2026-11-26"

PERSON = {
    "@type": "Person", "@id": SITE + "/library#author",
    "name": "S. Harrison Knudson", "honorificSuffix": "J.D.",
    "alternateName": ["Steele Harrison Knudson", "S Harrison Knudson", "Steele H. Knudson",
                      "Steele Knudson", "Harrison Knudson"],
    "givenName": "Steele", "additionalName": "Harrison", "familyName": "Knudson",
    "url": SITE + "/library",
    "sameAs": [ORCID, "https://semperism.org/about.html", "https://ifcsis.org/director.html",
               "https://semperism.substack.com", "https://superelements.com/"],
    "image": SITE + "/img/s-harrison-knudson.jpg",
  "knowsAbout": ["New Testament", "Gospel of Matthew", "Cleansing of the Temple",
                   "Social-scientific criticism", "Church and state", "Christian denominations"],
}

def e(s): return html.escape(s, quote=True)
def ld(obj): return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False)

def meta(title, desc, path, og_type="website", extra=""):
    url = SITE + path
    return (f'<meta name="description" content="{e(desc)}">\n'
            f'<link rel="canonical" href="{url}">\n'
            f'<meta property="og:type" content="{og_type}">\n'
            f'<meta property="og:site_name" content="Son of God · A Theological Spectrum">\n'
            f'<meta property="og:title" content="{e(title)}">\n'
            f'<meta property="og:description" content="{e(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta name="author" content="S. Harrison Knudson">\n'
            f'<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n' + extra)

NAV_ITEMS = [("home", "/", "Home"), ("glossary", "/glossary", "Glossary"),
             ("chart", "/chart", "View the chart"), ("survey", "/survey", "Take the survey"),
             ("library", "/library", "Library")]

def nav(here):
    links = "".join(f'<a href="{h}" data-to="{k}"{" class=\"here\"" if k == here else ""}>{t}</a>'
                    for k, h, t in NAV_ITEMS)
    return f'<nav class="sitenav"><span class="mark">A Theological Spectrum</span>{links}</nav>'

# ---------------------------------------------------------------- papers
PAPERS = [
    dict(
        slug="honor-patronage-and-sacred-space",
        title="Honor, Patronage, and Sacred Space",
        sub="A Social-Scientific Reading of the Temple Action of Jesus (Matt 21:12–17)",
        kind="Working paper", status="Revision in progress · 2026",
        description="Reads Matthew’s temple scene through three social-scientific lenses — honor, "
                    "patronage and sacred space — and asks whether the familiar picture of an angry "
                    "outburst survives them.",
        keywords=["Matthew 21", "Cleansing of the Temple", "honor and shame", "patronage",
                  "sacred space", "social-scientific criticism"],
        brief=[
            ("The question", [
                "The usual reading of the temple action is a reading of temperament: Jesus loses his "
                "patience with the traders and drives them out in anger. Matthew’s scene does not "
                "stop at the tables, though. It goes on, without a break, to the blind and the lame "
                "being healed in the temple and to children crying “Hosanna to the Son of David” "
                "loudly enough that the chief priests object (21:14–16).",
                "This paper asks what the whole scene looks like when it is read with the tools "
                "social scientists use for the ancient Mediterranean world, rather than with a "
                "modern assumption about anger.",
            ]),
            ("Three lenses", [
                "<b>Honor.</b> Public acts in a temple court were claims made before witnesses, and "
                "claims invite challenge. Matthew records the challenge the next day: “By what "
                "authority doest thou these things?” (21:23).",
                "<b>Patronage.</b> The temple stood between worshippers and God, and its personnel "
                "controlled access. In Matthew’s scene the blind and lame come to Jesus in the temple "
                "and are healed there, with no intermediary.",
                "<b>Sacred space.</b> The saying he quotes is about what the space is for: “My house "
                "shall be called the house of prayer” (Isaiah 56:7). The question becomes who decides "
                "the use of the house, and on whose authority.",
            ]),
            ("Why it matters", [
                "Read together, the lenses describe a scene of authority and restored use, not of "
                "disorder. The paper treats verses 14–17 as part of the event rather than its "
                "aftermath, and argues that they change what the overturned tables mean.",
            ]),
        ],
    ),
    dict(
        slug="one-cleansing-or-two",
        title="One Cleansing or Two",
        sub="Why the Scholarship Shifted",
        kind="Research note", status="November 2026",
        description="Why the English Lives of Christ of 1905 counted two cleansings of the temple, why "
                    "most scholars now count one, and why the question is a majority view rather than a "
                    "settled one.",
        keywords=["Cleansing of the Temple", "John 2", "Mark 11", "gospel harmony",
                  "James E. Talmage", "Jesus the Christ"],
        brief=[
            ("The question", [
                "John tells the clearing of the temple at the first Passover of the ministry; Matthew, "
                "Mark and Luke tell it in the last week. The core acts match, and the details and "
                "sayings differ. Every answer, one cleansing or two, is an answer to that table.",
            ]),
            ("Why 1905 counted two", [
                "The books an English-speaking scholar reached for in 1905 — Farrar, Geikie, Edersheim, "
                "Andrews, the Broadus harmony — all counted two. They read the four Gospels as four "
                "chronicles to be fitted into one timeline, so a different placement meant a different "
                "event. The method goes back to Augustine’s <i>Harmony of the Gospels</i>, about AD 400. "
                "James E. Talmage’s <i>Jesus the Christ</i> followed those sources.",
                "The other reading was already present in his day, mostly in German and critical work: "
                "Neander judged a repeat “hardly probable,” and a 1902 survey in <i>Bibliotheca Sacra</i> "
                "set out all three positions as live.",
            ]),
            ("What changed", [
                "No single discovery moved the question. Scholars stopped reading the Gospels as "
                "chronicles and began reading them as arranged testimony. Once an evangelist could place "
                "an event for its meaning, one cleansing told twice became the simpler reading.",
            ]),
            ("Where it stands", [
                "By 2015 Allan Chapple, who himself defends two cleansings, called one late cleansing "
                "the view of “the overwhelming majority.” It is a majority, not a settlement: a standing "
                "group of commentators still holds two, and a minority of one-event scholars places the "
                "single event early, where John has it. “Generally” is the honest word.",
            ]),
        ],
    ),
    dict(
        slug="the-church-binds-the-conscience",
        title="The Church Binds the Conscience, the State Binds the Estate",
        sub="Marriage as Incorporation",
        kind="Draft article", status="November 2026",
        description="Religious communities decide whom they regard as married; the state should decide "
                    "only what people owe one another. A proposal to replace civil marital status with "
                    "registered domestic incorporation.",
        keywords=["marriage", "church and state", "family law", "religious liberty",
                  "domestic incorporation", "Obergefell v. Hodges"],
        brief=[
            ("The wrong fight", [
                "The state has two powers over domestic life. One is the power to enforce obligations: "
                "support, property, the care of children. The other is the power to define what a "
                "relationship means — whether it is a marriage at all. The first is ordinary government. "
                "The second is a question of conscience, and the state answers it every time it licenses "
                "a union or asks on a form whether a person is married.",
                "The American argument over marriage has been an argument over who may enter the "
                "category. This article asks the prior question: why the state maintains the category "
                "at all.",
            ]),
            ("The proposal", [
                "<b>First, a narrow step.</b> A religious ceremony should have no civil effect on its own. "
                "Alabama has already moved this way, replacing marriage licenses with a recorded form in "
                "2019, and much of continental Europe keeps civil registration separate from the rite.",
                "<b>Second, the contribution.</b> Replace marital status with registered domestic "
                "incorporation: people register the household they are actually forming, choose among a "
                "small menu of standard forms, and sit on a floor no agreement can waive — support for "
                "children, recognition of caregiving, full disclosure, and protection against coercion "
                "and abuse.",
            ]),
            ("The hard question", [
                "<i>Obergefell v. Hodges</i> (2015) holds that marriage is a fundamental right. Whether a "
                "state could honor that right while withdrawing civil marriage from everyone is "
                "unanswered by precedent, and the article says so. If the answer is no, the framework "
                "survives in narrower form, with civil marriage kept as one standard form among several.",
            ]),
            ("In a sentence", [
                "The church binds the conscience. The state binds the estate.",
            ]),
        ],
    ),
]

# ---------------------------------------------------------------- shared CSS for new pages
def base_css():
    s = open("src/home.html").read()
    css = s[s.find("<style>") + 7:s.find("</style>")]
    return css + """
.sitenav a{margin-left:0}
.prose{max-width:72ch}
.prose h1{max-width:22ch}
.prose h2{font:400 24px/1.2 Georgia,serif;margin:38px 0 12px}
.prose p{color:var(--soft);font-size:16.5px;margin:0 0 14px}
.prose p b,.prose p i{color:var(--ink)}
.sub{font:400 20px/1.35 Georgia,serif;color:var(--soft);margin:0 0 18px;max-width:46ch}
.tag{display:inline-block;font:500 10px/1 ui-monospace,Menlo,monospace;letter-spacing:.14em;
 text-transform:uppercase;color:var(--verd);margin:0 0 14px}
.cards{display:grid;gap:18px;margin:34px 0 0}
.card{display:block;text-decoration:none;color:inherit;background:var(--surface);
 border:1px solid var(--rule);border-left:3px solid var(--verd);padding:24px 28px}
.card:hover{border-left-color:var(--gold);background:#F7F8F5}
.card h2{font:400 23px/1.2 Georgia,serif;margin:0 0 4px}
.card .s{color:var(--soft);font-style:italic;margin:0 0 10px}
.card p{margin:0;color:var(--soft);font-size:15px;max-width:70ch}
.card .m{display:block;margin-top:12px;font:500 10px/1 ui-monospace,Menlo,monospace;
 letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}
.actions{margin:34px 0 0;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.cite{font:400 13px/1.6 ui-monospace,Menlo,monospace;color:var(--faint);margin-top:30px;
 padding-top:16px;border-top:1px solid var(--rule)}
article.hero{padding:56px 0 10px}
.prose p.eyebrow{font:500 11px/1.5 ui-monospace,Menlo,monospace;letter-spacing:.2em;color:var(--verd);margin:0 0 16px}
.prose p.cite{font:400 12.5px/1.6 ui-monospace,Menlo,monospace;color:var(--faint)}
.prose p.lede{font-size:17.5px}
.prose a,.about a,footer a{color:var(--verd)}
.prose a.mail{color:#F1F4F1}
.note{background:var(--surface);border-left:3px solid var(--gold);padding:16px 22px;margin:28px 0 0;
 color:var(--soft);font-size:15px}
"""

FOOTER = ('<footer>Son of God · sonofgod.love · S. Harrison Knudson, J.D. (Steele Harrison Knudson)<br>'
          f'<a href="/library" style="color:inherit">Library</a> · '
          f'<a href="https://semperism.org" style="color:inherit">Semperism</a> · '
          f'<a href="{ORCID}" style="color:inherit">ORCID</a> · '
          f'<a href="mailto:{EMAIL}" style="color:inherit">{EMAIL}</a></footer>')

def page(path, title, desc, here, body, og_type="website", extra_head=""):
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
{meta(title, desc, path, og_type, extra_head)}<style>{CSS}</style>
</head>
<body>
<div class="wrap">
{nav(here)}
{body}
{FOOTER}
</div>
</body>
</html>
"""
    fn = os.path.join(OUT, (path.strip("/") or "index") + ".html")
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, "w").write(doc)

def req_link(p):
    subj = f"Request: {p['title']}"
    return "mailto:%s?subject=%s" % (EMAIL, html.escape(subj.replace(" ", "%20"), quote=True))

# ---------------------------------------------------------------- build
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
if os.path.isdir("img"): shutil.copytree("img", os.path.join(OUT, "img"))
CSS = base_css()

# 1. the four exported pages
OLD = {
    "home": ("/", "Christian Traditions: A Theological Spectrum",
             "Thirty Christian traditions placed along fourteen theological axes, with a glossary, an "
             "interactive chart and a self-placement survey. By S. Harrison Knudson."),
    "chart": ("/chart", "The Spectrum Chart — Christian Traditions: A Theological Spectrum",
              "Interactive chart of thirty Christian traditions across fourteen theological axes, with "
              "the reasoning behind each placement."),
    "survey": ("/survey", "Where Do You Sit? — A Theological Spectrum Self-Placement",
               "Three short surveys that place your own beliefs among thirty Christian traditions. "
               "Nothing is stored or sent."),
    "glossary": ("/glossary", "Glossary — A Theological Spectrum",
                 "Ninety-five theological terms defined in ordinary language, grouped by the spectrum's "
                 "axes."),
}
for key, (path, title, desc) in OLD.items():
    s = open(f"src/{key}.html").read()
    s = re.sub(r"\s*</body>\s*$", "", s.rstrip())          # drop GoDaddy wrapper's extra </body>
    s = s.rstrip() + "\n"
    s = re.sub(r"<title>.*?</title>", f"<title>{e(title)}</title>", s, count=1, flags=re.S)
    extra = ""
    if key == "home":
        extra = ld({"@context": "https://schema.org", "@graph": [
            {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Son of God",
             "alternateName": "Christian Traditions: A Theological Spectrum", "author": {"@id": PERSON["@id"]}},
            {"@type": "Dataset", "name": "Christian Traditions: A Theological Spectrum (version 7)",
             "description": desc, "url": SITE + "/chart", "creator": {"@id": PERSON["@id"]},
             "version": "7", "dateModified": "2026-11"},
            PERSON]}) + "\n"
    s = s.replace("</title>", "</title>\n" + meta(title, desc, path, "website", extra), 1)
    # nav: add Library after Take the survey
    s = re.sub(r'(<a href="/survey" data-to="survey"[^>]*>Take the survey</a>)',
               r'\1<a href="/library" data-to="library" target="_top">Library</a>', s, count=1)
    s = s.replace('survey:   "/survey"\n};', 'survey:   "/survey",\n  library:  "/library"\n};')
    s = s.replace(' target="_top"', "")
    if key == "home":
        s = s.replace('<section class="about">',
            '<section class="about">\n  <h3>The library</h3>\n  <p>Alongside the spectrum, this site '
            'keeps one-page briefs of current theological and church-and-state work by S. Harrison Knudson. '
            '<a href="/library" style="color:var(--verd)">Browse the library</a>.</p>\n</section>\n\n<section class="about">', 1)
    assert 'data-to="library"' in s, key
    open(os.path.join(OUT, "index.html" if key == "home" else f"{key}.html"), "w").write(s)

# 2. library index
cards = "".join(
    f'<a class="card" href="/papers/{p["slug"]}"><span class="tag">{e(p["kind"])}</span>'
    f'<h2>{e(p["title"])}</h2><p class="s">{e(p["sub"])}</p><p>{e(p["description"])}</p>'
    f'<span class="m">{e(p["status"])} · One-page brief</span></a>' for p in PAPERS)
lib_body = f"""<header class="hero prose">
  <p class="eyebrow">Library</p>
  <h1>Current work</h1>
  <p class="lede">One-page briefs of theological and church-and-state work in progress by S. Harrison Knudson, J.D. (Steele Harrison Knudson). Full papers are available on request.</p>
</header>
<div class="cards">{cards}</div>
<section class="about">
  <h3>About the author</h3>
  <div style="display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap">
  <img src="/img/s-harrison-knudson.jpg" alt="S. Harrison Knudson (Steele Knudson, Steele Harrison Knudson)" width="150" style="width:150px;height:auto;border:1px solid var(--rule);flex:none">
  <p style="flex:1;min-width:260px;margin:0">S. Harrison Knudson is an American lawyer and independent scholar in Arlington, Virginia. He writes on the New Testament, on the relation of church and state, and on constitutional theory. His constitutional work is collected at <a href="https://semperism.org">semperism.org</a>; he is also Director of the <a href="https://ifcsis.org">International Foundation for Child-Safe Internet Standards</a>. ORCID <a href="{ORCID}">0009-0004-3600-4115</a>.</p>
  </div>
</section>"""
page("/library", "Library — S. Harrison Knudson (Steele Harrison Knudson)",
     "One-page briefs of current theological and church-and-state work by S. Harrison Knudson, J.D.: "
     "the temple action of Jesus, one cleansing or two, and marriage as incorporation.",
     "library", lib_body,
     extra_head=ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Library",
                    "url": SITE + "/library", "author": PERSON,
                    "hasPart": [{"@type": "ScholarlyArticle", "headline": p["title"],
                                 "url": f"{SITE}/papers/{p['slug']}"} for p in PAPERS]}) + "\n")

# 3. paper briefs
for p in PAPERS:
    secs = "".join(f"<h2>{e(h)}</h2>" + "".join(f"<p>{para}</p>" for para in paras) for h, paras in p["brief"])
    cite = f"S. Harrison Knudson, “{p['title']}: {p['sub']},” {p['kind'].lower()}, {p['status'].split(' · ')[-1]}, {SITE}/papers/{p['slug']}."
    body = f"""<article class="hero prose">
  <p class="eyebrow">{e(p['kind'])} · {e(p['status'])}</p>
  <h1>{e(p['title'])}</h1>
  <p class="sub">{e(p['sub'])}</p>
  <p>By <a href="/library">S. Harrison Knudson, J.D.</a></p>
  {secs}
  <div class="note">This page is a one-page brief. The full paper is available on request.</div>
  <div class="actions"><a class="mail" href="{req_link(p)}">Request the full paper</a>
  <a href="/library">&larr; Back to the library</a></div>
  <p class="cite">Cite this brief: {e(cite)}</p>
</article>"""
    extra = (f'<meta name="citation_title" content="{e(p["title"] + ": " + p["sub"])}">\n'
             f'<meta name="citation_author" content="Knudson, S. Harrison">\n'
             f'<meta name="citation_author_orcid" content="{ORCID}">\n'
             f'<meta name="keywords" content="{e(", ".join(p["keywords"]))}">\n'
             + ld({"@context": "https://schema.org", "@type": "ScholarlyArticle",
                   "headline": p["title"], "alternativeHeadline": p["sub"], "description": p["description"],
                   "author": PERSON, "keywords": p["keywords"], "url": f"{SITE}/papers/{p['slug']}",
                   "isAccessibleForFree": True, "inLanguage": "en", "creativeWorkStatus": p["kind"]}) + "\n")
    page(f"/papers/{p['slug']}", f"{p['title']}: {p['sub']} — S. Harrison Knudson", p["description"],
         "library", body, og_type="article", extra_head=extra)

# 4. understanding (old GoDaddy page)
page("/understanding", "Understanding — A Theological Spectrum",
     "Love and respect among fellow believers: why the theological spectrum was made.", "",
     f"""<header class="hero prose">
  <p class="eyebrow">Understanding</p>
  <h1>Love and respect among fellow believers</h1>
  <p class="lede">This chart was designed to foster mutual respect and understanding of belief.</p>
</header>
<section class="about prose">
  <p>It is a draft, and it needs input from people of all creeds and traditions. Comments and suggestions are welcome at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</section>""")

# 5. 404, favicon, robots, sitemap, CNAME
page("/404", "Not found — Son of God", "Page not found.", "",
     '<header class="hero prose"><h1>Not found</h1><p class="lede">That page is not here. '
     'Try the <a href="/">home page</a> or the <a href="/library">library</a>.</p></header>')
open(os.path.join(OUT, "favicon.svg"), "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" fill="#2E6E60"/>'
    '<path d="M16 6v20M9 12h14" stroke="#EFE2C4" stroke-width="3"/></svg>')
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
urls = ["/", "/chart", "/survey", "/glossary", "/library", "/understanding"] + [f"/papers/{p['slug']}" for p in PAPERS]
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod>"
              + (f"<image:image><image:loc>{SITE}/img/s-harrison-knudson.jpg</image:loc></image:image>" if u == "/library" else "")
              + "</url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(OUT, "CNAME"), "w").write("sonofgod.love\n")
print("built", len(urls), "pages")
