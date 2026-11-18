#!/usr/bin/env python3
"""Pretendard Variable(OFL-1.1) -> 오프라인 내장용 woff2 서브셋.
사용: python3 make_font_subset.py <PretendardVariable.ttf|woff2> <out.woff2>
범위: ASCII + 한글 KS X 1001 완성형 2,350자 + 한글 자모 + 일반 구두점/기호.
범위 밖 글자는 시스템 폰트(Apple SD Gothic Neo / Malgun Gothic / Noto Sans CJK KR)로 대체된다."""
import sys
from fontTools import subset
from fontTools.ttLib import TTFont

src, out = sys.argv[1], sys.argv[2]
chars = set(chr(c) for c in range(0x20, 0x7F))
# KS X 1001 한글 2,350자: EUC-KR 0xB0A1~0xC8FE
for hi in range(0xB0, 0xC9):
    for lo in range(0xA1, 0xFF):
        try:
            chars.add(bytes([hi, lo]).decode("euc-kr"))
        except UnicodeDecodeError:
            pass
chars |= set("ㄱㄲㄳㄴㄵㄶㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ")
chars |= set("·…—–‘’“”•→←↑↓↔▶◀▲▼■□●○◆◇★☆✓✕×÷±≤≥≠≈°℃％‰①②③④⑤⑥⑦⑧⑨⑩※§¶©®™〈〉《》「」『』【】〔〕～₩")
opts = subset.Options()
opts.flavor = "woff2"
opts.layout_features = ["*"]
opts.notdef_outline = True
opts.name_IDs = ["*"]
f = TTFont(src)
s = subset.Subsetter(opts)
s.populate(text="".join(sorted(chars)))
s.subset(f)
f.flavor = "woff2"
f.save(out)
print("saved", out, "glyph chars requested:", len(chars))
