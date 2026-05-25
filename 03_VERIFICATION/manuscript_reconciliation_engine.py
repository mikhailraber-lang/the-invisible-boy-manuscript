#!/usr/bin/env python3
"""
MANUSCRIPT RECONCILIATION ENGINE
The Invisible Boy — Safe Harbor Investigations

Purpose: Compare manuscript versions from different AI sources (ChatGPT/Claude)
         and generate detailed reconciliation reports for human decision-making.

SAFETY PRINCIPLES:
    - NEVER auto-merge
    - NEVER overwrite manuscript files
    - NEVER decide which prose is better
    - NEVER silently modify anything
    - READ-ONLY analysis only
    - Human decides what becomes canon

Usage:
    python manuscript_reconciliation_engine.py --chatgpt <path> --claude <path> --output <path>
    python manuscript_reconciliation_engine.py --chatgpt ./WORKING_CHATGPT/ --claude ./WORKING_CLAUDE/ --output ./RECONCILIATION/
    python manuscript_reconciliation_engine.py --chatgpt ./WORKING_CHATGPT/CHAPTER_05_DRAFT.md --claude ./WORKING_CLAUDE/CHAPTER_05_DRAFT.md --output ./RECONCILIATION/

Author: Built for Misha's manuscript workflow
Version: 1.0.0
Date: 2026-05-24
"""

import argparse
import difflib
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# CANON TERMINOLOGY — locked rules from CANON_LOCKS.md
# ═══════════════════════════════════════════════════════════════

CANON_TERMS = {
    "victim_name": {
        "correct": "Maksim",
        "prohibited": ["Maxim", "Maxsim", "Makism", "Maksym", "Maxime"],
        "rule": "Always 'Maksim' with an 'i' — no alternate spellings"
    },
    "case_reference": {
        "correct": "the OD case",
        "prohibited": ["the overdose case", "the OD Case", "the od case", "OD Case"],
        "rule": "Always 'the OD case' — exact casing and phrasing"
    },
    "antagonist_alias": {
        "correct": "the Ghost",
        "prohibited": ["The Ghost", "the ghost", "Ghost", "the GHOST"],
        "rule": "Always 'the Ghost' — lowercase 'the', capital 'G'"
    }
}

CHARACTERS = {
    "Steve Barnes": {
        "role": "IT specialist",
        "relationship_to_victim": "caring connection (NOT romantic/loving)",
        "key_constraint": "Had caring, not romantic/loving connection to Maksim"
    },
    "Jeff Miller": {
        "role": "detective, protagonist",
        "key_constraint": "One of two protagonists"
    },
    "Carl Hansen": {
        "role": "lead detective, Jeff's mentor",
        "key_constraint": "Mentor figure, father-son dynamic with Jeff (NOT training officer)"
    },
    "Thomas Vance": {
        "role": "private investigator",
        "key_constraint": "Jeff's army buddy, later became PI"
    },
    "Travis": {
        "role": "the Ghost / antagonist",
        "key_constraint": "Exists in peripheral vision but never remembered"
    }
}


# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def read_file(filepath):
    """Safely read a file and return its contents."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"  [ERROR] Could not read {filepath}: {e}")
        return None


def extract_chapters_from_file(text):
    """
    Attempt to split a manuscript file into individual chapters.
    Looks for common chapter heading patterns.
    Returns dict: {chapter_identifier: chapter_text}
    """
    # Common patterns: "Chapter 1", "CHAPTER 1", "Chapter One", "# Chapter 1", "## Chapter 1"
    pattern = r'(?=(?:^|\n)(?:#{1,3}\s*)?(?:CHAPTER|Chapter|PROLOGUE|Prologue)\s*[\d\w]*)'
    parts = re.split(pattern, text)

    chapters = {}
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Extract chapter identifier from first line
        first_line = part.split('\n')[0].strip().strip('#').strip()
        if first_line:
            chapters[first_line.upper()] = part

    return chapters if chapters else {"FULL_DOCUMENT": text}


def normalize_text(text):
    """Normalize text for comparison (whitespace, line endings)."""
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def word_count(text):
    """Return word count of text."""
    return len(text.split())


def paragraph_count(text):
    """Return paragraph count of text."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return len(paragraphs)


