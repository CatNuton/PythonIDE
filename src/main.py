from kivy.app import App
from kivy.uix.codeinput import CodeInput
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from pygments.lexers import PythonLexer
from tkinter import filedialog
import subprocess
import keyboard

class PythonIDE(App):
    def build(self):
        self.title = 'Python IDE'
        self.file_path = ''
        self.lexer = PythonLexer()

        self.layout = BoxLayout(orientation='vertical')
        self.tool_bar = BoxLayout(orientation='horizontal')
        self.code_input = CodeInput(lexer=self.lexer, size_hint=(1, 11), font_size=20)
        self.console_text_input = TextInput(text='Welcome to Python IDE', size_hint=(1,4), multiline=True, readonly=True)
        self.button_run = Button(text='Run', on_press=self.RunPythonCode)
        self.button_new = Button(text='New', on_press=self.New)
        self.button_open = Button(text='Open', on_press=self.Open)
        self.button_save = Button(text='Save', on_press=self.Save)
        self.button_save_as = Button(text='Save as...', on_press=self.SaveAs)
        
        keyboard.hook(self.DeleteLine)
        keyboard.hook(self.DeleteWord)
        keyboard.hook(self.Increase)
        keyboard.hook(self.Decrease)

        self.tool_bar.add_widget(self.button_new)
        self.tool_bar.add_widget(self.button_open)
        self.tool_bar.add_widget(self.button_save)
        self.tool_bar.add_widget(self.button_save_as)
        self.tool_bar.add_widget(self.button_run)

        self.layout.add_widget(self.tool_bar)
        self.layout.add_widget(self.code_input)
        self.layout.add_widget(self.console_text_input)

        return self.layout

    def RunPythonCode(self, instance):
        self.Save(instance=0)
        try:
            if self.file_path != '':
                command = 'python '+self.file_path
                output = subprocess.check_output(command, shell=True, encoding='utf-8')
                self.console_text_input._set_text(output)
                self.console_text_input.foreground_color = (0, 0.5, 0, 1)
        except Exception as e:
            self.console_text_input.foreground_color = (1, 0, 0, 1)
            self.console_text_input._set_text(f'{str(e)} See error in concole.')

    def SaveAs(self, instance):
        self.file_path = filedialog.asksaveasfilename(defaultextension='.py', filetypes=[('Python code file', '*.py')])
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.code_input.text)
        elif self.code_input.text == '':
            pass
        print(self.file_path)

    def Save(self, instance):
        if self.file_path != '':
           if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.code_input.text) 
        elif self.code_input.text == '':
            pass
        else:
            self.SaveAs(instance=0)
        print(self.file_path)

    def Open(self, instance):
        self.file_path = filedialog.askopenfilename(defaultextension='.py', filetypes=[('Python code file', '*.py'), ('All files', '*.*')])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                self.code_input.text = file.read()
    
    def New(self, instance):
        if self.code_input.text != '':
            self.Save(instance=0)
            self.code_input.text = ''
            self.file_path = ''

    def DeleteLine(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("l"):
                cursor_row = self.code_input.cursor_row
                self.code_input._delete_line(cursor_row-1)

    def DeleteWord(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("backspace"):
                self.code_input._select_word()
                self.code_input.delete_selection()

    def Increase(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("+"):
                self.code_input.font_size += 10
    
    def Decrease(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if keyboard.is_pressed("ctrl") and keyboard.is_pressed("-"):
                self.code_input.font_size -= 10


if __name__ == '__main__':
    PythonIDE().run()
