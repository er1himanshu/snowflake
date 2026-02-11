"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from pathlib import Path
from api.routes import router
from config import HOST, PORT, DEBUG, FRONTEND_DIR

# Create FastAPI app
app = FastAPI(
    title="Snowflake - AI Policy Impact Simulator",
    description="Predictive governance platform for policy impact analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["simulation"])

# Serve frontend static files
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the main frontend page"""
        index_path = FRONTEND_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return {"message": "Frontend not found. Please check frontend directory."}
else:
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "Snowflake AI Policy Impact Simulator API",
            "version": "1.0.0",
            "docs": "/api/docs",
            "api_prefix": "/api"
        }


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    print("🚀 Starting Snowflake AI Policy Impact Simulator...")
    print("📊 Loading ML models...")
    
    # Pre-load models
    from models.inflation_model import get_inflation_model
    from models.sector_impact_model import get_sector_model
    from models.sentiment_model import get_sentiment_model
    from models.risk_index_model import get_risk_model
    
    try:
        inflation_model = get_inflation_model()
        print("✅ Inflation model loaded")
        
        sector_model = get_sector_model()
        print("✅ Sector impact model loaded")
        
        sentiment_model = get_sentiment_model()
        print("✅ Sentiment analysis model loaded")
        
        risk_model = get_risk_model()
        print("✅ Risk index model loaded")
        
        print(f"🌐 Server running on http://{HOST}:{PORT}")
        print(f"📚 API docs available at http://{HOST}:{PORT}/api/docs")
        
    except Exception as e:
        print(f"⚠️  Error loading models: {e}")
        print("Models will be loaded on first request.")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down Snowflake AI Policy Impact Simulator...")


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
