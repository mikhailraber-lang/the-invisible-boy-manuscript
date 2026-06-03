# Quick Start: Modulatio for The Invisible Boy

This guide walks you through setting up and running your first chapter job with Modulatio.

---

## Prerequisites

✅ Modulatio installed and activated:
```bash
source ~/modulatio/.venv/bin/activate
```

✅ API keys ready for your providers (Anthropic, OpenAI, xAI, etc.)

---

## Step 1: Initialize the Project

```bash
cd ~/the-invisible-boy-manuscript
chmod +x modulatio-init.sh
./modulatio-init.sh
```

This creates:
- `vault/` directory for projects, runs, and templates
- `invisible-boy-project` workspace

---

## Step 2: Configure Providers

```bash
modulatio config
```

In the TUI, add:

**Provider 1: Anthropic**
- Provider: `anthropic`
- Model: `claude-3-5-sonnet-20241022`
- API Key: [your key]

**Provider 2: OpenAI** (optional)
- Provider: `openai`
- Model: `gpt-4`
- API Key: [your key]

**Provider 3: xAI** (optional, for fast BUILDER)
- Provider: `xai`
- Model: `grok-2`
- API Key: [your key]

---

## Step 3: Create Agents

In the TUI Configuration tab, create agents and assign them to providers.

**Agent 1: LEADER**
- Provider: Anthropic (Claude 3.5 Sonnet)
- System Prompt: [Copy from MODULATIO_CONFIG.md, "LEADER Prompt" section]
- Role: Orchestrator

**Agent 2: ARCHITECT**
- Provider: Anthropic (Claude 3.5 Sonnet)
- System Prompt: [Copy from MODULATIO_CONFIG.md, "ARCHITECT Prompt"]
- Role: Planner

**Agent 3: BUILDER**
- Provider: xAI Grok or OpenAI GPT-4o
- System Prompt: [Copy from MODULATIO_CONFIG.md, "BUILDER Prompt"]
- Role: Writer

**Agent 4: VERIFICATION**
- Provider: Anthropic (Claude 3.5 Sonnet)
- System Prompt: [Copy from MODULATIO_CONFIG.md, "VERIFICATION Prompt"]
- Role: Quality Control

---

## Step 4: Create Your First Job

```bash
modulatio new-job
```

**Select:** Chapter Development (or create custom template)

**Provide Context:**
```
Chapter: 9
Plot Summary: Detective meets informant in noir setting
Character Focus: Detective's emotional state, informant's credibility

References:
- Upload: 01_CANON/MASTER_CHEAT_SHEET.md
- Reference: Chapter 8 (continuity context)
```

---

## Step 5: Follow the Workflow

**Stage 1: LEADER Interview**
- Modulatio asks clarifying questions
- Confirms chapter objective
- Reviews canon from MASTER_CHEAT_SHEET.md

**Stage 2: Plan Decomposition**
- ARCHITECT creates scene outline
- Verifies canon alignment
- Flags continuity risks

**Stage 3: Draft Generation**
- BUILDER writes chapter prose
- Follows ARCHITECT structure
- Maintains noir tone

**Stage 4: Verification**
- VERIFICATION reviews draft
- Checks canon, timeline, character consistency
- Identifies issues (BLOCKING vs. MEDIUM vs. ADVISORY)

**Stage 5: Author Review**
- You (Misha) review draft + verification report
- Approve or request revisions
- Lock approved chapters

---

## Step 6: Deliver Output

Completed chapters are saved to:

```
02_MANUSCRIPT/
├── WORKING_CLAUDE/
│   └── Chapter_9_Draft.md
├── RECONCILIATION/
│   └── Chapter_9_Verification_Report.md
└── LOCKED/
    └── Chapter_9_Final.md
```

---

## Running a Job from CLI (Optional)

```bash
modulatio run invisible-boy-project \
  --template chapter-development \
  --chapter 10 \
  --objective "Detective follows lead to warehouse"
```

---

## Key Principles

🎯 **Canon is Sacred**
- VERIFICATION confirms 100% canon compliance before delivery
- MASTER_CHEAT_SHEET.md is source of truth
- No automatic canon changes

🎯 **Human Authority**
- You (Misha) make final creative decisions
- Prose quality, tone, emotional authenticity: your judgment
- Verification supports storytelling; doesn't replace it

🎯 **Transparency**
- Every decision is documented
- Verification reports are visible
- No silent patches to locked chapters

🎯 **Efficiency**
- Fast producers generate drafts
- Smart verifier catches issues
- Cost of cheap model, quality of strong model

---

## Troubleshooting

**"modulatio: command not found"**
```bash
source ~/modulatio/.venv/bin/activate
```

**"API key invalid"**
- Check provider configuration in `modulatio config`
- Verify key is correct and has API access

**"VERIFICATION rejected chapter"**
- Review verification report for BLOCKING issues
- Update chapter prose in response
- Resubmit for verification

**"Canon mismatch"**
- Consult MASTER_CHEAT_SHEET.md
- Check character, timeline, and terminology
- Update MASTER_CHEAT_SHEET.md if canon changes are approved by Misha

---

## Documentation

- **Config Details:** `00_MASTER_CONTROL/MODULATIO_CONFIG.md`
- **Project Setup:** `SETUP.md`
- **Modulatio Docs:** https://modulatio.ai
- **CLI Reference:** https://modulatio.ai/reference/cli/

---

## Next: Your First Chapter

Ready to orchestrate your first chapter? Run:

```bash
modulatio new-job
```

Follow the conversational workflow, and your chapter will be structured, drafted, verified, and delivered—all with human authority preserved at every gate. 🚀

---

**Quick Reference: Chapter Workflow**

```
📝 Describe chapter objective
      ↓
🏗️  ARCHITECT creates outline (canon-checked)
      ↓
✍️  BUILDER generates prose (noir tone)
      ↓
✅ VERIFICATION reviews (canon verified)
      ↓
👁️  You approve or revise
      ↓
🔒 Lock to 02_MANUSCRIPT/LOCKED
```

Enjoy orchestrating *The Invisible Boy*! 📚
