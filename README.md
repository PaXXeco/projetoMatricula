# Projeto - Matrículas

## Membros do Grupo 3
- Lucas Della Giustina Schiochet
- Pedro Henrique Martini Pacheco
- Yuri Sabedot Venturin  

## Tecnologias Utilizadas

- **Linguagem:** Python  
- **Pandas:** Leitura e manipulação do dataset `matriculadosBrasil.csv`  
- **SQLAlchemy (ORM):** Mapeamento objeto-relacional entre classes Python e tabelas do banco  
- **MySQL:** Armazenamento dos dados estruturados  
- **PyQt6:** Interface gráfica do usuário  
- **Gerenciamento de dependências:** `requirements.txt`


## Arquitetura e Padrões

Este projeto adota uma **arquitetura em camadas**, com separação clara de responsabilidades:

- **Modelos (models):** Representam as entidades do domínio (curso, instituição, localização, matrícula).
- **Controllers:** Contêm a lógica de negócio e controle de fluxo entre a interface e os dados.
- **Configurações (config):** Centralizam parâmetros de conexão com o banco de dados.

### Padrões de Projeto Utilizados

- **MVC Simplificado:** Apesar de não se tratar de uma aplicação web, o projeto segue o padrão MVC com separação entre Model, View (PyQt6) e Controller.

## Importação de Dados

- Os dados são carregados do arquivo `matriculadosBrasil.csv`, localizado no diretório `data/`.
- A leitura é realizada com **Pandas**, e os dados são inseridos no banco **em lotes de 1000 linhas**, com:
  - Verificação de duplicatas (instituições, cursos, localizações)
  - Criação das associações corretas por meio de **chaves estrangeiras**
  - Registro de matrículas por ano, entre **2014 e 2022**
- Antes da inserção, a função `testar_conexao()` assegura a conectividade com o banco.

## Interface Gráfica (GUI)

### Biblioteca

- **PyQt6:** Utilizada para criação da interface gráfica.

### Telas da Aplicação

#### `MainWindow` (Janela Principal)

- Apresenta três listas para seleção de filtros:
  - Tipo de consulta (ex: "Total de alunos matriculados...", "Ranking de cursos...")
  - Unidade Federativa (ex: "SÃO PAULO", "RIO DE JANEIRO")
  - Modalidade (ex: "EAD", "Presencial")
- Um botão de pesquisa realiza a busca com base nos filtros.
- Lista de **consultas recentes** com realce ao clicar.

#### `NewWindow` (Janela Secundária)

- Exibe os **dados detalhados** da consulta selecionada.
- Mostra um **gráfico de fundo** e uma lista com os resultados formatados como `"nome - total"`.

---
