# Naur

### 1. The Core Fundamentals

**Project Title:** Naur (Inspired by **Peter Naur's** *Programming is Theory Building*)  
**Challenge Theme:** Intelligent Systems for the Future of Work

**The Friction: The Alignment Tax.**

When building software in teams, the biggest slowdown isn't writing code. It is mutual misunderstanding. A product manager asks for a "basic login" feature while the designer pictures a quick social-auth flow. Meanwhile, the backend engineer stresses over token expiration and database latency. Because multidisciplinary domains speak entirely different professional dialects, they pay a massive, hidden productivity penalty. Let’s call it the **Alignment Tax.**

To be completely fair, I stole this term from AI safety. In machine learning, it refers to the performance or speed penalty you pay to keep a model aligned with human values. Here, I am repurposing it to describe human-to-human communication friction.

This communication gap creates Comprehension Debt—a playful, slightly dramatic riff on "Technical Debt." It describes the cost of people failing to understand each other. The illusion of agreement masks entirely disjointed mental models. That debt eventually comes due during integration week, resulting in painful late-stage rewrites, broken databases, or abandoned pull requests

**The Gap in Modern Workflows**

Current workflows rely heavily on autonomous coding agents to write boilerplate faster. However, accelerating code generation without addressing human alignment simply helps a team build the wrong software at a higher speed. If you don't write the theory of the software first, the code is just an expensive shadow of a broken model. Naur handles this friction upstream.

**The Solution**

I designed Naur to act as an autonomous organizational linter that enforces Domain-Driven Design (DDD) constraints before a single line of execution code is ever written. Instead of building another disruptive chatbot, .

Naur acts as an automated organizational checker that enforces Domain-Driven Design (DDD) constraints before anyone writes execution code. Let’s be real: calling it an Ontological Linter is peak hackathon showmanship. It isn't a static compiler tool analyzing the nature of existence; it is a specialized LLM prompt strategy that runs quietly in the background as a Model Context Protocol (MCP) server that plugs directly into a team's active communication stream and flags for example, when two people use the same word to mean different things.


It builds cross-disciplinary empathy by executing three continuous architectural checks:

**The Missing Chair:** Inspired by Jeff Bezos’s old trick of leaving an empty chair at the table to represent the customer, this sounds like a complex architectural rule. Under the hood, it is a straightforward IF/THEN statement checking who is active in the chat. If engineering and product make UI choices without a designer present, Naur steps in to advocate for that missing discipline.

**Ubiquitous Language (DDD):** It catches terminology collisions. If an engineer and a product manager use the word "cache" differently, the system flags it and normalizes the definition into a centralized project glossary.

**3-Tiered Translation:** When a risky proposal surfaces, Naur intercepts it to evaluate what might break. I call this "calculating the cross-domain blast radius," but the LLM is simply making an educated guess based on the context. It translates the proposal into three views: precise technical requirements, a deep-dive rationale, and jargon-free business impacts.



The ultimate goal is to force shared understanding across domains, ensuring that whether a human or an AI agent ultimately writes the code, the underlying structural blueprint is "actually correct".

---

### 2. What did IBM Bob do?

I relied heavily on IBM Bob to engineer this prototype. It essentially served a dual purpose: acting as my strict principal architect during the build phase, and operating as the runtime orchestration engine in the live application.

**Phase 1: Architectural Planning & The Build Persona**

During the initial planning phase, I used Plan Mode to define Bob's system persona. I didn't want a yes-man autocomplete tool; I wanted a strict mentor. I configured Bob as a "Principal Systems Architect" operating under Peter Naur's principles. I gave it a few hard constraints:

* **The Mandatory Intervention Trigger:** If I asked Bob to write complex logic without defining architectural boundaries, it was instructed to strictly refuse, halt the conversation, and force me to fill out a 4-point scaffold (Goal, State, Feedback, Blast Radius).
* **The 3 In-Memory Gates:** To make the prompt design sound cooler, I named these "in-memory gates." In reality, they are not low-level hardware or server architecture constraints. They are three literal text questions (Where does state live? Where does feedback live? What breaks if I delete this?) that I forced the LLM to answer before generating code.

**Phase 2: Core Engineering (Agent Mode)**

With the boundaries set, I switched over to Agent Mode for the actual engineering work:

* **State Persistence:** I had Bob build the state manager to handle the SQLite layer. It generated three distinct tables and the core functions required to manage concurrent reads and writes safely.
* **Protocol Wiring:** I utilized Bob's specific `build-mcp-server` skill to architect the stdio transport setup and register my custom tools. I then activated the `configure-mcp` skill to map the custom server into the local project file (`.bob/mcp.json`), making sure the execution command pointed exactly to my local Python binary.
* **Frontend Execution:** Bob wrote the Streamlit presentation layer. It engineered a custom Markdown parser to bypass native rendering limits and implemented a "zero-latency translation toggle." basically a classic frontend trick: using a pure CSS checkbox hack (:checked) to hide and show HTML elements without waiting for server-side JS.

**Phase 3: The Runtime Engine (The Live Persona)**

In the final production prototype, IBM Bob transitions into the core logic engine of the tool itself. I swapped the system instructions to act as the "Ontological Linter," enforcing the "Missing Chair" logic and the three dynamic governance tiers. Because the configuration is tied directly to the local workspace, Bob operates as the autonomous linter. When you hit sync in the UI, Bob reads the ledger and fires parallel database mutations to rewrite project constraints directly from the IDE.

**Summary of Bob's Technical Contributions**

| Component | Engineering Task | Mode / Skill Used |
| --- | --- | --- |
| **Build Architecture** | Enforced the 3 In-Memory Gates and the Mandatory Intervention Trigger to prevent bad code. | `Plan` / System Authoring |
| **Persistence Ledger** | Built `state_manager.py` with idempotent table creation and locking buffers. | `Agent` |
| **MCP Server** | Built `mcp_server.py` and enforced strict JSON array schema typing to prevent hallucinations. | `Agent` / `build-mcp-server` |
| **MCP Registration** | Wired the `.bob/mcp.json` file to the local Python subprocess environment. | `Agent` / `configure-mcp` |
| **Presentation UI** | Wrote `app.py`, custom CSS layout engine, Markdown parser, and state sync. | `Agent` |

---

### 3. Architecture & AI Approach

I engineered Naur with a clear separation of concerns. The frontend presentation layer is entirely decoupled from the persistent relational ledger and the background AI orchestration loop.

**The Tech Stack**

| Component | Technology | Architectural Responsibility |
| :--- | :--- | :--- |
| **Presentation Layer** | `Streamlit` (1.59.1), `HTML5`, `CSS3` | Renders the corporate UI. Bypasses native rendering with a custom parser (`parse_markdown()`) and executes zero-latency technical/layman layout shifts using pure CSS pseudo-classes (`:checked`), completely avoiding slow server-side JavaScript execution. |
| **Persistence Ledger** | `SQLite3` (Native Python) | Concurrency-safe transactional database (`naur_state.db`) holding chat logs, domain constraints, and the project glossary. Hardcoded with a 15-second write-lock timeout buffer to absorb background multi-agent collisions. |
| **Protocol Engine** | `mcp` (1.28.1), `uvicorn`, `pydantic` | Exposes the SQLite ledger to external agent environments over standard input/output (stdio) channels. Strictly types all AI inputs as JSON arrays to validate payloads before database injection. |
| **Logic Engine** | IBM Bob (Claude) | Acts as the autonomous linter. Reads ledger states, calculates structural blast radii, and executes parallel database mutations directly from the user's local IDE workspace. |

**AI Integration: The Agentic Control Plane**

I wanted to push past the standard generative chatbot model. Naur uses agentic AI as an active architectural gatekeeper rather than a simple text summarizer. Driven by the system parameters, the AI executes a highly deterministic reasoning cycle:

Intake: It pulls the exact, chronological communication log via the MCP server (read_architecture_thread).

Analysis: It evaluates the active personas to figure out if any vital roles are missing from the conversation (The Missing Chair logic).

Execution: The agent dispatches parallel tool calls to update the domain constraints and the project dictionary.

**Schema Defense:** 

To keep the system acting as an objective data pipeline, I programmed the MCP server to enforce strict JSON array schemas on all AI tool inputs. This physically blocks the language model from hallucinating or injecting conversational commentary (e.g., "Here are the constraints you asked for:") into the production database. If it doesn't fit the array, it gets rejected.

**Architecture Diagram & System Flow**

This maps the live system flow from the human team to the autonomous linter.

```text
[ Human Stakeholder ] ➔ [ Streamlit UI: Chat Input ]
                               │
                               ▼
              (Writes tagged string to `chat_ledger`)
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│               State Ledger (naur_state.db / SQLite)             │
└─────────────────────────────────────────────────────────────────┘
                               ▲
             (Parallel Writes) │ (Reads Context)
                               │
┌──────────────────────────────┴──────────────────────────────────┐
│                      MCP Server (stdio)                         │
│   (Validates array schemas, strips conversational fluff)        │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│               IBM Bob Agent (Ontological Linter)                │
├─────────────────────────────────────────────────────────────────┤
│ 1. OBSERVE: read_architecture_thread                            │
│ 2. IDENTIFY: Detect missing roles & jargon collisions           │
│ 3. TRANSLATE: Synthesize engineering & layman impacts           │
│ 4. EMIT: update_domain_constraint, upsert_project_dictionary    │
└─────────────────────────────────────────────────────────────────┘

```
---

### 4. The Quickstart Guide

Naur is designed for immediate local deployment. You do not need any external cloud databases since it relies entirely on a dynamically generated SQLite ledger.

**Prerequisites**

1. Python 3.10+: You will need this for the structural pattern matching and schema typing.
2. IBM Bob: Installed and configured within your local IDE.

**Phase 1: Installation & Environment Setup**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/naur.git
   cd naur

2. **Create the virtual environment:**
*Critical:* You must name the environment `venv` because the `.bob/mcp.json` configuration is strictly hardcoded to look for the execution binary at `${workspaceFolder}/venv/Scripts/python.exe`.
```bash
python -m venv venv

```


3. **Activate the environment:**
* **Mac/Linux:** `source venv/bin/activate`
* **Windows:** `venv\Scripts\activate`


4. **Install pinned dependencies:**
```bash
pip install -r requirements.txt

```



**Phase 2: Execution Workflow**

The application requires two concurrent operations. You have to run the Streamlit frontend and execute the IBM Bob orchestration loop at the same time.

**Step 1: Boot the Presentation Workspace**
Run the Streamlit application from your active terminal. Upon execution, `src/state_manager.py` automatically runs `init_db()` to generate a clean `naur_state.db` file in your root directory.

```bash
streamlit run app.py

```

*The UI will open in your browser, typically at `http://localhost:8501`.*

**Step 2: Connect the Orchestration Engine**
Open the `naur` project folder inside your IBM Bob-enabled IDE. Because the `.bob/mcp.json` file is present, Bob automatically registers the local MCP server, granting it secure access to the SQLite database via standard input/output (stdio).

> **Troubleshooting:** > * **MCP Protocol Logs:** If the MCP server fails to connect or throws schema errors, look at the **Output** tab in your IDE and filter the dropdown to `IBM Bob` or `Model Context Protocol`.
> * **State Ledger Logs:** Database operations, write-locks, and Streamlit execution errors are piped directly to the terminal where you executed `streamlit run app.py`.

**Step 3: Run the Live Alignment Loop**
To see the autonomous linter in action, follow this exact loop:

1. **Human Input:** In the Streamlit UI, select a Role from the dropdown (e.g., *Frontend Engineer*), adjust the Governance phase slider, type a technical proposal into the chat box, and submit the message.
2. **Agent Initialization:** Switch to your IDE and open the IBM Bob chat interface. To initialize the linter's exact reasoning constraints, submit this initial execution prompt:
> *"Bob, act as the Ontological Linter and Principal Architect for Project Naur. Execute the following observation loop exactly 2 times, pausing for 10 seconds between each iteration. After the 2nd iteration, halt completely and explicitly say 'Loop Complete.'*
> *Action Chain:*
> *1. Invoke `read_architecture_thread`.*
> *2. Analyze new messages for risks across ALL five domains.*
> *3. If technical friction exists, invoke `update_domain_constraint` (Separate tool call for each domain).*
> *4. You MUST execute a separate tool call to `update_domain_constraint` with the domain set to `GLOBAL` for the rationale.*
> *5. If vague buzzwords exist, invoke `upsert_project_dictionary`."*


3. **Continuous Execution (Token Saver):** If you are continuing an existing thread and simply want Bob to re-evaluate new messages without burning unnecessary Bobcoins on the full prompt, use the shorthand execution:
> *"Execute your observation loop exactly 2 times, then halt."*


4. **State Synchronization:** Wait for Bob to finish calling the parallel MCP tools and declare "Loop Complete." Return to the Streamlit UI and click the **Sync** button in the sidebar.
5. **Review:** The UI instantly ingests the database mutations, rendering the updated multi-domain blast radius, the 3-tiered constraint translations, and any newly captured project glossary terms.

**State Reset**

If the SQLite ledger accumulates too much test data, click the **Clear** button in the Streamlit sidebar. This triggers `clear_ledger()`, performing a clean transaction wipe of all three database tables instantly without requiring a server restart or crashing the application state.


### 5. "Future of Work"?

The Wildcard category demands intelligent systems that rethink the future of work, focusing on workflow automation, AI co-workers, and decision intelligence. Naur hits this theme by shifting the focus from how fast we work to how clearly we think.

**Execution Velocity vs. Decision Intelligence**

Most modern AI tools focus entirely on speed—helping developers write boilerplate code faster or autocomplete lines. However, software development is rarely bottlenecked by typing speed. It is bottlenecked by human misalignment.

Naur focuses entirely on clear coordination. It serves as an automated organizational checkpoint that ensures product, engineering, and design teams are synced before execution begins. By forcing teams to resolve their communication gaps upstream, Naur prevents teams from using AI to simply build the wrong software at a higher speed.

**Enterprise Readiness via MCP**

Integrating Naur directly as a Model Context Protocol (MCP) server—rather than forcing teams to adopt another standalone web dashboard—projects true production readiness. 
* **Zero Friction:** It integrates seamlessly directly inside the IDE environments developers are already using.
* **Structural Safety:** It replaces standard, chaotic chat logs with heavily typed, deterministic architectural governance. 

Naur demonstrates how future AI co-workers can step away from being passive text-generation tools and become active, structural defenders of system integrity.

---

### 6. Future Roadmap

Right now, the prototype orchestrates local state via standard input and output through the IDE, requiring manual execution prompts for every sync. My roadmap focuses on shifting Naur from a manual tool into a fully automated, ambient daemon that permanently protects teams from **Comprehension Debt**.

*   **Autonomous Background Daemon (Zero-Prompting):** I want to upgrade Naur into a continuous background process. Instead of a developer having to manually paste initialization prompts into the Bob interface, the daemon will actively monitor the `chat_ledger`. The moment a team member proposes complex functional logic without clear boundaries, Naur will autonomously fire a **Mandatory Intervention Trigger** directly into the communication stream, halting the conversation until the 4-point Architectural Scaffold is settled.
*   **CI/CD Pre-Flight Enforcement:** I plan to build Naur into a GitHub Action that evaluates incoming Pull Requests against our **3 Continuous In-Memory Gates**. Before code can merge, Naur will audit the diff to verify: *Where does state live? Where does feedback live? What breaks if I delete this?* If a PR touches multiple domains without an agent-validated constraint logged during the architecture phase, the build will automatically fail, stopping unaligned code from polluting production.
*   **Bidirectional Tracker Sync (Jira & Linear):** I aim to bridge the gap between architectural chatter and actual project management. Naur will automatically map out the calculated blast radius of a slack or chat discussion and synchronously update targeted issue tracking tickets with explicit engineering requirements, technical rationales, and jargon-free business impacts.
*   **Multi-Agent Adversarial Debate Protocol:** For highly volatile proposals, I want to explore a decentralized debate layer. This phrase sounds incredibly high-tech, but under the hood, it just means prompting two different LLMs with opposing instructions—like a grumpy security engineer and a fast-moving product manager—and letting them bicker back and forth until they find common ground. This text debate will run in the background before synthesizing a unified, solid global architectural state for the human team.
---

### 7. Team & License

**Built for:** AI Builders Challenge with IBM Bob (Wildcard Challenge - Build Intelligent Systems for the Future of Work)

**The Team:**
* **Antonio III Buenafe** – Developer
* **Links:** [GitHub Profile](https://github.com/anton-buen) | [LinkedIn Profile](www.linkedin.com/in/antonio-iii-buenafe-488a1936b)

**Tech Stack:** IBM Bob, Model Context Protocol (MCP), Python 3.10+, SQLite, Streamlit 

**License:** Distributed under the [MIT License](https://opensource.org/licenses/MIT).

### 8. Project Evolution & History

Naur is the result of rigorous architectural iteration and structural pivots. To explore the complete history of how this system evolved from its original concept into its current deterministic MCP protocol, you can review the original build documentation here:

**[Explore how it evolved](https://github.com/anton-buen/cognitive-alignment-engine)**

> *"Programming properly should be regarded as an activity by which the programmers form or achieve a certain kind of insight, a theory, of the matters at hand."* — Peter Naur
