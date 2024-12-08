# Painel Administrativo para Gerenciamento de Sistema Linux

Painel administrativo desenvolvido em Python, com interface gráfica criada usando `tkinter`, para simplificar a administração de sistemas.

## Funcionalidades

- **Gerenciamento de Usuários**: Criar, editar e remover usuários do sistema.
- **Monitoramento de Sistema**: Exibir em tempo real o uso de CPU, memória e disco.
- **Gerenciamento de Serviços**: Iniciar, parar e reiniciar serviços do sistema.
- **Gerenciamento de Arquivos**: Navegar, criar, mover e excluir arquivos e diretórios.
- **Automação de Tarefas**: Criar, editar e remover tarefas agendadas.

## Requisitos

- Ambiente Linux
- **Python 3.7+**
- Bibliotecas:
  - `tkinter` (inclusa no Python)
  - `psutil` (instale com `pip install psutil`)

## Instalação e Execução

1. Execute o comando abaixo:
   ```bash
   git clone https://github.com/ithallotulio/painel-adm.git
   cd painel-adm
   python3 main.py