def extract_dialogue(text):
    """Extract all dialogue lines from text."""
    # Match text in quotes (both straight and curly)
    dialogue = re.findall(r'["\u201c]([^"\u201d]*)["\u201d]', text)
    return dialogue


def find_character_mentions(text):
    """Find all character name mentions in text."""
    mentions = {}
    for name in CHARACTERS:
        # Check full name and last name
        parts = name.split()
        for part in parts:
            if len(part) > 2:  # Skip very short name parts
                count = len(re.findall(r'\b' + re.escape(part) + r'\b', text, re.IGNORECASE))
                if count > 0:
                    if name not in mentions:
                        mentions[name] = 0
                    mentions[name] += count
    return mentions


# ═══════════════════════════════════════════════════════════════
# CANON COMPLIANCE CHECKS
# ═══════════════════════════════════════════════════════════════

def check_canon_terminology(text, source_label):
    """Check text for canon terminology violations."""
    violations = []

    for term_key, term_data in CANON_TERMS.items():
        correct = term_data["correct"]
        for prohibited in term_data["prohibited"]:
            matches = list(re.finditer(re.escape(prohibited), text))
            for match in matches:
                # Get surrounding context
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 40)
                context = text[start:end].replace('\n', ' ')
                violations.append({
                    "source": source_label,
                    "term": term_key,
                    "found": prohibited,
                    "correct": correct,
                    "rule": term_data["rule"],
                    "context": f"...{context}..."
                })

    return violations


def check_victim_last_name(text, source_label):
    """Check that Maksim's last name is never used."""
    warnings = []
    # Look for "Maksim [CapitalizedWord]" patterns that might be a last name
    matches = re.finditer(r'\bMaksim\s+([A-Z][a-z]+)\b', text)
    for match in matches:
        potential_last = match.group(1)
        # Exclude common follow-words that aren't last names
        exclude = {"was", "had", "is", "the", "and", "but", "who", "that", "would", "could",
                    "should", "did", "does", "will", "might", "may", "sat", "stood", "looked",
                    "said", "walked", "ran", "felt", "thought", "knew", "saw", "went", "came"}
        if potential_last.lower() not in exclude:
            context_start = max(0, match.start() - 20)
            context_end = min(len(text), match.end() + 20)
            context = text[context_start:context_end].replace('\n', ' ')
            warnings.append({
                "source": source_label,
                "issue": f"Possible last name usage: 'Maksim {potential_last}'",
                "context": f"...{context}...",
                "rule": "Victim's last name is never used"
            })

    return warnings


# ═══════════════════════════════════════════════════════════════
# COMPARISON ENGINE
# ═══════════════════════════════════════════════════════════════

