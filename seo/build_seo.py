#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO/GEO build for 工作的重构. Run from the repo root: python seo/build_seo.py

One long report, so it keeps one canonical URL: splitting a twenty-year argument into
fragment pages would just create thin URLs competing with each other. What it gets is
the canonical fixed to ourword.ai, Article + FAQPage schema built from its own section
headings, and the whole text in llms-full.txt for answer engines to read and cite.
"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo_kit as G

SITE = G.Site(
    path="ai-jobs-20yr-report",
    name="The Restructuring of Work", name_zh="工作的重构",
    tagline="how AI reshapes every kind of job, 2026–2046",
    tagline_zh="AI × 职业的二十年推演（2026–2046）",
    description=(
        "A twenty-year projection of how AI reshapes work, built on one idea: a job is a "
        "bundle of tasks, not a single thing. It grades twenty occupation clusters against "
        "five variables that decide when a task gets automated, lays out four phases from "
        "copilot to deep water, gives a five-minute exposure self-test, and ends with the "
        "signals to watch and an explicit list of where the projection could be wrong."),
    description_zh=(
        "一份 2026–2046 的二十年推演，起点只有一个判断：岗位是任务束，不是一个整体。"
        "用五个变量判断每项任务何时被自动化，推演 20 类职业、四个阶段（从副驾驶到深水区），"
        "给出五分钟暴露度自测、值得盯住的信号清单，并明写这份推演哪里可能是错的。"),
    keywords=("AI 取代 工作, AI 就业 影响, 岗位 自动化, 任务束, 职业规划 AI, 未来 职业, "
              "AI and jobs, task bundle, automation exposure, future of work 2046"),
    item_type="Article", item_noun="report", item_noun_zh="报告",
    lang="zh-Hans", changefreq="monthly",
)

HOW = ("Hand-written. The projection hangs on named, checkable anchors rather than vibes: "
       "each occupation cluster is scored on digitisation, verifiability, liability and "
       "licensing, data availability and demand elasticity, and the report lists the signals "
       "that would falsify it.")

CITE = ("Cite this page with its version date shown at the top. It is a projection, not a "
        "forecast, and the section on where it could be wrong is part of the argument — "
        "quote it alongside any conclusion. Attribute to \"工作的重构 (OurWord AI)\".")


def version():
    try:
        s = open("index.html", encoding="utf-8").read()
        m = re.search(r"(20\d\d)\.(\d\d)\s*·\s*V[\d.]+", s)
        if m:
            return "%s-%s-01" % (m.group(1), m.group(2))
    except Exception:
        pass
    return datetime.date.today().isoformat()


def main():
    today = datetime.date.today().isoformat()
    up = version()
    secs = G.sections_from_html("index.html", min_chars=240)

    doc = G.Item(slug="ai-jobs-20yr-report", title=SITE.name, summary=SITE.description,
                 blocks=secs, title_zh=SITE.name_zh, summary_zh=SITE.description_zh,
                 blocks_zh=secs, updated=up, url_override=SITE.base,
                 source_url="https://github.com/ourword-ai/ai-jobs-20yr-report")

    ld = [G.article_ld(SITE, SITE.base, SITE.name_zh + " · " + SITE.tagline_zh,
                       SITE.description_zh, secs, zh=True, updated=up)]
    f = G.faq_ld(doc, True)
    if f:
        ld.append(f)

    rep = G.build(SITE, [doc], root=".", today=today, how_built=HOW, cite_as=CITE,
                  item_pages=False, extra_ld=ld,
                  extra_sitemaps=["https://ourword.ai/sitemap.xml"])
    rep["sections"] = len(secs)
    print("ai-jobs-20yr-report seo/geo:", json.dumps(rep, ensure_ascii=False))
    return rep


if __name__ == "__main__":
    main()
