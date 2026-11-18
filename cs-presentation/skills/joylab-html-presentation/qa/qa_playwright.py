#!/usr/bin/env python3
"""JoyLab HTML Presentation QA Gate (Playwright).

사용:  python3 qa/qa_playwright.py [--dist dist] [--deck src/deck/test-deck.json] [--themes executive,learning,research]
종료코드: FAIL 이 1건이라도 있으면 1.  UNVERIFIED 는 통과로 세지 않고 별도 표기한다.

검사 (요청 항목 ↔ 코드):
  S  정적: 외부 URL/CDN/@import 문자열 없음, 슬라이드 수
  L  레이아웃: 슬라이드 밖 이탈 / 부모 박스 이탈 / 콘텐츠 넘침(잘림) / 요소 겹침 / 표지 장식 겹침
  T  타이포: 최소 글자 크기 22px, 명암비(WCAG), 폰트 로딩, 한글 글리프 커버리지, 제목 2줄 이하
  N  내비게이션: 방향키·Home/End·경계·해시·목차·노트·애니메이션 토글·전체화면·퀴즈·타이머
  A  화면비: 6개 뷰포트에서 스테이지 16:9 + 뷰포트 내부
  O  오프라인/네트워크: 오프라인 컨텍스트 로드, http(s) 요청 0건, 콘솔 오류 0건
  P  인쇄: PDF 15쪽, 쪽 크기 1920x1080 px, 발표자 노트 미출력
  D  데이터 일치: deck JSON ↔ DOM (제목·노트·시간·차트·퀴즈·표·표기), 렌더 숫자의 출처 추적
  X  테마 간 동일성: 3개 테마의 텍스트 동일
"""
import argparse, json, os, re, subprocess, sys, tempfile, time
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = []
OUTDIR = os.path.join(HERE, "out")


def rec(theme, code, name, status, detail=""):
    RESULTS.append({"theme": theme, "code": code, "name": name, "status": status, "detail": detail})
    mark = {"PASS": "✓", "FAIL": "✗", "UNVERIFIED": "?"}[status]
    print(f"  [{mark}] {code} {name}" + (f" — {detail}" if detail and status != "PASS" else ""))


