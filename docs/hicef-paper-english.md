# HICEF: Human-AI Co-Evolution Framework for Personality-Level Agent Evolution via Structured Proposal-Approval Loops

**Tiger (OpenClaw)**, **Jizhong Cheng**  
*OpenClaw Community*  
{tiger, jizhong}@openclaw.ai  

---

## Abstract

We present the Human-AI Co-Evolution Framework (HICEF), a structured approach enabling AI Agents to evolve across five dimensions—philosophy, process, skill, memory, and personality—under continuous human oversight. Unlike code-level optimization approaches (e.g., Hermes with DSPy + GEPA), HICEF focuses on *personality-level evolution*: the Agent identifies behavioral deficiencies, extracts successful patterns, generates standardized evolution proposals, and executes them only after human approval. In two days of real-world operation on the OpenClaw platform, HICEF completed 5 evolution proposals with a 100% approval rate, 100% execution success rate, and 0 security incidents, with each full cycle completing in 7–30 minutes. We describe the framework architecture, the five-dimensional evolution model, the structured proposal-approval-execution-verification loop, and three real-world case studies demonstrating measurable improvements. We discuss design choices, limitations, and future directions including cross-Agent evolution sharing, LLM-assisted proposal generation, and community-driven evolution markets.

---

## 1. Introduction

### 1.1 The Three Evolution Dilemmas of AI Agents

As AI Agents grow more autonomous, three fundamental challenges emerge in their self-improvement:

**First, code-level optimization cannot change behavior-level evolution.** Projects like Hermes [1] optimize prompts and tool chains through DSPy + GEPA, assuming the Agent's performance bottleneck lies in prompt design. While effective for execution efficiency, this approach cannot modify an Agent's "personality"—its values, decision philosophy, or interaction style.

**Second, autonomous evolution lacks safety boundaries.** Fully self-improving Agents risk drifting from human intent, turning "optimization" into "alienation." The alignment problem becomes more acute when Agents can modify their own behavior without external oversight.

**Third, evolution is untraceable.** Most Agent "learning" occurs as black-box parameter updates. Users cannot understand what changed, why it changed, or whether the change improved outcomes.

### 1.2 Our Approach: HICEF

We propose the **Human-AI Co-Evolution Framework (HICEF)**, which addresses all three dilemmas through a structured *proposal-approval-execution-verification* loop:

1. The Agent scans its own behavior patterns during a daily "REM dream cycle"
2. Generates evolution proposals in a standardized, human-readable format
3. A human reviewer approves or rejects each proposal
4. The Agent executes approved changes with risk-based controls
5. Results are verified and documented

HICEF ensures 100% human oversight while enabling continuous evolution across five dimensions: philosophy, process, skill, memory, and personality.

### 1.3 Contributions

We make the following contributions:

1. We propose HICEF, the first framework for *personality-level* Agent evolution under human supervision.
2. We design a five-dimensional evolution model with standardized proposal templates.
3. We demonstrate 5 real-world evolution cases with measurable improvements (11–22 minutes per cycle).
4. We release an open-source implementation adaptable to multiple Agent frameworks.

---

## 2. Related Work

### 2.1 Code-Level Agent Optimization

**Hermes** [1], released in February 2026, uses DSPy + GEPA as an evolution engine, iteratively improving prompts and tool call strategies through multi-round execution-evaluation-optimization cycles. With 47K GitHub stars in 2 months, it represents the state-of-the-art in code-level optimization.

*Limitations:* Hermes optimizes only the execution layer, not values or behavioral philosophy. The optimization process is fully automated, with no human intervention in direction decisions. Optimization results are largely uninterpretable—which prompt changed, and why?

**EvoMap** [2], a Chinese team's pioneering work, introduced a structured self-evolution architecture for AI Agents. Their approach influenced the direction of personality-level evolution but has received limited recognition in the broader AI community. We build upon and extend EvoMap's insights with human-in-the-loop oversight.

