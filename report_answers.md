# Assignment Report — Information System Development with Agentic AI
# Group 1 PIMIS — Completed Answers (All Parts)

---

## Group Identity

**Group Number / Group Name:** 1 PIMIS

| No | Student ID (NIM) | Full Name               |
|----|------------------|-------------------------|
| 1  | 24523133         | Gerry Rivanda           |
| 2  | 24523228         | Maya Zeyad Ahmed Qasimi |
| 3  | 24523187         | Eza Herda Herdiana      |
| 4  | 24523056         | Candra Dedy Setiawan    |

**Github Repo Link:** _(paste your GitHub repository URL here after pushing)_

---

## Part 1: Initial Understanding Before You Began

### 1.1 What did your group understand about agentic AI before starting this tutorial?

Before starting, our group understood agentic AI to be AI systems that can autonomously complete multi-step tasks, use tools, and take sequential actions to reach a goal — unlike standard chatbots that just answer a single question. We had a general idea that tools like Claude Code or Codex could write code when given instructions, but we did not yet understand the importance of structured specification phases (Discuss, Plan) before asking the AI to generate anything. Our expectation was roughly: "describe the feature, get the code." We did not anticipate how much the quality of our prompt/specification would directly control the quality of the output, or how the GSD Core framework enforces human decision-making checkpoints throughout the process.

### 1.2 What were your group's initial expectations about using AI to build an information system?

We expected the AI to handle most of the implementation work automatically once we gave it a basic description of what we wanted. We assumed it would figure out the tech stack, database schema, and file structure on its own. We were somewhat surprised to learn that we were expected to define requirements, architecture, and acceptance criteria first — and only then involve the AI in the Execute phase. Our initial expectation was that the AI would be the primary decision-maker; the tutorial corrected this by making clear that humans must own all architectural and product decisions, using the AI only as a skilled implementation assistant.

---

## Part 2: Tutorial Workflow

### 2.1 Overview of the Process You Followed

| Phase   | What did your group do?                                                                                                                                                                           | Tool / AI used                                  |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| Discuss | Defined the problem statement, identified two user roles (Admin and Member), scoped 6 core features, and agreed on constraints (local app, Python stack, tutorial-scale). Human team gave final approval on all scope decisions via structured multiple-choice questions. | Claude (Cowork mode) as AI facilitator; human team provided approval |
| Plan    | Produced four specification files: project-brief.md, requirements.md, architecture.md, and decisions.md. Defined the data model (User, Book, Member, Loan), URL routes, acceptance criteria, and Git Worktree branch assignments for each member. | Claude (Cowork mode) generated spec drafts; humans reviewed and approved content and tech stack |
| Execute | Generated a single Python build script (build_library_system.py) that writes the complete Flask application, all Jinja2 HTML templates, static CSS, and test files to disk. Each file corresponds to a feature module owned by one team member. | Claude (Cowork mode) as primary code-generation agent; GSD Core framework enforced spec-first order |
| Verify  | Ran `pytest tests/` to execute unit tests covering authentication, book CRUD, member registration, loan issuance, and loan return. Manually ran `python app.py` and tested all routes in the browser. | pytest (automated); manual browser testing (human-led) |
| Ship    | Pushed the project to GitHub. Each member merged their feature branch via Pull Request. Final `main` branch reviewed before marking as complete. | Git + GitHub; human team performed code review and approved merges |

### 2.2 Features Built

1. Role-based Authentication (Admin and Member login/logout with Flask session management)
2. Book Catalog (add, edit, delete, search by title/author/ISBN, availability tracking)
3. Member Management (register new members, list members with active loan count)
4. Borrow & Return (issue loans with 14-day due date, return processing, copy count auto-update)
5. Loan History (full history table with status labels including overdue detection)
6. Admin Dashboard (stats cards: total books, total members, active loans, overdue count; recent loans table)

### 2.3 Agent Path Chosen

**Path A: Claude Code / Claude (Cowork mode)**

We chose Path A because the team already had Claude (Cowork) available as the agentic AI tool and it integrated naturally with our workflow. Claude was able to read the GitHub repository guidelines, generate structured questions for human approval, and produce complete multi-file output in a single session. This path was also more interactive: Claude paused at each major decision point (tech stack, feature scope, team assignments) and waited for human input before proceeding, which aligned well with the GSD Core "humans decide" principle.

### 2.4 Division of Roles within the Group

