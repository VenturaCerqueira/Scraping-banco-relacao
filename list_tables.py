import os
import pymysql
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

# --- Configurações do Banco de Dados ---
try:
    host = os.getenv("MYSQL_HOST").strip()
    port = int(os.getenv("MYSQL_PORT").strip())
    user = os.getenv("MYSQL_USER").strip()
    password = os.getenv("MYSQL_PASSWORD").strip()
    database = os.getenv("MYSQL_DB").strip()
except AttributeError as e:
    print(f"❌ Erro: Uma ou mais variáveis de ambiente do MySQL não foram definidas ou estão vazias. Verifique seu arquivo .env. Detalhes: {e}")
    exit(1) 

output_file = f"{database}_schema.md"

def lower_keys(d):
    """Converte todas as chaves do dicionário para minúsculas para evitar KeyError."""
    return {k.lower(): v for k, v in d.items()}

def format_number(num):
    """Formata números com separador de milhares."""
    return f"{num:,.0f}".replace(",", ".") 

try:
    print("🔄 Conectando ao banco...")
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5
    )
    print("✅ Conectado com sucesso!\n")

    markdown = f"# 📦 Estrutura do Banco de Dados `{database}`\n\n"

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                table_name,
                engine,
                table_collation,
                table_comment,
                create_time,
                update_time,
                table_rows,
                ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
            FROM information_schema.tables
            WHERE table_schema = %s
            ORDER BY table_name
        """, (database,))
        tables = cursor.fetchall()

        if not tables:
            print("⚠️ Nenhuma tabela encontrada no banco de dados especificado.")
        else:
            for table_raw in tables:
                table = lower_keys(table_raw)
                tname = table["table_name"]
                engine = table["engine"]
                collation = table["table_collation"]
                comment = table["table_comment"] or '-' 
                create_time = table["create_time"]
                update_time_str = str(table["update_time"]) if table["update_time"] else "Nunca"
                rows = format_number(table["table_rows"]) if table["table_rows"] is not None else '0'
                size = table["size_mb"]

                markdown += f"## 🗂️ Tabela: `{tname}`\n\n"
                markdown += f"- **Engine:** {engine}\n"
                markdown += f"- **Collation:** {collation}\n"
                markdown += f"- **Comentário da tabela:** {comment}\n"
                markdown += f"- **Criada em:** {create_time}\n"
                markdown += f"- **Última atualização:** {update_time_str}\n"
                markdown += f"- **Número de linhas (estimado):** {rows}\n"
                markdown += f"- **Tamanho aprox. (MB):** {size}\n\n"

                markdown += "| Coluna | Tipo | Chave | Nulo | Padrão | Comentário |\n"
                markdown += "|--------|------|-------|------|--------|------------|\n"

                cursor.execute("""
                    SELECT
                        c.column_name,
                        c.column_type,
                        c.column_key,
                        c.is_nullable,
                        c.column_default,
                        c.column_comment,
                        k.referenced_table_name,
                        k.referenced_column_name
                    FROM information_schema.columns c
                    LEFT JOIN information_schema.key_column_usage k
                        ON c.table_schema = k.table_schema
                        AND c.table_name = k.table_name
                        AND c.column_name = k.column_name
                        AND k.referenced_table_name IS NOT NULL
                    WHERE c.table_schema = %s AND c.table_name = %s
                    ORDER BY c.ordinal_position
                """, (database, tname))
                columns_raw = cursor.fetchall()

                for col_raw in columns_raw:
                    col = lower_keys(col_raw)
                    col_name = col["column_name"]
                    col_type = col["column_type"]
                    col_key = col["column_key"]
                    is_nullable = col["is_nullable"]
                    
                    
                    col_default = col["column_default"]
                    default_str = "NULL" if col_default is None else str(col_default)
                    
                    col_comment = col["column_comment"] or ""
                    fk_table = col["referenced_table_name"]
                    fk_column = col["referenced_column_name"]

                    key_info = ""
                    if col_key == "PRI":
                        key_info = "PK"
                    elif fk_table:
                        key_info = f"FK → {fk_table}.{fk_column}"

                    markdown += f"| `{col_name}` | `{col_type}` | {key_info} | {is_nullable} | {default_str} | {col_comment} |\n"

                markdown += "\n---\n\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ Exportação concluída: `{output_file}`")

except pymysql.MySQLError as e:
    print(f"❌ Erro no MySQL: {e}")

except Exception as e:
    print(f"❌ Erro inesperado: {e}")

finally:
    if 'connection' in locals() and connection:
        connection.close()
        print("🔌 Conexão encerrada.")