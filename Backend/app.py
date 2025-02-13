from fastapi import FastAPI
import uvicorn
import router

app = FastAPI(title="Router Chains")

route = router.Router()

@app.get("/query", tags=["Query Input"])
def getResponse(input_query: str):  
    response = route.runrouters(input_query)
    return {"Response": response}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info", reload=True)