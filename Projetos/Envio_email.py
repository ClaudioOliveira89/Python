import win32com.client as win32

# Criando a integração com o Outlook
outlook = win32.Dispatch('outlook.application')

# Criando um e-mail
email = outlook.CreateItem(0)  # 0 significa email padrão (olMailItem)

# Definindo destinatário, assunto e corpo do e-mail
email.To = "@gmail.com; @hotmail.com"
email.Subject = "Assunto"
email.HTMLBody = """ 
<p>Olá Claudio, aqui é o código Python</p> 

<p>O código vai funcionar com o escopo do e-mail aqui.</p>
<p>Não se pode esquecer da tag de parágrafo.</p>

<p>Assim será o email.</p>
"""

# Adicionando anexo ao e-mail
 anexo = "C://Users/arquivo.xlsx"
 email.Attachments.Add(anexo)

# Enviando o e-mail
email.Send()
print("E-mail enviado")