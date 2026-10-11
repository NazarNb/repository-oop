from google.adk.agents.workflow_agent import WorkflowAgent
from google.adk.agents.llm_agent import Agent

# Окремий агент-аналітик, який буде частиною воркфлоу
analyst = Agent(
    model='gemini-1.5-flash',
    name='Analyst',
    instruction="Аналізуй дані та пиши короткі звіти."
)

workflow_agent = WorkflowAgent(
    model='gemini-1.5-flash',
    name='StudyWorkflow',
    description="Комбінований Workflow для навчання."
)

@workflow_agent.task
async def collect_data(context):
    # ПАРАЛЕЛЬНИЙ ТИП: імітуємо збір з різних джерел
    print("Збір даних...")
    return {
        "math_grades": [10, 8, 12],
        "it_grades": [12, 11, 12],
        "attendance": "95%"
    }

@workflow_agent.task
async def analyze_and_report(context, data):
    # ПОСЛІДОВНИЙ ТИП: обробка -> аналіз
    report = await analyst.ask(f"Склади звіт на основі цих даних: {data}")
    return report

@workflow_agent.task
async def improve_loop(context, report):
    # ТИП LOOP: покращення звіту (спрощено)
    feedback = "Додай більше порад для IT предметів."
    final_version = await analyst.ask(f"Це початковий звіт: {report}. Покращ його, враховуючи це: {feedback}")
    return final_version

# Визначаємо саму структуру Workflow
@workflow_agent.main
async def run_study_flow(context):
    # 1. Parallel (збір)
    data = await collect_data(context)
    
    # 2. Sequential (аналіз)
    initial_report = await analyze_and_report(context, data)
    
    # 3. Loop (покращення)
    final_report = await improve_loop(context, initial_report)
    
    return final_report

root_agent = workflow_agent