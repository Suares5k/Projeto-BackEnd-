# Sistema de Gestão Hospitalar - Backend

Este é o backend do Sistema de Gestão Hospitalar (SGHSS), desenvolvido em Python utilizando Flask. O sistema oferece funcionalidades para gerenciamento de pacientes, consultas e prontuários médicos.

## Tecnologias Utilizadas

- Python 3.x
- Flask
- MySQL
- JWT (JSON Web Tokens)
- Flask-Bcrypt

## Estrutura do Projeto

```
sghss_backend/
├── app.py              # Arquivo principal da aplicação
├── config.py           # Configurações do banco de dados
└── requirements.txt    # Dependências do projeto
```

## Funcionalidades

### Autenticação
- Login de pacientes com CPF e senha
- Geração de tokens JWT para autenticação
- Proteção de rotas com middleware de autenticação

### Gestão de Pacientes
- Cadastro de novos pacientes
- Armazenamento seguro de senhas com hash bcrypt

### Gestão de Consultas
- Agendamento de consultas
- Listagem de consultas por paciente
- Associação com médicos

### Gestão de Prontuários
- Adição de registros médicos
- Consulta de histórico de prontuários por paciente

## Comunicação com o Banco de Dados

O sistema utiliza MySQL como banco de dados e estabelece conexões através da biblioteca `mysql.connector`. A comunicação é gerenciada da seguinte forma:

1. **Configuração da Conexão**
   - As credenciais do banco são armazenadas no arquivo `config.py`
   - Uma função `get_db_connection()` gerencia a criação de conexões

2. **Padrão de Uso**
   ```python
   conn = get_db_connection()
   cursor = conn.cursor()
   try:
       # Execução de queries
       cursor.execute("QUERY SQL")
       conn.commit()
   finally:
       cursor.close()
       conn.close()
   ```

3. **Tabelas Principais**
   - `pacientes`: Armazena informações dos pacientes
   - `consultas`: Registra agendamentos de consultas
   - `prontuarios`: Mantém o histórico médico dos pacientes

## Segurança

- Senhas são armazenadas com hash usando bcrypt
- Autenticação via JWT com expiração de 1 hora
- Proteção de rotas sensíveis com decorator `@token_required`

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure o banco de dados no arquivo `config.py`

3. Execute a aplicação:
   ```bash
   python app.py
   ```

## Endpoints da API

### Autenticação
- `POST /login`: Autenticação de pacientes

### Pacientes
- `POST /pacientes`: Cadastro de novos pacientes

### Consultas
- `POST /consultas`: Agendamento de consultas
- `GET /consultas/<paciente_id>`: Listagem de consultas

### Prontuários
- `POST /prontuarios`: Adição de registros médicos
- `GET /prontuarios/<paciente_id>`: Consulta de prontuários

## Requisitos do Sistema

- Python 3.x
- MySQL Server
- Bibliotecas listadas em `requirements.txt`

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 