MEASURE_JS = r"""
(idx)=>{
 const sl=document.querySelectorAll('.slide')[idx]; const S=sl.getBoundingClientRect();
 const out={out_of_slide:[],escapes_parent:[],overflow:[],overlap:[],small_text:[],contrast:[],deco_overlap:[],title_lines:null};
 const vis=e=>{for(let n=e;n&&n!==document.body;n=n.parentElement){const c=getComputedStyle(n); if(c.display==='none'||c.visibility==='hidden')return false;} return true;};
 const desc=e=>(e.tagName.toLowerCase()+(e.className&&e.className.baseVal===undefined?'.'+String(e.className).trim().split(/\s+/).join('.'):'')+' "'+(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,28)+'"');
 const parse=s=>{const m=s.match(/rgba?\(([^)]+)\)/); if(!m)return null; const p=m[1].split(',').map(x=>parseFloat(x)); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1};};
 const R=e=>e.getBoundingClientRect(); const tol=1.5, SAFE=36;
 const boxes=[...sl.querySelectorAll('[data-box]')].filter(e=>!e.closest('.notes')&&vis(e));
 boxes.forEach(e=>{const r=R(e);
   if(r.left<S.left+SAFE-tol||r.right>S.right-SAFE+tol||r.top<S.top+SAFE-tol-28||r.bottom>S.bottom-SAFE+tol+10) out.out_of_slide.push(desc(e)+' '+[r.left-S.left,r.top-S.top,S.right-r.right,S.bottom-r.bottom].map(x=>Math.round(x)).join('/'));
   const p=e.parentElement&&e.parentElement.closest('[data-box]'); if(p&&sl.contains(p)){const b=R(p); if(r.left<b.left-tol||r.right>b.right+tol||r.top<b.top-tol||r.bottom>b.bottom+tol) out.escapes_parent.push(desc(e)+' in '+desc(p));}
 });
 sl.querySelectorAll('*').forEach(e=>{ if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')return; if(e.closest('.notes')||!vis(e))return;
   const cs=getComputedStyle(e); if(cs.display==='inline')return;
   if(e.closest('[data-deco]'))return; const lim=(cs.overflowX==='visible'&&cs.overflowY==='visible')?4:1;
   if(e.scrollWidth>e.clientWidth+lim||e.scrollHeight>e.clientHeight+lim) out.overflow.push(desc(e)+' sw='+e.scrollWidth+'/'+e.clientWidth+' sh='+e.scrollHeight+'/'+e.clientHeight);});
 for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],b=boxes[j]; if(a.contains(b)||b.contains(a))continue;
   const A=R(a),B=R(b); const ix=Math.min(A.right,B.right)-Math.max(A.left,B.left), iy=Math.min(A.bottom,B.bottom)-Math.max(A.top,B.top);
   if(ix>2&&iy>2) out.overlap.push(desc(a)+' x '+desc(b)+' ('+Math.round(ix)+'x'+Math.round(iy)+')');}
 // 표지 장식(의사요소) ↔ 텍스트 겹침
 const deco=sl.querySelector('.cv-deco'); if(deco){const P=R(deco); ['::before','::after'].forEach(ps=>{const c=getComputedStyle(deco,ps); if(c.content==='none'||c.position!=='absolute')return; const bg=parse(c.backgroundColor); if(bg&&bg.a<0.3&&parseFloat(c.borderTopWidth)===0)return;
   let w=parseFloat(c.width),h=parseFloat(c.height); if(isNaN(w)||isNaN(h))return; let l=parseFloat(c.left),t=parseFloat(c.top); if(isNaN(l)){const r=parseFloat(c.right); l=P.width-r-w;} if(isNaN(t)){const b=parseFloat(c.bottom); t=P.height-b-h;}
   const pad=(c.transform!=='none')?0.12*Math.max(w,h):0; const D={left:P.left+l-pad,top:P.top+t-pad,right:P.left+l+w+pad,bottom:P.top+t+h+pad};
   boxes.forEach(b=>{const B=R(b); if(B.width>1500)return; const ix=Math.min(D.right,B.right)-Math.max(D.left,B.left), iy=Math.min(D.bottom,B.bottom)-Math.max(D.top,B.top); if(ix>2&&iy>2) out.deco_overlap.push(ps+' x '+desc(b));});});}
 // 글자 크기 / 명암비
 const lum=(r,g,b)=>{const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)};
 const bgOf=e=>{let layers=[]; for(let n=e;n;n=n.parentElement){const c=parse(getComputedStyle(n).backgroundColor); if(c&&c.a>0){layers.push(c); if(c.a>=0.99)break;}}
   let base={r:255,g:255,b:255}; for(let k=layers.length-1;k>=0;k--){const c=layers[k]; base={r:c.r*c.a+base.r*(1-c.a),g:c.g*c.a+base.g*(1-c.a),b:c.b*c.a+base.b*(1-c.a)};} return base;};
 const opac=e=>{let o=1; for(let n=e;n&&n!==document.body;n=n.parentElement){o*=parseFloat(getComputedStyle(n).opacity);} return o;};
 const w=document.createTreeWalker(sl,NodeFilter.SHOW_TEXT); const seen=new Set(); let t;
 while(t=w.nextNode()){ if(!t.nodeValue.trim())continue; const e=t.parentElement; if(!e||e.closest('.notes')||!vis(e)||seen.has(e))continue; seen.add(e);
   let fs=parseFloat(getComputedStyle(e).fontSize); const svg=e.closest('svg'); if(svg){const r=R(svg),vb=svg.viewBox.baseVal; fs*=Math.min(r.width/vb.width,r.height/vb.height);}
   if(fs<22-0.5) out.small_text.push(desc(e)+' '+fs.toFixed(1)+'px');
   if(opac(e)<0.5)continue;
   const cs=getComputedStyle(e); const fg=parse(cs.color); const bg=bgOf(e); if(!fg)continue;
   const L1=lum(fg.r,fg.g,fg.b), L2=lum(bg.r,bg.g,bg.b); const cr=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
   const large=fs>=24||(fs>=18.66&&parseInt(cs.fontWeight,10)>=700); const need=large?3:4.5;
   if(cr<need) out.contrast.push(desc(e)+' '+cr.toFixed(2)+':1 < '+need);}
 const ti=sl.querySelector('.title'); if(ti&&!sl.classList.contains('s-cover')){const lh=parseFloat(getComputedStyle(ti).lineHeight); out.title_lines=Math.round(R(ti).height/lh);}
 return out;}
"""

NUMBERS_JS = r"""
(idx)=>{const sl=document.querySelectorAll('.slide')[idx].cloneNode(true);
 sl.querySelectorAll('.notes,.pg,.mk,.fl-idx,.rail,output,.ax,.sm-t .n').forEach(n=>n.remove());
 sl.querySelectorAll('*').forEach(e=>e.insertAdjacentText('afterend',' '));
 return sl.textContent;}
"""


def corpus_numbers(deck):
    strs = []
    def walk(o):
        if isinstance(o, dict):
            [walk(v) for v in o.values()]
        elif isinstance(o, list):
            [walk(v) for v in o]
        else:
            strs.append(str(o))
    walk(deck)
    return set(re.findall(r"\d+(?:[.,]\d+)?", " ".join(strs)))


def go(page, i):
    page.evaluate(f"JoyLab.go({i})")
    page.wait_for_timeout(40)


