import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Conecta ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="seu_banco_de_dados",
    user="seu_usuario",
    password="sua_senha",
    host="localhost"
)
cursor = conn.cursor()

# Consulta clientes com aniversário hoje
hoje = datetime.today().strftime('%Y-%m-%d')
cursor.execute("SELECT nome, email FROM clientes WHERE data_nascimento = %s AND email_enviado = FALSE", (hoje,))
clientes_aniversario = cursor.fetchall()

# Envia e-mails para os clientes com aniversário hoje
for cliente in clientes_aniversario:
    nome, email = cliente
    msg = MIMEMultipart()
    msg['From'] = 'seu_email@gmail.com'
    msg['To'] = email
    msg['Subject'] = 'Feliz Aniversário!'
    body = f'Olá {nome},\n\nFeliz aniversário! Esperamos que você tenha um dia maravilhoso.\n\nAtenciosamente,\nSua Loja Favorita'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('seu_email@gmail.com', 'sua_senha')
    text = msg.as_string()
    server.sendmail('seu_email@gmail.com', email, text)
    server.quit()

    # Atualiza o status de e-mail enviado para True
    cursor.execute("UPDATE clientes SET email_enviado = TRUE WHERE email = %s", (email,))
    conn.commit()

# Fecha conexão com o banco de dados
cursor.close()
conn.close()
