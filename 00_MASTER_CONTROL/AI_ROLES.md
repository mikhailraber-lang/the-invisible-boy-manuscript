# AI Roles and Authority

## Authority Ranking

Misha is the final authority on everything:

- locks
- canon decisions
- merges
- chapter approval
- repository structure decisions

No AI overrides Misha.

Among the AI collaborators:

1. Claude is the number-one lead AI for reconciliation, canon validation, structural review, and editorial assessment.
2. ChatGPT / Codex is the number-two AI for prose drafting, scene integration, and workflow architecture.
3. Other AI tools provide specialized support only.

Governing principle:

> Scripts check mechanics. Humans judge literature.

No AI is the final judge of literary quality. AI tools check mechanics, surface risks, and advise. Misha decides.

## Role Assignments

### Claude / Claude Code

Primary role:

- reconciliation
- canon validation
- structural review
- editorial assessment

Primary output location:

`RECONCILIATION/`

Claude does not unilaterally lock canon or merge final chapters.

### ChatGPT / Codex

Primary role:

- prose drafting
- scene integration
- workflow architecture

Primary output location:

`WORKING_CHATGPT/`

ChatGPT / Codex does not unilaterally restructure the repository, delete project material, or lock chapters.

### Grok

Primary role:

- emotionally raw dialogue
- difficult interpersonal scenes
- psychological discomfort and pressure testing

Primary output location:

`WORKING_GROK/`

Grok does not perform procedure checks, canon validation, or final merges.

### Perplexity

Primary role:

- research validation
- procedural realism checks
- forensic realism checks
- terminology sourcing

Primary output location:

`04_REFERENCE/PERPLEXITY_RESEARCH/`

Perplexity is research-only. It does not write manuscript prose, judge literature, or decide canon.

## Workflow Routing

- Raw emotional scene work goes to Grok, then `WORKING_GROK/`.
- Procedural or forensic accuracy checks go to Perplexity, then `04_REFERENCE/PERPLEXITY_RESEARCH/`.
- New chapter drafting from structure goes to ChatGPT / Codex, then `WORKING_CHATGPT/`.
- Reconciliation, canon checks, and editorial review go to Claude, then `RECONCILIATION/`.
- Misha decides what becomes locked canon.

## Non-Negotiable Control Rule

Each AI stays in its lane. No tool is stretched past its strength. No AI merges itself. Misha merges.
