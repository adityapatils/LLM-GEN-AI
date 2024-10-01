
from flask import Flask, request, jsonify
from phi.assistant import Assistant
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.llm.groq import Groq

app = Flask(__name__)

# Set up the knowledge base
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],  # PDF URL
    vector_db=PgVector2(
        collection="recipes",
        db_url="postgresql+psycopg2://main_owner:xxxxxxx@ep-xxx-xxx-xxxx.eu-central-1.aws.neonsslmode=require",  # PostgreSQL connection string
    ),
)
knowledge_base.load(recreate=False)

# Initialize the Assistant
assistant = Assistant(
    knowledge_base=knowledge_base,
    add_references_to_prompt=True,
    llm=Groq(model="llama-3.1-70b-versatile"),
)

@app.route('/', methods=['POST'])
def ask_assistant():
    data = request.json
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    response = assistant.run(question, stream=False)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)