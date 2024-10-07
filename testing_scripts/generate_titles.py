from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.json import JsonOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
import os

class LLM:
    template_messages = [
        SystemMessage(content='''
                    You are an assistant that writes titles for limericks. Give the provided limerick a title. Only output the title, nothing else.
                    '''),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]

    model = Ollama(model="llama3:latest")
    prompt_template = ChatPromptTemplate.from_messages(template_messages)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    runnable = (
        {"text": RunnablePassthrough()} | prompt_template | model | StrOutputParser()
    )

    def answer(self, question_filepath, answer_filepath):

        with open(question_filepath, 'r') as file:
            text = file.read()
            text = ' '.join(text.rsplit(' ')[:-1]) # remove termination keyword
            answer = LLM.runnable.invoke(text)
            
        with open(answer_filepath, 'w') as file:
            file.write(answer)
        

if __name__ == '__main__':
    llm = LLM()
    

    directory = os.fsencode('limericks_output') 

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print(filename)
        with open(f'limericks_output/{filename}', 'r') as f:
            text = f.readlines()
            title = llm.runnable.invoke(text) + '\n'
        print(title)
        print(text)
        poem = [title, "\n"] + text

        with open(f'limericks_with_titles/{filename}', 'w') as f:
            f.writelines(poem)

    # while True:
    #     print('Provide a limerick: ' , end ='')
    #     question = input()
        
    #     print(llm.runnable.invoke(question))


