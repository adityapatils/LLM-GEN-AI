from phi.assistant import Assistant
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.llm.groq import Groq

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],  # PDF URL
    vector_db=PgVector2(
        collection="recipes",
        db_url="postgresql+psycopg2://main_owner:xxxxxxx@ep-xxx-xxx-xxxx.eu-central-1.aws.n?sslmode=require",  # PostgreSQL connection string
    ),
)
knowledge_base.load(recreate=False)

assistant = Assistant(
    knowledge_base=knowledge_base,
    add_references_to_prompt=True,
    llm=Groq(model="llama-3.1-70b-versatile"),
)
assistant.print_response("This Document what about?", markdown=True)