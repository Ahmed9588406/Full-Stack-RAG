from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
#from langchain_community.chat_models import ChatOllama  # Changed to Ollama
from langchain_ollama import ChatOllama
from operator import itemgetter
from decouple import config

from qdrant import vector_Store  # Import vector_Store instead of vector_store

# Initialize Ollama model instead of OpenAI
model = ChatOllama(
    model="deepseek-r1:1.5b",  # Use any model you've downloaded (e.g., "mistral", "llama3")
    temperature=0,
    # base_url="http://localhost:11434"  # Uncomment if using custom Ollama server
)

# Keep the same prompt template
prompt_template = """
Answer the question based on the context, in a concise manner, in markdown and using bullet points where applicable.

Context: {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)
retriever = vector_Store.as_retriever()

""""
question": RunnablePassthrough()

What it does :
Passes the user's original question through the pipeline unchanged.
Example :
The question "How does photosynthesis work?" stays exactly as-is.



RunnableParallel({
    "response": prompt | model,
    "context": itemgetter("context"),
})

What it does :
Runs two tasks in parallel :
Generate a response :
Combines the prompt (a template for the AI) with the retrieved context and the user's question.
Feeds this into the AI model to generate an answer.
Save the context :
Stores the retrieved documents (for debugging or transparency).

"""

def create_chain():
    chain = (
        {
            "context": retriever.with_config(top_k=4),
            "question": RunnablePassthrough(), 
        }
        | RunnableParallel({
            "response": prompt | model,
            "context": itemgetter("context"),
        })
    )
    return chain




def get_answer_and_docs(question: str):
    chain = create_chain()
    response = chain.invoke(question)
    answer = response["response"].content
    context = response["context"]
    return {
        "answer": answer,
        "context": context
    }


#response = get_answer_and_docs("Who is the author of the article?")
#print(response)

