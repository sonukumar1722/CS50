operands = input("operands: ").split()

operand1 = float(operands[0])
operand2 = float(operands[2])
operator = operands[1]

if operator == "+":
    print(operand1 + operand2)
elif operator == "-":
    print(operand1 - operand2)
elif operator == "*":
    print(operand1 * operand2)
elif operator == "/" and not operand2 == 0:
    print(f"{(operand1 / operand2):.1f}")
