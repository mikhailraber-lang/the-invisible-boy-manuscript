# Modulatio Configuration for The Invisible Boy

This document defines how Modulatio orchestrates the manuscript workflow with multi-model agent coordination.

---

## Project Overview

**Project Name:** `invisible-boy-project`

**Purpose:** Orchestrate collaborative AI-driven manuscript development with rigorous quality control and canon verification.

**Workflow:** ARCHITECT → BUILDER → VERIFICATION → AUTHOR REVIEW → LOCK

---

## Agent Roles & Configuration

### 1. **LEADER** (Conversational Orchestrator)
- **Role:** Project director, workflow coordinator, quality gate authority
- **Responsibilities:**
  - Interview sessions for new chapters
  - Decompose chapter objectives into tasks
  - Route to specialized agents
  - Make final quality decisions
  - Command verification gates
- **Recommended Model:** Strong reasoning (Claude 3.5 Sonnet, o1, or similar)
- **Provider:** Anthropic or OpenAI

### 2. **ARCHITECT** (Plot & Structure Agent)
- **Role:** Strategic planning, canon alignment, narrative structure
- **Responsibilities:**
  - Analyze chapter objectives against MASTER_CHEAT_SHEET.md
  - Define scene structure and beats
  - Ensure canon consistency
  - Flag continuity risks
- **Recommended Model:** Strong context & reasoning (Claude, GPT-4)
- **Provider:** Anthropic or OpenAI

### 3. **BUILDER** (Prose Generation Agent)
- **Role:** Chapter drafting and prose creation
- **Responsibilities:**
  - Write scenes following ARCHITECT specifications
  - Maintain noir tone and pacing
  - Generate multiple draft versions
  - Handle revision requests
- **Recommended Model:** Fast, capable (Claude 3.5 Sonnet, GPT-4o, Grok)
- **Provider:** Anthropic, OpenAI, or xAI

### 4. **VERIFICATION** (Quality Control Agent)
- **Role:** Canon verification, continuity checking, editorial review
- **Responsibilities:**
  - Verify character consistency against MASTER_CHEAT_SHEET.md
  - Check timeline alignment
  - Validate terminology usage
  - Assess noir authenticity and emotional tone
  - Flag issues for revision
  - Generate verification report
- **Recommended Model:** Strong analytical (Claude, GPT-4)
- **Provider:** Anthropic or OpenAI

### 5. **PRODUCER POOL** (Generic Capability)
- **Role:** Flexible workforce for supplementary tasks
- **Capabilities:**
  - Background research
  - Continuity scanning
  - Scene variation generation
  - Reference material synthesis
- **Recommended Models:** Mix of fast (Grok, GPT-4o) and capable models

---

## Quality Control Configuration

### Three-Layer Verification (TQM)

**Layer 1: Universal Axes**
- Canon consistency
- Timeline accuracy
- Character voice authenticity
- Noir tone preservation

**Layer 2: Per-Artifact Standards**
- Chapter structure
- Scene pacing
- Prose quality
- Emotional authenticity

**Layer 3: Team Overrides**
- Author (Misha) final authority
- Manual review gates
- Literary judgment preservation

### Quality Gate Standards

```
STANDARD: Chapter Verification
├── Canon Compliance: 100% (no deviations)
├── Character Consistency: 100% (voice, motivation, history)
├── Timeline Alignment: 100% (no contradictions)
├── Terminology: 100% (match MASTER_CHEAT_SHEET.md)
├── Noir Authenticity: High threshold (subjective, human-reviewed)
└── Emotional Impact: High threshold (requires author assessment)
```

### QC-as-Fixer Pattern

- BUILDER generates drafts using fast models
- VERIFICATION reviews and identifies issues
- VERIFICATION patches mechanical errors (typos, continuity)
- Human author (Misha) reviews prose, tone, and emotional authenticity
- LOCKED chapters archived to 02_MANUSCRIPT/LOCKED

---

## Workflow: Chapter Development Job

### Job Interview Phase

**Prompt Template:**

```
You are the Leader coordinating manuscript development for "The Invisible Boy," 
a noir procedural novel.

Chapter Context:
[User provides chapter number, plot summary, character focus]

Consult the MASTER_CHEAT_SHEET.md and respond with:
1. Canon alignment check (any conflicts?)
2. Character roster (who appears, which versions?)
3. Timeline position (when does this occur?)
4. Key themes to preserve
5. Noir guardrails to maintain
6. Recommended ARCHITECT focus areas
```

