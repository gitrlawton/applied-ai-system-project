## Goals

- Extend and redesign a prior mini-project into a cohesive, end-to-end AI integrated system.
- Implement modular components (retrieval, logic, or agentic planning) using Python.
- Test and evaluate system reliability and guardrails through structured experiments.
- Document and explain the AI's decision-making process clearly and responsibly.
- Communicate results through a professional presentation and portfolio entry.

## Extension Idea Added AI Components:

| Extension Idea                                                              | Added AI Components          |
| --------------------------------------------------------------------------- | ---------------------------- |
| Add retrieval of external documentation and automated validation of answers | RAG + testing + guardrails   |
| Integrate agentic planning and error-logging into the existing workflow     | Agentic loop + logging       |
| Extend explanation module with bias detection and evaluation metrics        | RAG + validation             |
| Add reliability scoring or self-critique loop                               | Testing + confidence scoring |

---

## 1. Functionality: What Your System Should Do

Your project should **do something useful with AI**. For example:

- Summarize text or documents
- Retrieve information or data from a source
- Plan and complete a step-by-step task
- Help debug, classify, or explain something

To make your project more advanced, it must include **at least one** of the following AI features:

| Feature                                  | What It Means                                                        | Example                                                                   |
| ---------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Retrieval-Augmented Generation (RAG)** | Your AI looks up or retrieves information before answering.          | A study bot that searches notes before generating a quiz question.        |
| **Agentic Workflow**                     | Your AI can plan, act, and check its own work.                       | A coding assistant that writes, tests, and then fixes code automatically. |
| **Fine-Tuned or Specialized Model**      | You use a model that's been trained or adjusted for a specific task. | A chatbot tuned to respond in a company's tone of voice.                  |
| **Reliability or Testing System**        | You include ways to measure or test how well your AI performs.       | A script that checks if your AI gives consistent answers.                 |

The feature should be fully integrated into the main application logic. It is not enough to have a standalone script; the feature must meaningfully change how the system behaves or processes information. For example, if you add RAG, your AI should actively use the retrieved data to formulate its response rather than just printing the data alongside a standard answer.

Also, make sure your project:

- **Runs correctly and reproducibly:** If someone follows your instructions, it should work.
- **Includes logging or guardrails:** Your code should track what it does and handle errors safely.
- **Has clear setup steps:** Someone else should be able to run it without guessing what to install.

---

## 2. Design and Architecture: How Your System Fits Together

Show how your project is organized by creating a short **system diagram**. Your diagram should include:

- The **main components** (like retriever, agent, evaluator, or tester).
- How **data flows** through the system (input → process → output).
- Where **humans or testing** are involved in checking AI results.

---

## 3. Documentation: How You Explain Your Work

You'll write a **README file** that clearly explains your project. It should include:

- Explicitly name your original project (from Modules 1-3) and provide a 2-3 sentence summary of its original goals and capabilities.
- **Title and Summary:** What your project does and why it matters.
- **Architecture Overview:** A short explanation of your system diagram.
- **Setup Instructions:** Step-by-step directions to run your code.
- **Sample Interactions:** Include at least 2-3 examples of inputs and the resulting AI outputs to demonstrate the system is functional.
- **Design Decisions:** Why you built it this way, and what trade-offs you made.
- **Testing Summary:** What worked, what didn't, and what you learned.
- **Reflection:** What this project taught you about AI and problem-solving.

Write this for a future employer who might look at your GitHub portfolio! Clarity and completeness matter more than perfection.

---

## 4. Reliability and Evaluation: How You Test and Improve Your AI

Your AI should **prove that it works**, not just seem like it does. Include **at least one way** to test or measure its reliability, such as:

- Automated tests (e.g., unit tests or simple checks for key functions).
- Confidence scoring (the AI rates how sure it is).
- Logging and error handling (your code records what failed and why).
- Human evaluation (you or a peer review the AI's output).

Summarize your testing in a few lines, like:

> 5 out of 6 tests passed; the AI struggled when context was missing. Confidence scores averaged 0.8; accuracy improved after adding validation rules.

---

## 5. Reflection and Ethics: Thinking Critically About Your AI

AI isn't just about what works -- it's about what's responsible. Include a short reflection answering the following questions:

- What are the limitations or biases in your system?
- Could your AI be misused, and how would you prevent that?
- What surprised you while testing your AI's reliability?
- Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.

---

## 🚀 Optional: Stretch Features for Extra Points

These features are **completely optional** and go beyond the required 21 points. Completing them can earn up to **+8 additional points**, allowing your score to exceed 100%. See the [Grading Rubric] for how each is evaluated.

| Feature                               | What To Build                                                                                                                                                         | Points |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| **RAG Enhancement**                   | Extend your retrieval system to use custom documents or multiple data sources. Show how it measurably improves your AI's output quality.                              | +2     |
| **Agentic Workflow Enhancement**      | Implement multi-step reasoning with observable intermediate steps — tool-calls, planning steps, or a decision-making chain.                                           | +2     |
| **Fine-Tuning or Specialization**     | Demonstrate specialized model behavior using few-shot patterns, synthetic datasets, or constrained tone/style. Show that output measurably differs from the baseline. | +2     |
| **Test Harness or Evaluation Script** | Build a script that runs your system on a set of predefined inputs and prints a summary (pass/fail scores, confidence ratings, or similar).                           | +2     |

> **Note:** These stretch features build directly on the required AI feature you chose in Step 1. For example, if you added RAG as your required feature, the RAG Enhancement stretch would extend that same component further.
