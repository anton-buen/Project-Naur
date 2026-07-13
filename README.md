# Naur

## 1. What's the big idea?

>**Project Title:** Naur (Inspired by **Peter Naur's** *Programming is Theory Building*)  
>**Challenge Theme:** Intelligent Systems for the Future of Work
<br> <br> 
### **The Problem: Alignment Tax.**

As a CS student who has led numerous development teams, I’ve watched projects fail in real-time. It’s rarely because someone lacks the talent to write loops; it’s because humans are just remarkably bad at understanding each other.

In every project, you have specialists—frontend engineers, backend engineers, data scientists, and UI/UX designers. They look at the software through completely different professional lenses. You cannot force a backend engineer to deeply adopt a designer's big picture mindset without diluting their focus and specialization.
<br> 
<br>
However, this creates a massive drag during the planning and development phases. Let's call it the Alignment Tax. I openly admit to misappropriating this term from AI safety. Here, I’m repurposing it to describe human-to-human communication friction:

***Tax is Time and Effort*** — Teams waste hours trying to explain their domains to one another. Even if a dedicated facilitator is present, a human simply does not have the memory capacity to retain every architectural dependency and cross-domain constraint simultaneously.

***Comprehension Debt*** — Words mean different things to different specialists. A simple choice discussed during planning often turns into disjointed mental models. This misunderstanding hits like a train during integration week, leading to wasted effort and painful late-stage rewrites.

***Feature-Bloat*** — Without a clear, objective system to ground understanding, teams often lean on vague "design thinking" buzzwords, ending up with bloated, multi-functional apps that solve no real underlying problem.
<br> <br> 

>**A Gap in Modern Workflows**
>
>Current industry workflows rely heavily on autonomous AI agents to generate code faster. However, accelerating code output without addressing underlying human alignment simply helps a team build the wrong software at record speeds. If you haven’t co-authored the theory of the software first, the generated code is just an expensive shadow of a broken model. Naur intercepts this friction upstream.
>
<br> 

### **The Solution: ***An Agent-Driven Architectural Auditor*****
Look, calling this an "Ontological Linter" might sound like a hackathon play to sound smart. It isn't a static compiler analyzing the nature of cosmic existence. It is a specialized LLM orchestration strategy running over a local Model Context Protocol (MCP) server. Instead of forcing an AI to blindly guess your code intent, Naur exposes your team's communication ledger directly to your local IDE agent workspace. This allows a developer to run on-demand architectural audits, catching human misunderstandings upstream before anyone writes a single line of execution code.
<br> <br> 

***Naur consolidates the time teams waste teaching each other into explicit, data-driven design constraints by running three structural checks on command:***

***The Missing Chair***  — This is a straightforward validation loop checking who is active in the workspace channel. Naur steps in to advocate for that missing discipline.
>Inspired by Jeff Bezos’s trick of leaving an empty chair at the table to represent the customer. 

***Ubiquitous Language (DDD)***  —  It catches terminology collisions. If a backend engineer and a product manager use a word like "cache" or "state" differently, the system flags it and normalizes the definition in a centralized dictionary.

***Cross-Domain Blast Radius,*** — When a risky proposal surfaces, Naur intercepts it to evaluate what might break across all technical and business domains, acting as an automated risk assessor.<br> <br> <br> 


## **Naur  — Dashboard and Features** 
<img width="1917" height="1017" alt="Naur Dashboard Overview" src="https://github.com/user-attachments/assets/b95ee00f-f1d2-458e-b272-cec2d04ed74a" />
 <br> <br>
Instead of dumping a wall of text into the chat, the AI synthesizes its background analysis into a real-time, interactive dashboard that serves as the team's single source of truth.


<br><br> 

**1. Alignment Risk & Blast Radius:**<br> 
<img width="582" height="120" alt="Alignment Risk Score" src="https://github.com/user-attachments/assets/0365819f-bbe1-44f2-b4c6-1c1628e97987" />
- Dynamic badges (PROD, FE, BE, DS, UI) light up at the top of the UI to map exact dependencies and calculate a global risk score (LOW, MEDIUM, HIGH).

<br><br> 

**2. The Global Rationale:**<br> 
<img width="1492" height="390" alt="Global Rationale Card" src="https://github.com/user-attachments/assets/a1522b94-96e8-4962-9dde-e66ff310d9ab" />
- Sitting immediately below the risk score, this master card provides the executive summary. It justifies the total risk score by synthesizing all the cross-domain friction into a single, unified view.

<br><br> 

**3. Domain Constraint Cards:**<br> 
<img width="1537" height="777" alt="Domain Constraint Cards Breakdown" src="https://github.com/user-attachments/assets/db1faeca-68a9-4a45-866e-2bca4a02e418" />
- The specific blast radius is then isolated into individual discipline cards (Product, Frontend, Backend, Data Science, UI/UX). Each card outlines the exact Engineering Requirements and Business Impacts justifying its respective badge.

<br><br> 

**4. Zero-Latency "Translate" & "Deep Dive" Toggles:**<br> 
<img width="1001" height="692" alt="Pure CSS Translation Toggle View" src="https://github.com/user-attachments/assets/e34c825f-95c9-4866-bee0-e01756d26c16" />
- Every single card—both the Global Rationale and the individual Domain Cards—is equipped with a pure-CSS "Translate" toggle to instantly flip technical jargon into layman's terms, and a "Deep Dive" expander to reveal the raw code-level strict blockers.

<br><br> 

**5. The Project Dictionary:**<br> 
<img width="1542" height="611" alt="Persistent Glossary State" src="https://github.com/user-attachments/assets/2c50de9e-9796-4a9a-9811-1bac5c2a88e6" />
- A persistent, centralized glossary pinned to the bottom of the dashboard that houses the normalized terms caught by the Ubiquitous Language check.

<br> <br> 
**The ultimate goal is to force shared understanding across domains, ensuring that whether a human or an AI agent ultimately writes the code, the underlying structural blueprint is “actually correct”. Any change or addition moving forward is also forced to be understood across said domains.**
<br>
<br>
<br>

---

## 2. What did IBM Bob do?

I wanted to genuinely stress-test the workspace and file-coordination capabilities of IBM Bob. Instead of relying on the easy path of the "Recommended technologies" (like pre-built LangFlow or watsonx pipelines), I undertook a tedious, highly customized local configuration to leverage Bob as the backbone for my local MCP server.  I discovered that Bob has highly reliable capability to coordinate and reason across an entire codebase during development without breaking existing structure:

<br> <br> 
**1: Database & State Refactor** — 
Halfway through the build, I realized a flat JSON file wouldn't survive concurrent agent operations. I deployed Bob to completely rewire the Streamlit frontend (`app.py`) to connect seamlessly to a new transactional SQLite `state_manager.py` API without introducing a single regression. Bob successfully refactored the state persistence layer to decouple the active chat history loop from the presentation logic entirely. This allowed the application to dynamically pull computed metrics out of the SQLite ledger and render the Alignment Risk Score, Blast Radius Badges, and Domain Constraint Cards persistently at the top of the screen.

**2: UI** — 
I used Bob to execute the CSS without having to wrestle with Streamlit's native layout limitations. I gave it exact hex codes and typography rules to rewrite the `apply_adaptive_theme()` function. 

**3: Code Polish** — 
I prompted Bob to act as a ruthless Code Reviewer with strict parameters: make zero logic or UI alterations, but strip out all development clutter, legacy test strings, and inline "FIXME" tags while enforcing clean Python docstrings across the final codebase.


>***Because Naur's entire mission is to enforce omnidirectional understanding across entirely different domains, this exact architectural governance edge made Bob a sufficient engine. It proved that Bob was more than capable of acting as the live, autonomous context brain that orchestrates Naur at runtime***

**4: Runtime** — 
Naur uses IBM Bob as the live processing brain. Under a strict, deterministic prompt routine, Bob processes incoming communication logs from the state engine, isolates the cross-disciplinary domain boundaries, dispatches parallel tool mutations back to the database, and builds the single source of truth dashboard
<br> <br> 

---

## 3. Architecture & AI Approach

I made Naur with a clear separation of concerns. The frontend presentation layer is entirely decoupled from the persistent relational ledger and the background AI orchestration loop.

**The Tech Stack**
| Component | Technology | Role in the Architecture |
| :--- | :--- | :--- |
| **Presentation Layer** | Streamlit (1.59.1), HTML5, CSS3 | Renders the team interface. Uses custom Markdown parsers and pure CSS pseudo-classes (`:checked`) to toggle technical/layman deep-dives with zero runtime lag. |
| **Persistence Ledger** | SQLite3 (Native Python) | Concurrency-safe relational database (`naur_state.db`) that acts as the single source of truth for chat histories, constraints, and the unified glossary. |
| **Protocol Engine** | `mcp` (1.28.1) | Exposes the SQLite ledger to the AI environment over standard input/output (`stdio`) channels, providing direct tool execution bindings. |
| **Logic Engine** | **IBM Bob** | The core AI model. Reads architectural threads, evaluates cross-domain friction, and fires tool parameters back to the persistence layer. |

<br> <br> 
**AI Integration: The Human-in-the-Loop Control Plane**
I wanted to push past the standard generative chatbot model. Naur utilizes agentic AI as an active, on-demand architectural validator rather than a simple text summarizer. Because this is a localized proof of concept, the orchestration engine relies on a human-in-the-loop trigger. Once initialized by the developer within the IDE workspace, the local agent executes a highly deterministic reasoning cycle:
* **Intake** —  It targets and pulls the exact, chronological communication log from the ledger via the MCP server tool (`read_architecture_thread`), which runs a direct `SELECT * FROM chat_ledger` query.
* **Analysis**  —  It evaluates the active personas to determine if any vital engineering roles were missing from the conversation (The Missing Chair logic).
* **Execution** —  The agent dispatches parallel tool calls (`update_domain_constraint`, `upsert_project_dictionary`) with explicitly typed parameters back through the server. The MCP server converts these payloads into atomic `INSERT OR REPLACE` mutations to update domain constraints and log definitions instantly.

To maintain an extremely lightweight messaging bus between the UI and the MCP server, meta-tags for active user roles and governance rules are stamped directly into the raw text payloads of the `chat_ledger`. The processing engine parses these structural prefixes at runtime to evaluate context constraints, and the presentation layer strips them out seamlessly via regular expressions immediately before rendering the historical chat bubbles back to the browser.
<br> <br> 
**Architecture Diagram & System Flow**

This maps the live synchronization flow between the human interface, the database state, the protocol server, and the IDE linter.
<br>
```text
[ Team Member ] ➔ [ app.py (Streamlit UI) ]
                               │
               (Calls append_message, get_constraints)
                               │
                               ▼
                   [ src/state_manager.py ]
                               │
                        (SQL Read/Write)
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│               Persistence: naur_state.db (SQLite)               │
└─────────────────────────────────────────────────────────────────┘
                               ▲
                        (SQL Read/Write)
                               │
                   [ src/state_manager.py ]
                               ▲
                 (Executes sm.update_constraint())
                               │
                 [ src/mcp_server.py (stdio) ]
                               ▲
                  (Invokes Tools via stdio / MCP)
                               │
┌──────────────────────────────┴──────────────────────────────────┐
│                   IBM Bob Agent (VS Code)                       │
│    (Persona: .bob/system.md | Registration: .bob/mcp.json)      │
└─────────────────────────────────────────────────────────────────┘
```
<br>

--- 

## 4. The Quickstart Guide

Because Naur is heavily integrated with the local development environment via the Model Context Protocol, **it requires manual orchestration through the Bob IDE** workspace. Consequently, there is no hosted, publicly visitable web link; the application must be evaluated locally using the following steps.

**Prerequisites**

1. Python 3.10+
2. IBM Bob

**Phase 1: Installation & Environment Setup**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anton-buen/Project-Naur
   cd Project-Naur

2. **Create the virtual environment:**
   Note: It must be named exactly venv as the local .bob/mcp.json schema looks for this precise
   execution path:
   ```bash
   python -m venv venv
    ```

3. **Activate the environment and install the pinned dependencies:**
   ```bash
   # Mac/Linux:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

**Phase 2: Execution Workflow**

The application requires two concurrent operations. You have to run the Streamlit frontend and execute the IBM Bob orchestration loop at the same time.

1. **Boot the Presentation Workspace**
   Run the Streamlit application from your active terminal. Upon execution, `src/state_manager.py`
   automatically runs `init_db()` to generate a clean `naur_state.db` file in your root folder.
   ```bash
   streamlit run app.py
   ```
   *The UI will open in your browser, typically at `http://localhost:8501`.*

2. **Connect the Orchestration Engine**
   Open the `naur` project folder inside your IBM Bob-enabled IDE. Because the `.bob/mcp.json` file
   is present, Bob automatically registers the local MCP server, granting it secure access to the
   SQLite database via standard input/output (stdio).

3. **Run the Live Alignment Loop**
To see the autonomous linter in action, follow this exact loop:

   3.1. **Human Step:** In the Streamlit UI, select a Role from the dropdown (e.g., *Frontend
      Engineer*), provide context (e.g. Tech Stack), adjust the Governance phase slider,
<br>
<img width="477" height="876" alt="Sidebar Context and Role Selection" src="https://github.com/user-attachments/assets/449523a1-6d82-4e08-b440-ac1c978fc17b" />
<br>
<br>
type a technical proposal into the chat box, and submit the message.
<br>
<img width="1387" height="306" alt="Chat Workspace Interface" src="https://github.com/user-attachments/assets/cdea994e-d92d-4149-95b6-ac2de5c69796" />
<br>
<br>

  3.2. **AI Step:** Switch to your IDE and open the IBM Bob chat interface. To initialize the
  linter's exact reasoning constraints, submit this initial execution prompt with the **MCP and read permissions**:
<br><br><br>
<img width="507" height="1001" alt="IDE MCP Setup Verification" src="https://github.com/user-attachments/assets/4f295490-bf88-47ca-8694-5be5ea11ebfa" /> <img width="326" height="542" alt="Bob Orchestration Panel" src="https://github.com/user-attachments/assets/1fe8c222-5a96-4b46-a191-ad201299b4ce" />




<br>
<br>

```
 "Bob, act as the Ontological Linter and Principal Architect for Project Naur. Execute the following observation loop exactly 2 times, pausing for 10 seconds between each iteration. After the 2nd iteration, halt completely and explicitly say 'Loop Complete.'

Action Chain:
1. Invoke read_architecture_thread.
2. Analyze new messages for risks across ALL five domains (FE, BE, DS, UI, PROD).
3. If technical friction exists, invoke update_domain_constraint (Separate tool call for each domain using the arguments: text, business_impact, deep_dive, risk_level).
4. You MUST execute a separate tool call to update_domain_constraint with the domain set to 'GLOBAL' for the rationale.
5. If vague buzzwords exist, invoke upsert_project_dictionary." 
```

  3.3 **Sync Step** Wait for Bob to finish calling the parallel MCP tools and declare "Loop Complete." Return to the Streamlit UI and click the **SYNC** button in the sidebar.


  3.4. **Continue Thread?** If you are continuing an existing thread and simply want Bob to re-evaluate new messages without burning unnecessary Bobcoins on the full prompt:
> *"Execute your observation loop exactly 2 times, then halt."*

3.5. **Review:** The UI instantly ingests the database mutations, rendering the updated **Alignment Risk Score**, populating the **Domain Constraint Cards**, and injecting any newly captured terminology into the **Project Dictionary**.
<br>
<br>
<img width="337" height="182" alt="Dashboard State Mutations Re-cached" src="https://github.com/user-attachments/assets/172f2cdb-e008-4097-b199-91f7eb200661" />
<br>
<br>

>NOTE: I intentionally limited Bob's execution prompt to exactly two iterations. This gives the agent just enough cycles to double-check its own reasoning and outputs, while strictly budgeting our Bobcoin expenditure.
>
>
**State Reset**
If the SQLite ledger accumulates too much chat history or test data, simply click the **CLEAR** button in the sidebar. This triggers `sm.clear_ledger()`, performing a clean transaction wipe across all three database tables instantly.

<br><br>


---

## 5. Track Alignment: The Future of Work

The Wildcard track strictly demands intelligent systems that evolve AI from a simple utility into a true workspace collaborator. Naur achieves this not by writing code faster, but by optimizing the collective intelligence of the human team before execution begins.  

It directly checks every box of the track's core directives:

### I. Intelligent Automation  —  Eliminating Cognitive Overhead

Traditional workflows waste immense human capital on manual alignment checking—project managers constantly reminding teams of baseline scopes, and developers manually parsing internal wikis. Naur automates this entire cognitive burden. While the execution loop is currently triggered on-demand within the IDE to maintain developer control, the processing of the data is completely automated. The local agent parses the raw communication stream, extracts domain requirements, intercepts jargon, and populates the localized database ledger without a human having to sort or map the architectural dependencies manually.

### II. Workflow Orchestration  — Achieving Outcomes Faster

Projects rarely stall because engineers cannot code fast enough; they stall because specialized disciplines operate in disconnected silos. A backend engineer changes a data schema, a designer alters an asset layout, and the disconnect isn't discovered until late-stage integration week, causing painful rewrites. Naur provides proactive orchestration upstream. By acting as an automated gatekeeper during the planning phase, it flags missing disciplinary perspectives (The Missing Chair validation) and forces absolute cross-domain synchronization before execution code is ever written. This transforms the development cycle from a series of fragmented tasks into a unified, outcome-driven system.

### III. Decision Support  — Improving Decision-Making

When high-stakes or risky technical proposals surface, human teams are highly susceptible to cognitive bias or simply forgetting downstream dependencies. Naur provides objective decision support. The system instantly calculates a cross-domain Blast Radius metric and populates dedicated Domain Constraint Cards. By synthesizing technical requirements and business impacts into a clear, data-driven dashboard, it gives teams the exact visibility they need to make rapid, risk-aware architectural choices without relying on vague guesswork or superficial design buzzwords.


>NOTE: Per the official rules of "AI Builders Challenge with IBM Bob", Naur's architecture directly serves the high-velocity requirements of professional **racing** environments by eliminating communication latency and ensuring multi-disciplinary teams maintain peak operational speed without internal friction.
>
>>
<br>
<br>

---

## 6. Realities of the Proof of Concept & What's Next

### The Technical Reality: Why There’s No Live URL

Let’s be real: you cannot click a live website link to instantly test Naur in your browser, and that is entirely by design.

Per the guidelines, I am delivering this project as a **working prototype and proof of concept**. Because I built Naur to stress-test IBM Bob's native workspace capabilities, I architected it strictly as a local Model Context Protocol (MCP) server that communicates via standard input/output (`stdio`) channels directly inside the developer's IDE. It handles local database ledgers and workspace files, meaning a generic, hosted web sandbox simply cannot replicate its environment. To see the PoC in action, it has to be run locally following the **Quickstart** guide above.
<br>
>The AI engine handles the complex reasoning, data mapping, and validation automatically, but I am keeping a human hand on the ignition switch for this local proof of concept.
>
>
<br>

### The Prompt Trade-Off:
Building an AI agent that evaluates *other* architecture creates a unique context-window challenge. During development, I put IBM Bob through 20+ distinct prompt iterations to try and perfectly sterilize its output. 

Because I commanded the agent to run a two-pass validation loop, the LLM constantly wanted to break the fourth wall and narrate its own execution (e.g., writing *"Iteration 2 analysis..."* into the database). I discovered that aggressively locking down the model with strict negative constraints (*"DO NOT mention iterations," "DO NOT define your own rules"*) successfully stopped the context bleeding, but it completely suffocated the model's technical reasoning. The outputs became bland, generic, and useless.

>The reality of this PoC is a deliberate engineering compromise: **I chose to optimize for high-quality, actionable architectural insights over perfectly sterile metadata.** I rolled the prompt back to a loosely constrained version. Bob might occasionally leak an internal execution phrase into the UI, but in exchange, it delivers **senior-level, highly specific technical deep-dives.**

<br>
Because I am executing this as a solo developer, I had to make practical design trade-offs for this version. The biggest one? Right now, you still have to manually prompt Bob in the IDE to trigger the orchestration loops. I proved the underlying engine works flawlessly—now here is how I plan to scale it.

### Where I Am Taking Naur Next:
* **Zero-Prompt Ambient Mode (Solving the Manual Trigger)**  —  Manually copying prompts into the IDE chat is a temporary workaround. My immediate next milestone is turning Naur into a continuous background daemon process. The AI engine will passively track the communication ledger and autonomously intervene *only* when an alignment risk score crosses a critical threshold. No prompting required.
* **Blocking Bad Merges at the Gate (CI/CD Integration)** —  I want to move Naur out of the local IDE and straight into code review pipelines as a native GitHub Action. If a developer attempts to merge a pull request containing structural code changes that conflict with the domain constraints established during the planning phase, Naur will automatically flag it and freeze the merge until the team resolves the communication gap.
* **Bi-Directional Task Syncing** —  Teams talk in chat apps but live in task managers. I plan to connect the local SQLite ledger directly to platforms like Jira or Linear. Naur will ingest verified chat consensus and automatically translate messy developer debates into clean, actionable project tickets without human intervention.
* **Multi-Agent Pressure Testing** —  For high-risk architectural proposals, Naur will spin up specialized, competing AI personas in the background (think a hyper-conservative Security Engineer vs. a high-velocity Frontend Developer). They will actively debate the proposal from their respective lenses and present a unified, stress-tested recommendation to the human team.

---

## 7. Team & License

**Built for:** AI Builders Challenge with IBM Bob (Wildcard Challenge - Build Intelligent Systems for the Future of Work)

**The Team:**
* **Antonio III Buenafe** – Developer
* **Links:** [GitHub Profile](https://github.com/anton-buen) | [LinkedIn Profile](www.linkedin.com/in/antonio-iii-buenafe-488a1936b)

**Tech Stack:** IBM Bob, Model Context Protocol (MCP), Python 3.10+, SQLite, Streamlit 

**License:** Distributed under the [MIT License](https://opensource.org/licenses/MIT).
<br>
> *"Programming properly should be regarded as an activity by which the programmers form or achieve a certain kind of insight, a theory, of the matters at hand."* — Peter Naur

<br>

---

### 8. Project Evolution & History

Great software is discovered through trial, error, and a stubborn belief that teams can always find a better way to work together. Naur is the proud result of those necessary failures and architectural pivots. If you want to explore the journey of how this tool evolved from a raw, ambitious concept into the deterministic MCP protocol it is today, you can read the original build history here:

**[Explore how it started differently](https://github.com/anton-buen/cognitive-alignment-engine)**

