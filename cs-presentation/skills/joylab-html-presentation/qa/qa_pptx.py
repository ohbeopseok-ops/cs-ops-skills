#!/usr/bin/env python3
"""PPTX 내보내기 QA. 사용: python3 qa/qa_pptx.py [--dist dist] [--render]
검사: 재로드·장수 / 제목·노트 = JSON / 도형 슬라이드 내부 / 최소 글자 크기 / 텍스트 적합 추정 / 텍스트 박스 겹침 / 외부 링크 / (옵션) LibreOffice PDF 렌더 15쪽.
주의: 렌더는 LibreOffice 기준이며 PowerPoint 실제 렌더는 검증하지 않는다(UNVERIFIED 로 표기)."""
import argparse, json, math, os, re, subprocess, sys, tempfile, zipfile
from pptx import Presentation
from pptx.util import Emu

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
R = []
def rec(theme, code, name, status, detail=""):
    R.append(dict(theme=theme, code=code, name=name, status=status, detail=detail))
    print(f"  [{ {'PASS':'✓','FAIL':'✗','UNVERIFIED':'?'}[status] }] {code} {name}" + (f" — {detail}" if detail and status != "PASS" else ""))

def est_lines(text, width_in, pt):
    cap = width_in * 72.0
    tot = 0
    for ln in text.split("\n"):
        w = sum(pt * (0.93 if ord(c) > 0x2E80 or 0xAC00 <= ord(c) <= 0xD7A3 else 0.56) for c in ln)
        tot += max(1, math.ceil(w / max(cap, 1)))
    return tot

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dist", default=os.path.join(ROOT, "dist")); ap.add_argument("--render", action="store_true")
    ap.add_argument("--deck", default=os.path.join(ROOT, "src", "deck", "test-deck.json")); ap.add_argument("--outdir", default=os.path.join(HERE, "out"))
    a = ap.parse_args(); os.makedirs(a.outdir, exist_ok=True)
    deck = json.load(open(a.deck, encoding="utf-8")); S = deck["slides"]; n = len(S)
    for th in ("executive", "learning", "research"):
        path = os.path.join(a.dist, f"{deck['meta']['id']}-{th}.pptx"); print(f"\n=== pptx theme: {th} ===")
        prs = Presentation(path); sw, sh = prs.slide_width, prs.slide_height
        rec(th, "PX1", "재로드 성공·장수 = JSON·16:9", "PASS" if len(prs.slides) == n and abs(sw / sh - 16 / 9) < 0.005 else "FAIL", f"{len(prs.slides)} {sw/sh:.4f}")
        bad_t, bad_n, oob, small, fit, ovl, notxt = [], [], [], [], [], [], []
        for i, (sl, s) in enumerate(zip(prs.slides, S)):
            title = next((sh_.text_frame.text for sh_ in sl.shapes if sh_.name == "title"), None)
            if title != s["title"]: bad_t.append(s["id"])
            nt = sl.notes_slide.notes_text_frame.text
            if not nt.startswith(s["notes"]): bad_n.append(s["id"])
            texts = []
            for sh_ in sl.shapes:
                x0, y0, x1, y1 = sh_.left, sh_.top, sh_.left + sh_.width, sh_.top + sh_.height
                if x0 < -Emu(9525) or y0 < -Emu(9525) or x1 > sw + 9525 or y1 > sh + 9525: oob.append(f"{s['id']}:{sh_.name}")
                if sh_.has_text_frame and sh_.text_frame.text.strip():
                    tf = sh_.text_frame; sizes = [r.font.size.pt for p in tf.paragraphs for r in p.runs if r.font.size]
                    if sizes:
                        mn = min(sizes)
                        floor = 28 if sh_.name == "title" and s["type"] != "cover" else 12
                        if mn < floor: small.append(f"{s['id']}:{sh_.name}:{mn}pt")
                        wi = (sh_.width - tf.margin_left - tf.margin_right) / 914400; hi = (sh_.height - tf.margin_top - tf.margin_bottom) / 914400
                        need = sum(est_lines(p.text, wi, max([r.font.size.pt for r in p.runs if r.font.size] or [18])) * max([r.font.size.pt for r in p.runs if r.font.size] or [18]) * 1.2 * 1.15 / 72 for p in tf.paragraphs)
                        if need > hi + 0.06: fit.append(f"{s['id']}:{sh_.name}:{tf.text[:14]} need={need:.2f}in>{hi:.2f}in")
                    texts.append((sh_, x0, y0, x1, y1))
            for ai in range(len(texts)):
                for bi in range(ai + 1, len(texts)):
                    A, B = texts[ai], texts[bi]
                    ix = min(A[3], B[3]) - max(A[1], B[1]); iy = min(A[4], B[4]) - max(A[2], B[2])
                    if ix > 45720 and iy > 45720: ovl.append(f"{s['id']}:{A[0].text_frame.text[:8]}×{B[0].text_frame.text[:8]}")
        rec(th, "PX2", "슬라이드 제목 = JSON", "PASS" if not bad_t else "FAIL", ",".join(bad_t))
        rec(th, "PX3", "발표자 노트 = JSON(퀴즈는 정답·해설 추가)", "PASS" if not bad_n else "FAIL", ",".join(bad_n))
        rec(th, "PX4", "모든 도형이 슬라이드 안", "PASS" if not oob else "FAIL", ",".join(oob[:6]))
        rec(th, "PX5", "최소 글자: 제목 ≥28pt, 나머지 ≥12pt", "PASS" if not small else "FAIL", ",".join(small[:6]))
        rec(th, "PX6", "텍스트 적합 추정(글자 폭·줄 수 휴리스틱)", "PASS" if not fit else "FAIL", " | ".join(fit[:5]))
        rec(th, "PX7", "텍스트 박스 간 겹침 없음", "PASS" if not ovl else "FAIL", " | ".join(ovl[:5]))
        z = zipfile.ZipFile(path); ext = [m for nme in z.namelist() if nme.endswith(".rels") for m in re.findall(r'Target="(https?://[^"]+)"[^>]*TargetMode="External"', z.read(nme).decode("utf8", "ignore"))]
        rec(th, "PX8", "외부 링크/원격 리소스 0건", "PASS" if not ext else "FAIL", str(ext[:3]))
        if a.render:
            td = tempfile.mkdtemp(prefix="jl-px-")
            r = subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", td, path], capture_output=True, text=True, timeout=240)
            pdf = os.path.join(td, os.path.basename(path).replace(".pptx", ".pdf"))
            if os.path.exists(pdf):
                pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
                rec(th, "PX9", "LibreOffice PDF 변환 쪽수 = 슬라이드 수", "PASS" if pages == n else "FAIL", f"pages={pages}")
                sd = os.path.join(a.outdir, "pptx_screens", th); os.makedirs(sd, exist_ok=True)
                subprocess.run(["pdftoppm", "-r", "60", "-png", pdf, os.path.join(sd, "p")], capture_output=True)
            else:
                rec(th, "PX9", "LibreOffice PDF 변환", "FAIL", r.stderr[:200])
        rec(th, "PX10", "PowerPoint 실제 렌더·폰트 대체 표시", "UNVERIFIED", "이 환경에는 PowerPoint 가 없음. LibreOffice 렌더만 확인. Pretendard 미설치 PC 에서는 대체 폰트로 표시됨")
    tot = {k: sum(1 for x in R if x["status"] == k) for k in ("PASS", "FAIL", "UNVERIFIED")}
    print("\nSUMMARY", tot); json.dump({"summary": tot, "results": R}, open(os.path.join(a.outdir, "qa_pptx_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(1 if tot["FAIL"] else 0)
main()
