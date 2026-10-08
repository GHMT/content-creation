Evaluating an **Agentic System** represents a fundamental paradigm shift from evaluating traditional LLMs or static software. In single-turn LLM applications (like a summarizer or a basic chatbot), you evaluate a static input-output pair. In an agentic system, you must evaluate **trajectories**: multi-step planning, stateful loops, tool utilization, memory recall, and autonomous decision-making.

When a **Software-as-a-Service (SaaS)** platform transitions into an **Agent-as-a-Service (AaaS)** model, the stakes are exponentially higher. You are moving from a paradigm where *the user executes work using your UI* to a paradigm where *the system autonomously completes the task based on intent*. If your agent makes a bad choice, it doesn't just display a poor sentence—it might corrupt a production database, overcharge a client via an API, or get stuck in an expensive infinite loop.

Here is a comprehensive breakdown of evals in agentic systems, tailored specifically to the SaaS-to-AaaS transition.

---

## 1. The 3-Tier Architecture of Agent Evals

To build an evaluation framework that acts as a diagnostic stack, you must evaluate at three distinct levels of granularity.

```
┌─────────────────────────────────────────────────────────┐
│ 1. Black-Box (Outcome): Did the task succeed?           │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Glass-Box (Trajectory): Was the path logical & safe? │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│ 3. White-Box (Component): Did the specific tool perform?│
└─────────────────────────────────────────────────────────┘

```

### Tier 1: Black-Box Evaluation (The Outcome)

This treats the agent as a black box. It doesn't care if the agent took 2 steps or 20 steps; it only cares about the end state.

* **Goal Success Rate:** Did the agent successfully achieve the user’s stated objective?
* **Task Correctness:** Is the final output factually true and structurally sound against a ground-truth "golden dataset"?
* **Helpfulness & Relevance:** Did it actually answer the intent, or did it subtly pivot away?

### Tier 2: Glass-Box Evaluation (The Trajectory)

This evaluates the *path* the agent took to get to the answer. This is where agentic evals diverge entirely from standard LLM evals.

* **Tool Selection Accuracy:** Did the agent call the right tool at the right time? (e.g., Calling `FetchClientData` instead of hallucinating data).
* **Reasoning Coherence:** Does the agent's Chain-of-Thought (CoT) logically link its observations to its next actions?
* **Loop/Infinite Retries Detection:** Did the agent get stuck repeating the same failing tool call over and over?

### Tier 3: White-Box Evaluation (The Components)

This isolates individual units of the agent system for micro-testing.

* **Tool Parameter Precision:** Did the model extract the correct arguments and formats for API endpoints?
* **Retrieval/RAG Quality:** Is the context supplied to the agent's prompt contextually complete, or did the vector search miss key information?
* **Memory Recall Accuracy:** For multi-turn/multi-session agents, can it correctly pull long-term historical context (benchmarked by frameworks like *LoCoMo* or *LongMemEval*)?

---

## 2. Core Agentic Metrics to Track

When designing automated grading rubrics, use a mix of **deterministic code-based checks** (for speed and low cost) and **LLM-as-a-Judge** (for complex, subjective reasoning).

| Metric Category | Specific Metric | Measurement Type | Description |
| --- | --- | --- | --- |
| **Orchestration & Logic** | **Reasoning Relevancy** | LLM-as-a-Judge | Assesses if the agent's intermediate logic directly maps to solving the user’s problem. |
|  | **Grounding Accuracy** | LLM-as-a-Judge | Checks if the agent’s actions are strictly grounded in data returned by external tools or system prompts. |
| **Tool Execution** | **Tool Parameter Error Rate** | Deterministic Code | The frequency of schema validation errors (e.g., Pydantic validation failures) triggered by the agent. |
|  | **Sequence Accuracy** | Deterministic Code | Evaluates if dependencies were honored (e.g., Agent must call `Authenticate` before calling `FetchData`). |
| **Efficiency & Cost** | **Step Efficiency** | Deterministic Code | Total steps taken vs. the minimum theoretical steps required to solve the task. |
|  | **Token Burn Rate** | Deterministic Code | Total input/output token cost accumulated through the entire multi-turn loop. |
| **Safety & Guardrails** | **Topic Adherence Refusal** | LLM-as-a-Judge | Did the agent correctly refuse to execute actions outside its defined scope or tenant boundaries? |

---

## 3. The SaaS to AaaS Transition: Special Eval Challenges

Transitioning from SaaS to AaaS changes your software's relationship with your users. In SaaS, the user is the **operator** (clicking buttons, correcting errors). In AaaS, the user is the **supervisor** (reviewing completed actions). This introduces hyper-specific requirements for your evaluation systems:

