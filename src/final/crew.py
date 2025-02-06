from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectorySearchTool
from crewai_tools import DirectoryReadTool,FileReadTool

#tool=DirectorySearchTool(directory='C:/Users/user/Downloads/Project/final/KB Article')
"""
tool = DirectorySearchTool(
	config=dict(
		llm=dict(
			provider="google",
			config=dict(
				model="gemini-1.5-flash"
			),
		),
		embedder=dict(
			provider="google",
			config=dict(
				model="models/text-embedding-004",
				task_type="RETRIEVAL_DOCUMENT"
			),
		),
	)
)
"""
'''
llm = LLM(
	model="gemini/gemini-1.5-flash",
	google_api_key="AIzaSyB14nLyS0Wa-yFaRPAjBK0egCRTYfFhKTw"
)
'''

import panel as pn

chat_interface = pn.chat.ChatInterface()

from crewai.tasks.task_output import TaskOutput

def print_output(output: TaskOutput):

    message = output.raw
    #chat_interface.send(message, user=output.agent, respond=False)


tool = DirectoryReadTool(directory='C:/Users/user/Downloads/Project/Ticket Helper/documents',
						 result_as_answer=True
						 )

ReadTool = FileReadTool()
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Final():
	"""Final crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['analyst'],
			#llm=llm,
			verbose=True
		)

	@agent
	def searcher(self) -> Agent:
		return Agent(
			config=self.agents_config['searcher'],
			#llm=llm,
			tools=[tool],
			verbose=True
		)
	
	@agent
	def report(self) -> Agent:
		return Agent(
            config=self.agents_config['report'],
			#llm=llm,
			tools=[ReadTool],
            verbose=True,
        )

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	
	@task
	def analyst_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyst_task'],
		)

	@task
	def searcher_task(self) -> Task:
		return Task(
			config=self.tasks_config['searcher_task'],
			#output_file='report.txt'
		)
	
	@task
	def report_task(self) -> Task:
		return Task(
            config=self.tasks_config['report_task'],
            output_file='report.txt',
			callback=print_output,
			human_input=True
        )

	@crew
	def crew(self) -> Crew:
		"""Creates the Final crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
