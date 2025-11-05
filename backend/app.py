from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import events, facts, jokes, quiz, about # routers for events, facts, jokes, quiz and about

# === FastAPI app instance === #
app = FastAPI(
    title="CyberBot Backend API",
    description="API for managing club events and cybersecurity facts",
    version="1.0.0"
)

# === Middleware === #
# Allow the bot and local testing to access the API
origins = [
    "http://localhost",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# === Include Routers === #
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(facts.router, prefix="/facts", tags=["CyberFacts"])
app.include_router(jokes.router, prefix="/jokes", tags=["CyberJokes"])
app.include_router(quiz.router, prefix="/quiz", tags=["CyberQuiz"])
app.include_router(about.router, prefix="/about", tags=["About-us"])