def compare_texts(text_a, text_b, label_a="ChatGPT", label_b="Claude"):
    """
    Compare two text versions and return detailed analysis.
    NEVER decides which is better. Only identifies differences.
    """
    results = {
        "metrics": {},
        "differences": [],
        "additions": {"a_only": [], "b_only": []},
        "canon_issues": [],
        "character_differences": {},
        "dialogue_differences": {},
        "decision_points": []
    }

    # --- Basic Metrics ---
    norm_a = normalize_text(text_a)
    norm_b = normalize_text(text_b)

    results["metrics"] = {
        f"{label_a}_word_count": word_count(norm_a),
        f"{label_b}_word_count": word_count(norm_b),
        "word_count_difference": abs(word_count(norm_a) - word_count(norm_b)),
        f"{label_a}_paragraph_count": paragraph_count(norm_a),
        f"{label_b}_paragraph_count": paragraph_count(norm_b),
        "paragraph_count_difference": abs(paragraph_count(norm_a) - paragraph_count(norm_b)),
        "similarity_ratio": round(
            difflib.SequenceMatcher(None, norm_a, norm_b).ratio() * 100, 2
        )
    }

    # --- Line-by-Line Diff ---
    lines_a = norm_a.splitlines()
    lines_b = norm_b.splitlines()

    differ = difflib.unified_diff(
        lines_a, lines_b,
        fromfile=label_a, tofile=label_b,
        lineterm=''
    )
    diff_lines = list(differ)

    addition_count = 0
    deletion_count = 0
    change_regions = []
    current_region = []

    for line in diff_lines:
        if line.startswith('+++') or line.startswith('---'):
            continue
        if line.startswith('@@'):
            if current_region:
                change_regions.append(current_region)
            current_region = [line]
        elif line.startswith('+'):
            addition_count += 1
            current_region.append(line)
        elif line.startswith('-'):
            deletion_count += 1
            current_region.append(line)
        else:
            current_region.append(line)

    if current_region:
        change_regions.append(current_region)

    results["differences"] = {
        "total_diff_regions": len(change_regions),
        "lines_only_in_a": deletion_count,
        "lines_only_in_b": addition_count,
        "raw_diff": diff_lines[:500] if len(diff_lines) > 500 else diff_lines,
        "diff_truncated": len(diff_lines) > 500
    }

    # --- Canon Terminology Check ---
    violations_a = check_canon_terminology(text_a, label_a)
    violations_b = check_canon_terminology(text_b, label_b)
    lastname_a = check_victim_last_name(text_a, label_a)
    lastname_b = check_victim_last_name(text_b, label_b)

    results["canon_issues"] = {
        "terminology_violations": violations_a + violations_b,
        "victim_lastname_warnings": lastname_a + lastname_b,
        "total_issues": len(violations_a) + len(violations_b) + len(lastname_a) + len(lastname_b)
    }

    # --- Character Mention Comparison ---
    chars_a = find_character_mentions(text_a)
    chars_b = find_character_mentions(text_b)

    all_chars = set(list(chars_a.keys()) + list(chars_b.keys()))
    for char in all_chars:
        count_a = chars_a.get(char, 0)
        count_b = chars_b.get(char, 0)
        if count_a != count_b:
            results["character_differences"][char] = {
                label_a: count_a,
                label_b: count_b,
                "difference": abs(count_a - count_b)
            }

    # --- Dialogue Comparison ---
    dialogue_a = extract_dialogue(text_a)
    dialogue_b = extract_dialogue(text_b)

    results["dialogue_differences"] = {
        f"{label_a}_dialogue_count": len(dialogue_a),
        f"{label_b}_dialogue_count": len(dialogue_b),
        "count_difference": abs(len(dialogue_a) - len(dialogue_b))
    }

    # --- Decision Points ---
    similarity = results["metrics"]["similarity_ratio"]

    if similarity == 100.0:
        results["decision_points"].append(
            "IDENTICAL: Both versions are exactly the same. No reconciliation needed."
        )
    elif similarity > 95.0:
        results["decision_points"].append(
            "NEAR-IDENTICAL: Minor differences only. Review diff for small edits."
        )
    elif similarity > 75.0:
        results["decision_points"].append(
            "MODERATE DIFFERENCES: Significant sections differ. Manual review required."
        )
    elif similarity > 50.0:
        results["decision_points"].append(
            "SUBSTANTIAL DIFFERENCES: These are meaningfully different versions. "
            "Careful section-by-section reconciliation needed."
        )
    else:
        results["decision_points"].append(
            "MAJOR DIVERGENCE: These may be fundamentally different drafts. "
            "Full chapter-level comparison needed before any merge."
        )

    if results["canon_issues"]["total_issues"] > 0:
        results["decision_points"].append(
            f"CANON ALERT: {results['canon_issues']['total_issues']} canon "
            f"terminology issues found. These must be resolved regardless of "
            f"which version is chosen."
        )

    word_diff = results["metrics"]["word_count_difference"]
    if word_diff > 500:
        results["decision_points"].append(
            f"LENGTH DIVERGENCE: {word_diff} word difference between versions. "
            f"One version may contain scenes or passages missing from the other."
        )

    return results


# ═══════════════════════════════════════════════════════════════
# REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════

