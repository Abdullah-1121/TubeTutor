from crewai import Agent, Crew, Process, Task , LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool
from dotenv import load_dotenv
from researcher_flow.tool import Transcript_getter
import yaml
import os
import litellm

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

# API KEYS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ.pop("OPENAI_API_KEY", None)
llm = LLM(model='gemini/gemini-1.5-flash', api_key=GEMINI_API_KEY)

# Load YAML configurations
agents_config_path = os.path.join(CONFIG_DIR, 'agents.yaml')
tasks_config_path = os.path.join(CONFIG_DIR, 'tasks.yaml')

with open(agents_config_path, 'r') as f:
    agents_config = yaml.safe_load(f)

with open(tasks_config_path, 'r') as f:
    tasks_config = yaml.safe_load(f)

# Tools
web_search_tool = SerperDevTool()
transcript_tool = Transcript_getter()

@CrewBase
class LessonPlanner:
    """LessonPlanner crew"""

    model = 'gemini/gemini-1.5-flash'

    @agent
    def Transcript_Extractor(self) -> Agent:
        return Agent(
            config=agents_config['video_content_extraction_agent'],
            tools=[transcript_tool],
            verbose=True,
            llm=llm
        )
    
    @agent
    def lesson_generator_agent(self) -> Agent:
        return Agent(
            config=agents_config['lesson_generator_agent'],
            verbose=True,
            llm=llm
        )

    @agent
    def key_points_extractor_agent(self) -> Agent:
        return Agent(
            config=agents_config['key_points_extractor_agent'],
            verbose=True,
            allow_code_execution=False,
            llm=llm
        )

    @agent
    def summary_generator_agent(self) -> Agent:
        return Agent(
            config=agents_config['summary_generator_agent'],
            verbose=True,
            llm=llm
        )
    @agent
    def quiz_generator_agent(self) -> Agent:
        return Agent(
            config=agents_config['quiz_generator_agent'],
            verbose=True,
            llm=llm
        )
    @agent
    def chapter_compiler_agent(self) -> Agent:
        return Agent(
            config=agents_config['chapter_compiler_agent'],
            verbose=True,
            llm=llm
        )
    @task
    def extract_video_content(self) -> Task:
        return Task(
            config=tasks_config['extract_video_content'],
            agent=self.Transcript_Extractor()  # Reference the method directly
        )

    @task
    def generate_lesson(self) -> Task:
        return Task(
            config=tasks_config['generate_lesson'],
            agent=self.lesson_generator_agent()  # Assign an agent
        )
    @task
    def extract_key_points(self) -> Task:
        return Task(
            config=tasks_config['extract_key_points'],
            agent=self.key_points_extractor_agent()  # Assign an agent
        )
    
    @task
    def generate_summary(self) -> Task:
        return Task(
            config=tasks_config['generate_summary'],
            agent=self.summary_generator_agent() # Assign an agent
        )

    @task
    def generate_quiz(self) -> Task:
        return Task(
            config=tasks_config['generate_quiz'],
            agent=self.quiz_generator_agent(), # Assign an agent
            
        )
    @task
    def compile_chapter(self) -> Task:
        return Task(
            config=tasks_config['compile_chapter'],
            agent=self.chapter_compiler_agent(), # Assign an agent
            
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MarketResearcher crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=False
        )



