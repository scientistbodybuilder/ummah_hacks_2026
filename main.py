from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.shariahengine import check_shariah_compliance, ShariaCheckRequest, ShariaCheckResponse

app = FastAPI(title="Shariah Compliance API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "shariah-compliance-api"}


@app.post("/api/shariah-check", response_model=ShariaCheckResponse)
async def shariah_check_endpoint(request: ShariaCheckRequest):
    """
    Main endpoint for checking Shariah compliance of financial products.
    """
    return await check_shariah_compliance(request)
