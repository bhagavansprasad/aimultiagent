from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import GenerationConfig
from backend.config import Config
import json
import logging
   
def prompt_llm(prompt):
    gemini_model = Config.GEMINI_MODEL

    model = GenerativeModel(gemini_model)
    gen_config = GenerationConfig(temperature=0.1)
    response = model.generate_content(prompt, generation_config=gen_config)
    
    return response

def repharsed_queries(original_query):
    # original_query = "common questions people have about millet consumption and provide me the answers"

    prompt = f"""
    ### You are a strict assistant. You must only answer using the provided context.
    
    ### Context
    Rephrase the following query into 5 more specific questions: 
    
    ### Query
    {original_query}
    
    ### Rules: 
    1. Do not add any information not present in the context.
    2. Just rephrase the given query    
    3. Be very specific and short, just point to the question
    4. Do not repeate
    5. No numbering
    
    ### Answer:
    """
    
    logging.debug(f"Generating similar questions to :{original_query}")
    response = prompt_llm([prompt])
    
    reply = f"""{response.text}""".split('\n')
    new_queries = []
    for q in reply:
        q = q.strip()
        if (len(q) > 0):
            new_queries.append(q)
    # print(f"new_queries :{new_queries}")
    return new_queries
