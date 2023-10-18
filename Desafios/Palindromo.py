#Palindrome.

#Criando a função is_palindrome para o max_palindrome.

def is_palindrome(str): #declarando a função
    size = len(str) #cálcula o tamanho da String.
    if size == 0: #verifica se a String está vazia.
        return False #se não retorna como falso.
    return all(str[i] == str[size - i - 1] for i in range(0, size // 2)) #verifica se é o palindromo.


#Criando o Palindromo.
#  
def maior_palindromo(): #declarando a função.
    max_palindrome = 0  #iniciando do zero.
    for i in range(999, 99, -1):  #o loop da sequência com três digitos.
        for j in range(i, 99, -1):  #o loop da sequência com dois digitos.
            product = i * j  #calculando o produto dos valores.
            if is_palindrome(str(product)) and product > max_palindrome: #verificando se o produto é maior.
                max_palindrome = product #atualiza os valores

    return max_palindrome

print(maior_palindromo())            
