#!/usr/bin/env python3
"""JoyLab HTML Presentation V1.0 — PPTX 내보내기 (동일 deck JSON → 네이티브 .pptx).
HTML 의 인터랙션(퀴즈 클릭, 타이머, 애니메이션)은 PPTX 로 옮겨지지 않는다. 퀴즈 정답·해설은 발표자 노트에 기록한다.
사용: python3 build_pptx.py [--deck deck/test-deck.json] [--out ../dist] [--themes executive,learning,research] [--font Pretendard]
요건: python-pptx>=1.0. 폰트는 PPTX 에 내장되지 않는다 → 실행 PC 에 Pretendard 가 없으면 PowerPoint 가 대체 폰트(맑은 고딕 등)로 표시한다."""
import argparse, json, os
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 13.333, 7.5
PAL = {
    "executive": dict(bg="FAFAF7", bg2="F0EDE4", ink="1A1A1A", ink2="57564F", accent="C17F24", accent_ink="1A1A1A", accent_text="8A5510", teal="2D7D6F",
                      card="FFFFFF", line="DDD8CB", bad="B3322F", bad_bg="FBEDEC", good="1F6B5E", good_bg="E4F1EE", cover_bg="1A1A1A", cover_ink="FAFAF7", cover_ink2="CFC9BA", foot_bg="1A1A1A", foot_ink="FAFAF7", radius=False),
    "learning":  dict(bg="FAFAF7", bg2="E9F2EF", ink="1D2B28", ink2="4B5E59", accent="C17F24", accent_ink="1A1A1A", accent_text="8A5510", teal="2D7D6F",
                      card="FFFFFF", line="D6E3DF", bad="B3322F", bad_bg="FBEBE9", good="1F6B5E", good_bg="DFF1EC", cover_bg="256A5E", cover_ink="FFFFFF", cover_ink2="EAF6F2", foot_bg="FAFAF7", foot_ink="1D2B28", radius=True),
    "research":  dict(bg="12201E", bg2="1B2E2B", ink="F2EFE6", ink2="B7C6C0", accent="E0A040", accent_ink="14201E", accent_text="EDB65C", teal="5FBFAE",
                      card="1B2E2B", line="33504B", bad="FF9C93", bad_bg="3A2423", good="7AD3C2", good_bg="1D3A35", cover_bg="0E1918", cover_ink="F2EFE6", cover_ink2="B7C6C0", foot_bg="12201E", foot_ink="F2EFE6", radius=False),
}
CIRC = ["①", "②", "③", "④"]


def rgb(h): return RGBColor.from_string(h)


