# Naur

### 1. The Core Fundamentals

**Project Title:** Naur (Inspired by Peter Naur's *Programming is Theory Building*)  
**Challenge Theme:** Work Reimagined (Wildcard Challenge: Intelligent Systems for the Future of Work)

**Problem Statement: The Alignment Tax & Comprehension Debt**

Whether you are coordinating a university group project, surviving a 48-hour hackathon, or shipping enterprise software in a Fortune 500 company, the highest cost to productivity is never bad code—it is human friction. We call this the Alignment Tax. 

A Product Manager asks for a "simple login," a Designer envisions a seamless social-auth flow, and a Backend Engineer immediately worries about JWT token expiration and database latency. Because multidisciplinary teams speak entirely different professional dialects, they spend hours talking past each other. This communication gap creates **Comprehension Debt**. It is a hidden, structural misunderstanding where team members falsely believe they are in agreement. When left unchecked, this debt always comes due as painful, late-stage rewrites, abandoned pull requests, and broken integrations when the team finally realizes they were never building the same mental model.

**Why Naur Outperforms Legacy & Modern Workflows (2026)**
Old-school workflows rely on disjointed Jira tickets and endless Slack threads where context inevitably dies. Conversely, modern 2026 workflows rely heavily on autonomous coding agents and LLM co-pilots. However, accelerating code generation without addressing human alignment simply means a team builds the *wrong software much faster*. 

Naur improves both old and new workflows because it sits strictly upstream of execution. While other AI tools focus on writing code, Naur focuses on writing the *theory*. By aligning the organizational intent before execution begins, Naur ensures that whether a human or an AI agent ultimately writes the code, the structural blueprint is actually correct.

**Solution Description: The Autonomous Organizational Linter**
Naur is an intelligent AI Co-Worker designed to catch this misalignment in real time. Rather than operating as a traditional, disruptive chatbot, Naur runs quietly in the background as a Model Context Protocol (MCP) server, plugging directly into the team's communication stream. 

As the team discusses features and architecture, Naur runs a continuous observation loop to enforce Domain-Driven Design (DDD) and cross-disciplinary empathy:
1. **The Missing Chair:** It analyzes the active participants. If backend and product are making UI decisions without a designer present, Naur actively advocates for the missing discipline's boundaries.
2. **Ubiquitous Language:** It catches technical terminology collisions (e.g., stopping a PM and an Engineer from using the word "Cache" to mean two different things) and normalizes them into a shared, centralized project dictionary.
3. **3-Tiered Translation:** When a risky architectural proposal is made, Naur intercepts it and instantly calculates the blast radius. It translates the proposal into three clear, decoupled realities: precise **Engineering Requirements**, highly detailed **Technical Rationales**, and 100% jargon-free **Business Impacts** that anyone on the team can immediately understand.

Naur forces shared understanding and maps technical constraints into business realities before a single line of unviable code is ever written.



### 2. The "IBM Bob" Audit Trail

To build Naur, IBM Bob was not merely used as a standard code-generation autocomplete tool. Bob served a dual purpose: first as the **Principal Architect & Development Agent** during the build phase, and ultimately as the **Runtime Orchestration Engine** powering the live Model Context Protocol (MCP) loop. 

Here is the exact audit trail of how IBM Bob was utilized to engineer this prototype.

**Phase 1: Architectural Planning (Plan Mode)**
* **Persona Engineering:** Used Plan Mode to define Bob’s role strictly as the "Ontological Linter and Principal Architect" via the `.bob/system.md` configuration. 
* **Rule Enforcement:** Prompted Bob to codify 5 strict behavioral constraints, including "The Missing Chair" principle (advocating for absent disciplines) and three dynamic governance tiers (Ideation, Architecture, Pre-Flight).

**Phase 2: Core Engineering & Scaffolding (Agent Mode)**
* **State Persistence:** Instructed Bob to build `src/state_manager.py`. It generated the complete SQLite persistence layer, including 3 distinct tables (`chat_ledger`, `domain_constraints`, `project_glossary`) and the 6 core CRUD functions required to safely handle concurrent reads/writes without dropping data.
* **Protocol Server Generation:** Utilized Bob's specific `build-mcp-server` skill to architect `src/mcp_server.py`. Bob correctly scaffolded the stdio transport setup and registered the three custom tools (`read_architecture_thread`, `update_domain_constraint`, `upsert_project_dictionary`).
* **Environment Wiring:** Activated Bob's `configure-mcp` skill to map the custom server into `.bob/mcp.json`, correctly pointing the execution command to the local virtual environment's Python binary (`${workspaceFolder}/venv/Scripts/python.exe`).
* **Frontend UI Execution:** Deployed Bob to write the ~440-line `app.py` Streamlit presentation layer. Bob engineered a custom Markdown-to-HTML parser (`parse_markdown()`) to bypass native rendering limits and built the zero-latency "Translate" toggle using a pure-CSS checkbox hack (`<input type="checkbox">`), completely avoiding slow JavaScript execution.

**Phase 3: Bob as the Runtime Execution Engine**
For the final production prototype, IBM Bob transitions from being the *developer* of the tool to becoming the *core logic engine* of the tool itself. By tying the `.bob` configuration directly to the local project, Bob operates as the autonomous linter. When a user hits "Sync" in the UI, Bob reads the ledger, calculates the architectural blast radius, and fires parallel database mutations to rewrite the project constraints. **By utilizing Bob as the MCP client rather than a standard external API call, Naur embeds architectural governance directly into the active IDE where the developer is working, removing the need for a disconnected third-party management dashboard.**

**Summary of Bob's Technical Contributions**

| Component | Engineering Task | Mode / Skill Used |
| :--- | :--- | :--- |
| **System Prompt** | Defined the Naur persona, Missing Chair logic, and 3-tier governance. | `Plan` / System Authoring |
| **Persistence Ledger** | Built `state_manager.py` with idempotent table creation and locking buffers. | `Agent` |
| **MCP Server** | Built `mcp_server.py` and enforced strict JSON array schema typing. | `Agent` / `build-mcp-server` |
| **MCP Registration** | Wired the `.bob/mcp.json` file to the local Python subprocess environment. | `Agent` / `configure-mcp` |
| **Streamlit UI** | Wrote `app.py`, custom CSS layout engine, markdown parser, and state sync. | `Agent` |


### 3. Architecture & AI Approach

Naur is engineered with a strict separation of concerns, completely decoupling the volatile frontend presentation layer from the persistent relational ledger and the background AI orchestration loop. 

**The Tech Stack**

| Component | Technology | Architectural Responsibility |
| :--- | :--- | :--- |
| **Presentation Layer** | `Streamlit` (1.59.1), `HTML5`, `CSS3` | Renders the corporate UI. Bypasses native rendering with a custom parser (`parse_markdown()`) and executes zero-latency technical/layman layout shifts using pure CSS pseudo-classes (`:checked`), completely avoiding slow server-side JavaScript execution. |
| **Persistence Ledger** | `SQLite3` (Native Python) | Concurrency-safe transactional database (`naur_state.db`) holding chat logs, domain constraints, and the project glossary. Hardcoded with a 15-second write-lock timeout buffer to absorb background multi-agent collisions. |
| **Protocol Engine** | `mcp` (1.28.1), `uvicorn`, `pydantic` | Exposes the SQLite ledger to external agent environments over standard input/output (stdio) channels. Strictly types all AI inputs as JSON arrays to validate payloads before database injection. |
| **Logic Engine** | IBM Bob (Claude) | Acts as the autonomous linter. Reads ledger states, calculates structural blast radii, and executes parallel database mutations directly from the user's local IDE workspace. |

**AI Integration: The Agentic Control Plane**
In the context of the "Future of Work" challenge, Naur demonstrates how AI must evolve past simple generative chatbots. Naur does not use LLMs to summarize text or write boilerplate code; it utilizes **Agentic AI** as an active architectural gatekeeper. 

Driven by the `.bob/system.md` parameters, the AI executes a deterministic autonomous reasoning cycle:
1. **Intake:** The agent triggers `read_architecture_thread` via the MCP server to pull the exact chronological communication log and active governance state.
2. **Analysis:** The AI evaluates the active personas against system boundaries to calculate "The Missing Chair" (e.g., advocating for UI/UX if only Backend and Product are speaking).
3. **Execution:** The agent dispatches parallel tool calls to `update_domain_constraint` and `upsert_project_dictionary`. 
4. **Schema Defense:** To ensure the system remains an objective data pipeline rather than a chat interface, the MCP server enforces strict `array` schemas on the AI's tool inputs. This physically blocks the LLM from injecting conversational meta-commentary (e.g., *"Here is your constraint:"*) into the production database.

**Architecture Diagram & System Flow**
This diagram maps the exact live system flow between the human team, the database, and the autonomous AI co-worker.

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

Naur is engineered for immediate local deployment. It requires zero external cloud databases, relying entirely on a local Python virtual environment and a dynamically generated SQLite ledger.

**Prerequisites**
* **Python 3.10+**: Required for advanced structural pattern matching and strict schema typing.
* **IBM Bob**: Installed and configured within your local IDE (e.g., VS Code extension).

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

Naur requires two concurrent operations: running the Streamlit presentation layer and executing the IBM Bob orchestration loop.

**Step 1: Boot the Presentation Workspace**
Run the Streamlit application from your active terminal. Upon execution, `src/state_manager.py` automatically runs `init_db()` to generate a clean `naur_state.db` file in your root directory.

```bash
streamlit run app.py

```

*The UI will open in your browser, typically at `http://localhost:8501`.*

**Step 2: Connect the Orchestration Engine**
Open the `naur` project folder inside your IBM Bob-enabled IDE. Because the `.bob/mcp.json` file is present, Bob automatically registers the local MCP server, granting it secure access to the SQLite database via standard input/output (stdio).

> **Observability & Troubleshooting:** > * **MCP Protocol Logs:** If the MCP server fails to connect or throws schema errors, look at the **Output** tab in your IDE and filter the dropdown to `IBM Bob` or `Model Context Protocol`.
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

```


```

### 5. Why Naur is "Work Reimagined" 

The Wildcard category asks for intelligent systems that define the future of work, focusing heavily on workflow automation, AI co-workers, and decision intelligence. 

Most AI tools in 2026 focus purely on **Execution Velocity**—writing code faster, generating boilerplate, or automating pull requests. However, enterprise software is not constrained by typing speed; it is constrained by human misalignment. 

Naur focuses entirely on **Decision Intelligence**. It acts as an autonomous organizational linter that ensures the mental models of Product, Engineering, and Design are perfectly synced *before* execution begins. By integrating directly as an MCP server rather than a standalone dashboard, Naur projects production readiness and fits seamlessly into the tools developers and PMs are already using. It eliminates "Hackathon Chaos" and replaces it with deterministic, heavily typed architectural governance.

---

### 6. Future Roadmap

While the current prototype effectively orchestrates local SQLite state via standard I/O through the IBM Bob IDE, the production roadmap for Naur focuses on removing the human entirely from the execution loop and expanding into distributed environments.

* **Fully Autonomous Execution (Zero-Prompting):** Upgrading from the manual IDE-based MCP loop to a background daemon watcher. Naur will automatically monitor the `chat_ledger` for state changes and trigger the LLM via API in the background, eliminating the need to manually paste prompts into Bob for every synchronization.
* **Jira & Linear Sync (Bi-directional):** Upgrading the server to not just read local threads, but pull active ticket constraints and push calculated blast radii directly into issue trackers.
* **Continuous Integration (CI) Pre-Flight Checks:** Running the Naur linter as a GitHub Action. If a PR touches multiple domains (e.g., Backend and UI) but the UI constraint was never validated by the agent in the architecture phase, the PR is automatically flagged for comprehension debt.
* **Multi-Agent Debate Protocol:** Allowing Naur to spawn sub-agents for specific domains (e.g., a dedicated "Security Agent" and a dedicated "Performance Agent") that debate constraints in the background before synthesizing the final `GLOBAL` recommendation to the human team.

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
