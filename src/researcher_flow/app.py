from fastapi import FastAPI
import uvicorn
from researcher_flow.crew import LessonPlanner
from pydantic import BaseModel
from fastapi.responses import JSONResponse
app = FastAPI()
class RequestState(BaseModel):
    video_id : str
@app.post("/get_lesson")
def get_lesson(query : RequestState):
    result = LessonPlanner().crew().kickoff(inputs=query.model_dump())
    print(type(result))
    print ('result : ' , result)
    print(type(str(result)))
    return JSONResponse(content={"Lesson": str(result)})
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)