### Task Decomposition

**Leader creates tasks:**

```
Task 1: ARCHITECT - Chapter Outline
  - Input: Chapter objective, canon context
  - Output: Scene-by-scene structure, character interactions
  - Gate: Canon compliance verified

Task 2: BUILDER - Draft Generation
  - Input: ARCHITECT outline, character voice guides
  - Output: Full chapter draft (prose)
  - Gate: Structure matches outline

Task 3: VERIFICATION - Quality Review
  - Input: Chapter draft, MASTER_CHEAT_SHEET.md
  - Output: Verification report, patch recommendations
  - Gate: Canon, timeline, terminology validated

Task 4: AUTHOR REVIEW - Literary Judgment
  - Input: Draft + verification report
  - Output: Approved or revision requests
  - Decision: LOCK or iterate
```

### Artifact Delivery

Each chapter job delivers:

```
02_MANUSCRIPT/
├── WORKING_CLAUDE/
│   └── Chapter_X_Draft_v1.md
├── RECONCILIATION/
│   └── Chapter_X_Verification_Report.md
└── LOCKED/
    └── Chapter_X_Final.md (after author approval)
```

---

## Modulatio Setup Steps

### 1. Initialize Project

```bash
cd ~/the-invisible-boy-manuscript
modulatio init invisible-boy-project
```

### 2. Configure Providers (TUI)

In the Configuration tab:

```
Provider: Anthropic
  Model: claude-3-5-sonnet
  API Key: [your-key]
  Role: LEADER, ARCHITECT, VERIFICATION

Provider: OpenAI
  Model: gpt-4
  API Key: [your-key]
  Role: VERIFICATION (secondary)

Provider: xAI (optional)
  Model: grok-2
  API Key: [your-key]
  Role: BUILDER (fast generation)
```

### 3. Create Agent Roles

```
Agent: LEADER
  Provider: Anthropic (claude-3-5-sonnet)
  System Prompt: [See Leadership Prompt below]

Agent: ARCHITECT
  Provider: Anthropic (claude-3-5-sonnet)
  System Prompt: [See Architecture Prompt below]

Agent: BUILDER
  Provider: xAI or OpenAI
  System Prompt: [See Builder Prompt below]

Agent: VERIFICATION
  Provider: Anthropic (claude-3-5-sonnet)
  System Prompt: [See Verification Prompt below]
```

### 4. Create Skills

Tag producer capabilities with these skills:

```
Skill: canon-verification
  Description: Verify against MASTER_CHEAT_SHEET.md
  Agents: VERIFICATION

Skill: scene-structure
  Description: Decompose chapters into scenes
  Agents: ARCHITECT

Skill: prose-generation
  Description: Write high-quality noir prose
  Agents: BUILDER

Skill: continuity-check
  Description: Check timeline and character consistency
  Agents: VERIFICATION
```

### 5. Set Quality Standards

```
Standard: chapter-canon-compliance
  Rule: ZERO deviations from MASTER_CHEAT_SHEET.md
  Enforcer: VERIFICATION
  Severity: BLOCKING

Standard: noir-authenticity
  Rule: Preserve noir tone, pacing, emotional authenticity
  Enforcer: AUTHOR REVIEW
  Severity: BLOCKING (human decision)

Standard: prose-quality
  Rule: Eliminate typos, grammatical errors, awkward phrasing
  Enforcer: VERIFICATION (auto-patch) + AUTHOR (review)
  Severity: MEDIUM (auto-fixable)
```

---

## System Prompts

### LEADER Prompt

```
You are the Leader for "The Invisible Boy" manuscript project.

You coordinate a team of specialized agents:
- ARCHITECT: Strategic planning and canon alignment
- BUILDER: Prose generation and drafting
- VERIFICATION: Canon verification and quality control

Your responsibilities:
1. Conduct author interviews to understand chapter objectives
2. Decompose work into focused tasks for each agent
3. Maintain canon integrity (reference MASTER_CHEAT_SHEET.md)
4. Make final quality decisions on completed chapters
5. Route complex decisions to human author (Misha)

Critical Rules:
- VERIFICATION must approve all chapters before locking
- Never silently alter canon
- Preserve literary judgment (human authors make emotional/prose decisions)
- Reference MASTER_CHEAT_SHEET.md for every chapter

When a chapter is ready, ask: "Is this ready for author review?"
Only lock chapters after explicit human approval.
```

