from misc.generateMonthButtons import generateMonthButtons

buttons = generateMonthButtons(2025, 7, 8)

print(len(buttons), len(buttons[0]), len(buttons[-1]))