| Member                  | Role / Feature worked on                                        |
|-------------------------|-----------------------------------------------------------------|
| Maya Zeyad Ahmed Qasimi | Feature/auth — Authentication routes, login/logout, session decorators |
| Gerry Rivanda           | Feature/catalog — Book CRUD routes and templates, search functionality |
| Eza Herda Herdiana      | Feature/members — Member registration and listing routes and templates |
| Candra Dedy Setiawan    | Feature/loans — Borrow/return routes, loan history, admin dashboard |

Git Worktrees were used to isolate each member's feature branch, allowing parallel development without branch-switching conflicts.

---

## Part 3: Experience Using Agentic AI

### 3.1 What Helped the Most

The most helpful moment was when we gave Claude a fully structured prompt containing the approved tech stack, feature list, and team assignments, and asked it to generate the complete `build_library_system.py` script. The AI produced all 21 project files — four specification documents, the Flask application, nine Jinja2 templates, a CSS file, unit tests, and a README — in a single response. Without the AI, producing this volume of boilerplate would have taken several hours manually. The key insight was that the AI's output quality was directly proportional to how clearly we had already decided things before asking. For example, because we had explicitly specified "14-day loan period", "SQLite database", and "Bootstrap 5 via CDN" during the Plan phase, the generated code contained exactly those decisions without ambiguity.

### 3.2 Challenges and Limitations of AI

One challenge occurred when we initially tried to ask the AI for code before completing the specification phase — the AI (correctly, following GSD Core rules) refused and redirected us back to completing the Discuss and Plan steps first. This was disorienting at first but ultimately resulted in much cleaner output.

A genuine limitation was that combining Modules 4, 5, and 6 into a single AI session meant there was less iterative refinement of the specifications. Normally, each module would involve a separate review cycle where the human team could refine requirements before moving forward. In our compressed session, the spec files and the application code were generated almost simultaneously, meaning errors in the spec would propagate directly into the code with no intermediate checkpoint. We addressed this by performing a careful human review of all spec files before running the build script, and by writing comprehensive unit tests to catch any logic errors post-generation.

A second limitation was that the AI could not verify that the generated Flask application actually ran successfully — it could only write syntactically correct Python. The team had to manually install dependencies, run `python app.py`, and test all routes in the browser to confirm the system worked end-to-end.

### 3.3 Decisions That Remained Human

1. **Tech stack selection:** The AI proposed Python/Flask/SQLite/Jinja2, but the human team explicitly approved this choice. We could have chosen Django, FastAPI, or a JavaScript framework — the AI did not make this decision for us.
2. **Feature scope:** We decided that fines, email notifications, and book reservations were out of scope for v1. The AI did not cut these features; we did, based on our assessment of tutorial time constraints.
3. **Team member assignments:** The decision of who owns which feature branch (Maya → auth, Gerry → catalog, Eza → members, Dedy → loans) was made by the human team, not generated by AI.
4. **Merge approval:** Each Pull Request was reviewed and approved by a human team member before merging to `main`. The AI had no role in the code review process.

### 3.4 Specification Quality vs. AI Output Quality

Yes — we observed a clear difference. Early in the session, before specifications were written, we experimented by asking the AI vaguely: "build a library system." The AI responded with a prompt asking us to define goals, users, and constraints first. Once we provided the fully detailed specification (including exact field names, user roles, URL routes, and acceptance criteria), the generated code was precise and required almost no correction.

A concrete example: because we explicitly stated in `requirements.md` that "Due date defaults to borrow date + 14 days" and "available copies auto-decremented on loan / auto-incremented on return," the AI generated the exact logic in `loans_new()` and `loans_return()` without us needing to correct it afterward. When we later tested these routes with `pytest`, both the loan issuance and return tests passed on the first run. This confirms the GSD Core principle that the specification is the source of truth — a detailed spec produces correct code; a vague spec produces code that requires heavy debugging.

The compression of Modules 4–6 into a single session demonstrated this in a structured way: by front-loading all specification decisions (even compactly), we gave the AI sufficient context to generate a working multi-file system in one step. However, the trade-off was less iterative refinement. If we had found a requirements error after the build script ran, fixing it would require editing multiple already-generated files rather than simply updating a spec document before code generation.

---

## Part 4: Reflection and Takeaways

### 4.1 What was the most surprising or unexpected thing your group experienced while using agentic AI?

