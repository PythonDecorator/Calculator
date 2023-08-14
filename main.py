import customtkinter as ctk
from styling import *
import os
import sys


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)
        self.title(" Amos' Calculator")
        self.iconbitmap(self.resource_path("files/images/logo.ico"))
        self.resizable(False, False)
        app_width = 400
        app_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cor = int((screen_width / 2) - (app_width / 2))
        y_cor = int((screen_height / 2) - (app_height / 2))
        self.geometry("{}x{}+{}+{}".format(app_width, app_height, x_cor, y_cor))

        # VARIABLES
        self.calculate_var = ctk.StringVar()
        self.result_var = ctk.StringVar(value="0")
        self.number_var = ctk.StringVar()

        self.number_list = []
        self.operator_list = []
        self.calculate_list = []

        self.all_operator_list = ["/", "x", "+", "-", "=", "."]

        # LAYOUT DESIGN
        # OUTPUT FRAME
        self.output_frame = ctk.CTkFrame(self, fg_color=OUTPUT_COLOR, corner_radius=10)
        self.output_frame.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.22)

        # BUTTONS FRAME
        self.button_frame = ctk.CTkFrame(self, fg_color=BTN_COLOR, corner_radius=10)
        self.button_frame.place(relx=0.01, rely=0.25, relwidth=0.98, relheight=0.7)

        for n in range(5):
            if n < 4:
                self.button_frame.columnconfigure(n, weight=1, uniform="a")
            self.button_frame.rowconfigure(n, weight=1, uniform="a")

        # WIDGETS
        # OUTPUT LABELS
        OutputLabel(self.output_frame, anchor="nw", textvariable=self.calculate_var, font=FORMULA_FONT)
        OutputLabel(self.output_frame, anchor="se", textvariable=self.result_var, font=RESULT_FONT)

        # BUTTONS
        # FUNCTIONS
        function_dict = {"Exp": [0, 0, self.exponential],
                         "(-)": [1, 0, self.negative],
                         "%": [2, 0, self.percentage],
                         "AC": [3, 0, self.clear],
                         }
        for key, value in function_dict.items():
            ConvertButtons(self, text=key, col=value[0], row=value[1], command=value[2], text_color=OPERATOR_TEXT_COLOR)

        # MAIN CALCULATOR
        for key, value in CALCULATOR_NUM.items():
            if key not in self.all_operator_list:
                CalculateButtons(self, text=key, col=value[0], row=value[1], command=self.get_num, text_color=value[2])
            else:
                CalculateButtons(self, text=key, col=value[0], row=value[1], command=self.operator,
                                 text_color=value[2])

        # BOTTOM TEXT
        ctk.CTkLabel(self, fg_color=BG_COLOR, text_color=BOTTOM_TEXT_COLOR, font=BOTTOM_TEXT_FONT,
                     text="Designed by Amos @PythonDecorator").pack(side="bottom", pady=2)

        self.calculate_var.trace_add("write", self.calculate)

    def calculate(self, *args):
        user_input_list = self.calculate_var.get().split(" ")
        for index, item in enumerate(user_input_list):
            if item == "x":
                user_input_list[index] = "*"

            if item == "":
                user_input_list.remove(item)

        if len(user_input_list) % 2:
            try:
                calculated_result = eval("".join(user_input_list))
            except SyntaxError:
                pass
            except NameError:
                pass
            except ZeroDivisionError:
                pass
            else:
                if isinstance(calculated_result, float):
                    try:
                        if str(calculated_result).split(".")[1] == "0":
                            result = str(round(calculated_result))
                        else:
                            result = str(round(calculated_result, 6))
                        self.result_var.set(value=result)
                    except IndexError:
                        result = str(eval("".join(user_input_list)))
                        self.result_var.set(value=result)
                else:
                    self.result_var.set(value=str(calculated_result))

    def operator(self, operator):
        if self.number_list and operator != "=":
            if self.calculate_list[-1] not in self.all_operator_list:
                self.number_list.append(f" {operator} ")
                self.calculate_list.append(operator)
                self.calculate_var.set("".join(self.number_list))

    def get_num(self, number):
        self.number_list.append(number)
        self.calculate_list.append(number)
        self.calculate_var.set("".join(self.number_list))

    def exponential(self):
        if self.number_list:
            self.number_list.append("E")
            self.calculate_var.set("".join(self.number_list))

    def negative(self):
        if not self.number_list:
            self.number_list.insert(0, "-")
            self.calculate_var.set("".join(self.number_list))
        else:
            try:
                if self.calculate_list[-1] in self.all_operator_list or self.number_list[-1] == "E":
                    self.number_list.append("-")
                    self.calculate_var.set("".join(self.number_list))
            except IndexError:
                pass

    def percentage(self):
        if self.number_list:
            try:
                self.result_var.set(str((float(self.result_var.get()) / 100)))
            except ValueError:
                pass
            else:
                self.number_list.clear()
                self.number_list.append(self.result_var.get())

    def clear(self):
        self.number_list.clear()
        self.calculate_list.clear()
        self.calculate_var.set("")
        self.result_var.set("")

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)


class ConvertButtons(ctk.CTkButton):
    def __init__(self, parent: App, text, text_color, col, row, command):
        super().__init__(parent.button_frame, text=text, fg_color=BTN_COLOR, text_color=text_color, font=BTN_FONT,
                         command=command, border_width=2, border_color=BORDER_COLOR,
                         hover_color=BTN_HOVER_COLOR)
        self.grid(column=col, row=row, padx=4, pady=4, sticky="news")


class CalculateButtons(ctk.CTkButton):
    def __init__(self, parent: App, text, text_color, col, row, command):
        super().__init__(parent.button_frame, text=text, fg_color=BTN_COLOR, text_color=text_color, font=BTN_FONT,
                         command=lambda: command(text), border_width=2, border_color=BORDER_COLOR,
                         hover_color=BTN_HOVER_COLOR)
        self.grid(column=col, row=row, padx=4, pady=4, sticky="news")


class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, anchor, textvariable, font):
        super().__init__(parent, fg_color=OUTPUT_COLOR, text_color=TEXT_COLOR,
                         anchor=anchor, font=font, textvariable=textvariable)
        self.pack(side="top", expand=True, fill="both", padx=10, pady=5)


if __name__ == '__main__':
    app = App()
    app.mainloop()
