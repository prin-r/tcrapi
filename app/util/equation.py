PRECEDENCES = {
    "+": 2,
    "-": 2,
    "*": 4,
    "/": 4,
    "%": 4,
    "^": 6,
    "(": 1,
    ")": 1,
    "#": 1,
}


def tokenized(str):
    token = []
    for ch in str.replace(" ", ""):
        if "0" <= ch <= "9":
            if token and isinstance(token[-1], int):
                token.append(token.pop() * 10 + int(ch))
            else:
                token.append(int(ch))
        else:
            token.append(ch)

    return token


def infix_to_prefix(tokens):
    tokens.reverse()
    stack = []
    new_tokens = []
    stack.append("#")
    for token in tokens:
        if token not in PRECEDENCES:
            new_tokens.append(token)
        else:
            if token == ")":
                stack.append("(")
            elif token == "(":
                while stack[-1] != "(":
                    new_tokens.append(stack.pop())
                stack.pop()
            else:
                while PRECEDENCES[stack[-1]] > PRECEDENCES[token]:
                    new_tokens.append(stack.pop())
                stack.append(token)

    while stack[-1] != "#":
        new_tokens.append(stack.pop())

    return list(reversed(new_tokens))


def prefix_to_opcode(tokens):
    result = []
    for token in tokens:
        if token == "+":
            result.append(4)
        elif token == "-":
            result.append(5)
        elif token == "*":
            result.append(6)
        elif token == "/":
            result.append(7)
        elif token == "^":
            result.append(8)
        elif token == "x":
            result.append(1)
        else:
            result.append(0)
            result.append(token)

    return result


def validate(tokens):
    last_was_op = True
    last_was_open = False
    parenth_count = 0

    for token in tokens:
        if token in PRECEDENCES:
            if token == "(":
                parenth_count += 1
                last_was_open = True
                continue
            elif token == ")":
                if parenth_count <= 0 or last_was_op:
                    raise ValueError("Equation is not valid")
                parenth_count -= 1
            else:
                if last_was_op or last_was_open:
                    raise ValueError("Equation is not valid")
                last_was_op = True
                continue
        last_was_op = False
        last_was_open = False

    if parenth_count != 0 or last_was_op:
        raise ValueError("Equation is not valid")


def dump(str):
    tokens = tokenized(str)
    validate(tokens)
    return prefix_to_opcode(infix_to_prefix(tokens))
