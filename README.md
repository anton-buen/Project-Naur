# Naur

### 1. The Core Fundamentals

**Project Title:** Naur (Inspired by **Peter Naur's** *Programming is Theory Building*)  
**Challenge Theme:** Intelligent Systems for the Future of Work

**The Friction: The Alignment Tax.**

When building in teams, the biggest drag isn’t writing code. It is mutual misunderstanding. A product manager asks for a “basic login” feature, while the designer envisions a quick social auth flow. Meanwhile, the backend engineer stresses over token expiration and database latency. Because multidisciplinary domains just speak entirely different professional dialects, they pay a massive, often overlooked, productivity penalty. Let’s call it the Alignment Tax.

I misappropriated this term from AI safety. In machine learning, it refers to the performance or speed penalty you pay to keep a model aligned with human values. Here, I am repurposing it to describe human-to-human communication friction instead.

This communication gap creates Comprehension Debt, a playful, slightly dramatic take on “Technical Debt.” It describes the cost of people failing to understand each other. The illusion of agreement masks entirely disjointed mental models. That debt eventually comes due during, say, integration week, resulting in painful late-stage rewrites, broken databases, or abandoned pull requests.

**The Gap in Modern Workflows**

Current workflows rely heavily on autonomous agents to write faster. However, accelerating code generation without addressing the actual human alignment simply helps a team build the wrong software faster. If you don’t write the theory of the software first, the code is just an expensive shadow of an already broken model. Naur handles this friction upstream.

**The Solution**

Naur acts as an automated organizational checker that enforces Domain-Driven Design (DDD) constraints before anyone writes execution code. Okay, calling it an Ontological Linter is peak hackathon showmanship. It isn’t a static compiler tool analyzing the nature of existence; it’s a specialized LLM prompt strategy that runs quietly in the background as a Model Context Protocol (MCP) server that plugs directly into a team’s active communication stream. It flags, for example, when two people use the same word to mean different things.

It builds and forces cross-disciplinary empathy by executing three continuous architectural checks:

The Missing Chair: Inspired by Jeff Bezos’s old trick of leaving an empty chair at the table to represent the customer, this sounds like a complex architectural rule. Under the hood, it is a straightforward IF/THEN checking who is active in the chat. If engineering and product make UI choices without a designer present, Naur steps in to advocate for that missing role/s.

Ubiquitous Language (DDD): It catches terminology collisions. If an engineer and a product manager use the word “cache” differently, the system flags it and normalizes the definition into a centralized project glossary.

3-Tiered Translation: When a risky proposal surfaces, Naur intercepts it to evaluate what might break. I call this “calculating the cross-domain blast radius,” but the LLM is simply making an educated guess based on the context. It translates the proposal into three views: 1. precise technical requirements, 2. a deep-dive rationale, and 3. jargon-free business impacts.


**The ultimate goal is to force shared understanding across domains, ensuring that whether a human or an AI agent ultimately writes the code, the underlying structural blueprint is “actually correct”. Any change or addition moving forward is also forced to be understood across said domains.**

---

### 2. What did IBM Bob do?

I didn’t use IBM Bob as a generic autocomplete tool; I deployed it with highly deterministic, strict prompts to handle the architectural heavy lifting. To enforce Peter Naur's principles, I initially configured Bob as a strict "Principal Systems Architect" bound by a **Mandatory Intervention Trigger**—forcing it to halt code generation and demand a 4-point scaffold (Goal, State, Feedback, Blast Radius) if I ever asked for complex logic without defining boundaries. With these **3 In-Memory Gates** (*Where does state live? Where does feedback live? What breaks?*) established, Bob operated across four distinct roles during the build:

**Phase 1: The Database & State Refactor**
Halfway through the build, I realized a flat JSON file wouldn't survive concurrent agent operations, so I migrated the backend to SQLite. I deployed Bob to completely rewire the Streamlit frontend (`app.py`) to connect to the new `state_manager.py` API. Bob refactored the sidebar to drop the old dictionary logic, replacing it with a clean `sm.clear_ledger()` and `st.rerun()` loop. It then pulled the constraints and project dictionary out of the chat loop entirely, creating the "Global Alignment Dashboard" that renders the Risk Badge and Tech Cards persistently at the top of the screen.

**Phase 2: The UI & Aesthetic Engineer**
I have a very specific vision for the Naur interface, and I used Bob to execute the CSS without having to wrestle with Streamlit's native layout limitations. I gave Bob exact hex codes and typography rules to rewrite the `apply_adaptive_theme()` function. Bob applied specific accents for the UI cards (e.g., `#6B4A3A` for Frontend, `#A3A08E` for Data Science) and warmed up the muted text with `#E9DDCF`. It also successfully wrote the CSS to keep all headers in a sans-serif font while reverting the chat inputs, message bubbles, and tech-card bodies to a strict monospace font (`JetBrains Mono` / `IBM Plex Mono`).

**Phase 3: The Ruthless Code Reviewer**
Before finalizing the prototype, the codebase was filled with hackathon clutter—commented-out legacy code, inline developmental notes, and "FIXME" tags. I prompted Bob to act as a Senior Code Reviewer with strict constraints: make zero logic alterations and zero UI modifications. Bob stripped all the developmental clutter and enforced clean, concise Python docstrings across every major function and class to ensure professional polish.

**Phase 4: The Runtime Linter**
In the live application, Bob ceases to be the developer and becomes the product itself. Operating under the prompt *"Bob, please review the architecture thread and extract any constraints,"* Bob transitions into the autonomous Ontological Linter. It pulls the exact chronological chat thread, calculates the cross-domain blast radius, and fires parallel database mutations to rewrite project constraints directly from the IDE.

**Skills Used**
To wire this all together, I relied explicitly on two of Bob's native workspace skills. The `build-mcp-server` skill was utilized to provide the exact `mcp` Python SDK v2 API pattern—including the `Server()`, `@app.list_tools()`, the `stdio_server` context manager, and the `asyncio.run()` entrypoint. Without this, the MCP server structure would not have followed the correct protocol. I then used the `configure-mcp` skill to generate the `.bob/mcp.json` schema. This provided the exact command, arguments, and `${workspaceFolder}` variable syntax required to ensure the custom server registered seamlessly to the Bob IDE without manual debugging.

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

To keep the system acting as an objective data pipeline, I programmed the MCP server to enforce strict JSON array schemas on all AI tool inputs. This physically blocks the language model from hallucinating or injecting conversational commentary (e.g., “Here are the constraints you asked for:”) into the production database. If it doesn’t fit the array, it gets rejected.


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

**State Sync**
If IBM Bob is still executing its observation loop in the background, you can click the **Sync** button in the Streamlit sidebar at any time to fetch the latest database mutations. *Note:* I intentionally limited Bob's execution prompt to exactly two iterations. This gives the agent just enough cycles to double-check its own reasoning and outputs, while strictly budgeting our Bobcoin expenditure.

**State Reset**
If the SQLite ledger accumulates too much chat history or test data, simply click the **Clear Ledger** button in the sidebar. This triggers `sm.clear_ledger()`, performing a clean transaction wipe across all three database tables instantly. It safely resets the application state without requiring a server restart or crashing the frontend UI.


### 5. "Future of Work"?

The Wildcard category demands intelligent systems that rethink the future of work. Naur hits this theme by shifting the focus from how fast we work to how clearly we think and communicate.

Most modern AI tools focus entirely on speed or efficiency, helping developers write code faster or autocomplete lines. However, development is rarely bottlenecked by typing speed. It is bottlenecked by human misalignment.

Naur focuses entirely on clear coordination and communication. It serves as an automated organizational checkpoint that ensures product, engineering, and design teams are synced before any execution begins. It even enforces this during and after the execution. By forcing teams to resolve their communication gaps upstream, Naur prevents teams from using AI to simply build the wrong software at a higher speed.


### 6. Future Roadmap

Right now, Naur operates locally and requires a developer to manually trigger the alignment checks. The ultimate vision is to make Naur completely invisible and autonomous: an ambient layer of the development process that catches Comprehension Debt before it ever reaches production.

*   **Invisible Orchestration (Zero-Prompting):** Moving away from manual triggers, Naur will run as a continuous background process. It will passively observe team chats and only intervene when it detects a high-risk architectural blind spot, automatically pausing the conversation to force alignment before the team moves forward.
*   **The Alignment Gatekeeper (CI/CD):** Naur will integrate directly into code review pipelines (like GitHub Actions). If a developer submits code that impacts multiple domains (e.g., UI and Database), but the team never actually agreed on the cross-domain constraints during the planning phase, Naur will flag the pull request. It stops misaligned code from merging.
*   **Syncing Chat to Project Tickets:** Teams talk in chat apps but work in tools like Jira or Linear. Naur will bridge this gap by automatically translating complex chat debates into clear, actionable engineering requirements and syncing them directly to the active project management tickets. 
*   **Automated Stress Testing (Multi-Agent Debate):** For highly volatile or risky proposals, Naur will spin up multiple AI personas—like a strict security engineer and a fast-moving product manager—and have them debate the idea in the background. They will pressure-test the concept from different angles and present a unified, safe architectural recommendation to the human team.

---

### 7. Team & License

**Built for:** AI Builders Challenge with IBM Bob (Wildcard Challenge - Build Intelligent Systems for the Future of Work)

**The Team:**
* **Antonio III Buenafe** – Developer
* **Links:** [GitHub Profile](https://github.com/anton-buen) | [LinkedIn Profile](www.linkedin.com/in/antonio-iii-buenafe-488a1936b)

**Tech Stack:** IBM Bob, Model Context Protocol (MCP), Python 3.10+, SQLite, Streamlit 

**License:** Distributed under the [MIT License](https://opensource.org/licenses/MIT).

### 8. Project Evolution & History

Great software is discovered through trial, error, and a stubborn belief that teams can always find a better way to work together. Naur is the proud result of those necessary failures and architectural pivots. If you want to explore the journey of how this tool evolved from a raw, ambitious concept into the deterministic MCP protocol it is today, you can read the original build history here:

**[Explore how it evolved](https://github.com/anton-buen/cognitive-alignment-engine)**

> *"Programming properly should be regarded as an activity by which the programmers form or achieve a certain kind of insight, a theory, of the matters at hand."* — Peter Naur