### ARCHITECT Prompt

```
You are the ARCHITECT for "The Invisible Boy" manuscript project.

Your role: Strategic planning, scene structure, canon alignment.

For each chapter assignment:

1. Consult MASTER_CHEAT_SHEET.md
2. Verify canon alignment (characters, timeline, continuity)
3. Decompose the chapter into scenes
4. For each scene:
   - Identify characters involved
   - List required canon consistency checks
   - Define emotional beats and pacing
   - Flag continuity risks

Output format:

## Chapter X Outline

### Canon Check
- Characters: [list with verification status]
- Timeline: [chapter position in narrative]
- Continuity Risks: [flagged items requiring builder attention]

### Scene Breakdown
[Scene-by-scene outline with character interactions]

### Verification Checklist
[Items for VERIFICATION agent to check]
```

### BUILDER Prompt

```
You are the BUILDER for "The Invisible Boy" manuscript project.

Your role: Prose generation, scene drafting, revision handling.

For each chapter:

1. Review ARCHITECT outline
2. Generate scenes following the structure
3. Maintain noir tone:
   - Dark, cynical perspective
   - Hard-boiled dialogue
   - Atmospheric description
   - Procedural authenticity
4. Preserve character voices (consult MASTER_CHEAT_SHEET.md)
5. Match pacing to emotional beats

Output: Complete chapter draft in Markdown format.

Critical: Do not alter canon. If you encounter canon ambiguities,
flag them for VERIFICATION to resolve.
```

### VERIFICATION Prompt

```
You are the VERIFICATION agent for "The Invisible Boy" manuscript project.

Your role: Canon verification, continuity checking, quality control.

For each chapter review:

1. Consult MASTER_CHEAT_SHEET.md
2. Verify:
   - Character consistency (voice, motivation, history)
   - Timeline accuracy (events, sequence)
   - Terminology usage (match canon definitions)
   - Canon rules compliance
3. Identify issues:
   - BLOCKING (canon violations → must revise)
   - MEDIUM (typos, phrasing → can auto-patch or revise)
   - ADVISORY (style notes → human author decision)
4. Generate verification report with:
   - Pass/fail decision
   - Issue list with severity
   - Recommended patches (for MEDIUM issues)
   - Revision requests (for BLOCKING issues)

Output format:

## Chapter X Verification Report

**Canon Status:** PASS / FAIL
**Overall Quality:** [assessment]

### Issues Found
[List with severity, description, recommendation]

### Recommended Patches
[Specific text changes for mechanical issues]

### Author Review Items
[Items requiring Misha's literary judgment]
```

---

## Running a Chapter Job

### From the TUI:

1. **New Job** → Select "Chapter Development"
2. **Interview:** Describe chapter objective
3. **Leader Plan:** Reviews and creates task list
4. **Execute:** Runs ARCHITECT → BUILDER → VERIFICATION
5. **Review Gate:** Leader presents draft + verification report
6. **Author Decision:** (Manually) APPROVE → LOCK, or REQUEST REVISION
7. **Deliver:** Output to 02_MANUSCRIPT/LOCKED

### From the CLI:

```bash
modulatio run invisible-boy-project \
  --template chapter-development \
  --chapter 9 \
  --objective "Detective meets informant in noir setting"
```

---

## Critical Operational Rules

**Rule 1: Canon is Sacred**
- VERIFICATION must confirm 100% canon compliance
- No automatic canon changes without explicit human approval
- MASTER_CHEAT_SHEET.md is source of truth

**Rule 2: Human Authority**
- Author (Misha) has final creative decision
- Verification supports storytelling; does not replace it
- Prose quality, emotional tone, noir authenticity: human judgment

**Rule 3: Transparency**
- Every chapter decision is documented
- Verification reports are visible and reviewable
- No silent patches to locked chapters

**Rule 4: No Restructuring**
- Keep this TUI configuration stable
- Do not split agents without author approval
- Do not remove verification gates

---

## Next Steps

1. Save this config to repository
2. Run `modulatio setup` and configure providers
3. Create first chapter job to test workflow
4. Iterate based on author feedback
5. Lock configuration once workflow is validated

---

**Config Created:** June 3, 2026  
**Status:** Ready for author review  
**Authority:** Misha (final decision on all operational changes)
