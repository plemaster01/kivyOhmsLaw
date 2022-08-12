# Ohm's Law Solver using kivy!!
import math
from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class OhmsLawInputScreen(GridLayout):
    def __init__(self, **kwargs):
        super(OhmsLawInputScreen, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 10
        title = Label(
            text="Ohm's Law Solver!",
            font_size="32sp",
            color=(1, 0.8, 0),
            bold=True,
            size_hint=(1, 0.5),
        )
        self.add_widget(title)
        instructions = Label(
            text="Enter Known Values (Minimum 2)",
            font_size="20sp",
            bold=True,
            size_hint=(1, 0.5),
        )
        self.add_widget(instructions)
        self.voltage = LabelAndInput("Voltage (V - volts): ", (1, 0, 0))
        self.current = LabelAndInput("Current (I - amps): ", (0, 1, 0))
        self.resist = LabelAndInput("Resistance (R - ohms): ", (0, 0.5, 1))
        self.power = LabelAndInput("Power (P - watts): ", (1, 0, 1))
        self.add_widget(self.voltage)
        self.add_widget(self.current)
        self.add_widget(self.resist)
        self.add_widget(self.power)
        self.solve = Button(text="Solve", color=(0, 0, 0), bold=True)
        self.add_widget(self.solve)
        self.solve.bind(on_press=self.callback)
        self.answer = Label(text="Answer: ", bold=True, size_hint=(1, 0.5))
        self.add_widget(self.answer)
        self.formula = Label(text="Formula: ", bold=True, size_hint=(1, 0.5))
        self.add_widget(self.formula)

    def callback(self, instance) -> None:
        # convert inputs to float numbers
        v = float(self.voltage.input.text) if self.voltage.input.text else float(0)
        i = float(self.current.input.text) if self.current.input.text else float(0)
        r = float(self.resist.input.text) if self.resist.input.text else float(0)
        p = float(self.power.input.text) if self.power.input.text else float(0)

        # check if exactly 2 values are entered
        num_zero = [value == 0 for value in (v, i, r, p)]
        if sum(num_zero) != 2:
            self.answer.text = "You should enter two values"
            self.formula.text = ""
            return

        calc_dict = {
            "vi": "(v, i, v / i, v * i)",
            "vr": "(v, v / r, r, v * v / r)",
            "vp": "(v, p / v, v * v / p, p)",
            "ir": "(i * r, i, r, r * i * i)",
            "ip": "(p / i, i, p / (i * i), p)",
            "rp": "(math.sqrt(p * r), math.sqrt(p / r), r, p)",
        }

        # find the couple of values we have
        couple = ""
        for index, value in enumerate(("v", "i", "r", "p")):
            if not num_zero[index]:
                couple += value

        # do calculations
        v, i, r, p = eval(calc_dict[couple])
        self.formula.text = calc_dict[couple]

        # update answer text
        self.answer.text = (
            f"{str(round(v,4))} V == {str(round(i,4))} A == "
            f"{str(round(r,4))} Ω == {str(round(p,4))} W"
        )


class LabelAndInput(BoxLayout):
    def __init__(self, input_text=None, input_color=(0, 0, 0), **kwargs):
        super(LabelAndInput, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.value = Label(
            text=input_text, color=input_color, bold=True, size_hint=(0.4, 1)
        )
        self.add_widget(self.value)
        self.input = TextInput(
            multiline=False, size_hint=(0.6, 1), input_filter="float"
        )
        self.add_widget(self.input)


class OhmsLawApp(App):
    def build(self):
        return OhmsLawInputScreen()


if __name__ == "__main__":
    OhmsLawApp().run()
