from tkinter import *
from chat import chat_responder

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 11"
FONT_BOLD = "Helvetica 10 bold"

class WSMChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, "Wbot: Halo, ada yang bisa saya bantu?\n")
        self.text_widget.configure(state=DISABLED)

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("WSM Chat")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome to DWCU",
            font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        #tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=.07, relheight=.012)

        #text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR,
            fg=TEXT_COLOR,font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=.745, relwidth=1, rely=.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        #scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=.974)
        scrollbar.configure(command=self.text_widget.yview)

        #bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=.825)

        #message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=.74, relheight=.06, rely=.008, relx=.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        #send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, 
            command=lambda : self._on_enter_pressed(None))
        send_button.place(relx=.77, rely=.008, relheight=.06, relwidth=.22)
    
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"'WBot': {responder.get_response(msg1)}\n\n" # function to get bot response
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

if __name__ == "__main__":
    app = WSMChatApplication()
    responder = chat_responder()
    app.run()
    