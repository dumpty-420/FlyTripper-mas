"""
FlyTripper API — FastAPI entrypoint for the multi-agent travel planner.

Endpoints
---------
GET  /               Health check
POST /itinerary      Generate a day-by-day travel itinerary (JSON)
POST /itinerary/ics  Generate and download an .ics calendar file
POST /chat           Chat with the ReAct conversational agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.orchestrator import TravelOrchestrator
from app.agents.reactive import ReactiveAgent

# ────────────────────────────── App ──────────────────────────────────
app = FastAPI(
    title="FlyTripper API",
    description=(
        "AI-powered travel itinerary planner using a multi-agent "
        "architecture with Gemini + LangChain 🚀"
    ),
    version="2.0.0",
)


# ────────────────────────────── Models ───────────────────────────────
class ItineraryRequest(BaseModel):
    destination: str = Field(..., description="Travel destination", examples=["Paris"])
    num_days: int = Field(
        ..., ge=1, le=30, description="Number of travel days", examples=[7]
    )
    preferences: str = Field(
        "", description="Optional preferences", examples=["prefer museums over nightlife"]
    )


class ItineraryResponse(BaseModel):
    destination: str
    num_days: int
    itinerary: str


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message", examples=["What is the capital of France?"])


class ChatResponse(BaseModel):
    response: str


# ────────────────────────── Singletons ───────────────────────────────
orchestrator = TravelOrchestrator()
reactive_agent = ReactiveAgent(verbose=True)


# ────────────────────────────── Routes ───────────────────────────────
@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "FlyTripper API", "version": "2.0.0"}


@app.post("/itinerary", response_model=ItineraryResponse, tags=["Itinerary"])
async def generate_itinerary(request: ItineraryRequest):
    """Generate a day-by-day travel itinerary using the multi-agent pipeline."""
    try:
        result = orchestrator.run(
            destination=request.destination,
            num_days=request.num_days,
            preferences=request.preferences,
        )
        return ItineraryResponse(
            destination=result.destination,
            num_days=result.num_days,
            itinerary=result.itinerary,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/itinerary/ics", tags=["Itinerary"])
async def generate_itinerary_ics(request: ItineraryRequest):
    """Generate a travel itinerary and return it as a downloadable .ics file."""
    try:
        result = orchestrator.run(
            destination=request.destination,
            num_days=request.num_days,
            preferences=request.preferences,
        )
        return Response(
            content=result.ics_bytes,
            media_type="text/calendar",
            headers={
                "Content-Disposition": 'attachment; filename="travel_itinerary.ics"'
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """Chat with the ReAct conversational agent (web search, Wikipedia, calculator, datetime)."""
    try:
        response = reactive_agent.run(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
