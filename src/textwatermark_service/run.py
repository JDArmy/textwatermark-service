"""uvicorn runner"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "textwatermark_service.main:app", host="127.0.0.1", port=8000, reload=True
    )