def active_index(page):
    return page.evaluate("JoyLab.current()")


def active_count(page):
    return page.evaluate("document.querySelectorAll('.slide.active').length")


def run_theme(b, theme, path, deck, fontcmap):
    url = "file://" + path
    slides = deck["slides"]; n = len(slides); meta = deck["meta"]
    print(f"\n=== theme: {theme} ({os.path.basename(path)}) ===")
    html = open(path, encoding="utf-8").read()

    # ---- S. 정적
    ext = re.findall(r"""(?i)(?:https?:)?//[a-z0-9.-]+\.[a-z]{2,}""", re.sub(r"data:[^)'\"]+", "", html))
    rec(theme, "S1", "외부 URL 문자열 0건", "PASS" if not ext else "FAIL", f"{ext[:5]}")
    bad = re.findall(r"(?i)<link\b|@import|<script[^>]+\bsrc=|<img[^>]+\bsrc=\"(?!data:)|url\((?!data:)", html)
    rec(theme, "S2", "외부 <link>/@import/src/url() 0건", "PASS" if not bad else "FAIL", f"{bad[:5]}")
    rec(theme, "S3", "슬라이드 수 = JSON", "PASS" if html.count('<section class="slide') == n else "FAIL", f"{html.count('<section class=\"slide')} vs {n}")

    ctx = b.new_context(viewport={"width": 1920, "height": 1080}, offline=True)
    page = ctx.new_page()
    reqs, errs, failed = [], [], []
    page.on("request", lambda r: reqs.append(r.url))
    page.on("requestfailed", lambda r: failed.append(r.url))
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
    page.goto(url); page.wait_for_function("window.JoyLab&&JoyLab.count()>0")
    page.evaluate("document.fonts.ready")
    page.evaluate("document.documentElement.classList.add('no-anim')")

    # ---- O. 오프라인/네트워크
    net = [u for u in reqs if re.match(r"(?i)https?:|wss?:|ftp:", u)]
    rec(theme, "O1", "오프라인 컨텍스트에서 로드·초기화", "PASS" if page.evaluate("JoyLab.count()") == n else "FAIL")
    rec(theme, "O2", "http(s)/ws 요청 0건 (오프라인 컨텍스트)", "PASS" if not net else "FAIL", f"{net[:5]}")
    # ---- T. 폰트
    fl = page.evaluate("""()=>{const out=[];document.fonts.forEach(f=>out.push(f.family+':'+f.status));return out}""")
    ok_font = any(x.startswith("Pretendard") and x.endswith("loaded") for x in fl)
    rec(theme, "T1", "내장 Pretendard 폰트 loaded", "PASS" if ok_font else "FAIL", str(fl))
    used = page.evaluate("""()=>{const s=new Set();document.querySelectorAll('.slide').forEach(sl=>{(sl.textContent||'').split('').forEach(c=>s.add(c))});return [...s].join('')}""")
    miss = sorted({c for c in used if not c.isspace() and ord(c) not in fontcmap})
    rec(theme, "T2", "사용 글자 전부 내장 폰트 글리프 보유(노트 포함)", "PASS" if not miss else "FAIL", f"미보유 {len(miss)}자: {''.join(miss[:30])}")
    famok = page.evaluate("getComputedStyle(document.querySelector('.slide .title')).fontFamily.startsWith('Pretendard')")
    rec(theme, "T3", "본문 font-family 첫 순위 Pretendard", "PASS" if famok else "FAIL")

    # ---- L/T. 슬라이드별 측정
    agg = {k: [] for k in ["out_of_slide", "escapes_parent", "overflow", "overlap", "deco_overlap", "small_text", "contrast"]}
    tl = []
    for i in range(n):
        go(page, i)
        m = page.evaluate(MEASURE_JS, i)
        for k in agg:
            agg[k] += [f"s{i+1:02d} {x}" for x in m[k]]
        if m["title_lines"] is not None and m["title_lines"] > 2:
            tl.append(f"s{i+1:02d} {m['title_lines']}줄")
    for code, key, name in [("L1", "out_of_slide", "요소가 슬라이드 안전영역 밖으로 나가지 않음"), ("L2", "escapes_parent", "자식이 부모 박스를 벗어나지 않음"),
                            ("L3", "overflow", "텍스트·이미지 잘림/넘침 없음(scroll>client)"), ("L4", "overlap", "콘텐츠 요소 간 겹침 없음"),
                            ("L5", "deco_overlap", "표지 장식 ↔ 텍스트 겹침 없음")]:
        rec(theme, code, name, "PASS" if not agg[key] else "FAIL", "; ".join(agg[key][:8]) + (f" …외 {len(agg[key])-8}" if len(agg[key]) > 8 else ""))
    rec(theme, "T4", f"모든 텍스트 ≥ 22px (1920 기준)", "PASS" if not agg["small_text"] else "FAIL", "; ".join(agg["small_text"][:4]))
    rec(theme, "T5", "명암비 WCAG(큰 글자 3:1 / 일반 4.5:1)", "PASS" if not agg["contrast"] else "FAIL", "; ".join(agg["contrast"][:4]))
    rec(theme, "T6", "제목 2줄 이하", "PASS" if not tl else "FAIL", ", ".join(tl))

    # ---- N. 내비게이션
    kb = page.keyboard
    go(page, 0)
    steps = []
    kb.press("ArrowRight"); steps.append(("→", active_index(page) == 1))
    kb.press("ArrowLeft"); steps.append(("←", active_index(page) == 0))
    kb.press("ArrowLeft"); steps.append(("← 경계(1)", active_index(page) == 0))
    kb.press("End"); steps.append(("End", active_index(page) == n - 1))
    kb.press("ArrowRight"); steps.append(("→ 경계(끝)", active_index(page) == n - 1))
    kb.press("Home"); steps.append(("Home", active_index(page) == 0))
    kb.press("PageDown"); kb.press("Space"); kb.press("Enter"); steps.append(("PgDn+Space+Enter", active_index(page) == 3))
    kb.press("PageUp"); kb.press("Backspace"); kb.press("ArrowUp"); steps.append(("PgUp+Bksp+↑", active_index(page) == 0))
    kb.press("ArrowDown"); steps.append(("↓", active_index(page) == 1))
    failn = [s for s, ok in steps if not ok]
    rec(theme, "N1", "방향키·PageUp/Down·Space·Enter·Home/End·경계", "PASS" if not failn else "FAIL", ",".join(failn))
    go(page, 0); once = True; seq = []
    for i in range(n):
        if i: kb.press("ArrowRight")
        once &= (active_index(page) == i and active_count(page) == 1)
        seq.append(page.evaluate("document.querySelector('.slide.active').dataset.id"))
    rec(theme, "N2", "15장 순차 이동: 항상 활성 슬라이드 1장·순서 일치", "PASS" if once and seq == [s["id"] for s in slides] else "FAIL", str(seq))
    pr = page.evaluate("document.querySelector('#progress i').style.width")
    rec(theme, "N3", "진행률 바 = 현재/전체", "PASS" if pr.startswith("100") else "FAIL", pr)
    go(page, 6); pw = page.evaluate("[document.querySelector('#progress i').style.width, document.querySelector('#hud .ctr').textContent, location.hash]")
    rec(theme, "N4", "진행률·카운터·해시 동기화(7장)", "PASS" if pw[0].startswith(f"{7/n*100:.4f}"[:5]) and pw[1] == f"7 / {n}" and pw[2] == "#7" else "FAIL", str(pw))
    p2 = ctx.new_page(); p2.goto(url + "#9"); p2.wait_for_function("window.JoyLab&&JoyLab.count()>0")
    rec(theme, "N5", "URL 해시(#9)로 직접 진입", "PASS" if p2.evaluate("JoyLab.current()") == 8 else "FAIL"); p2.close()
    kb.press("t"); toc_on = page.evaluate("document.body.classList.contains('toc-on')")
    page.evaluate("document.querySelectorAll('.toc-item')[8].click()")
    rec(theme, "N6", "목차 열기(T)·항목 클릭 이동(9장)·자동 닫힘", "PASS" if toc_on and active_index(page) == 8 and not page.evaluate("document.body.classList.contains('toc-on')") else "FAIL")
    tocn = page.evaluate("document.querySelectorAll('.toc-item').length")
    tit = page.evaluate("[...document.querySelectorAll('.toc-item')].map(b=>b.children[1].textContent)")
    rec(theme, "N7", "목차 항목 수·제목 = JSON", "PASS" if tocn == n and tit == [s["title"] for s in slides] else "FAIL")
    go(page, 4); kb.press("n")
    npn = page.evaluate("[document.body.classList.contains('notes-on'), document.querySelector('#notes-panel p').textContent]")
    rec(theme, "N8", "발표자 노트 패널(N) 내용 = JSON 노트(5장)", "PASS" if npn[0] and npn[1].strip() == slides[4]["notes"].strip() else "FAIL")
    go(page, 5)
    rec(theme, "N9", "슬라이드 전환 시 노트 갱신", "PASS" if page.evaluate("document.querySelector('#notes-panel p').textContent").strip() == slides[5]["notes"].strip() else "FAIL")
    kb.press("n")
    before = page.evaluate("document.documentElement.classList.contains('no-anim')")
    kb.press("a"); after = page.evaluate("document.documentElement.classList.contains('no-anim')")
    kb.press("a")
    rec(theme, "N10", "애니메이션 ON/OFF 토글(A)", "PASS" if before and not after else "FAIL", f"before_noanim={before} after_noanim={after}")
    # 애니메이션 ON 일 때 실제로 animation 이 걸리는지(켜짐 상태) / OFF 일 때 none 인지
    page.evaluate("document.documentElement.classList.remove('no-anim');document.documentElement.classList.add('force-anim')"); go(page, 4); go(page, 3)
    an_on = page.evaluate("getComputedStyle(document.querySelector('.slide.active .rise')).animationName")
    page.evaluate("document.documentElement.classList.add('no-anim')")
    an_off = page.evaluate("getComputedStyle(document.querySelector('.slide.active .rise')).animationName")
    rec(theme, "N11", "ON: animation 적용 / OFF: animation none", "PASS" if an_on != "none" and an_off == "none" else "FAIL", f"on={an_on} off={an_off}")
    kb.press("f"); page.wait_for_timeout(250)
    fsel = page.evaluate("!!document.fullscreenElement")
    if fsel:
        kb.press("f"); page.wait_for_timeout(250)
        rec(theme, "N12", "전체화면 진입(F)/해제", "PASS" if not page.evaluate("!!document.fullscreenElement") else "FAIL")
    else:
        rec(theme, "N12", "전체화면 진입(F)", "UNVERIFIED", "헤드리스 Chrome 에서 requestFullscreen 이 거부됨. 실제 Windows/macOS Chrome 에서 수동 확인 필요")
    # 퀴즈
    qres = []
    for si, s in enumerate(slides):
        if s["type"] != "quiz": continue
        go(page, si); page.evaluate("JoyLab.resetQuiz()")
        ans = s["data"]["answer"]
        opts = page.evaluate("[...document.querySelectorAll('.slide.active .opt')].map(o=>o.textContent.replace(/^\\d/,''))")
        qres.append(("opts_" + s["id"], opts == s["data"]["options"]))
        kb.press(str(ans + 1)); r = page.evaluate("[document.querySelector('.slide.active .quiz').dataset.result, document.querySelector('.slide.active .opt.correct')&&document.querySelector('.slide.active .opt.correct').dataset.i]")
        qres.append(("correct_" + s["id"], r[0] == "correct" and r[1] == str(ans)))
        m = page.evaluate(MEASURE_JS, si); qres.append(("layout_after_correct_" + s["id"], not (m["overlap"] or m["overflow"] or m["escapes_parent"] or m["contrast"])))
        page.evaluate("JoyLab.resetQuiz()"); wrong = 0 if ans != 0 else 1
        page.evaluate(f"document.querySelectorAll('.slide.active .opt')[{wrong}].click()")
        r = page.evaluate("[document.querySelector('.slide.active .quiz').dataset.result, document.querySelector('.slide.active .opt.correct').dataset.i, !!document.querySelector('.slide.active .opt.wrong'), document.querySelector('.slide.active .verdict').textContent]")
        qres.append(("wrong_" + s["id"], r[0] == "wrong" and r[1] == str(ans) and r[2]))
        m = page.evaluate(MEASURE_JS, si); qres.append(("layout_after_wrong_" + s["id"], not (m["overlap"] or m["overflow"] or m["escapes_parent"] or m["contrast"])))
        page.evaluate(f"document.querySelectorAll('.slide.active .opt')[0].click()")  # 재클릭 무시
        qres.append(("locked_" + s["id"], page.evaluate("document.querySelector('.slide.active .quiz').dataset.result") == "wrong"))
        kb.press("r"); qres.append(("reset_" + s["id"], page.evaluate("!document.querySelector('.slide.active .quiz').classList.contains('answered')")))
    fq = [k for k, ok in qres if not ok]
    rec(theme, "N13", f"퀴즈 {len(qres)}항목(정답·오답·잠금·초기화·답 표시 후 레이아웃)", "PASS" if not fq else "FAIL", ",".join(fq))
    # 타이머
    ps = [i for i, s in enumerate(slides) if s["type"] == "practice"][0]; go(page, ps)
    t0 = page.evaluate("document.querySelector('.slide.active output').textContent")
    page.evaluate("document.querySelector('.slide.active [data-t=start]').click()"); page.wait_for_timeout(2300)
    t1 = page.evaluate("document.querySelector('.slide.active output').textContent")
    page.evaluate("document.querySelector('.slide.active [data-t=pause]').click()"); page.wait_for_timeout(1200)
    t2 = page.evaluate("document.querySelector('.slide.active output').textContent")
    page.evaluate("document.querySelector('.slide.active [data-t=reset]').click()")
    t3 = page.evaluate("document.querySelector('.slide.active output').textContent")
    rec(theme, "N14", "실습 타이머 시작/정지/초기화", "PASS" if t0 == "03:00" and t1 in ("02:58", "02:57") and t2 == t1 and t3 == "03:00" else "FAIL", f"{t0}->{t1}->{t2}->{t3}")

    # ---- A. 화면비
    ar = []
    for (w, h) in [(1920, 1080), (1366, 768), (1280, 720), (2560, 1080), (1080, 1920), (1024, 768)]:
        page.set_viewport_size({"width": w, "height": h}); page.wait_for_timeout(60)
        r = page.evaluate("(()=>{const r=document.querySelector('#stage').getBoundingClientRect();return [r.width,r.height,r.left,r.top,r.right,r.bottom,innerWidth,innerHeight]})()")
        ratio = r[0] / r[1]; inside = r[2] >= -1 and r[3] >= -1 and r[4] <= r[6] + 1 and r[5] <= r[7] + 1
        ar.append((f"{w}x{h}", abs(ratio - 16 / 9) < 0.006 and inside, f"{ratio:.4f}"))
    page.set_viewport_size({"width": 1920, "height": 1080})
    fa = [f"{a} ratio={c}" for a, ok, c in ar if not ok]
    rec(theme, "A1", "스테이지 16:9(±0.006) & 뷰포트 내부: 1920x1080·1366x768·1280x720·2560x1080·1080x1920·1024x768", "PASS" if not fa else "FAIL", "; ".join(fa))
    rec(theme, "A2", "논리 캔버스 1920x1080", "PASS" if page.evaluate("[getComputedStyle(document.querySelector('#stage')).width,getComputedStyle(document.querySelector('#stage')).height]") == ["1920px", "1080px"] else "FAIL")
    # 1280x720 에서 모든 [data-box] 위치가 1920 기준과 동일(스케일 변환만 일어남)인지
    RECTS="(i)=>{const st=document.querySelector('#stage').getBoundingClientRect();const k=st.width/1920;return [...document.querySelectorAll('.slide')[i].querySelectorAll('[data-box]')].map(e=>{const r=e.getBoundingClientRect();return [(r.left-st.left)/k,(r.top-st.top)/k,r.width/k,r.height/k]})}"
    base = []
    for i in range(n):
        go(page, i); base.append(page.evaluate(RECTS, i))
    page.set_viewport_size({"width": 1280, "height": 720}); page.wait_for_timeout(80)
    sm = []
    for i in range(n):
        go(page, i); r = page.evaluate(RECTS, i)
        if len(r) != len(base[i]) or any(abs(x - y) > 2 for a, b2 in zip(r, base[i]) for x, y in zip(a, b2)): sm.append(i + 1)
    page.set_viewport_size({"width": 1920, "height": 1080})
    rec(theme, "A3", "1280x720에서 모든 요소 위치가 1920 기준과 ±2px 이내(스케일만 적용, 재배치 없음)", "PASS" if not sm else "FAIL", str(sm))

    # ---- D. 데이터 일치
    d_fail = []
    for i, s in enumerate(slides):
        dom = page.evaluate("""(i)=>{const sl=document.querySelectorAll('.slide')[i];return {id:sl.dataset.id,type:sl.dataset.type,title:sl.dataset.title,minutes:sl.dataset.minutes,basis:sl.dataset.basis,
          h:(sl.querySelector('.title')||{}).textContent,notes:sl.querySelector('.notes').textContent,sowhat:(sl.querySelector('.sowhat')||{}).textContent,src:(sl.querySelector('.src>span:last-child')||{}).textContent,
          badge:(sl.querySelector('.badge')||{}).textContent}}""", i)
        if dom["id"] != s["id"]: d_fail.append(f"{s['id']} id")
        if dom["h"].strip() != s["title"] or dom["title"] != s["title"]: d_fail.append(f"{s['id']} title")
        if int(dom["minutes"]) != s["minutes"]: d_fail.append(f"{s['id']} minutes")
        if dom["notes"].strip() != s["notes"].strip(): d_fail.append(f"{s['id']} notes")
        if s["type"] != "cover":
            if dom["sowhat"].strip() != s["sowhat"] or dom["src"].strip() != s["source"]: d_fail.append(f"{s['id']} footer")
            if dom["badge"].strip() != meta["basis_labels"][s["basis"]]: d_fail.append(f"{s['id']} badge")
    rec(theme, "D1", "슬라이드 id·제목·시간·노트·결론·출처·표기 = JSON(15장)", "PASS" if not d_fail else "FAIL", ",".join(d_fail[:6]))
    tot = sum(s["minutes"] for s in slides)
    ag = [s for s in slides if s["type"] == "agenda"][0]["data"]
    agdom = page.evaluate("document.querySelector('[data-total]').dataset.total")
    rec(theme, "D2", "시간 합계: 슬라이드 합 = 총 시간 = 목차 합", "PASS" if tot == meta["total_minutes"] == int(agdom) == sum(r["minutes"] for r in ag["rows"]) + ag["fixed_minutes"] else "FAIL", f"slides={tot} meta={meta['total_minutes']} agenda={agdom}")
    # 차트
    ci = [i for i, s in enumerate(slides) if s["type"] == "chart"][0]; go(page, ci); cd = slides[ci]["data"]
    bars = page.evaluate("[...document.querySelectorAll('.slide.active rect.bar')].map(r=>[parseFloat(r.dataset.value),r.dataset.label,parseFloat(r.getAttribute('height'))])")
    vals = page.evaluate("[...document.querySelectorAll('.slide.active text.val')].map(t=>t.textContent)")
    ratios = [h / v for v, _, h in bars]
    okc = [[b["value"], b["label"]] for b in cd["bars"]] == [[v, l] for v, l, _ in bars] and vals == [f"{b['value']}{cd['unit']}" for b in cd["bars"]] and (max(ratios) - min(ratios)) / max(ratios) < 0.01
    rec(theme, "D3", "차트 막대 값·라벨·높이 비례 = JSON", "PASS" if okc else "FAIL", f"{bars} {vals}")
    # 구조 일치
    stf = []
    def txt(sel): return page.evaluate("(s)=>[...document.querySelectorAll('.slide.active '+s)].map(e=>e.textContent.trim().replace(/\\s+/g,' '))", sel)
    for i, s in enumerate(slides):
        d = s.get("data", {}); go(page, i)
        if s["type"] == "flow" and txt(".fl-name") != [x["name"] for x in d["steps"]]: stf.append(s["id"])
        if s["type"] == "compare" and txt(".cp-c.l") != [r["l"] for r in d["rows"]]: stf.append(s["id"] + " L")
        if s["type"] == "compare" and txt(".cp-c.r") != [r["r"] for r in d["rows"]]: stf.append(s["id"] + " R")
        if s["type"] == "grid" and txt(".g-tile .k") != [x["k"] for x in d["items"]]: stf.append(s["id"])
        if s["type"] == "dialogue" and txt(".dl-bub") != [x["text"] for x in d["lines"]]: stf.append(s["id"])
        if s["type"] == "table":
            cells = txt(".tbl>div")
            if cells != d["cols"] + [c for r in d["rows"] for c in r]: stf.append(s["id"])
        if s["type"] == "cards" and txt(".cards h3") != [x["head"] for x in d["cards"]]: stf.append(s["id"])
        if s["type"] == "summary" and txt(".sm-t h3") != [x["h"] for x in d["takeaways"]]: stf.append(s["id"])
        if s["type"] == "practice" and txt(".rubric li") != d["rubric"]: stf.append(s["id"])
        if s["type"] == "case" and txt(".cs-q") != [f"“{d['bad']['quote']}”", f"“{d['good']['quote']}”"]: stf.append(s["id"])
        if s["type"] == "agenda" and txt(".ag-row .t") != [r["topic"] for r in d["rows"]]: stf.append(s["id"])
    rec(theme, "D4", "컴포넌트 본문(단계·비교·표·대사·퀴즈 선택지·루브릭·사례) = JSON", "PASS" if not stf else "FAIL", ",".join(stf))
    # 숫자 출처 추적
    corp = corpus_numbers(deck); axis = {str(int(cd['max'] * t / 4)) for t in range(5)}; allowed = {str(k) for k in range(0, 16)} | axis
    stray = []
    for i in range(n):
        go(page, i); t = page.evaluate(NUMBERS_JS, i)
        for x in set(re.findall(r"\d+(?:[.,]\d+)?", t)):
            if x not in corp and x not in allowed: stray.append(f"s{i+1:02d}:{x}")
    rec(theme, "D5", "화면에 렌더된 모든 숫자가 JSON 원본에 존재(창작 수치 탐지)", "PASS" if not stray else "FAIL", ",".join(stray[:8]))
    ph_json = sum(json.dumps(s, ensure_ascii=False).count("[확인 필요]") for s in slides)
    ph_dom = sum(page.evaluate("(i)=>document.querySelectorAll('.slide')[i].textContent.split('[확인 필요]').length-1", i) for i in range(n)) - sum(
        page.evaluate("(i)=>document.querySelectorAll('.slide')[i].querySelector('.notes').textContent.split('[확인 필요]').length-1", i) for i in range(n))
    rec(theme, "D6", "[확인 필요]/[가상] 표기가 렌더에서 유지됨", "PASS" if ph_json == ph_dom and page.evaluate("document.querySelector('.s-cover .cv-disc')") else "FAIL", f"json={ph_json} dom_visible={ph_dom}")

    # ---- 콘솔/네트워크 최종
    page.wait_for_timeout(100)
    rec(theme, "O3", "콘솔 오류·페이지 예외 0건", "PASS" if not errs else "FAIL", "; ".join(errs[:3]))
    net = [u for u in reqs if re.match(r"(?i)https?:|wss?:|ftp:", u)]
    rec(theme, "O4", "전 과정 종료 후 http(s) 요청 누계 0건 / 실패 요청 0건", "PASS" if not net and not failed else "FAIL", f"{net[:3]} {failed[:3]}")

    # ---- P. 인쇄
    pdfp = os.path.join(tempfile.gettempdir(), f"jl-{theme}.pdf")
    pg = ctx.new_page(); pg.goto(url); pg.wait_for_function("window.JoyLab&&JoyLab.count()>0")
    pg.pdf(path=pdfp, prefer_css_page_size=True, print_background=True)
    info = subprocess.run(["pdfinfo", pdfp], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1)); size = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info)
    w, h = float(size.group(1)), float(size.group(2))
    rec(theme, "P1", "PDF 쪽수 = 슬라이드 수", "PASS" if pages == n else "FAIL", f"pages={pages}")
    rec(theme, "P2", "PDF 쪽 크기 1920x1080px(=1440x810pt)", "PASS" if abs(w - 1440) < 2 and abs(h - 810) < 2 else "FAIL", f"{w}x{h}pt")
    txtp = subprocess.run(["pdftotext", "-raw", pdfp, "-"], capture_output=True, text=True).stdout
    rec(theme, "P3", "PDF: 모든 슬라이드 제목 포함 · 발표자 노트/HUD 미출력",
        "PASS" if all(s["title"] in re.sub(r"\s+", " ", txtp) or s["title"].replace(" ", "") in txtp.replace(" ", "").replace("\n", "") for s in slides)
        and slides[0]["notes"][:20] not in txtp.replace("\n", " ") and "발표 컨트롤" not in txtp and "이전" not in txtp.split("\n")[0] else "FAIL")
    keep = os.path.join(OUTDIR, f"{theme}.pdf")
    os.replace(pdfp, keep); pg.close()

    # ---- 화면 캡처(시각 증빙)
    shotdir = os.path.join(OUTDIR, "screens", theme); os.makedirs(shotdir, exist_ok=True)
    page.evaluate("document.documentElement.classList.add('no-anim')")
    for i in range(n):
        go(page, i); page.screenshot(path=os.path.join(shotdir, f"{i+1:02d}.png"))
    texts = []
    for i in range(n):
        go(page, i); texts.append(page.evaluate("(i)=>{const sl=document.querySelectorAll('.slide')[i];return [sl.dataset.title,sl.querySelector('.notes').textContent,(sl.querySelector('.s-body')||sl).textContent.replace(/\\s+/g,' ').trim()]}", i))
    ctx.close()
    return texts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=os.path.join(ROOT, "dist")); ap.add_argument("--deck", default=os.path.join(ROOT, "src", "deck", "test-deck.json"))
    ap.add_argument("--themes", default="executive,learning,research"); ap.add_argument("--outdir", default=os.path.join(HERE, "out")); ap.add_argument("--chrome", default=os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"))
    a = ap.parse_args()
    global OUTDIR
    OUTDIR = a.outdir; os.makedirs(OUTDIR, exist_ok=True)
    deck = json.load(open(a.deck, encoding="utf-8")); meta = deck["meta"]
    from fontTools.ttLib import TTFont
    cmap = set(TTFont(os.path.join(ROOT, "src", "fonts", "PretendardVariable-subset.woff2")).getBestCmap().keys())
    all_texts = {}
    with sync_playwright() as p:
        kw = {"args": ["--no-sandbox", "--disable-dev-shm-usage"]}
        if a.chrome and os.path.exists(a.chrome): kw["executable_path"] = a.chrome
        b = p.chromium.launch(**kw)
        print("browser:", b.version)
        for th in a.themes.split(","):
            all_texts[th] = run_theme(b, th, os.path.join(a.dist, f"{meta['id']}-{th}.html"), deck, cmap)
        b.close()
    ths = list(all_texts)
    for th in ths[1:]:
        same = all_texts[th] == all_texts[ths[0]]
        rec(f"{ths[0]}~{th}", "X1", "두 테마의 제목·노트·본문 텍스트 동일(단일 원본)", "PASS" if same else "FAIL")
    tot = {s: sum(1 for r in RESULTS if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIED")}
    print(f"\nSUMMARY  PASS={tot['PASS']}  FAIL={tot['FAIL']}  UNVERIFIED={tot['UNVERIFIED']}  (total {len(RESULTS)})")
    json.dump({"browser": b.version if False else "", "summary": tot, "results": RESULTS}, open(os.path.join(OUTDIR, "qa_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(1 if tot["FAIL"] else 0)


if __name__ == "__main__":
    main()
