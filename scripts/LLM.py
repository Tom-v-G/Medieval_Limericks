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

class LLM:
    template_messages = [
        SystemMessage(content='''
                    You are an assistant that writes medieval limericks. Give the limerick a title. Only output the title and the limerick. Nothing else.
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
    
    with open('temp/subjects.txt', 'r') as f:
        subjects = [text.strip('\n') for text in f.readlines()]
    # print(subjects)
    llm = LLM()
    
    for idx, subject in enumerate(subjects):
        limerick = llm.runnable.invoke(subject)
        with open(f'temp/limerick_{idx}.txt', 'w') as f:
            f.writelines(limerick)


