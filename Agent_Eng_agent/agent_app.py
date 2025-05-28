import os
from langchain_deepseek import ChatDeepSeek
# from langchain.chains import ConversationChain
# from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from memory import  memories
from prompts import prompts
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType


os.environ["DEEPSEEK_API_KEY"] = "sk-423c3a20326f49a98823c9c934cacd81"
os.environ["SERPAPI_API_KEY"] = "b430ba1186db7e10e7b07ec6e6fa884d3391bbeaa92196629f7120dc35b42aa6"


llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    streaming=False,
) 

tools = load_tools(["serpapi","llm-math"],llm=llm)

memory = memories()
prompt_template = prompts()  # 获取的是PromptTemplate对象

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    prompt=prompt_template,
    verbose=True
)


while True:
    user_input = input("我：")
    if user_input.lower() == "退出":  # 输入“退出”结束对话
        break

    full_response = agent.invoke({"input": user_input})
    print("lex：", end="")  # 先打印“lex：”，然后逐字输出内容

    # for chunk in llm.stream(full_response):  # 遍历生成器，逐个拿响应片段
    #     # 打印当前片段（比如第一个字“阿”，第二个字“丹”...）
    #     print(chunk.content, end="", flush=True)  # flush=True强制立即显示
    #     full_response += chunk.content  # 把片段拼到完整响应里
