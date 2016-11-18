from Tkinter import *
import socket, threading

def acceptMessage(s, text, theSystem):

	sock, addr = s.accept()
	theSystem.sock = sock
	while True:
		text.insert(END, "[Other's Message] : "+sock.recv(1024)+"\n")

class Chat:
	def __init__(self):

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = socket.gethostname()
		port = 12345
		self.s.bind((host, port))
		self.s.listen(1)
		window = Tk()
		window.title("Chat")
		self.text = Text(window)
		self.text.pack()
		frame1 = Frame(window)
		frame1.pack()
		label = Label(frame1,text="Enter Your Meaasge: ")
		self.Message = StringVar()
		entryMessage = Entry(frame1,textvariable=self.Message)
		btSend = Button(frame1,text="Send",
							command=self.processSendButton)
		label.grid(row=1,column=1)
		entryMessage.grid(row=1,column=2)
		btSend.grid(row=1,column=4)
		self.text.insert(END, "\t\t\t\t----------------------\n\t\t\t\tWelcome to Chat  \n\t\t\t\tEnjoy yourself \n\t\t\t\t------------------------\n\n\n")
		self.text.insert(END, "[NO PERSON] Wait for another one \n")
		t = threading.Thread(target=acceptMessage, args=(self.s, self.text, self))
		t.start()
		window.mainloop()

	def processSendButton(self):

		self.sock.send(self.Message.get())
		self.text.insert(END, "[Your Message] : "+self.Message.get()+"\n")

Chat()

