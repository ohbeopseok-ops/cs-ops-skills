#!/usr/bin/env python3
"""JoyLab HTML Presentation V1.0 — 빌더.
deck JSON + 컴포넌트 + 테마 + 엔진 + 내장 폰트 → 단일 오프라인 HTML (테마별 1개).

사용:  python3 build.py [--deck deck/test-deck.json] [--out ../dist] [--themes executive,learning,research]
요건:  파이썬 표준 라이브러리만 사용. 외부 네트워크 호출 없음.
"""
import argparse, base64, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
THEMES = {
    "executive": "Executive Strategy",
    "learning": "Learning Experience",
    "research": "Research Intelligence",
}
CIRCLED = ["①", "②", "③", "④", "⑤", "⑥"]


def esc(s):
    return html.escape(str(s), quote=True)


def md(s):
    """**굵게** 만 지원 (먼저 이스케이프)."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(s))


def rise(i):
    return f'class="rise" style="--d:{i}"'


# ───────────────────────── 컴포넌트 (type → html) ─────────────────────────
def c_agenda(d, s, meta):
    rows = "".join(
        f'<div class="ag-row rise" style="--d:{i}" data-box><span class="pill">{esc(r["stage"])}</span>'
        f'<span class="t">{esc(r["topic"])}</span><span class="sl">슬라이드 {esc(r["slides"])}</span>'
        f'<span class="m" data-min="{r["minutes"]}">{r["minutes"]}<small>분</small></span></div>'
        for i, r in enumerate(d["rows"])
    )
    total = sum(r["minutes"] for r in d["rows"]) + d["fixed_minutes"]
    return (f'<div class="agenda">{rows}<div class="ag-sum" data-box>표지·목차 {d["fixed_minutes"]}분 포함 합계 '
            f'<b data-total="{total}">{total}분</b></div></div>')


def c_statement(d, s, meta):
    qs = "".join(f'<p class="st-q card rise" style="--d:{i+2}" data-box>{esc(q)}</p>' for i, q in enumerate(d["questions"]))
    return (f'<div class="statement"><p class="st-text rise" data-box>{md(d["statement"])}</p>'
            f'<div class="st-qs">{qs}</div></div>')


def c_cards(d, s, meta):
    out = []
    for i, c in enumerate(d["cards"]):
        out.append(f'<article class="card rise" style="--d:{i}" data-box><span class="big" data-box>{esc(c["tag"])}</span>'
                   f'<h3>{esc(c["head"])}</h3><p>{esc(c["body"])}</p><p class="chg">{esc(c["change"])}</p></article>')
    return f'<div class="cards">{"".join(out)}</div>'


def c_flow(d, s, meta):
    out = []
    for i, st in enumerate(d["steps"]):
        if i:
            out.append('<div class="fl-arrow" data-deco aria-hidden="true"><i></i></div>')
        out.append(f'<article class="card fl-step rise" style="--d:{i}" data-box><div class="fl-idx" data-deco>{i+1}</div>'
                   f'<h3 class="fl-name">{esc(st["name"])}</h3><p class="fl-desc">{esc(st["desc"])}</p>'
                   f'<p class="fl-ex">{esc(st["ex"])}</p></article>')
    return f'<div class="flow">{"".join(out)}</div>'


def c_compare(d, s, meta):
    h = (f'<div></div><div class="cp-h l" data-box>{esc(d["left_head"])}</div>'
         f'<div class="cp-h r" data-box>{esc(d["right_head"])}</div>')
    rows = "".join(
        f'<div class="cp-k" data-box>{esc(r["k"])}</div><div class="cp-c l" data-box>{esc(r["l"])}</div>'
        f'<div class="cp-c r" data-box>{esc(r["r"])}</div>' for r in d["rows"])
    return f'<div class="compare rise">{h}{rows}</div>'


def c_case(d, s, meta):
    def card(kind, x):
        return (f'<article class="card cs-card {kind} rise" style="--d:{1 if kind=="bad" else 2}" data-box><span class="pill">{esc(x["label"])}</span>'
                f'<p class="cs-q">“{esc(x["quote"])}”</p><p class="cs-why">{esc(x["why"])}</p></article>')
    return (f'<div class="case"><p class="cs-sit rise" data-box>{esc(d["situation"])}</p>'
            f'<div class="cs-cols">{card("bad", d["bad"])}{card("good", d["good"])}</div></div>')


def c_dialogue(d, s, meta):
    rows = []
    for i, l in enumerate(d["lines"]):
        coach = "coach" if l["who"] == "코치" else "agent"
        step = f'<span class="pill am dl-step" data-box>{esc(l["step"])}</span>' if l["step"] else "<span></span>"
        rows.append(f'<div class="dl-row {coach} rise" style="--d:{i}"><span class="dl-who">{esc(l["who"])}</span>'
                    f'<p class="dl-bub" style="margin:0" data-box>{esc(l["text"])}</p>{step}</div>')
    return f'<div class="dialogue">{"".join(rows)}</div>'


def c_chart(d, s, meta):
    W, H = 1180, 640
    x0, x1, yt, yb = 110, 1160, 50, 540
    bars = d["bars"]; mx = d["max"]; n = len(bars)
    slot = (x1 - x0) / n; bw = 170
    g = []
    for t in range(0, 5):
        v = mx * t / 4; y = yb - (yb - yt) * t / 4
        g.append(f'<line class="grid" x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}"/>'
                 f'<text class="ax" x="{x0-14}" y="{y+8:.1f}" text-anchor="end">{int(v)}</text>')
    b = []
    for i, bar in enumerate(bars):
        h = (yb - yt) * bar["value"] / mx
        x = x0 + slot * i + (slot - bw) / 2; y = yb - h
        cls = "bar hi" if i == n - 1 else "bar"
        b.append(f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{h:.1f}" rx="4" data-value="{bar["value"]}" data-label="{esc(bar["label"])}"/>'
                 f'<text class="val" x="{x+bw/2:.1f}" y="{y-14:.1f}" text-anchor="middle">{bar["value"]}{esc(d["unit"])}</text>'
                 f'<text class="lab" x="{x+bw/2:.1f}" y="{yb+46}" text-anchor="middle">{esc(bar["label"])}</text>')
    asks = "".join(
        f'<div class="card ch-ask rise" style="--d:{i+1}" data-box><span class="q">{esc(a["q"])}</span>'
        f'<span class="pill" style="justify-self:start;background:var(--bad-bg);color:var(--bad)">{esc(a["a"])}</span></div>'
        for i, a in enumerate(d["asks"]))
    svg = (f'<svg class="ch-svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(d["chart_title"])}" data-box>'
           f'{"".join(g)}{"".join(b)}</svg>')
    return (f'<div class="chartwrap"><div class="ch-main"><p class="ch-title" data-box>{esc(d["chart_title"])} (단위: {esc(d["unit"])})</p>{svg}</div>'
            f'<div class="ch-asks">{asks}</div></div>')


def c_grid(d, s, meta):
    t = "".join(f'<div class="card g-tile rise" style="--d:{i}" data-box><span class="k">{esc(x["k"])}</span><span class="q">{esc(x["q"])}</span></div>'
                for i, x in enumerate(d["items"]))
    return f'<div class="grid8">{t}</div>'


def c_practice(d, s, meta):
    steps = "".join(f'<div class="card pr-step rise" style="--d:{i}" data-box><span class="tm">{esc(x["t"])}</span><span class="s">{esc(x["s"])}</span></div>'
                    for i, x in enumerate(d["steps"]))
    rub = "".join(f"<li>{esc(r)}</li>" for r in d["rubric"])
    sec = d["timer_seconds"]
    timer = (f'<div class="card timer" id="tm-{s["id"]}" data-seconds="{sec}" data-box><output aria-live="off">{sec//60:02d}:{sec%60:02d}</output>'
             f'<div class="bt"><button type="button" data-t="start">시작</button><button type="button" data-t="pause">정지</button>'
             f'<button type="button" data-t="reset">초기화</button></div></div>')
    return (f'<div class="practice"><div class="pr-steps">{steps}</div><div class="pr-side">{timer}'
            f'<div class="card" style="padding:18px 0" data-box><div class="rubric-h" style="padding-left:30px">피드백 기준</div><ul class="rubric">{rub}</ul></div>'
            f'<div class="pr-del" data-box>산출물: {esc(d["deliverable"])}</div></div></div>')


def c_quiz(d, s, meta):
    opts = "".join(
        f'<button type="button" class="opt rise" style="--d:{i+1}" data-i="{i}" data-box><span class="mk">{i+1}</span><span>{esc(o)}</span></button>'
        for i, o in enumerate(d["options"]))
    return (f'<div class="quiz" data-answer="{d["answer"]}"><p class="q rise" data-box>{esc(d["question"])}</p>'
            f'<div class="opts">{opts}</div><div class="explain" data-box><span class="verdict"></span>{esc(d["explain"])}</div></div>')


def c_table(d, s, meta):
    cells = "".join(f'<div class="h" data-box>{esc(c)}</div>' for c in d["cols"])
    for r in d["rows"]:
        for c in r:
            ph = " ph" if "[확인 필요]" in c else ""
            cells += f'<div class="{ph.strip()}" data-box>{esc(c)}</div>'
    return f'<div class="tbl rise">{cells}</div>'


def c_summary(d, s, meta):
    tk = "".join(f'<div class="card sm-t rise" style="--d:{i}" data-box><span class="n">{i+1}</span><div><h3>{esc(x["h"])}</h3><p>{esc(x["b"])}</p></div></div>'
                 for i, x in enumerate(d["takeaways"]))
    pl = "".join(f'<div><b>{esc(x["k"])}</b><span>{esc(x["v"])}</span></div>' for x in d["plan"])
    return (f'<div class="summary"><div class="sm-take">{tk}</div>'
            f'<div class="card sm-plan rise" style="--d:3" data-box><h3>{esc(d["plan_head"])}</h3><div class="sm-pl">{pl}</div></div></div>')


COMPONENTS = {
    "agenda": c_agenda, "statement": c_statement, "cards": c_cards, "flow": c_flow, "compare": c_compare,
    "case": c_case, "dialogue": c_dialogue, "chart": c_chart, "grid": c_grid, "practice": c_practice,
    "quiz": c_quiz, "table": c_table, "summary": c_summary,
}


def rail(meta, s):
    if not s["stage"]:
        return ""
    cur = meta["stages"].index(s["stage"])
    dots = []
    for i, name in enumerate(meta["stages"]):
        if i == cur:
            dots.append(f'<i class="cur">{esc(name)}</i>')
        else:
            dots.append(f'<i class="{"done" if i < cur else ""}" title="{esc(name)}"></i>')
    return f'<div class="rail" data-deco aria-label="학습 흐름: {esc(s["stage"])}">{"".join(dots)}</div>'


def slide_html(s, i, n, meta):
    notes = f'<aside class="notes">{esc(s["notes"])}</aside>'
    common = (f'data-id="{s["id"]}" data-type="{s["type"]}" data-title="{esc(s["title"])}" '
              f'data-minutes="{s["minutes"]}" data-stage="{esc(s["stage"])}" data-basis="{s["basis"]}" aria-hidden="true"')
    if s["type"] == "cover":
        m = [("대상", meta["audience"]), ("버전", meta["version"]), ("작성일", meta["date"]), ("상태", meta["status"])]
        dl = "".join(f"<div data-box><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in m)
        return (f'<section class="slide s-cover" {common}><div class="cv-deco" data-deco></div>'
                f'<div class="cv-main"><p class="kicker rise" data-box>{esc(s["kicker"])}</p>'
                f'<h1 class="title rise" style="--d:1" data-box>{esc(s["title"])}</h1>'
                f'<p class="cv-sub rise" style="--d:2" data-box>{esc(meta["subtitle"])}</p></div>'
                f'<p class="cv-disc" data-box>{esc(meta["disclaimer"])}</p>'
                f'<dl class="cv-meta">{dl}</dl>{notes}</section>')
    body = COMPONENTS[s["type"]](s.get("data", {}), s, meta)
    badge = f'<span class="badge b-{s["basis"]}" data-box>{esc(meta["basis_labels"][s["basis"]])}</span>'
    return (f'<section class="slide s-{s["type"]}" {common}>'
            f'<header class="s-head">{rail(meta, s)}<p class="kicker{" dup" if s["kicker"]==s["stage"] else ""}" data-box>{esc(s["kicker"])}</p><h2 class="title" data-box>{esc(s["title"])}</h2></header>'
            f'<div class="s-body">{body}</div>'
            f'<footer class="s-foot"><span class="sowhat" data-box>{esc(s["sowhat"])}</span>'
            f'<span class="src" data-box>{badge}<span>{esc(s["source"])}</span></span><span class="pg" data-box>{i+1} / {n}</span></footer>{notes}</section>')


HUD = ('<nav id="hud" aria-label="발표 컨트롤"><button type="button" data-act="prev" aria-label="이전 슬라이드">◀ 이전</button>'
       '<span class="ctr" aria-live="polite"></span><button type="button" data-act="next" aria-label="다음 슬라이드">다음 ▶</button>'
       '<button type="button" data-act="toc" aria-pressed="false">목차 (T)</button>'
       '<button type="button" data-act="notes" aria-pressed="false">노트 (N)</button>'
       '<button type="button" data-act="anim" aria-pressed="true">애니메이션 ON</button>'
       '<button type="button" data-act="fs" aria-pressed="false">전체화면 (F)</button>'
       '<button type="button" data-act="print">PDF 인쇄 (P)</button>'
       '<button type="button" data-act="help" aria-pressed="false">?</button></nav>')
HELP = ('<div id="help" role="dialog" aria-label="단축키">← → ↑ ↓ Space PageUp/Down : 이동<br>Home / End : 처음 / 끝<br>F : 전체화면 · T : 목차 · N : 발표자 노트<br>'
        'A : 애니메이션 ON/OFF · P : PDF 인쇄 · R : 퀴즈 초기화<br>퀴즈 슬라이드에서 1–4 : 답 선택 · Esc : 패널 닫기</div>')


def font_css():
    p = os.path.join(HERE, "fonts", "PretendardVariable-subset.woff2")
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return ("@font-face{font-family:'Pretendard';font-weight:45 930;font-style:normal;font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}\n")


def read(*p):
    with open(os.path.join(HERE, *p), encoding="utf-8") as f:
        return f.read()


def build(deck_path, out_dir, themes):
    deck = json.load(open(deck_path, encoding="utf-8"))
    meta, slides = deck["meta"], deck["slides"]
    n = len(slides)
    fonts = font_css()
    os.makedirs(out_dir, exist_ok=True)
    outs = []
    for th in themes:
        body = "\n".join(slide_html(s, i, n, meta) for i, s in enumerate(slides))
        doc = (f'<!DOCTYPE html>\n<html lang="{meta["lang"]}" data-deck="{esc(meta["title"])}" data-theme="{th}">\n<head>\n'
               f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
               f'<meta name="generator" content="JoyLab HTML Presentation V1.0 / theme={th}">\n'
               f'<title>{esc(meta["title"])}</title>\n<style>\n{fonts}{read("engine.css")}\n{read("components.css")}\n{read("themes", th + ".css")}\n</style>\n</head>\n'
               f'<body class="theme-{th}">\n<div id="progress" role="progressbar" aria-label="진행률" aria-valuemin="1"><i></i></div>\n'
               f'<main id="viewport"><div id="stage">\n{body}\n</div></main>\n{HUD}\n<aside id="toc" aria-label="슬라이드 목차"><h3>슬라이드 목차</h3></aside>\n'
               f'<aside id="notes-panel" aria-label="발표자 노트"><h4></h4><p></p></aside>\n{HELP}\n'
               f'<script>\n{read("engine.js")}\n</script>\n</body>\n</html>\n')
        path = os.path.join(out_dir, f'{meta["id"]}-{th}.html')
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc)
        outs.append(path)
        print(f"built {path}  ({os.path.getsize(path)/1024:.0f} KB, {n} slides)")
    return outs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", default=os.path.join(HERE, "deck", "test-deck.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "..", "dist"))
    ap.add_argument("--themes", default=",".join(THEMES))
    a = ap.parse_args()
    th = [t.strip() for t in a.themes.split(",") if t.strip()]
    bad = [t for t in th if t not in THEMES]
    if bad:
        sys.exit(f"unknown theme: {bad}")
    build(a.deck, a.out, th)
