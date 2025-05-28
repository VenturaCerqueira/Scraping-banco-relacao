#   🚀 Gerador de Esquema de Banco de Dados MySQL em Markdown

Este é um script Python simples e eficaz para gerar automaticamente a documentação do esquema do seu banco de dados MySQL em formato Markdown. 
Ele se conecta ao seu banco de dados, extrai informações detalhadas sobre tabelas e colunas, e as organiza em um arquivo .md de fácil leitura e compartilhamento.

#   ✨ Funcionalidades

- **Extração Abrangente:** Coleta dados essenciais sobre tabelas (engine, collation, comentários, datas de criação/atualização, número de linhas estimado e tamanho) e colunas (tipo, chaves primárias e estrangeiras, nulidade, valores padrão e comentários).
-   **Saída em Markdown:** Gera um arquivo .md bem formatado, ideal para visualização em repositórios (GitHub, GitLab, Bitbucket), wikis ou qualquer editor de Markdown.
-   **Configuração Segura:** Utiliza variáveis de ambiente (.env) para as credenciais do banco de dados, garantindo que informações sensíveis não sejam expostas diretamente no código.
-   **Tratamento de Erros:** Inclui tratamento robusto para erros de conexão e outras exceções, com mensagens informativas.
-   **Dados Legíveis:** Formata números grandes (como o número de linhas) com separadores de milhares e trata valores NULL ou vazios para uma apresentação mais limpa.

#   📦 Como Usar
##  Pré-requisitos
Certifique-se de ter o Python 3 instalado em sua máquina.

1. **Clonar o Repositório** (ou baixar o script)
   
```bash
git clone <URL_DO_SEU_REPOSITORIO>
```
2. **Abrindo projeto:**
```bash
cd <nome-do-diretorio>
```

3. **Instalar as Dependências**
   
Este projeto requer as bibliotecas **pymysql** para conexão com o MySQL e **python-dotenv** para carregar as variáveis de ambiente.

```bash
pip install pymysql python-dotenv
```

4. **Configurar as Variáveis de Ambiente**
Crie um arquivo chamado **.env** na raiz do projeto (no mesmo diretório do script Python) e adicione as seguintes informações do seu banco de dados:

**Fragmento do código**

```bash
MYSQL_HOST=seu_host_mysql
MYSQL_PORT=3306
MYSQL_USER=seu_usuario_mysql
MYSQL_PASSWORD=sua_senha_mysql
MYSQL_DB=seu_banco_de_dados
```
**Importante:** Nunca compartilhe seu arquivo **.env** publicamente! Adicione-o ao seu **.gitignore**.

4. **Executar o Script**
Com as dependências instaladas e o arquivo **.env** configurado, você pode executar o script:

```Bash
python seu_script_de_esquema.py
```

O script criará um arquivo **Markdown** chamado **<nome_do_banco>_schema.md** (por exemplo, meu_banco_schema.md) no mesmo diretório.


# 📦 Estrutura do Banco de Dados `minha_aplicacao_db`

## 🗂️ Tabela: `usuarios`

- **Engine:** InnoDB
- **Collation:** utf8mb4_0900_ai_ci
- **Comentário da tabela:** Armazena informações dos usuários do sistema.
- **Criada em:** 2023-01-15 10:30:00
- **Última atualização:** 2024-05-28 09:00:00
- **Número de linhas (estimado):** 1.250
- **Tamanho aprox. (MB):** 0.15

| Coluna | Tipo | Chave | Nulo | Padrão | Comentário |
|--------|------|-------|------|--------|------------|
| `id` | `int` | PK | NO | NULL | Identificador único do usuário |
| `nome` | `varchar(255)` | | NO | NULL | Nome completo do usuário |
| `email` | `varchar(255)` | | NO | NULL | Endereço de e-mail (único) |
| `data_cadastro` | `datetime` | | NO | CURRENT_TIMESTAMP | Data e hora do cadastro |
| `perfil_id` | `int` | FK → perfis.id | YES | NULL | ID do perfil do usuário |

---

## 🗂️ Tabela: `produtos`

- **Engine:** InnoDB
- **Collation:** utf8mb4_0900_ai_ci
- **Comentário da tabela:** Catálogo de produtos.
- **Criada em:** 2023-02-01 14:00:00
- **Última atualização:** Nunca
- **Número de linhas (estimado):** 50
- **Tamanho aprox. (MB):** 0.05

| Coluna | Tipo | Chave | Nulo | Padrão | Comentário |
|--------|------|-------|------|--------|------------|
| `produto_id` | `int` | PK | NO | NULL | ID do produto |
| `nome` | `varchar(100)` | | NO | NULL | Nome do produto |
| `preco` | `decimal(10,2)` | | NO | 0.00 | Preço do produto |
| `descricao` | `text` | | YES | NULL | Descrição detalhada |
