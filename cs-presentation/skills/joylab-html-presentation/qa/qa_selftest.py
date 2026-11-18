#!/usr/bin/env python3
"""QA 자체 검증(음성 대조군): 결함을 주입한 HTML 복사본이 지정한 검사 코드에서 반드시 FAIL 해야 한다.
QA 가 항상 PASS 만 내는 '무의미한 게이트'가 아님을 증명하기 위한 테스트.
사용: python3 qa/qa_selftest.py   (약 6~8분, executive 테마 1개로 변이 10종 실행)"""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "dist", "joylab-test-deck-executive.html")
base = open(SRC, encoding="utf-8").read()

def sub(pat, rep, s=None, count=1):
    s = base if s is None else s
    new, n = re.subn(pat, rep, s, count=count, flags=re.S)
    assert n, f"mutation target not found: {pat}"
    return new

MUT = {
 "M1 외부 CSS 주입":        (sub(r"</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR"></head>'), {"S1", "S2"}),
 "M2 본문 글자 90px(넘침)":  (sub(r'class="fl-desc"', 'class="fl-desc" style="font-size:90px"'), {"L3"}),
 "M3 쪽번호 14px(작은 글자)": (sub(r'class="pg"', 'class="pg" style="font-size:14px"'), {"T4"}),
 "M4 막대 data-value 변조":  (sub(r'data-value="81"', 'data-value="82"'), {"D3"}),
 "M5 렌더 숫자 35%→53%":     (sub(r">35%<", ">53%<"), {"D3", "D5"}),
 "M6 퀴즈 정답 인덱스 변조":  (sub(r'data-answer="2"', 'data-answer="1"'), {"N13"}),
 "M7 낮은 명암비 글자":       (sub(r'class="st-text rise"', 'class="st-text rise" style="color:#D8D6CC"'), {"T5"}),
 "M8 스테이지 높이 1000px":  (sub(r"height:1080px;\n?\s*transform", "height:1000px;transform"), {"A1", "A2"}),
 "M9 발표자 노트 변조":       (sub(r'<aside class="notes">인사와', '<aside class="notes">변조된 노트 인사와'), {"D1", "N8", "N9"}),
 "M10 요소 겹침(절대위치)":   (sub(r'class="st-q card rise"', 'class="st-q card rise" style="position:relative;top:-330px"'), {"L4", "L1"}),
}

tmp = tempfile.mkdtemp(prefix="jl-selftest-")
summary = []
ONLY = os.environ.get('ONLY')
for name, (html, expect) in MUT.items():
    if ONLY and not name.startswith(ONLY): continue
    d = os.path.join(tmp, name.split()[0]); os.makedirs(d)
    open(os.path.join(d, "joylab-test-deck-executive.html"), "w", encoding="utf-8").write(html)
    out = os.path.join(d, "out")
    subprocess.run([sys.executable, os.path.join(HERE, "qa_playwright.py"), "--dist", d, "--themes", "executive", "--outdir", out],
                   capture_output=True, text=True, timeout=300)
    res = json.load(open(os.path.join(out, "qa_results.json")))["results"]
    failed = {r["code"] for r in res if r["status"] == "FAIL"}
    caught = bool(expect & failed)
    summary.append((name, sorted(expect), sorted(failed), caught))
    print(("CAUGHT " if caught else "MISSED ") + name + f"  expect⊇any{sorted(expect)}  failed={sorted(failed)}", flush=True)
shutil.rmtree(tmp, ignore_errors=True)
ok = all(c for *_, c in summary)
json.dump([{"mutation": a, "expect_any_of": b, "failed_codes": c, "caught": d} for a, b, c, d in summary],
          open(os.path.join(HERE, "out", "selftest_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nSELFTEST: {sum(1 for *_, c in summary if c)}/{len(summary)} caught")
sys.exit(0 if ok else 1)
