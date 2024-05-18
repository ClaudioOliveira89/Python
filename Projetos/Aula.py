def merge_sort(V, p, r):
    if p < r:
        q = (p + r) // 2
        merge_sort(V, p, q)
        merge_sort(V, q + 1, r)
        merge(V, p, q, r)

def merge(V, p, q, r):
    n1 = q - p + 1
    n2 = r - q
    L = [0] * (n1 + 1)
    R = [0] * (n2 + 1)
    
    for i in range(n1):
        L[i] = V[p + i]
    for j in range(n2):
        R[j] = V[q + j + 1]
        
    L[n1] = float('inf')
    R[n2] = float('inf')
    i = j = 0
    
    for k in range(p, r + 1):
        if L[i] <= R[j]:
            V[k] = L[i]
            i += 1
        else:
            V[k] = R[j]
            j += 1

# Exemplo de uso
V = [5, 2, 4, 7, 1, 3]
merge_sort(V, 0, len(V) - 1)
print("Lista ordenada:", V)