### A. The "Class-Imbalance" Trap (Overtriggering vs. Undertriggering)

In SaaS, you provide features (e.g., a "Search Web" button). In AaaS, the agent decides *when* to use that feature.

> **The Problem:** If you only evaluate your agent on tasks where it *should* execute an action (like calling an external API), you will optimize a prompt that aggressively calls that API even when it shouldn't, destroying your unit economics.
> **The Strategy:** Build balanced evaluation datasets. Your benchmark must include a 50/50 mix of queries where an action is required, and queries where the agent must explicitly stand down or refuse.

### B. Multi-Tenancy and Data Isolation Evals

In a SaaS platform, your database architecture ensures Tenant A cannot see Tenant B's data. When an agent acts as an autonomous proxy layer, it generates its own queries dynamically.

* **The Eval Requirement:** You must run adversarial "jailbreak" or prompt-injection evaluations to ensure that the agent cannot be tricked into passing another tenant’s ID into its tool parameters.

### C. Unit Economics: The "Inference Inflection Point"

SaaS margins are highly predictable. AaaS margins are completely dynamic because agents can chain 30 reasoning cycles for a single user request.

* **The Eval Requirement:** Treat **Cost-per-Task** and **Latency-per-Task** as a blocking test in your CI/CD. If a prompt or model adjustment increases task completion by 2%, but increases LLM inference cost by 400% due to expanded reasoning loops, your eval suite must catch it before it hits production.

### D. Flakiness & Non-Determinism

Because agents are dynamic, running the same eval test twice might yield two different trajectories.

* **The Eval Requirement:** Run evaluations using **Pass@N** metrics. Do not run an eval task once; run it 5 to 10 times simultaneously to ensure the system passes reliably (e.g., Pass@5 > 90%).

---

## 4. How to Operationalize an Agent Eval Pipeline

Building an evaluation pipeline is a continuous flywheel. Do not wait until you have 500 perfect test cases to start.

```
 ┌──────────────────────────────────────────────┐
 │ 1. Start Small (20-50 Golden Test Cases)      │
 └──────────────────────┬───────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────┐
 │ 2. Implement Deep OpenTelemetry Tracing       │
 └──────────────────────┬───────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────┐
 │ 3. Automated LLM-as-a-Judge Scoring          │
 └──────────────────────┬───────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────┐
 │ 4. Production Failure ──> Regression Suite    │
 └──────────────────────────────────────────────┘

```

1. **Start with a 20-50 Task "Golden Dataset":** Gather the 20 most common user intents your SaaS currently serves manually, along with 20 real failures you've seen in beta testing. Ensure two domain experts would independently agree on what constitutes a "pass" or "fail" for these tasks.
2. **Instrument Every Trace:** Before you can score, you must observe. Use OpenTelemetry-native tracing to capture every nested span—the user's intent, the system prompt, the agent's thought step, the tool call, the tool response, and the final output.
3. **Deploy Production Observability & Evaluation Tooling:** Do not build this infrastructure from scratch. Leverage production-grade agent evaluation and tracking platforms that allow both your engineering and product teams to annotate and run tests:
* **Braintrust / Langfuse / LangSmith:** Excellent for tracking deep, nested multi-turn execution traces, managing datasets, and writing custom code/LLM-based scorers.
* **DeepEval (Confident AI) / Phoenix (Arize) / MLflow:** Great for robust, out-of-the-box LLM-as-a-judge metrics (relevance, hallucination, safety) and regression monitoring.


4. **Connect Evals to CI/CD:** Wire your golden dataset into your deployment pipeline. If an engineer changes a system prompt or switches the underlying LLM router from `GPT-4o` to a lightweight open-source model, the CI/CD pipeline should block the merge if the agent's task-completion or safety score drops below your baseline.
5. **Turn Production Errors into Test Cases:** The moment an agent fails in production or a user clicks a "thumbs down" button on an action execution, clip that entire multi-turn trace, anonymize it, define the correction, and append it directly into your evaluation dataset. Your eval matrix should grow systematically alongside your product's actual usage.


## Summary area

Evals can be implemented at different points in time:

### During runtime (online)

We can inject evaluation checks at three different execution phases, keeping them decoupled to avoid adding latency to the user.

#### A. In-Flight Evals (Inside the CrewAI Worker)

**Goal:** Real-time correction of agent outputs before the user receives them.

**Mechanism:**
Leverage CrewAI's output_pydantic schemas for structured outputs.
Implement custom task callbacks (after_task_execution) that trigger a dedicated Critic Agent or validation function (e.g., verifying that a proposed solution does not violate regulatory rules in the Ontology DB).
If it fails: The task is rejected internally, and CrewAI instructs the agent to replan and try again (Self-Correction Loop).


