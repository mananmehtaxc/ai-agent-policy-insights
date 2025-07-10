from langchain.llms import huggingface_hub
from langchain_core.prompts import PromptTemplate   
from langchain.chains import LLMChain

#load prompt template from prompt/summarize_prompt.txt
with open('prompt/summarize_prompt.txt', 'r') as file:
    summarize_prompt = file.read()

# Initialize the prompt template
prompt_template = PromptTemplate(
    input_variables=["text"],
    template=summarize_prompt
)

# Initialize the LLM with the Hugging Face model
llm = huggingface_hub.HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct",
    model_kwargs={"temperature": 0.1, "max_new_tokens": 2048}
)
# Initialize the LLMChain with the prompt template and LLM
summarize_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    verbose=True
)   

def summarize_text(text: str) -> str:
    """
    Summarize the given text using the LLMChain.
    
    :param text: The text to be summarized.
    :return: The summary of the text.
    """
    # Run the LLMChain with the provided text
    summary = summarize_chain.run(text=text)
    return summary
