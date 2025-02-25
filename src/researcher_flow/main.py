from crewai.flow.flow import Flow, start, listen
from litellm import completion
from dotenv import load_dotenv
from researcher_flow.crew import LessonPlanner
from IPython.display import display, Markdown
from rich.console import Console
from rich.markdown import Markdown
import uvicorn
from researcher_flow.app import app
load_dotenv()


ins = {
    'video_id': 'qYNweeDHiyU',
    
}

def kickoff():
    result = LessonPlanner().crew().kickoff(inputs=ins)
    result_str = str(result)
    # console = Console()
    # console.print(Markdown(result.raw))
    # Define the file name
    output_file = "Chapter.md"

    # Write the result to the Markdown file
    with open(output_file, "w", encoding="utf-8") as file:
      
        file.write(result_str)
        file.write("\n```\n")  # End code block

    print(f"✅ Markdown output saved to {output_file}!")

def train():
    LessonPlanner().crew().train(n_iterations=1, filename='training.pkl' , inputs = ins)
def plot():
    # prompt_chaining_flow = TopicOutlineFlow()
    # prompt_chaining_flow.plot()
    result = LessonPlanner()
    
    result.plot()

def test():
    Planner = LessonPlanner()
    print(type(LessonPlanner)) # <class 'type'>
    print(type(LessonPlanner().crew())) # <class 'function'>
    print(type(Planner)) #<class 'crewai.project.crew_base.CrewBase(LessonPlanner)'>
    print(type(Planner.crew)) # <class 'method'>

def run():
    uvicorn.run(app, host='127.0.0.1', port=8000)    

if __name__ == "__main__":
    kickoff()
    plot()
    test()
    run()