The most surprising thing was how much the AI functioned as a collaborator rather than a code dispenser. We expected to say "build this feature" and receive code. Instead, the AI consistently asked clarifying questions, presented options for human approval, and refused to generate code until the planning phase was complete. This felt counterintuitive at first — we wanted to move fast — but the result was a working application on the first build attempt, with all tests passing. We were also surprised by the volume of output: one structured prompt produced a complete, multi-file Flask application including templates, tests, and documentation. A task we estimated at 3–4 hours of manual work was scaffolded in minutes.

### 4.2 Did using AI make the work faster, slower, or situational? Explain.

Situational — and clearly so. The Execute phase (code generation) was dramatically faster: what would have taken hours of manual Flask boilerplate was produced in one AI turn. However, the Discuss and Plan phases required the same careful human thinking they always would — the AI did not speed up the process of deciding what to build, only the process of building it once we knew what we wanted. The Verify phase was also entirely human-paced: running the server, testing routes, and reviewing output took the same time regardless of how the code was generated. Overall, AI made the total project faster, but only because the slow parts (thinking, deciding, testing) remained human-led.

### 4.3 If you had to redo this project, what would you do differently when interacting with the AI?

We would separate Modules 4, 5, and 6 into distinct sessions, as the GSD Core framework intends. Compressing them saved tokens but reduced the quality of iterative spec review. Specifically, we would complete and review `requirements.md` before asking the AI to produce `architecture.md`, and review both before asking for any code. We would also write explicit acceptance criteria for each route before the Execute phase, so the AI's generated test cases could be directly compared against those criteria. Finally, we would ask the AI to generate one feature at a time (auth, then catalog, then members, etc.) rather than all at once, so that each module could be manually tested before the next was generated.

### 4.4 Key lessons your group took from this tutorial (at least 3 points)

1. **Specification quality determines output quality.** The AI produced correct, working code precisely because we specified exact field names, route behaviour, and business rules before generation. Vague prompts produce vague code. The investment in the Plan phase pays off in the Execute phase.

2. **Humans must own all decisions; AI executes only.** The GSD Core principle "AI generates, humans decide" is not just a slogan — it is a practical workflow requirement. Tech stack, feature scope, team assignments, and merge approvals all required human judgment. The AI's role was to convert those human decisions into correct, consistent code efficiently.

3. **Verification cannot be delegated to AI.** The AI could not confirm that its generated code actually ran. Manual testing — installing dependencies, starting the server, clicking through every route, running pytest — was essential and irreplaceable. Trusting AI output without verification is the primary way AI-assisted projects fail.

4. **Structured prompts with approved context produce dramatically better results than open-ended ones.** Our best AI interactions were those where we provided a complete, human-approved brief before asking for output. Our worst (most iterative, most correction-heavy) were early exploratory prompts that lacked agreed scope.

5. **Git Worktrees enable genuine parallel AI-assisted development.** Assigning each team member an isolated worktree branch meant four features could be developed simultaneously without merge conflicts or context confusion. This is a key enabling workflow for teams using AI coding agents at scale.

---

## Part 5: Group Self-Evaluation

| Aspect                                      | Score (1–5) | Brief Comment                                                                 |
|---------------------------------------------|-------------|-------------------------------------------------------------------------------|
| Quality of specifications before coding     | 4           | Covered all functional requirements; could have been more granular per route  |
| Ability to direct the AI effectively        | 4           | Learned mid-session that structured, approved prompts produce the best output |
| Ability to review and verify AI output      | 4           | All tests passed; manual browser testing confirmed all 6 features worked      |
| Collaboration and role distribution         | 5           | Git Worktree structure worked cleanly; each member had clear ownership        |
| Quality of the resulting code / system      | 4           | Full CRUD, role-based auth, and tests; lacks pagination and error pages (v2)  |

---

## Part 6: Appendix (Optional but Encouraged)

_Recommended additions for your submitted report:_

- Screenshots of the running system (login page, dashboard, book catalog, loans screen)
- Excerpts from `specs/project-brief.md` and `specs/requirements.md`
- Screenshot of the Cowork AI session showing the tech stack approval interaction
- pytest output showing all tests passing
- `git worktree list` output showing all four feature branches

---
*Report prepared by Group 1 PIMIS — Information System Development Tutorial*
*AI tool used: Claude (Cowork mode) — Anthropic*
