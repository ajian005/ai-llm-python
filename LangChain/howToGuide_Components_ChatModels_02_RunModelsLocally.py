"""
  Run models locally : https://python.langchain.com/docs/how_to/local_llms/
"""

''' Ollama ''' 
# ollama pull llama3.1:8b
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3.1:8b")
llm.invoke("The first man on the moon was ...")
for chunk in llm.stream("The first man on the moon was ..."):
    print(chunk, end="|", flush=True)


from langchain_ollama import ChatOllama
chat_model = ChatOllama(model="llama3.1:8b")
chat_model.invoke("Who was the first man on the moon?")



''' Llama.cpp ''' 
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

llm = LlamaCpp(
    model_path="/Users/rlm/Desktop/Code/llama.cpp/models/openorca-platypus2-13b.gguf.q4_0.bin",
    n_gpu_layers=1,
    n_batch=512,
    n_ctx=2048,
    f16_kv=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    verbose=True,
)
llm.invoke("The first man on the moon was ... Let's think step by step")



''' GPT4All ''' 
from langchain_community.llms import GPT4All

llm = GPT4All(
    model="/Users/rlm/Desktop/Code/gpt4all/models/nous-hermes-13b.ggmlv3.q4_0.bin"
)
llm.invoke("The first man on the moon was ... Let's think step by step")


''' llamafile ''' 
# Download a llamafile from HuggingFace
# Download a llamafile from HuggingFace
# wget https://huggingface.co/jartine/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile

# Make the file executable
# Make the file executable. On Windows, instead just rename the file to end in ".exe".
# chmod +x TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile

# Run the file
# Start the model server. Listens at http://localhost:8080 by default.
# ./TinyLlama-1.1B-Chat-v1.0.Q5_K_M.llamafile --server --nobrowser

from langchain_community.llms.llamafile import Llamafile

llm = Llamafile()

llm.invoke("The first man on the moon was ... Let's think step by step.")


""" ==========Prompts=========================================================== """
# Set our LLM
llm = LlamaCpp(
    model_path="/Users/rlm/Desktop/Code/llama.cpp/models/openorca-platypus2-13b.gguf.q4_0.bin",
    n_gpu_layers=1,
    n_batch=512,
    n_ctx=2048,
    f16_kv=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    verbose=True,
)

from langchain.chains.prompt_selector import ConditionalPromptSelector
from langchain_core.prompts import PromptTemplate

DEFAULT_LLAMA_SEARCH_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""<<SYS>> \n You are an assistant tasked with improving Google search \
results. \n <</SYS>> \n\n [INST] Generate THREE Google search queries that \
are similar to this question. The output should be a numbered list of questions \
and each should have a question mark at the end: \n\n {question} [/INST]""",
)

DEFAULT_SEARCH_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an assistant tasked with improving Google search \
results. Generate THREE Google search queries that are similar to \
this question. The output should be a numbered list of questions and each \
should have a question mark at the end: {question}""",
)

QUESTION_PROMPT_SELECTOR = ConditionalPromptSelector(
    default_prompt=DEFAULT_SEARCH_PROMPT,
    conditionals=[(lambda llm: isinstance(llm, LlamaCpp), DEFAULT_LLAMA_SEARCH_PROMPT)],
)

prompt = QUESTION_PROMPT_SELECTOR.get_prompt(llm)

# Chain
chain = prompt | llm
question = "What NFL team won the Super Bowl in the year that Justin Bieber was born?"
chain.invoke({"question": question})