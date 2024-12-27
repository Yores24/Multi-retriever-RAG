from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def generation(compression_retriever,chatllm):
    memory = ConversationBufferMemory(memory_key="chat_history",
                                    return_messages=True)

    qa_withmemory = ConversationalRetrievalChain.from_llm(chatllm,
                                            compression_retriever,
                                            memory=memory)
    return qa_withmemory


def update_chat_history(chat_history, user_query, answer):
    chat_history.append(("You", user_query))
    chat_history.append(("Bot", answer))

    return chat_history