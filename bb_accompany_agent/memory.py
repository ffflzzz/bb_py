from langchain.memory import ConversationBufferMemory

def get_memory():
    memory = ConversationBufferMemory(    
    memory_key="history",  # 存对话的变量名，要和prompt里的{history}一致！
    input_key="input",     # 用户输入的变量名（对应prompt里的{input}）
    output_key="response", # 智能体输出的变量名（可选，不写默认用"text"）
    return_messages=True,
    k=10,  # 保留最近的10条对话记录，不写默认无限长（会爆显存）
    )  
    return memory