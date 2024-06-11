def partition(arr, p, r):
    x = arr[r]  # Pivô
    i = p - 1

    for j in range(p, r):
        if arr[j] <= x:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    return i + 1

# Vetor dado
V = [9, 4, 3, 5, 1, 2]
# Chamando o Partition
partition(V, 0, len(V) - 1)
print("Vetor após Partition:", V)