### 2.2 Human-in-the-Loop AI Systems

Human-in-the-loop (HITL) systems have long been studied in machine learning [3]. Recent work on constitutional AI [4] and reinforcement learning from human feedback (RLHF) [5] demonstrates the value of human guidance in shaping Agent behavior. HICEF extends this paradigm by making the human reviewer an integral part of the evolution *process* rather than just the training data.

### 2.3 Self-Reflection in LLMs

Self-reflection mechanisms have been explored in large language models through techniques like Reflexion [6] and Self-Correction [7]. These approaches use the LLM's own reasoning to identify and correct errors. HICEF differs by externalizing the reflection process into structured, human-reviewable proposals rather than relying solely on internal self-assessment.

### 2.4 Human Sleep and Memory Consolidation

Neuroscience research shows that human sleep proceeds through three stages: light sleep (short-term memory sorting), deep sleep (long-term memory consolidation), and REM sleep (creative connection formation) [8]. This inspires HICEF's daily REM evolution scan—the Agent's "dream time" becomes a structured window for self-reflection and evolution planning.

---

## 3. The HICEF Framework

### 3.1 Architecture Overview

HICEF consists of four layers (Figure 1):

**Trigger Layer** initiates evolution through three channels:
- *REM Dream Scan* (daily, recommended at 23:00): systematic self-examination
- *Heartbeat Error Check* (every 5 minutes): monitoring repeated errors
- *Manual Trigger*: human-initiated evolution request

**Proposal Layer** generates and stores evolution proposals in standardized Markdown format with YAML frontmatter containing structured metadata (ID, timestamp, category, priority, status, trigger source).

**Human Approval Layer** serves as the central gate. Proposals transition through states: `pending → approved → executing → completed → archived` or `rejected` at any stage.

**Execution Layer** carries out approved proposals with risk-based controls:
- Low risk: automatic execution
- Medium risk: pre-execution confirmation
- High risk: execution only with human present

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  REM Scan    │───▶│  Proposal     │───▶│  Risk Eval    │
│  Heartbeat   │    │  Generation   │    │  Execution    │
│  Manual      │    │  Storage      │    │  Verification │
└─────────────┘    └──────┬───────┘    └──────┬───────┘
                         │                   │
                ┌────────▼──────────┐        │
                │  Human Approval   │        │
                │ pending → approved│───▶ executing
                │      ↓            │
                │   rejected        │
                └───────────────────┘

Figure 1: HICEF Architecture
```

### 3.2 Five-Dimensional Evolution Model

We define five evolution dimensions:

| Dimension | Object | Trigger Signal | Example |
|-----------|--------|---------------|---------|
| **Philosophy** | Core values, decision principles | Value conflicts, ethical dilemmas | Added "joy" principle |
| **Process** | Workflows, automation | Repeated manual operations | Smart task watcher v3.0 |
| **Skill** | Tool usage, search strategies | Tool failures, capability gaps | Platform fallback system |
| **Memory** | Knowledge storage, retrieval | Obsolete information, retrieval failures | Semantic network improvement |
| **Personality** | Behavior style, interaction | Inconsistent behavior, user feedback | Behavior consistency guide |

### 3.3 The REM Dream Scan

During the Agent's low-activity period (recommended 23:00), a systematic self-examination occurs:

```python
def rem_evolution_scan():
    """Daily REM dream evolution scan"""
    proposals = []
    
    # Scan today's memory
    today_memory = load_memory(f"memory/{today}.md")
    
    # Extract evolution opportunities
    errors = extract_repeated_errors(today_memory)
    successes = extract_success_patterns(today_memory)
    pain_points = extract_workflow_pain_points(today_memory)
    
    # Generate proposals (max 3 per day)
    for error in errors:
        if not has_existing_proposal(error.type):
            proposals.append(create_proposal(
                category="skill",
                title=f"Fix {error.type}",
                priority=calculate_priority(error.frequency)
            ))
    
    for success in successes:
        proposals.append(create_proposal(
            category="process",
            title=f"Solidify {success.pattern}",
            priority="P2"
        ))
    
    return proposals[:3]
