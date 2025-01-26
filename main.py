import re

variables = {}

def tokenize(code):
    token_pattern = r'(\b(?:yo|yap)\b|".*?"|[a-zA-Z_]\w*|[=;()])'
    tokens = re.findall(token_pattern, code)
    return [token for token in tokens if token.strip()]

def parse(tokens):
    if tokens[0] == "yap" and len(tokens) >= 4:
        if tokens[1] != "(":
            raise SyntaxError(f"Expected '(' after 'yap', but got '{tokens[1]}'.\nOffending code: {' '.join(tokens)}")
        if tokens[-2] != ")":
            raise SyntaxError(f"Expected ')' before ';', but got '{tokens[-2]}'.\nOffending code: {' '.join(tokens)}")
        if tokens[-1] != ";":
            raise SyntaxError(f"Expected ';' at the end of the statement, but got '{tokens[-1]}'.\nOffending code: {' '.join(tokens)}")
        return {"type": "print", "value": tokens[2][1:-1] if tokens[2].startswith('"') else tokens[2]}

    elif tokens[0] == "yo" and len(tokens) >= 5:
        if not re.match(r'[a-zA-Z_]\w*$', tokens[1]):
            raise SyntaxError(f"Invalid variable name: '{tokens[1]}'. Variable names must start with a letter or '_'.\nOffending code: {' '.join(tokens)}")
        if tokens[2] != "=":
            raise SyntaxError(f"Expected '=' after variable name, but got '{tokens[2]}'.\nOffending code: {' '.join(tokens)}")
        if tokens[-1] != ";":
            raise SyntaxError(f"Expected ';' at the end of the statement, but got '{tokens[-1]}'.\nOffending code: {' '.join(tokens)}")
        return {"type": "declare", "name": tokens[1], "value": tokens[3][1:-1]}

    else:
        raise SyntaxError(f"Unknown statement: {' '.join(tokens)}\nEnsure you are using valid Brainrot syntax.")

def interpret(statement):
    if statement["type"] == "print":
        value = statement["value"]
        if value in variables:
            print(variables[value])
        else:
            print(value)
    elif statement["type"] == "declare":
        variables[statement["name"]] = statement["value"]

def run_brainrot_file(file_path):
    try:
        with open(file_path, "r") as file:
            code = file.read()
        for line in code.splitlines():
            line = line.strip()
            if line.startswith("//") or not line:
                continue
            tokens = tokenize(line)
            statement = parse(tokens)
            interpret(statement)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python brainrot_interpreter.py <file_path>")
    else:
        run_brainrot_file(sys.argv[1])
