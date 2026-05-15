# FlyTripper MAS ✈️

An AI-powered travel itinerary planner built with a custom multi-agent system using LangChain and Google Gemini — no CrewAI. A pipeline of specialized agents researches, plans, optimizes, and quality-checks your trip, then outputs a day-by-day itinerary you can download as a `.ics` calendar file.

---

## What it does

- Generates day-by-day travel itineraries for any destination using a custom LangChain multi-agent pipeline
- Supports optional user preferences (e.g. "prefer museums over nightlife, budget-friendly")
- Exports the final itinerary as a downloadable `.ics` calendar file
- Exposes a FastAPI backend with three endpoints: itinerary (JSON), itinerary (ICS), and chat
- Includes a conversational `ReactiveAgent` with web search, Wikipedia, calculator, and datetime tools
- Provides a Streamlit UI with live pipeline progress via a status container

---

## How this differs from FlyTripper (CrewAI version)

| | FlyTripper-mas (this repo) | FlyTripper |
|---|---|---|
| Agent framework | Custom LangChain agents | CrewAI (`Crew`, `Task`, `Process`) |
| LLM format | LangChain `ChatGoogleGenerativeAI` | LiteLLM `gemini/gemini-*` format for CrewAI |
| API version | `v2.0.0` | `v3.0.0` |
| `/chat` endpoint | Synchronous (`reactive_agent.run()`) | Async (`await reactive_agent.run()`) |
| Config | Root-level `config.py` (no `app/config.py`) | `app/config.py` with `CREWAI_LLM_MODEL` |
| Caption | "multi-agent AI pipeline" | "CrewAI + Gemini" |

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini (`gemini-2.5-flash` via LangChain) |
| Multi-agent | Custom LangChain agent pipeline |
| API | FastAPI + Uvicorn |
| UI | Streamlit |
| Orchestration | LangChain (`ChatGoogleGenerativeAI`) |
| Config | `python-dotenv` |
| Package manager | `uv` |

---

## Project Structure

```
FlyTripper-mas/
├── app/
│   ├── agents/
│   │   ├── researcher.py
│   │   ├── planner.py
│   │   ├── optimizer.py
│   │   ├── qa.py
│   │   └── reactive.py
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   └── travel_orchestrator.py
│   └── __init__.py
├── main.py
├── streamlit_app.py
├── pyproject.toml
├── uv.lock
└── .gitignore
```

---

## File Explanations

### `main.py`
The FastAPI application entrypoint (version `2.0.0`). Defines three endpoints: `GET /` (health check), `POST /itinerary` (returns a JSON itinerary via the multi-agent pipeline), and `POST /itinerary/ics` (returns the itinerary as a downloadable `.ics` calendar file). Also exposes `POST /chat` which routes messages to the `ReactiveAgent` **synchronously** — unlike the CrewAI version, `reactive_agent.run()` is called directly without `await`. Initializes `TravelOrchestrator` and `ReactiveAgent` as module-level singletons. Run with:

```bash
uv run uvicorn main:app --reload
```

### `streamlit_app.py`
The Streamlit UI entrypoint. Renders destination input, day count, and preferences fields. On submit, creates a `TravelOrchestrator` with an `on_stage` callback that updates a live status container as each agent in the pipeline runs. Displays the final itinerary as markdown and provides a download button for the `.ics` file. Unlike the CrewAI version, the caption reads "multi-agent AI pipeline" with no mention of CrewAI. Run with:

```bash
uv run streamlit run streamlit_app.py
```

### `app/orchestrator/travel_orchestrator.py`
The core multi-agent pipeline. Wires together four LangChain-based agents in sequence: Researcher → Planner → Optimizer → QA. Accepts an optional `on_stage` callback so the UI can display live progress updates as each agent completes. Returns an `ItineraryResult` dataclass containing the destination, number of days, final itinerary text, and `.ics` bytes.

### `app/agents/researcher.py`
The Researcher agent. Uses web search (SerpAPI) to gather up-to-date travel information for the destination — attractions, hotels, restaurants, and transport tips. Returns a structured research summary without creating an itinerary.

### `app/agents/planner.py`
The Planner agent. Takes the Researcher's output and produces a day-by-day itinerary with morning, afternoon, and evening activities. Groups nearby attractions to minimize travel time and respects the requested number of days.

### `app/agents/optimizer.py`
The Optimizer agent. Refines the Planner's draft itinerary for efficiency and user preferences — removes overpacked days, adds local hidden gems, and improves logical sequencing.

### `app/agents/qa.py`
The QA agent. Validates the Optimizer's output for factual accuracy, consistency, and clarity — removes hallucinations, rewrites vague entries, and confirms each day is realistic before passing the final plan back to the orchestrator.

### `app/agents/reactive.py`
The `ReactiveAgent` — a standalone conversational LangChain ReAct agent separate from the itinerary pipeline. Handles general travel questions via the `/chat` endpoint using tools for web search, Wikipedia, calculator, and datetime. Runs **synchronously** in this version (no `async`/`await`).

### `pyproject.toml`
Project configuration for `uv`. Defines the package name, Python version, and all dependencies. Use `uv sync` to install everything.

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/dumpty-420/FlyTripper-mas.git
cd FlyTripper-mas
```

### 2. Install dependencies

```bash
pip install uv
uv sync
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
SERP_API_KEY=your_serpapi_key
```

Get your keys from:
- Google API key: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- SerpAPI key: [https://serpapi.com](https://serpapi.com)

### 4. Run the Streamlit UI

```bash
uv run streamlit run streamlit_app.py
```

### 5. Or run the FastAPI backend

```bash
uv run uvicorn main:app --reload
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## How It Works

FlyTripper MAS uses a **sequential custom multi-agent pipeline** built with LangChain:

1. **Researcher** — searches the web via SerpAPI for up-to-date information about the destination
2. **Planner** — transforms research into a structured day-by-day itinerary
3. **Optimizer** — refines the plan for efficiency, user preferences, and realistic timings
4. **QA Agent** — validates the final plan for accuracy and clarity, removing hallucinations
5. **ICS Export** — converts the verified itinerary into a `.ics` calendar file for download

The Streamlit UI shows live progress as each agent completes via a status container. The FastAPI backend exposes the same pipeline as REST endpoints.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/itinerary` | Generate itinerary (JSON) |
| `POST` | `/itinerary/ics` | Generate itinerary (`.ics` download) |
| `POST` | `/chat` | Chat with the ReAct agent |

---

## Notes

- The `.env` file is gitignored — never commit your API keys
- If you hit Gemini quota limits (`429 RESOURCE_EXHAUSTED`), wait a few minutes or switch to `gemini-1.5-flash` in `config.py`
- The `/chat` endpoint is synchronous in this version — if you need async chat, see the [FlyTripper CrewAI version](https://github.com/dumpty-420/FlyTripper)

---

## Author

Built by [Seerat Chugh](https://github.com/dumpty-420)
