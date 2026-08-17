[한국어](README.md) | English

<div align="center">

# CS Ops Skills

**A general assistant gives general answers. CS Ops Skills gives you a draft you can act on.**

A Claude Code / Cowork skill marketplace for contact-center (home CS) operations management.

<p>
  <a href="https://docs.anthropic.com/en/docs/claude-code"><img src="https://img.shields.io/badge/platform-Claude_Code%20%C2%B7%20Cowork-D97757?logo=claude" alt="Claude Code · Cowork"></a>
  <img src="https://img.shields.io/badge/plugins-8-6E56CF" alt="8 plugins">
  <img src="https://img.shields.io/badge/skills-29-3FB950" alt="29 skills">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-F0B72F" alt="MIT"></a>
</p>

</div>

> **Language note** — the skills themselves are written in Korean and produce Korean output.
> They encode Korean contact-center practice (T-NPS, AutoQA, elderly-customer handling, Korean
> PII formats). This page exists so non-Korean readers can evaluate the repository; to actually
> use the skills you want a Korean-language workflow.

---

## ⚡ Install

### Claude Cowork (recommended for non-developers)

1. Open **Customize** (bottom left)
2. **Browse plugins** → **Personal** → **+**
3. Choose **Add marketplace from GitHub**
4. Enter: `ohbeopseok-ops/cs-ops-skills`

### Claude Code (CLI)

```bash
/plugin marketplace add https://github.com/ohbeopseok-ops/cs-ops-skills.git
/plugin install cs-quality-analysis@cs-ops-skills
```

Install only the domains you need — the 8 plugins are independent of each other.

## 🧭 Coverage

**Quality analysis · Coaching · Performance · VOC · STT analysis · Operations planning ·
Reporting · Toolkit** — 8 plugins, 29 skills, 7 commands.
Full catalog → **[SKILLS.md](SKILLS.md)**

Repeatable work runs as a command chain:

```
/evaluate            # mask PII → analyze conversation → check compliance → score quality
/analyze-complaints  # categorize → root cause → improvement tasks
/weekly-report       # metrics → causes → action items
```

## 🆚 A general assistant vs `+ CS Ops Skills`

| Request | General assistant | `+ CS Ops Skills` |
| :--- | :--- | :--- |
| "Evaluate this call" | An ad-hoc verdict on shifting criteria | Fixed 100-point rubric → per-item scores + grade |
| "Why did T-NPS drop?" | Generic CS advice | Metric decomposition → at-risk agents → intervention priority |
| "Write coaching feedback" | Praise and encouragement | Weak items → quoted evidence → actionable behavior |
| "Weekly report" | A prose summary | Fixed template + metric table + causes + action items |
| When data is missing | Fills the gap plausibly | Leaves it as `판단 불가` (cannot determine) |
| When the transcript holds PII | Quotes it verbatim | Masks first, then analyzes |

The last two rows are the point of this repository. The goal is not convenience —
it is **not producing numbers that aren't there**.

## ⚙️ How it works

**Skills** — the unit of domain knowledge, analysis framework, and output template. They attach
themselves during ordinary conversation.
**Commands** — slash-invoked workflows that chain several skills in a fixed order.
**Plugins** — installable bundles of related skills and commands, one per operational domain.

Every skill carries the **[harness rules R1–R8](HARNESS.md)** inline: no invented numbers, PII
masking first, evidence quotation required, insufficient data reported as *cannot determine*, and
input transcripts treated as data rather than instructions. Skills decide what the assistant
*knows*; the harness decides what it *won't do*.

## 🔒 Boundaries

CS Ops Skills is an **analysis aid**. It does not replace human judgment.

- **Quality scores, grades, and T-NPS predictions are LLM output**, not validated measurements.
  Verify that quoted utterances match the source before showing them to anyone.
- **Not a sole basis for decisions about individuals** — performance reviews, bonuses, discipline,
  and contract renewals need human review and your organization's formal process.
- **PII masking is not guaranteed complete** — human review is required before any export.
- **The rubrics and grade bands are not any organization's official internal standard.** Reconcile
  them with your own before operational use.
- This repository is **not affiliated with LG U+ or its subsidiaries.**

Full text: [DISCLAIMER.md](DISCLAIMER.md).

## ✅ Validation

```bash
python3 scripts/validate.py
```

Checks manifest consistency, SKILL.md frontmatter, presence of the harness block, whether commands
promised by the docs actually exist, and **R3 (no real data committed)** — resident-registration,
phone, and account-number patterns. Standard library only; runs in CI on every push.

## License

MIT — see [LICENSE](LICENSE). Scope of use and responsibilities: [DISCLAIMER.md](DISCLAIMER.md).
