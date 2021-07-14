from tkinter import *
from tkinter.ttk import *
import secrets
import string

class Password_Check(Tk):
    def __init__(self):
        super().__init__()
        self.title('Check and generate password')
        self.geometry("600x400")

        self.password_var = StringVar()
        self.password_var.trace('w', self.validate)
        self.generated_password_var = StringVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)

        self.password_label = Label()
        self.verify_password_label = Label()

        self.num_char_label = Label()
        self.digit_label = Label()
        self.symbol_label = Label()
        self.uppercase_label = Label()
        self.lowercase_label = Label()

        # set style
        self.style = Style()
        self.style.configure('Valid.TLabel', foreground='green')
        self.style.configure('Invalid.TLabel', foreground='orange')
        
        self.create_widgets()

    def create_widgets(self):
        padding = {'padx':5, 'pady':0}

        self.verify_password_label.grid(column=0, row=0, rowspan=5, **padding)
        self.verify_password_label.config(text='Verify the password strength.\nKeep entering password until\nall conditions are green:', style='Valid.TLabel')

        self.num_char_label.config(text='8 characters length or more', style='Invalid.TLabel')
        self.num_char_label.grid(column=1, row=0, columnspan=2, **padding, sticky=W)

        self.digit_label.config(text='1 digit or more', style='Invalid.TLabel')
        self.digit_label.grid(column=1, row=1, columnspan=2, **padding, sticky=W)
        
        self.symbol_label.config(text='1 symbol(!@#$%^&?,etc) or more', style='Invalid.TLabel')
        self.symbol_label.grid(column=1, row=2, columnspan=2, **padding, sticky=W)
        
        self.uppercase_label.config(text='1 uppercase letter or more', style='Invalid.TLabel')
        self.uppercase_label.grid(column=1, row=3, columnspan=2, **padding, sticky=W)
        
        self.lowercase_label.config(text='1 lowercase letter or more', style='Invalid.TLabel')
        self.lowercase_label.grid(column=1, row=4, columnspan=2, **padding, sticky=W)
        
        self.password_label.config(text='Enter password:')
        self.password_label.grid(column=0, row=5, **padding)
        
        password = Entry(self, textvariable=self.password_var)
        password.grid(column=1, row=5)

        Style().configure('TButton', foreground="red", background="white")
        Button(self, text='Reset passwd', command=self.reset_entered_passwd, style='TButton').grid(column=2, row=5, **padding)

        Button(self, text='Generate passwd', command=self.generate_passwd, style='TButton').grid(column=0, row=6, **padding)
        generated_passwd = Entry(self, textvariable=self.generated_password_var)
        generated_passwd.grid(column=1, row=6)

        Button(self, text='Reset ge_passwd', command=self.reset_generated_passwd, style='TButton').grid(column=2, row=6, **padding)

        Button(self, text='Close', command=self.close, style='TButton').grid(column=1, row=7, **padding)


    def reset_entered_passwd(self):
        self.password_var.set('')

    def reset_generated_passwd(self):
        self.generated_password_var.set('')

    def generate_passwd(self):
        result_str = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(result_str) for i in range(20)) # for a 20-character password
        self.generated_password_var.set(password)

    def close(self):
        self.destroy()

    def password_check(self, passwd):
        if(len(passwd) > 8):
            self.num_char_label.config(style='Valid.TLabel')
        else:
            self.num_char_label.config(style='Invalid.TLabel')

        if any(c.isdigit() for c in passwd):
            self.digit_label.config(style='Valid.TLabel')
        else:
            self.digit_label.config(style='Invalid.TLabel')
        
        if any(c.isupper() for c in passwd):
            self.uppercase_label.config(style='Valid.TLabel')
        else:
            self.uppercase_label.config(style='Invalid.TLabel')
        
        if any(c.islower() for c in passwd):
            self.lowercase_label.config(style='Valid.TLabel')
        else:
            self.lowercase_label.config(style='Invalid.TLabel')
        
        if re.search(r"\W", passwd):
            self.symbol_label.config(style='Valid.TLabel')
        else:
            self.symbol_label.config(style='Invalid.TLabel')

    def validate(self, *agrs):
        passwd = self.password_var.get()
        self.password_check(passwd)

if __name__ == "__main__":
    app = Password_Check()
    app.mainloop()