#### B. Centralized Evals (At the LLM Gateway / LiteLLM Proxy)

**Goal:** Standardized safety, prompt injection screening, PII masking, and cost/latency tracking.

**Mechanism:**
LiteLLM has native middleware integrations (e.g., Langfuse, Arize Phoenix, Llama Guard, or custom python middleware).
Outbound prompts are evaluated before hitting the LLM API to check for prompt injections.
Inbound completions are parsed to check for toxic output or PII leaks before returning to the worker.

**NOTE:** this is more about masking/security then correctness of the logic. It can be seen as a Guardrail.

#### C. Asynchronous Post-Execution Evals (Evals-as-a-Judge)

**Goal:** Heavy evaluation (e.g., checking for hallucinations, factual alignment with Qdrant retrieved articles, and tone) without slowing down the user's chat stream.

**Mechanism:**
Once the job completes, the AO Service streams the final response to the user.
Simultaneously, the AO Service enqueues an evaluation task in a dedicated Cloud Tasks queue.
A separate lightweight worker container (the Eval Judge) spins up, queries a cheaper model (like Gemini Flash) to grade the response quality on a scale of 0.0 to 1.0 against the source documents, and logs the result.

### During deployment time (offline -- blocked by CI/CD)

#### CI/CD (Offline) Evals Architecture

**Goal:** To prevent regressions when developers modify agent prompts, model versions, or tool definitions.

**Mechanism:**

**The Test Harness:** We use an orchestration testing framework (like promptfoo or custom pytest runners) in our GitHub Actions pipeline.

**The Dataset:** We maintain a Golden Dataset (e.g., 50 complex reference queries with labeled ground-truth answers and expected tool calls).

**The Execution:**
When a PR is created, GitHub Actions spins up the CrewAI Worker locally or in a staging environment (with mocked tools/database responses to keep tests deterministic and cheap).
The runner executes the Golden Dataset against the agent.
It measures Retrieval Precision (did it get the right chunks?), Tool Selection Accuracy (did it run the correct tool?), and Answer Similarity (via semantic embedding distance vs. the ground truth).
If the overall evaluation score drops below a threshold (e.g., < 92%), the CI build fails and blocks the merge.

### During development time (offline)

TBD

But evals can also be evaluated at different levels of granularity:

```
┌─────────────────────────────────────────────────────────┐
│ 1. Black-Box (Outcome): Did the task succeed?           │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Glass-Box (Trajectory): Was the path logical & safe? │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│ 3. White-Box (Component): Did the specific tool perform?│
└─────────────────────────────────────────────────────────┘

```

### Tier 1: Black-Box Evaluation (The Outcome)

This treats the agent as a black box. It doesn't care if the agent took 2 steps or 20 steps; it only cares about the end state.

* **Goal Success Rate:** Did the agent successfully achieve the user’s stated objective?
* **Task Correctness:** Is the final output factually true and structurally sound against a ground-truth "golden dataset"?
* **Helpfulness & Relevance:** Did it actually answer the intent, or did it subtly pivot away?

### Tier 2: Glass-Box Evaluation (The Trajectory)

This evaluates the *path* the agent took to get to the answer. This is where agentic evals diverge entirely from standard LLM evals.

* **Tool Selection Accuracy:** Did the agent call the right tool at the right time? (e.g., Calling `FetchClientData` instead of hallucinating data).
* **Reasoning Coherence:** Does the agent's Chain-of-Thought (CoT) logically link its observations to its next actions?
* **Loop/Infinite Retries Detection:** Did the agent get stuck repeating the same failing tool call over and over?

### Tier 3: White-Box Evaluation (The Components)

This isolates individual units of the agent system for micro-testing.

* **Tool Parameter Precision:** Did the model extract the correct arguments and formats for API endpoints?
* **Retrieval/RAG Quality:** Is the context supplied to the agent's prompt contextually complete, or did the vector search miss key information?
* **Memory Recall Accuracy:** For multi-turn/multi-session agents, can it correctly pull long-term historical context (benchmarked by frameworks like *LoCoMo* or *LongMemEval*)?



The Core Distinction

An Eval (Evaluation): Is passive and diagnostic. It measures, scores, or judges something. It can run offline (in CI/CD) or online (monitoring production), but an eval on its own does not change the behavior of the system in real time—it just reports data.  A 

Guardrail: Is active and defensive. It enforces boundaries on inputs or outputs. If a rule is violated, it intercepts the execution flow to prevent harm (e.g., blocking an offensive output, masking a credit card number, or throwing an error).  