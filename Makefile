# Template C++ - GitHub Classroom
# Makefile para compilação e testes de exercícios

# Configurações
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
LISTAS_DIR = listas
PDFS_DIR = pdfs
TEMP_DIR = temp

# Encontra todos os diretórios de exercícios
EXERCISE_DIRS := $(wildcard $(LISTAS_DIR)/*/ex*)
EXERCISE_NAMES := $(notdir $(EXERCISE_DIRS))
LISTA_DIRS := $(wildcard $(LISTAS_DIR)/*)

# Alvos principais
.PHONY: all clean test process-pdfs help

# Compila todos os exercícios
all: $(EXERCISE_DIRS)

# Regra para compilar cada exercício
$(LISTAS_DIR)/*/ex%:
	@echo "Compilando $@..."
	@mkdir -p $@/bin
	$(CXX) $(CXXFLAGS) $@/main.cpp -o $@/bin/exercise 2>&1 || echo "Erro na compilação de $@"

# Compila lista específica (ex: make lista-basico-cpp)
%: $(filter $(LISTAS_DIR)/%/ex*,$(EXERCISE_DIRS))
	@echo "Lista $* compilada."

# Compila exercício específico (ex: make lista-basico-cpp/ex01)
$(LISTAS_DIR)/%/ex%:
	@if [ -f $@/main.cpp ]; then \
		echo "Compilando $@..."; \
		mkdir -p $@/bin; \
		$(CXX) $(CXXFLAGS) $@/main.cpp -o $@/bin/exercise || echo "Erro na compilação"; \
	else \
		echo "Exercício $@ não encontrado"; \
	fi

# Executa testes locais
test:
	@echo "Executando testes locais..."
	@python3 scripts/run_tests.py

# Testa lista específica
test-lista%:
	@echo "Testando lista $*..."
	@python3 scripts/run_tests.py --lista $*

# Processa PDFs e gera exercícios
process-pdfs:
	@echo "Processando PDFs..."
	@python3 scripts/pdf_processor.py
	@python3 scripts/exercise_parser.py
	@python3 scripts/test_generator.py
	@python3 scripts/autograding_generator.py
	@echo "Processamento concluído!"

# Limpa binários e arquivos temporários
clean:
	@echo "Limpando arquivos..."
	@find $(LISTAS_DIR) -type d -name "bin" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf $(TEMP_DIR)/*
	@echo "Limpo!"

# Mostra ajuda
help:
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Alvos disponíveis:"
	@echo "  make all                     - Compila todos os exercícios"
	@echo "  make lista-basico-cpp        - Compila todos da lista"
	@echo "  make lista-basico-cpp/ex01   - Compila exercício específico"
	@echo "  make test                    - Executa todos os testes locais"
	@echo "  make test-lista-basico-cpp   - Testa lista específica"
	@echo "  make clean                   - Limpa binários e temporários"
	@echo "  make help                    - Mostra esta ajuda"
	@echo ""
	@echo "Exercícios disponíveis:"
	@for dir in $(EXERCISE_DIRS); do \
		echo "  - $$dir"; \
	done