def generate_report(chapter_name, results, label_a="ChatGPT", label_b="Claude"):
    """Generate a markdown reconciliation report."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = []
    report.append(f"# RECONCILIATION REPORT: {chapter_name}")
    report.append(f"")
    report.append(f"**Generated:** {timestamp}")
    report.append(f"**Source A:** {label_a}")
    report.append(f"**Source B:** {label_b}")
    report.append(f"**Engine:** manuscript_reconciliation_engine.py v1.0.0")
    report.append(f"")
    report.append(f"---")
    report.append(f"")
    report.append(f"⚠️ **THIS REPORT IS ADVISORY ONLY.**")
    report.append(f"No files have been modified. No merges have been performed.")
    report.append(f"All decisions require Misha's explicit approval.")
    report.append(f"")
    report.append(f"---")
    report.append(f"")

    # --- Metrics ---
    report.append(f"## 1. BASIC METRICS")
    report.append(f"")
    m = results["metrics"]
    report.append(f"| Metric | {label_a} | {label_b} | Difference |")
    report.append(f"|--------|----------|---------|------------|")
    report.append(f"| Word Count | {m[f'{label_a}_word_count']} | {m[f'{label_b}_word_count']} | {m['word_count_difference']} |")
    report.append(f"| Paragraphs | {m[f'{label_a}_paragraph_count']} | {m[f'{label_b}_paragraph_count']} | {m['paragraph_count_difference']} |")
    report.append(f"| Similarity | — | — | {m['similarity_ratio']}% |")
    report.append(f"")

    # --- Decision Points ---
    report.append(f"## 2. DECISION POINTS FOR MISHA")
    report.append(f"")
    for i, point in enumerate(results["decision_points"], 1):
        report.append(f"{i}. {point}")
    report.append(f"")

    # --- Canon Issues ---
    report.append(f"## 3. CANON COMPLIANCE")
    report.append(f"")
    canon = results["canon_issues"]
    if canon["total_issues"] == 0:
        report.append(f"✅ No canon terminology violations detected in either version.")
    else:
        report.append(f"🚨 **{canon['total_issues']} canon issue(s) found:**")
        report.append(f"")
        for v in canon["terminology_violations"]:
            report.append(f"- **[{v['source']}]** Found `{v['found']}` — should be `{v['correct']}`")
            report.append(f"  - Rule: {v['rule']}")
            report.append(f"  - Context: `{v['context']}`")
        for w in canon["victim_lastname_warnings"]:
            report.append(f"- **[{w['source']}]** ⚠️ {w['issue']}")
            report.append(f"  - Rule: {w['rule']}")
            report.append(f"  - Context: `{w['context']}`")
    report.append(f"")

    # --- Character Mentions ---
    report.append(f"## 4. CHARACTER MENTION COMPARISON")
    report.append(f"")
    if results["character_differences"]:
        report.append(f"| Character | {label_a} | {label_b} | Difference |")
        report.append(f"|-----------|----------|---------|------------|")
        for char, data in results["character_differences"].items():
            report.append(f"| {char} | {data[label_a]} | {data[label_b]} | {data['difference']} |")
        report.append(f"")
        report.append(f"*Significant differences in character mention counts may indicate missing scenes or altered character involvement.*")
    else:
        report.append(f"✅ Character mention counts are identical across both versions.")
    report.append(f"")

    # --- Dialogue ---
    report.append(f"## 5. DIALOGUE COMPARISON")
    report.append(f"")
    d = results["dialogue_differences"]
    report.append(f"| Metric | {label_a} | {label_b} |")
    report.append(f"|--------|----------|---------|")
    report.append(f"| Dialogue Lines | {d[f'{label_a}_dialogue_count']} | {d[f'{label_b}_dialogue_count']} |")
    report.append(f"| Difference | — | {d['count_difference']} |")
    report.append(f"")
    if d['count_difference'] > 5:
        report.append(f"⚠️ Significant dialogue count difference. One version may have added or removed conversations.")
    report.append(f"")

    # --- Diff Summary ---
    report.append(f"## 6. DIFFERENCE SUMMARY")
    report.append(f"")
    diff = results["differences"]
    report.append(f"- Total difference regions: {diff['total_diff_regions']}")
    report.append(f"- Lines only in {label_a}: {diff['lines_only_in_a']}")
    report.append(f"- Lines only in {label_b}: {diff['lines_only_in_b']}")
    if diff.get('diff_truncated'):
        report.append(f"- ⚠️ Diff output truncated (over 500 lines of differences)")
    report.append(f"")

    # --- Raw Diff (abbreviated) ---
    report.append(f"## 7. DETAILED DIFF (first 100 lines)")
    report.append(f"")
    report.append(f"```diff")
    for line in diff["raw_diff"][:100]:
        report.append(line)
    if len(diff["raw_diff"]) > 100:
        report.append(f"")
        report.append(f"... [{len(diff['raw_diff']) - 100} more diff lines truncated] ...")
    report.append(f"```")
    report.append(f"")

    # --- Footer ---
    report.append(f"---")
    report.append(f"")
    report.append(f"## RECONCILIATION DECISION LOG")
    report.append(f"")
    report.append(f"*To be filled by Misha after review:*")
    report.append(f"")
    report.append(f"- [ ] Reviewed both versions")
    report.append(f"- [ ] Chose primary version: ________")
    report.append(f"- [ ] Incorporated elements from other version: YES / NO")
    report.append(f"- [ ] Canon issues resolved: YES / NO / N/A")
    report.append(f"- [ ] Final version moved to LOCKED: YES / NO")
    report.append(f"- [ ] Decision date: ________")
    report.append(f"")
    report.append(f"---")
    report.append(f"*This report was generated by manuscript_reconciliation_engine.py*")
    report.append(f"*No files were modified during this analysis.*")

    return "\n".join(report)


# ═══════════════════════════════════════════════════════════════
# DIRECTORY COMPARISON MODE
# ═══════════════════════════════════════════════════════════════

def compare_directories(dir_a, dir_b, output_dir, label_a="ChatGPT", label_b="Claude"):
    """Compare all matching chapter files between two directories."""

    dir_a = Path(dir_a)
    dir_b = Path(dir_b)
    output_dir = Path(output_dir)

    if not dir_a.exists():
        print(f"[ERROR] Directory not found: {dir_a}")
        return
    if not dir_b.exists():
        print(f"[ERROR] Directory not found: {dir_b}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    files_a = {f.name: f for f in dir_a.glob("*.md")}
    files_b = {f.name: f for f in dir_b.glob("*.md")}

    all_files = sorted(set(list(files_a.keys()) + list(files_b.keys())))

    if not all_files:
        print("[WARNING] No .md files found in either directory.")
        return

    print(f"\n{'='*60}")
    print(f"MANUSCRIPT RECONCILIATION ENGINE v1.0.0")
    print(f"{'='*60}")
    print(f"  {label_a} directory: {dir_a} ({len(files_a)} files)")
    print(f"  {label_b} directory: {dir_b} ({len(files_b)} files)")
    print(f"  Output directory:    {output_dir}")
    print(f"{'='*60}\n")

    # --- Inventory Report ---
    inventory_lines = []
    inventory_lines.append(f"# MANUSCRIPT INVENTORY REPORT")
    inventory_lines.append(f"")
    inventory_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    inventory_lines.append(f"")
    inventory_lines.append(f"## Files Found")
    inventory_lines.append(f"")
    inventory_lines.append(f"| File | {label_a} | {label_b} | Status |")
    inventory_lines.append(f"|------|----------|---------|--------|")

    for filename in all_files:
        in_a = "✅" if filename in files_a else "❌"
        in_b = "✅" if filename in files_b else "❌"
        if filename in files_a and filename in files_b:
            status = "READY FOR COMPARISON"
        elif filename in files_a:
            status = f"ONLY IN {label_a}"
        else:
            status = f"ONLY IN {label_b}"
        inventory_lines.append(f"| {filename} | {in_a} | {in_b} | {status} |")

    inventory_path = output_dir / "INVENTORY_REPORT.md"
    with open(inventory_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(inventory_lines))
    print(f"  [CREATED] {inventory_path}")

    # --- Compare matching files ---
    compared = 0
    for filename in all_files:
        if filename in files_a and filename in files_b:
            print(f"\n  Comparing: {filename}")
            text_a = read_file(files_a[filename])
            text_b = read_file(files_b[filename])

            if text_a is None or text_b is None:
                print(f"  [SKIP] Could not read one or both files.")
                continue

            results = compare_texts(text_a, text_b, label_a, label_b)
            chapter_name = filename.replace('.md', '').replace('_', ' ').title()
            report = generate_report(chapter_name, results, label_a, label_b)

            report_name = filename.replace('.md', '_RECONCILIATION_REPORT.md')
            report_path = output_dir / report_name
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"  [CREATED] {report_path}")
            print(f"           Similarity: {results['metrics']['similarity_ratio']}%")
            print(f"           Canon issues: {results['canon_issues']['total_issues']}")
            compared += 1

        elif filename in files_a:
            print(f"\n  [NOTICE] {filename} exists only in {label_a}")
        else:
            print(f"\n  [NOTICE] {filename} exists only in {label_b}")

    print(f"\n{'='*60}")
    print(f"RECONCILIATION COMPLETE")
    print(f"  Files compared: {compared}")
    print(f"  Reports saved to: {output_dir}")
    print(f"  ⚠️  NO FILES WERE MODIFIED")
    print(f"{'='*60}\n")


# ═══════════════════════════════════════════════════════════════
# SINGLE FILE COMPARISON MODE
# ═══════════════════════════════════════════════════════════════

def compare_single_files(file_a, file_b, output_dir, label_a="ChatGPT", label_b="Claude"):
    """Compare two individual files."""

    file_a = Path(file_a)
    file_b = Path(file_b)
    output_dir = Path(output_dir)

    if not file_a.exists():
        print(f"[ERROR] File not found: {file_a}")
        return
    if not file_b.exists():
        print(f"[ERROR] File not found: {file_b}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    text_a = read_file(file_a)
    text_b = read_file(file_b)

    if text_a is None or text_b is None:
        print("[ERROR] Could not read one or both files.")
        return

    print(f"\n{'='*60}")
    print(f"MANUSCRIPT RECONCILIATION ENGINE v1.0.0")
    print(f"{'='*60}")
    print(f"  {label_a}: {file_a}")
    print(f"  {label_b}: {file_b}")
    print(f"{'='*60}\n")

    results = compare_texts(text_a, text_b, label_a, label_b)

    chapter_name = file_a.stem.replace('_', ' ').title()
    report = generate_report(chapter_name, results, label_a, label_b)

    report_name = f"{file_a.stem}_RECONCILIATION_REPORT.md"
    report_path = output_dir / report_name
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"  [CREATED] {report_path}")
    print(f"  Similarity: {results['metrics']['similarity_ratio']}%")
    print(f"  Canon issues: {results['canon_issues']['total_issues']}")
    print(f"\n  ⚠️  NO FILES WERE MODIFIED\n")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Manuscript Reconciliation Engine — The Invisible Boy",
        epilog="This tool NEVER modifies source files. All output is advisory."
    )

    parser.add_argument(
        '--chatgpt', required=True,
        help='Path to ChatGPT version (file or directory)'
    )
    parser.add_argument(
        '--claude', required=True,
        help='Path to Claude version (file or directory)'
    )
    parser.add_argument(
        '--output', required=True,
        help='Path to output directory for reconciliation reports'
    )
    parser.add_argument(
        '--label-a', default='ChatGPT',
        help='Label for first source (default: ChatGPT)'
    )
    parser.add_argument(
        '--label-b', default='Claude',
        help='Label for second source (default: Claude)'
    )

    args = parser.parse_args()

    chatgpt_path = Path(args.chatgpt)
    claude_path = Path(args.claude)

    if chatgpt_path.is_dir() and claude_path.is_dir():
        compare_directories(
            args.chatgpt, args.claude, args.output,
            args.label_a, args.label_b
        )
    elif chatgpt_path.is_file() and claude_path.is_file():
        compare_single_files(
            args.chatgpt, args.claude, args.output,
            args.label_a, args.label_b
        )
    else:
        print("[ERROR] Both paths must be either files or directories.")
        print(f"  --chatgpt: {'directory' if chatgpt_path.is_dir() else 'file' if chatgpt_path.is_file() else 'not found'}")
        print(f"  --claude:  {'directory' if claude_path.is_dir() else 'file' if claude_path.is_file() else 'not found'}")
        sys.exit(1)


if __name__ == "__main__":
    main()