class Deck:
    def __init__(self, deck, theme, font):
        self.d, self.t, self.font, self.p = deck, theme, font, PAL[theme]
        self.prs = Presentation(); self.prs.slide_width = Inches(W); self.prs.slide_height = Inches(H)
        self.blank = self.prs.slide_layouts[6]

    # ---------- primitives
    def box(self, sl, x, y, w, h, fill=None, line=None, shape=None, lw=1.0):
        shp = sl.shapes.add_shape(shape or (MSO_SHAPE.ROUNDED_RECTANGLE if self.p["radius"] else MSO_SHAPE.RECTANGLE), Inches(x), Inches(y), Inches(w), Inches(h))
        if shp.shape_type is not None and self.p["radius"] and shape is None:
            try: shp.adjustments[0] = 0.08
            except Exception: pass
        if fill: shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill)
        else: shp.fill.background()
        if line: shp.line.color.rgb = rgb(line); shp.line.width = Pt(lw)
        else: shp.line.fill.background()
        shp.shadow.inherit = False
        return shp

    def text(self, sl, x, y, w, h, s, size=18, color=None, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, fill=None, line=None, pad=0.08, name=None, spacing=1.15):
        shp = self.box(sl, x, y, w, h, fill=fill, line=line) if (fill or line) else sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = shp.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = Inches(pad); tf.margin_top = tf.margin_bottom = Inches(pad * 0.6)
        lines = s if isinstance(s, list) else [s]
        for i, ln in enumerate(lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = align; para.line_spacing = spacing
            r = para.add_run(); r.text = str(ln); f = r.font
            f.size = Pt(size); f.bold = bold; f.name = self.font; f.color.rgb = rgb(color or self.p["ink"])
            rPr = r._r.get_or_add_rPr()
            for tag in ("a:ea", "a:cs"):
                el = rPr.makeelement(qn(tag), {"typeface": self.font}); rPr.append(el)
        if name: shp.name = name
        shp._jl_fit = (w - 2 * pad, h - 1.2 * pad, size, lines)
        return shp

    def new(self, s):
        sl = self.prs.slides.add_slide(self.blank)
        bg = sl.background.fill; bg.solid(); bg.fore_color.rgb = rgb(self.p["cover_bg"] if s["type"] == "cover" else self.p["bg"])
        sl.notes_slide.notes_text_frame.text = s["notes"]
        return sl

    def chrome(self, sl, s, i, n):
        p = self.p; meta = self.d["meta"]
        self.text(sl, 0.6, 0.32, 9.5, 0.36, s["kicker"], 14, p["accent_text"] if self.t != "research" else p["teal"], True, name="kicker")
        self.text(sl, 0.6, 0.66, 12.1, 0.8, s["title"], 30, p["ink"], True, anchor=MSO_ANCHOR.MIDDLE, name="title")
        yb = 6.78
        self.text(sl, 0.6, yb, 7.6, 0.5, s["sowhat"], 16, p["foot_ink"] if self.t == "executive" else p["ink"], True, anchor=MSO_ANCHOR.MIDDLE,
                  fill=p["foot_bg"] if self.t == "executive" else None, name="sowhat", pad=0.14)
        lab = meta["basis_labels"][s["basis"]]
        self.text(sl, 8.3, yb, 3.7, 0.5, f"[{lab}] {s['source']}", 12, p["ink2"], False, anchor=MSO_ANCHOR.MIDDLE, name="source")
        self.text(sl, 12.0, yb, 0.75, 0.5, f"{i+1} / {n}", 12, p["ink2"], False, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE, name="pagenum")

    # ---------- components
    def cover(self, sl, s):
        p = self.p; m = self.d["meta"]
        self.text(sl, 0.9, 2.0, 11, 0.4, s["kicker"], 16, "E0A040" if self.t != "learning" else "FFE2AE", True)
        self.text(sl, 0.9, 2.45, 11.6, 1.7, s["title"], 44, p["cover_ink"], True, anchor=MSO_ANCHOR.TOP, name="title")
        self.text(sl, 0.9, 4.2, 11, 0.6, m["subtitle"], 20, p["cover_ink2"])
        meta = [("대상", m["audience"]), ("버전", m["version"]), ("작성일", m["date"]), ("상태", m["status"])]
        xs = [0.9, 4.6, 6.2, 8.2]; ws = [3.6, 1.5, 1.9, 4.6]
        for (k, v), x, w in zip(meta, xs, ws):
            self.text(sl, x, 6.0, w, 0.3, k, 12, p["cover_ink2"], False)
            self.text(sl, x, 6.3, w, 0.5, v, 16, p["cover_ink"], True)
        self.text(sl, 7.4, 0.5, 5.4, 0.8, m["disclaimer"], 12, p["cover_ink2"], False, PP_ALIGN.RIGHT, name="disclaimer")

    def agenda(self, sl, d):
        p = self.p
        for i, r in enumerate(d["rows"]):
            y = 1.7 + i * 0.78
            self.box(sl, 0.6, y, 12.1, 0.66, p["card"], p["line"])
            self.text(sl, 0.7, y, 3.3, 0.66, r["stage"], 16, p["ink"], True, anchor=MSO_ANCHOR.MIDDLE)
            self.text(sl, 4.0, y, 5.3, 0.66, r["topic"], 18, p["ink"], False, anchor=MSO_ANCHOR.MIDDLE)
            self.text(sl, 9.4, y, 1.7, 0.66, f"슬라이드 {r['slides']}", 14, p["ink2"], False, anchor=MSO_ANCHOR.MIDDLE)
            self.text(sl, 11.2, y, 1.4, 0.66, f"{r['minutes']}분", 22, p["accent_text"], True, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE)
        tot = sum(r["minutes"] for r in d["rows"]) + d["fixed_minutes"]
        self.text(sl, 8.0, 6.4, 4.7, 0.4, f"표지·목차 {d['fixed_minutes']}분 포함 합계 {tot}분", 14, p["ink2"], False, PP_ALIGN.RIGHT)

    def statement(self, sl, d):
        p = self.p
        self.text(sl, 0.6, 1.6, 12.1, 2.4, d["statement"].replace("**", ""), 36, p["ink"], True, anchor=MSO_ANCHOR.MIDDLE, name="statement")
        for i, q in enumerate(d["questions"]):
            self.text(sl, 0.6 + i * 4.1, 4.5, 3.9, 1.7, q, 18, p["ink"], True, anchor=MSO_ANCHOR.MIDDLE, fill=p["card"], line=p["line"], pad=0.18)

    def cards(self, sl, d):
        p = self.p
        for i, c in enumerate(d["cards"]):
            x = 0.6 + i * 4.1
            self.box(sl, x, 1.65, 3.9, 4.95, p["card"], p["line"])
            self.text(sl, x + 0.15, 1.7, 3.6, 0.9, c["tag"], 44, p["accent_text"], True)
            self.text(sl, x + 0.15, 2.6, 3.6, 1.05, c["head"], 22, p["ink"], True)
            self.text(sl, x + 0.15, 3.7, 3.6, 1.6, c["body"], 18, p["ink"])
            self.text(sl, x + 0.15, 5.4, 3.6, 1.1, c["change"], 14, p["ink2"])

    def flow(self, sl, d):
        p = self.p
        for i, st in enumerate(d["steps"]):
            x = 0.6 + i * 3.1
            self.box(sl, x, 1.65, 2.75, 4.95, p["card"], p["line"])
            c = self.box(sl, x + 0.2, 1.8, 0.55, 0.55, p["accent"], None, MSO_SHAPE.OVAL)
            self.text(sl, x + 0.2, 1.8, 0.55, 0.55, str(i + 1), 20, p["accent_ink"], True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, pad=0)
            self.text(sl, x + 0.15, 2.45, 2.45, 0.6, st["name"], 24, p["ink"], True)
            self.text(sl, x + 0.15, 3.1, 2.45, 0.9, st["desc"], 18, p["ink"])
            self.text(sl, x + 0.15, 4.2, 2.45, 2.2, st["ex"], 14, p["ink"], fill=p["bg2"], pad=0.14, anchor=MSO_ANCHOR.MIDDLE)
            if i < 3:
                self.box(sl, x + 2.8, 3.8, 0.26, 0.4, p["accent"], None, MSO_SHAPE.CHEVRON)

    def compare(self, sl, d):
        p = self.p
        rows = len(d["rows"]) + 1
        gt = sl.shapes.add_table(rows, 3, Inches(0.6), Inches(1.65), Inches(12.1), Inches(0.8 * rows)).table
        for j, wd in enumerate([2.6, 4.75, 4.75]): gt.columns[j].width = Inches(wd)
        def cell(r, c, s, size, color, fill, bold=False):
            ce = gt.cell(r, c); ce.fill.solid(); ce.fill.fore_color.rgb = rgb(fill); ce.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = ce.text_frame; tf.word_wrap = True; pa = tf.paragraphs[0]; ru = pa.add_run(); ru.text = s
            ru.font.size = Pt(size); ru.font.bold = bold; ru.font.name = self.font; ru.font.color.rgb = rgb(color)
        cell(0, 0, "", 18, p["ink"], p["bg"]); cell(0, 1, d["left_head"], 22, p["bad"], p["bad_bg"], True); cell(0, 2, d["right_head"], 22, p["good"], p["good_bg"], True)
        for i, r in enumerate(d["rows"], 1):
            cell(i, 0, r["k"], 18, p["ink2"], p["bg"], True); cell(i, 1, r["l"], 20, p["ink"], p["card"]); cell(i, 2, r["r"], 20, p["ink"], p["card"], True)
            gt.rows[i].height = Inches(0.8)
        gt.rows[0].height = Inches(0.8)

    def case(self, sl, d):
        p = self.p
        self.text(sl, 0.6, 1.55, 12.1, 0.95, d["situation"], 18, p["ink"], fill=p["bg2"], anchor=MSO_ANCHOR.MIDDLE, pad=0.16)
        for i, (k, c, col, bg) in enumerate([("bad", d["bad"], p["bad"], p["bad_bg"]), ("good", d["good"], p["good"], p["good_bg"])]):
            x = 0.6 + i * 6.15
            self.box(sl, x, 2.65, 5.95, 3.95, p["card"], col, lw=2.0)
            self.text(sl, x + 0.2, 2.8, 4.0, 0.45, c["label"], 16, col, True, fill=bg, pad=0.12)
            self.text(sl, x + 0.2, 3.4, 5.55, 2.0, "“" + c["quote"] + "”", 20, p["ink"], True, anchor=MSO_ANCHOR.MIDDLE)
            self.text(sl, x + 0.2, 5.55, 5.55, 0.9, c["why"], 16, p["ink2"])

    def dialogue(self, sl, d):
        p = self.p
        for i, l in enumerate(d["lines"]):
            y = 1.7 + i * 0.96
            self.text(sl, 0.6, y, 1.1, 0.8, l["who"], 16, p["ink2"], True, PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE)
            self.text(sl, 1.85, y, 8.5, 0.8, l["text"], 18, p["ink"], False, anchor=MSO_ANCHOR.MIDDLE, fill=p["bg2"] if l["who"] == "코치" else p["card"], line=p["line"], pad=0.16)
            if l["step"]: self.text(sl, 10.55, y + 0.15, 2.0, 0.5, l["step"], 16, p["accent_ink"], True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, fill=p["accent"], pad=0.06)

    def chart(self, sl, d):
        p = self.p
        self.text(sl, 0.6, 1.55, 7.8, 0.45, f"{d['chart_title']} (단위: {d['unit']})", 18, p["ink"], True)
        cd = CategoryChartData(); cd.categories = [b["label"] for b in d["bars"]]; cd.add_series("값", [b["value"] for b in d["bars"]])
        gf = sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.6), Inches(2.05), Inches(7.8), Inches(4.6), cd); ch = gf.chart
        ch.has_legend = False; ch.has_title = False
        va = ch.value_axis; va.maximum_scale = d["max"]; va.minimum_scale = 0; va.major_unit = d["max"] / 4
        va.tick_labels.font.size = Pt(14); va.tick_labels.font.color.rgb = rgb(p["ink2"]); va.major_gridlines.format.line.color.rgb = rgb(p["line"])
        va.format.line.fill.background()
        ca = ch.category_axis; ca.tick_labels.font.size = Pt(16); ca.tick_labels.font.color.rgb = rgb(p["ink"]); ca.format.line.color.rgb = rgb(p["line"])
        pl = ch.plots[0]; pl.gap_width = 60; pl.has_data_labels = True
        dl = pl.data_labels; dl.font.size = Pt(20); dl.font.bold = True; dl.font.color.rgb = rgb(p["ink"]); dl.position = XL_LABEL_POSITION.OUTSIDE_END
        dl.number_format = '0"%"' if d["unit"] == "%" else "General"; dl.number_format_is_linked = False
        ser = pl.series[0]
        for i in range(len(d["bars"])):
            pt = ser.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(p["accent"] if i == len(d["bars"]) - 1 else ("9C978A" if self.t == "executive" else "7FB5A9" if self.t == "learning" else "4E8077"))
        for i, a in enumerate(d["asks"]):
            y = 1.65 + i * 1.65
            self.box(sl, 8.7, y, 4.0, 1.5, p["card"], p["line"])
            self.text(sl, 8.8, y + 0.08, 3.8, 0.85, a["q"], 18, p["ink"], True)
            self.text(sl, 8.8, y + 0.92, 2.2, 0.42, a["a"], 14, p["bad"], True, fill=p["bad_bg"], pad=0.1)

    def grid(self, sl, d):
        p = self.p
        for i, it in enumerate(d["items"]):
            x = 0.6 + (i % 4) * 3.05; y = 1.65 + (i // 4) * 2.55
            self.box(sl, x, y, 2.9, 2.4, p["card"], p["line"])
            self.box(sl, x + 0.2, y + 0.2, 0.5, 0.07, p["accent"])
            self.text(sl, x + 0.12, y + 0.35, 2.66, 0.6, it["k"], 22, p["ink"], True)
            self.text(sl, x + 0.12, y + 1.0, 2.66, 1.3, it["q"], 16, p["ink2"])

    def practice(self, sl, d):
        p = self.p
        for i, st in enumerate(d["steps"]):
            y = 1.65 + i * 1.22
            self.box(sl, 0.6, y, 7.3, 1.1, p["card"], p["line"])
            self.text(sl, 0.7, y, 1.3, 1.1, st["t"], 26, p["accent_text"], True, anchor=MSO_ANCHOR.MIDDLE)
            self.text(sl, 2.0, y, 5.8, 1.1, st["s"], 20, p["ink"], True, anchor=MSO_ANCHOR.MIDDLE)
        sec = d["timer_seconds"]
        self.text(sl, 8.2, 1.65, 4.5, 1.1, f"{sec//60:02d}:{sec%60:02d}", 48, p["ink"], True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE, fill=p["card"], line=p["line"])
        self.box(sl, 8.2, 2.9, 4.5, 2.7, p["card"], p["line"])
        self.text(sl, 8.3, 2.95, 4.3, 0.4, "피드백 기준", 14, p["ink2"], True)
        for j, r in enumerate(d["rubric"]):
            self.text(sl, 8.3, 3.35 + j * 0.55, 4.3, 0.5, "☐ " + r, 16, p["ink"], True)
        self.text(sl, 8.2, 5.75, 4.5, 0.85, "산출물: " + d["deliverable"], 16, p["accent_ink"], True, anchor=MSO_ANCHOR.MIDDLE, fill=p["accent"], pad=0.16)

    def quiz(self, sl, d):
        p = self.p
        self.text(sl, 0.6, 1.55, 12.1, 0.8, d["question"], 28, p["ink"], True, anchor=MSO_ANCHOR.MIDDLE)
        for i, o in enumerate(d["options"]):
            x = 0.6 + (i % 2) * 6.15; y = 2.55 + (i // 2) * 2.0
            self.text(sl, x, y, 5.95, 1.8, f"{CIRC[i]}  {o}", 20, p["ink"], True, anchor=MSO_ANCHOR.MIDDLE, fill=p["card"], line=p["line"], pad=0.2)
        self.text(sl, 0.6, 6.55, 12.1, 0.2, "", 12)

    def table(self, sl, d):
        p = self.p
        gt = sl.shapes.add_table(4, 4, Inches(0.6), Inches(1.65), Inches(12.1), Inches(4.8)).table
        for j, wd in enumerate([4.6, 2.2, 2.7, 2.6]): gt.columns[j].width = Inches(wd)
        def cell(r, c, s, size, color, fill, bold):
            ce = gt.cell(r, c); ce.fill.solid(); ce.fill.fore_color.rgb = rgb(fill); ce.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = ce.text_frame; tf.word_wrap = True; ru = tf.paragraphs[0].add_run(); ru.text = s
            ru.font.size = Pt(size); ru.font.bold = bold; ru.font.name = self.font; ru.font.color.rgb = rgb(color)
        hb = p["ink"] if self.t != "research" else p["bg2"]; hi = p["bg"] if self.t != "research" else p["ink"]
        if self.t == "learning": hb, hi = p["teal"], "FFFFFF"
        for j, c in enumerate(d["cols"]): cell(0, j, c, 18, hi, hb, True)
        for i, r in enumerate(d["rows"], 1):
            for j, c in enumerate(r): cell(i, j, c, 18, p["bad"] if "[확인 필요]" in c else p["ink"], p["card"], "[확인 필요]" in c)
        gt.rows[0].height = Inches(0.7)
        for i in range(1, 4): gt.rows[i].height = Inches(1.35)

    def summary(self, sl, d):
        p = self.p
        for i, t in enumerate(d["takeaways"]):
            y = 1.65 + i * 1.65
            self.box(sl, 0.6, y, 6.9, 1.5, p["card"], p["line"])
            self.text(sl, 0.7, y, 0.8, 1.5, str(i + 1), 36, p["accent_text"], True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
            self.text(sl, 1.55, y + 0.12, 5.8, 0.55, t["h"], 22, p["ink"], True)
            self.text(sl, 1.55, y + 0.68, 5.8, 0.75, t["b"], 16, p["ink2"])
        self.box(sl, 7.8, 1.65, 4.9, 4.8, p["bg2"], None)
        self.text(sl, 7.95, 1.75, 4.6, 0.6, d["plan_head"], 20, p["ink"], True)
        for j, it in enumerate(d["plan"]):
            self.text(sl, 7.95, 2.55 + j * 1.3, 1.0, 0.5, it["k"], 16, p["teal"], True)
            self.text(sl, 8.95, 2.5 + j * 1.3, 3.65, 1.2, it["v"], 16, p["ink"])

    # ---------- build
    def build(self):
        n = len(self.d["slides"])
        for i, s in enumerate(self.d["slides"]):
            sl = self.new(s)
            if s["type"] == "cover": self.cover(sl, s); continue
            self.chrome(sl, s, i, n)
            getattr(self, s["type"])(sl, s["data"])
            if s["type"] == "quiz":
                sl.notes_slide.notes_text_frame.text = s["notes"] + f"\n\n[정답] {CIRC[s['data']['answer']]} {s['data']['options'][s['data']['answer']]}\n[해설] {s['data']['explain']}\n(PPTX 에서는 클릭 응답이 동작하지 않습니다. 인터랙티브 퀴즈는 HTML 버전을 사용하세요.)"
        return self.prs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", default=os.path.join(HERE, "deck", "test-deck.json")); ap.add_argument("--out", default=os.path.join(HERE, "..", "dist"))
    ap.add_argument("--themes", default="executive,learning,research"); ap.add_argument("--font", default="Pretendard")
    a = ap.parse_args()
    deck = json.load(open(a.deck, encoding="utf-8")); os.makedirs(a.out, exist_ok=True)
    for th in a.themes.split(","):
        prs = Deck(deck, th, a.font).build()
        path = os.path.join(a.out, f"{deck['meta']['id']}-{th}.pptx"); prs.save(path)
        print("saved", path, f"{os.path.getsize(path)/1024:.0f} KB")


if __name__ == "__main__":
    main()
