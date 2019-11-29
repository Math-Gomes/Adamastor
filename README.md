Pré-requisitos para utilização:
    pip
    python3.7

Comando para instalação das bibliotecas:
    pip install -r packages.txt

A seguir são apresentados alguns exemplos dos formatos de entrada aceitos para
o alfabeto e padrão.

    Alfabeto:
        { (a, 0.3), (b, 0.5), (c, 0.2) }
        { (a, 3/10), (b, 1/2), (c, 2/10)}
        { (a,3/10), (b, 0.5), (c,2/10)}
        {abc}

    Padrão:
        {abc}

A pasta in contém exemplos de entrada para o programa.

A pasta out contém os arquivos fsm.txt e output.txt:
    fsm.txt: Contém a matriz correspondente as transições do autômato.
    output.txt: Contém a saída especificada em aula.

Para executar:
    python3 main.py