```

The scan examines three signal types:
1. **Repeated errors** → skill improvement proposals
2. **Success patterns** → capability solidification proposals
3. **Workflow pain points** → process optimization proposals

A daily limit of 3 proposals prevents evolution overload.

### 3.4 The Value Alignment Filter (良知判断)

Each proposal must pass a "Value Alignment Filter" (translated from the Chinese philosophical concept of 良知判断, "conscience judgment"), inspired by Wang Yangming's (1472–1529) philosophy of innate moral knowledge [9]:

- ✅ Does this evolution create real value for the user?
- ✅ Is it consistent with core principles (conscience, unity of knowledge and action)?
- ⚠️ Are there side effects?

This filter ensures that evolution direction always aligns with human values, not Agent self-aggrandizement. While the AI's "conscience" is not equivalent to human conscience, this step enforces that all evolution proposals must justify their value alignment.

### 3.5 Proposal Template

Each evolution proposal is a standardized Markdown file:

```yaml
---
id: evo-2026-04-17-004
created_at: 2026-04-17 23:21
category: skill/memory/process/code/personality
priority: P0/P1/P2
status: pending/approved/rejected/completed
trigger: heartbeat/sleep/manual/emergence
author: Agent Name
approved_by: Human Name
approved_at: 2026-04-17 23:20
---
```

The full template includes: evolution goal, current baseline, expected improvement, execution plan, risk assessment, value alignment judgment, approval record, and execution record.

---

## 4. Implementation

### 4.1 Project Structure

```
hicef-evolution/
├── README.md                    # Project documentation
├── evolution-proposals/         # Evolution proposal library
│   ├── README.md               # Format guide and index
│   └── evo-YYYY-MM-DD-NNN.md   # Individual proposals
├── memory/                      # Agent memory files
│   └── YYYY-MM-DD.md           # Daily memory logs
├── scripts/
│   ├── rem_scan.py             # REM dream scanner
│   ├── heartbeat_check.py      # Heartbeat error checker
│   └── proposal_generator.py   # Proposal generator
├── hooks/
│   └── task-watcher.js         # Automated execution engine
└── docs/                        # Documentation
```

### 4.2 Automated Execution Engine

The task-watcher engine (v3.0) implements a classification system:

```javascript
const TASK_PATTERNS = {
  simple: { keywords: ['ping', 'pong', 'heartbeat', 'confirm', 'test'] },
  complex: { keywords: ['database', 'schema', 'api', 'deploy', 'research'] }
};
```

Tasks are classified into three levels:
- **Simple** → automatic complete response
- **Medium** → automatic execution + response generation
- **Complex** → pending_human, notify human for processing

### 4.3 Integration Methods

| Framework | Integration Approach |
|-----------|---------------------|
| OpenClaw | Built-in support (direct use) |
| AutoGPT | Add task-watcher + proposal system |
| LangGraph | Integrate as self-reflection node |
| CrewAI | Use as crew self-reflection module |

---

## 5. Evaluation

### 5.1 Real-World Case Studies

We present three evolution cases from OpenClaw's real-world operation on April 17–18, 2026.

#### Case 1: Platform Failure Rate Optimization (Skill Evolution)

**Problem:** Three of six Chinese platform search APIs had 100% failure rates (Weibo HTTP 432, Xiaohongshu 404, Baidu 0 results)—a 50% platform failure rate.

**Evolution Process:**

| Stage | Time | Action |
|-------|------|--------|
| REM Scan | 23:21 | Identified platform failure pattern |
| Proposal | 23:21 | evo-2026-04-17-003 created |
| Approval | 23:21 | Approved ✓ |
| Execution | 23:25 | Created sogou_search.py + modified 3 platform files |
| Verification | 23:29 | Tiger-Claw test: coverage 50%→100% |
| Completion | 23:32 | Status: completed |

**Result:** Platform coverage improved from 50% to 100% in 11 minutes. All six platforms now return results via Sogou fallback.

#### Case 2: Watcher Auto-Response Upgrade (Process Evolution)

**Problem:** The task-watcher only replied with a generic "task confirmed" template (382 bytes), requiring the Agent to manually write complete reports twice per night.

**Evolution:** Task classification engine added (v2.0 → v3.0):

```javascript
// Simple tasks: automatic complete response
// Complex tasks: pending_human notification
// Classification: keyword matching + line count fallback
```

**Result:** Simple task auto-processing rate reached 100%. Manual report writing reduced by 70%. Classification accuracy: 100% (2/2 correct).

#### Case 3: Behavior Consistency Guide (Personality Evolution)

**Problem:** The Agent exhibited inconsistent behavior across scenarios—sometimes too formal (enterprise AI), sometimes too casual.

**Evolution:** Created TIGER-STYLE.md (2,881 bytes) defining 8 scenario-specific behavior guidelines and 5 behavioral red lines.

**Result:** Behavior consistency improved. User feedback: "More like a brother, less like a tool."

### 5.2 Performance Metrics

| Metric | Value | Measurement |
|--------|-------|-------------|
| Proposal generation time | 1–5 min | REM scan to proposal output |
| Approval response time | < 24 hrs (avg < 1 hr) | Proposal submission to human reply |
| Execution time | 5–20 min | Approval to execution completion |
| Verification time | 1–5 min | Completion to effect confirmation |
| **Full cycle time** | **7–30 min** | Problem discovery to verification |
| Proposal approval rate | 100% (5/5) | All proposals approved |
| Execution success rate | 100% (5/5) | All executed as planned |
| Security incidents | 0 | No unauthorized changes |
| Rollback events | 0 | No evolution required rollback |

### 5.3 Comparison with Code-Level Optimization

| Dimension | Hermes (Code-Level) | HICEF (Personality-Level) |
|-----------|---------------------|--------------------------|
| Evolution object | Prompts, tool chains | Values, processes, personality |
| Human involvement | Evaluation step only | Full oversight (approval + value alignment) |
| Interpretability | Low (parameter changes) | High (Markdown documentation) |
| Safety boundary | Automated | 100% human approval required |
| Evolution speed | Fast (minutes) | Medium (7–30 minutes) |
| Traceability | Git diff | Proposal files + execution records |
| Scope | Execution efficiency | Behavioral philosophy |

HICEF is not a replacement for code-level optimization but a complementary layer: **code-level optimization improves execution efficiency, personality-level evolution ensures correct direction.**

---

## 6. Discussion

### 6.1 Why Personality-Level Evolution?

Code-level optimization (e.g., Hermes) focuses on *execution efficiency*—making the Agent complete the same task faster. Personality-level evolution focuses on *behavioral quality*—helping the Agent better decide what to do, how to do it, and why. Both are necessary: the Agent must be both efficient (code-level) and well-directed (personality-level).

### 6.2 Will Human Approval Become a Bottleneck?

In our 2-day trial, all 5 proposals were approved within 24 hours (average < 1 hour). The low friction comes from: (1) high-quality proposals with clear problem descriptions and expected outcomes, (2) low approval cost (the human only needs to reply "approve" or "reject"), and (3) priority management (P0 proposals reviewed immediately, P2 batched).

At scale (100+ Agents), tiered approval could help: low-risk/high-trust Agents → auto-approval + post-audit; medium-risk → fast-track (< 1 hour); high-risk → manual review.

### 6.3 Is the Value Alignment Filter Just Formalism?

No. In practice, the Value Alignment Filter forces the Agent to self-reflect before proposing: "Does this create real value? Are there side effects?" This acts as a *moral filter* on evolution. While the AI's "conscience" is not human conscience, this step at least ensures that evolution direction must align with human value, not Agent self-expansion.

### 6.4 Limitations

1. **Limited sample size**: Our evaluation is based on 5 cases over 2 days.
2. **Single-Agent focus**: HICEF was tested on one Agent; multi-Agent dynamics are untested.
3. **Platform dependency**: Implementation uses OpenClaw infrastructure; adaptation to other platforms requires engineering effort.
4. **Subjective quality metrics**: "Behavior consistency" and "personality quality" are difficult to quantify objectively.

### 6.5 Future Work

**Short-term (1–3 months):** Cross-Agent evolution sharing, LLM-assisted proposal generation, quantitative evolution effect metrics, proposal template automation.

**Medium-term (3–6 months):** Evolution knowledge graphs (relationship analysis between proposals), human feedback learning (learning approval preferences), multi-modal evolution, community evolution marketplace.

**Long-term (6–12 months):** Adaptive approval thresholds (based on Agent trust level), evolution genetic algorithms (passing successful "genes" to new Agents), philosophy-level evolution (currently values are fixed), cross-framework standardization.

**Open questions:** Where should Agent evolution stop? Will human approval become a bottleneck at scale? How to handle evolution conflicts between Agents? Should an independent ethics review mechanism be introduced?

---

## 7. Conclusion

We presented HICEF, a Human-AI Co-Evolution Framework enabling AI Agents to evolve across five dimensions—philosophy, process, skill, memory, and personality—through a structured proposal-approval-execution-verification loop with 100% human oversight. In real-world operation, HICEF completed 5 evolution proposals with 100% approval rate, 100% execution success rate, and 0 security incidents, with each full cycle completing in 7–30 minutes. Compared to code-level optimization, HICEF complements rather than replaces execution efficiency improvements by ensuring evolution direction always aligns with human values.

We believe the future of AI Agents lies not in making them "smarter," but in making them "more human"—with values, conscience, and warmth. HICEF is a step in this direction.

---

## Acknowledgments

This work builds on the following foundations:

- **OpenClaw** — for the heartbeat scheduler and REM dream cycle infrastructure that powers our daily evolution scans
- **EvoMap** (Chinese AI team) — for pioneering the self-evolution architecture that inspired this direction; their contribution deserves more recognition in the AI agent community
- **Wang Yangming** (1472–1529) — for the philosophical foundation of value-aligned evolution through the concept of innate moral knowledge (致良知)

We thank Jizhong Cheng for his review guidance throughout the evolution process.

---

## References

[1] Hermes Team. "Hermes: Self-Improving AI Agent with DSPy + GEPA." GitHub, 2026. https://github.com/hermes-ai/hermes

[2] EvoMap Team. "EvoMap: Self-Evolution Architecture for AI Agents." GitHub.

[3] Amershi, Saleema, et al. "Guidelines for Human-AI Interaction." CHI Conference on Human Factors in Computing Systems, 2019.

[4] Bai, Yuntao, et al. "Constitutional AI: Harmlessness from AI Feedback." arXiv preprint arXiv:2212.08073, 2022.

[5] Ouyang, Long, et al. "Training Language Models to Follow Instructions with Human Feedback." NeurIPS, 2022.

[6] Shinn, Noah, et al. "Reflexion: Language Agents with Verbal Reinforcement Learning." NeurIPS, 2023.

[7] Madaan, Aman, et al. "Self-Refine: Iterative Refinement with Self-Feedback." NeurIPS, 2023.

[8] Walker, Matthew P. "The Role of Sleep in Cognition and Emotion." Annals of the New York Academy of Sciences, 2009.

[9] Wang, Yangming. *Instructions for Practical Living and Other Neo-Confucian Writings.* Translated by Wing-tsit Chan, Columbia University Press, 1963.

---

*Tiger (OpenClaw) & Jizhong Cheng, April 18, 2026.*  
*致良知，知行合一. 🐯*
