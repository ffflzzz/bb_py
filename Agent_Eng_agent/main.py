import os
import langchain
from langchain_deepseek import ChatDeepSeek
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage,AIMessage,SystemMessage
from memory import  memories
from prompts import prompts


os.environ["DEEPSEEK_API_KEY"] = "sk-58164d4e3ef94c32b37d8097f072dbd8"

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    streaming=True,
    # api_key="...",
    # other params...
)  # temperature控制回答随机性，0.5偏稳定

memory = memories()
prompt_template = prompts()  # 获取的是PromptTemplate对象
template_str = prompt_template.template  # 获取实际的模板字符串

system_prompt = template_str.split("当前对话历史：{history}")[0]  # 使用模板字符串
system_message = SystemMessage(content=system_prompt.strip())  # 转成SystemMessage


while True:
    user_input = input("我：")
    if user_input.lower() == "退出":  # 输入“退出”结束对话
        break
    # 2. 手动构造消息列表（因为stream需要传入消息列表）
    # 从memory里拿历史消息（格式是[HumanMessage(...), AIMessage(...), ...]）
    history_messages = memory.load_memory_variables({})["history"]
    # 添加当前用户输入（HumanMessage）
    messages = [system_message] + history_messages + [HumanMessage(content=user_input)]

    # 3. 调用流式输出（关键！）
    full_response = ""  # 存完整响应
    print("lex：", end="")  # 先打印“lex：”，然后逐字输出内容
    for chunk in llm.stream(messages):  # 遍历生成器，逐个拿响应片段
        # 打印当前片段（比如第一个字“阿”，第二个字“丹”...）
        print(chunk.content, end="", flush=True)  # flush=True强制立即显示
        full_response += chunk.content  # 把片段拼到完整响应里

    # 4. 把完整响应存到memory里（否则下一轮对话会丢失当前回复）
    memory.save_context(
        {"input": user_input},  # 用户输入
        {"response": full_response}  # 完整的智能体回复
    )
    print()  # 换行，保持输出格式整洁