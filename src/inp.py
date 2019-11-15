from re import findall
from collections import Counter

def parseInputAlphabet(userInput):

    userInput = userInput.replace(" ", "")

    if userInput[0] != '{' and userInput[-1] != '}':
        # print("Erro:", "Não inicia/termina com { }")
        return None, "The alphabet must start and end with { }"

    splitInput = findall('\(.*?\)', userInput)

    if splitInput == []:
        return None, "Syntax error"

    for t in splitInput:
        if t.index(',') > 2:
            # print("Erro:", "Caractere inválido =>", "'" + t[1:t.index(',')] + "'")
            return None, "Invalid character: " + "'" + t[1:t.index(',')] + "'"

    result = list(map(eval,[f'("{l[1]}",{l[3:-1]})' for l in splitInput]))

    characters = ''.join(list(map(lambda k: k[0], result)))
    if Counter(characters).most_common(1)[0][1] > 1:
        # print("Erro:", "Existem caracteres repetidos no alfabeto")
        return None, "There are repeated characters in the alphabet"

    if sum(map(lambda k: k[1], result)) != 1:
        # print("Erro:", "A soma das probabilidades é diferente de 1")
        return None, "The sum of the probabilities of occurrence of characters is different from 1"

    return result, None

def parseInputPattern(userInput, alphabet):

    userInput = userInput.replace(" ", "")

    if userInput[0] != '{' and userInput[-1] != '}':
        # print("Erro:", "Não inicia/termina com { }")
        return None, "The pattern should start and end with { }"

    pattern = userInput[1:-1]

    if not all(l in alphabet for l in pattern):
        # print("Erro:", "O padrão contém caracteres que não estão no alfabeto")
        return None, "The pattern contains a value that is not in alphabet."

    return pattern, None


if __name__ == "__main__":
    r = parseInputAlphabet(userInput = "{ (a, 0.5), (b, 0.3), (c, 0.1), (d, 0.1)}")
    if r:
        print(r)

    alphabet_str = ''.join(list(map(lambda k: k[0], r))) 
    r2 = parseInputPattern(userInput = "{ abc }", alphabet = alphabet_str)
    if r2:
        print(r2)

    # { (c, 0.5), (k, 0.5) }
    # { ckck }
    # {(a,0.3), (b, 0.3), (c, 0.2), (d, 0.2)}