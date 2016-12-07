import Chatbot.chatbot as Chatbot

chatter = Chatbot.Chatbot(build_console=False)

print("Hello, I am Mianbot.")

while True:
    raw = input()
    reply,confidence = chatter.testQuestionAnswering(raw)
    print("%s ,%d" % (reply,confidence))