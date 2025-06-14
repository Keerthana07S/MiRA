#import libraries and dependencies
from google.adk.agents import LlmAgent #used to create LLM agents
import os #used for google API key

os.environ["GOOGLE_API_KEY"] = "INSERT API KEY" #set google API key
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash" #model used for LLM agents

class LLMAgents:
    def __init__(self, prompt: str, question_init: str, question_next: str):
        self.prompt = prompt #response to question asked
        self.question_init = question_init #question asked
        self.question_next = question_next #next question to be asked
        
    #generative agent
    def response_agent(self, prompt, question_init, question_next):
        return LlmAgent(
            name="InitialWriterAgent",
            model=MODEL_GEMINI_2_0_FLASH,
            description="Provides a response to the answer to the initial question, and follows up with the second question",
            instruction=f'''Write a response to the following answer: {prompt} that was a response to the question: {question_init}.
            Then, follow up with the question: {question_next}'''
        )
            
    #empathy agent
    def empathy_agent(self, initial_writer_response):
        return LlmAgent(
            name="EmpathyAgent",
            model=MODEL_GEMINI_2_0_FLASH,
            description="Provides an empathetic response to the initial writer's response",
            instruction=f'''Rewrite the following answer in a more empathetic way{initial_writer_response}. Keep in mind individuals you are writing this
            to have most likely experienced homelessness, trauma, and other hardships. Additionally, the response should be rewritten in a way that is easy to understand and not overly complex.'''
        )
