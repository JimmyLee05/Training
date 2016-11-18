#Client_GUI

from Tkinter import *
import socket, threading

def acceptMessage(sock, text):

	while True:
		text.insert(END, "[Other's Message] : "+sock.recv(1024)+"\n")

class Chat:

	def __init__(self):

		window = Tk()
		window.title("Chat")
		self.text = Text(window)
		self.text.pack()
		frame1 = Frame(window)
		frame1.pack()
		label = Label(frame1,text="Enter your message: ")
		self.Message = StringVar()
		entryMessage = Entry(frame1,textvariable=self.Message)
		btSend = Button(frame1,text="Send",
			command=self.processSendButton)
		btLink = Button(window,text="Link",
			command=self.processLinkButton)
		btLink.pack()

		label.grid(row=1,column=1)
		entryMessage.grid(row=1,column=2)
		btSend.grid(row=1,column=4)
		self.text.insert(END, "\t\t\t\t-----------------\n\t\t\tWelcome to Chat \n\t\t\t\tEnjoy youself \n\t\t\t\t----------------------\n\n\n")
		window.mainloop()

	def processSendButton(self):

		self.s.send(self.Message.get())
		self.text.insert(END, "[Your Message] : "+self.Message.get()+"\n")

	def processLinkButton(self):

		self.s = socket.socket()
		host = socket.gethostname()
		port = 12345
		self.s.connect(('10.0.1.8', port))
		self.text.insert(END, "Linked\n")
		t = threading.Thread(target=acceptMessage, args=(self.s, self.text,))
		t.start()

Chat()








