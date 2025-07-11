import os
from hipporag import HippoRAG

# 通过环境变量传递密钥（安全推荐）
os.environ['OPENAI_API_KEY'] ='sk-izwzkvgrlfqhkcsxdhgrsylzskdkcnvcwxiqdtqrfvryqmwp'
# Prepare datasets and evaluation
docs = [
    "Oliver Badman is a politician.",
    "George Rankin is a politician.",
    "Thomas Marwick is a politician.",
    "Cinderella attended the royal ball.",
    "The prince used the lost glass slipper to search the kingdom.",
    "When the slipper fit perfectly, Cinderella was reunited with the prince.",
    "Erik Hort's birthplace is Montebello.",
    "Marina is bom in Minsk.",
    "Montebello is a part of Rockland County."
]

save_dir = 'outputs'# Define save directory for HippoRAG objects (each LLM/Embedding model combination will create a new subdirectory)
llm_model_name = 'deepseek-ai/DeepSeek-R1-0528-Qwen3-8B' # Any OpenAI model name
embedding_model_name = 'BAAI/bge-m3'# Embedding model name (NV-Embed, GritLM or Contriever for now)
# OPENAI_API_KEY='sk-izwzkvgrlfqhkcsxdhgrsylzskdkcnvcwxiqdtqrfvryqmwp'
llm_base_url='https://api.siliconflow.cn/v1'
embedding_base_url='https://api.siliconflow.cn/v1'

#Startup a HippoRAG instance
hipporag = HippoRAG(save_dir=save_dir,
                    llm_model_name=llm_model_name,
                    llm_base_url=llm_base_url,
                    embedding_model_name=embedding_model_name,  
                    embedding_base_url=embedding_base_url 
                    ) 

#Run indexing
hipporag.index(docs=docs)

#Separate Retrieval & QA
queries = [
    "What is George Rankin's occupation?",
    "How did Cinderella reach her happy ending?",
    "What county is Erik Hort's birthplace a part of?"
]

retrieval_results = hipporag.retrieve(queries=queries, num_to_retrieve=2)
qa_results = hipporag.rag_qa(retrieval_results)

#Combined Retrieval & QA
rag_results = hipporag.rag_qa(queries=queries)

#For Evaluation
answers = [
    ["Politician"],
    ["By going to the ball."],
    ["Rockland County"]
]

gold_docs = [
    ["George Rankin is a politician."],
    ["Cinderella attended the royal ball.",
    "The prince used the lost glass slipper to search the kingdom.",
    "When the slipper fit perfectly, Cinderella was reunited with the prince."],
    ["Erik Hort's birthplace is Montebello.",
    "Montebello is a part of Rockland County."]
]

rag_results = hipporag.rag_qa(queries=queries, 
                              gold_docs=gold_docs,
                              gold_answers=answers)
