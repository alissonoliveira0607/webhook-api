# Importando bibliotecas necessárias
import os
import sys
import time
import pymysql

# Função para aguardar o banco de dados ficar disponível
def wait_for_db(host, port, user, password, max_attempts=60, delay=15):
    attempts = 0
    while attempts < max_attempts:
        try:
            # Tenta fazer uma conexão ao banco de dados MySQL
            pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            # Se a conexão for bem-sucedida, imprime "Database is ready!" e retorna True
            print("Database is ready!")
            return True
        except pymysql.Error as e:
            # Se ocorrer um erro na conexão, imprime uma mensagem de erro e tenta novamente após um atraso
            print(f"Database connection attempt {attempts + 1}/{max_attempts} failed: {e}")
            attempts += 1
            time.sleep(delay)
    # Se o número máximo de tentativas for atingido sem sucesso, retorna False
    return False

if __name__ == "__main__":
    # Obtém informações do banco de dados a partir de variáveis de ambiente ou usa valores padrão
    db_host = os.environ.get('DB_HOST')
    db_port = int(os.environ.get('DB_PORT', 3306))
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')

    # Chama a função wait_for_db para esperar que o banco de dados fique disponível
    if wait_for_db(db_host, db_port, db_user, db_password):
        # Se o banco de dados estiver pronto, imprime "Starting Flask app..."
        print("Starting Flask app...")
        # Inicia o aplicativo Flask usando o comando "flask run --host=0.0.0.0"
        os.execvp("flask", ["flask", "run", "--host=0.0.0.0"])
    else:
        # Se a função wait_for_db retornar False (ou seja, falhou em se conectar ao banco de dados),
        # imprime "Failed to connect to the database. Exiting..." e sai com código de erro 1.
        print("Failed to connect to the database. Exiting...")
        sys.exit(1)
