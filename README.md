# Template C++ - GitHub Classroom

Template completo para criação de assignments de C++ no GitHub Classroom com correção automática.

## Funcionalidades

- **Processamento de PDFs**: Extrai exercícios automaticamente de PDFs usando OCR
- **Geração de Testes**: Cria casos de teste automaticamente baseado no tipo de problema
- **Correção Automática**: Integração com GitHub Classroom para auto-grading
- **Testes Locais**: Alunos podem testar localmente antes de submeter

## Estrutura do Projeto

```
.
├── pdfs/                    # Coloque os PDFs das listas aqui
├── src/                     # Código fonte gerado automaticamente
│   ├── lista01/
│   │   ├── ex01/
│   │   │   └── main.cpp    # Exercício com Doxygen + testes
│   │   └── ex02/
│   │       └── main.cpp
│   └── lista02/
├── scripts/                 # Scripts de processamento
│   ├── pdf_processor.py    # Extrai texto de PDFs
│   ├── exercise_parser.py  # Identifica exercícios
│   ├── test_generator.py   # Gera testes automaticamente
│   ├── autograding_generator.py  # Configura GitHub Classroom
│   └── run_tests.py        # Executa testes locais
├── .github/classroom/
│   └── autograding.json    # Configuração do Classroom
├── Makefile                # Comandos de compilação
└── README.md
```

## Fluxo de Trabalho do Professor

### 1. Preparação Inicial

Instale as dependências Python:

```bash
pip install -r requirements.txt
```

Para OCR (opcional, mas recomendado):
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-por poppler-utils

# macOS
brew install tesseract tesseract-lang poppler
```

### 2. Processar PDFs

Coloque os PDFs na pasta `pdfs/` e execute:

```bash
make process-pdfs
```

Isso irá:
1. Extrair texto dos PDFs (OCR se necessário)
2. Identificar exercícios
3. Gerar casos de teste automaticamente
4. Criar código C++ com Doxygen comments
5. Configurar GitHub Classroom

### 3. Revisar e Ajustar

Os arquivos são gerados em `src/`. Você pode:
- Revisar os testes gerados
- Ajustar entradas/saídas esperadas
- Modificar pontuação
- Adicionar mais casos de teste

### 4. Publicar no GitHub Classroom

1. Crie um repositório no GitHub
2. Configure como template no GitHub Classroom
3. O arquivo `.github/classroom/autograding.json` já está configurado
4. Distribua para os alunos

## Comandos do Makefile

```bash
# Compilar tudo
make all

# Compilar lista específica
make lista01

# Compilar exercício específico
make lista01/ex01

# Executar testes locais
make test

# Testar lista específica
make test-lista01

# Processar PDFs e gerar exercícios
make process-pdfs

# Limpar binários
make clean

# Mostrar ajuda
make help
```

## Formato Doxygen dos Exercícios

Cada exercício gerado segue o formato:

```cpp
/**
 * @exercise Lista 1 - Exercício 1
 * @title Soma de dois números
 * @description Leia dois inteiros e imprima a soma
 * @input stdin
 * @output stdout
 * @timeout 1000
 * @test name="Caso básico" input="5 3" expected="8"
 * @test name="Caso edge" input="0 5" expected="5"
 * @test name="Caso grande" input="1000 2000" expected="3000"
 */
```

## Fluxo de Trabalho do Aluno

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd template-cpp-assignments
```

### 2. Resolver Exercícios

Edite o arquivo `main.cpp` do exercício desejado:

```bash
# Editar exercício 1 da lista 1
nano src/lista01/ex01/main.cpp
```

### 3. Testar Localmente

```bash
# Testar todos os exercícios
make test

# Testar lista específica
make test-lista01

# Compilar e rodar exercício específico
make lista01/ex01
./src/lista01/ex01/bin/exercise
```

### 4. Submeter

```bash
git add .
git commit -m "Resolução dos exercícios"
git push origin main
```

O GitHub Classroom corrigirá automaticamente!

## Tipos de Problemas Suportados

O sistema detecta automaticamente e gera testes para:

- **Matemática**: Soma, subtração, multiplicação, divisão, média, área, etc.
- **Strings**: Manipulação de texto, palíndromos, cifras, etc.
- **Arrays/Vetores**: Soma de elementos, busca, ordenação, etc.
- **Condicionais**: Verificações, comparações, classificações
- **Loops**: Repetições, iterações, sequências
- **Funções**: Recursão, procedimentos
- **Structs/Classes**: Registros, objetos
- **Arquivos**: Leitura/escrita de arquivos
- **Geral**: Problemas genéricos

## Personalização

### Adicionar Novos Tipos de Testes

Edite `scripts/test_generator.py` e adicione funções geradoras:

```python
def generate_meu_tipo_tests(problem_types, description):
    tests = []
    # Seus casos de teste aqui
    return tests
```

### Modificar Testes

Ajuste os valores `input` e `expected` nos comentários Doxygen ou adicione novos `@test` conforme necessário.

### Configurar Timeout

Altere `@timeout` nos comentários Doxygen (em milissegundos).

## Solução de Problemas

### OCR não funciona

- Verifique se o Tesseract está instalado: `tesseract --version`
- Verifique se as linguagens estão instaladas: `tesseract --list-langs` (deve mostrar `por`)
- Para PDFs com texto selecionável, o sistema usa PyMuPDF automaticamente

### Compilação falha

- Verifique se o g++ está instalado: `g++ --version`
- Padrão C++17 é necessário

### Testes não passam

- Verifique se o formato de saída está exatamente igual ao esperado
- Espaços em branco e quebras de linha são significativos
- Use `make test` para ver detalhes dos erros

## Contribuindo

Para melhorar o template:

1. Ajuste os geradores de teste em `scripts/test_generator.py`
2. Adicione novos padrões de exercícios em `scripts/exercise_parser.py`
3. Melhore a detecção de tipos de problemas

## Licença

MIT License - Livre para uso acadêmico e comercial.

## Suporte

Em caso de dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Execute `make clean` e tente novamente
3. Verifique os logs em `temp/` para debugging
