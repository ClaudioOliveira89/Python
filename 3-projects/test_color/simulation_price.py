import numpy as np
import matplotlib.pyplot as plt

# Parâmetros
preco_inicial = 100
retorno_esperado = 0.12      # 12% ao ano
volatilidade = 0.25          # 25% ao ano
anos = 1
dias_por_ano = 252
simulacoes = 1000

# Configuração
dias = anos * dias_por_ano
dt = 1 / dias_por_ano

rng = np.random.default_rng(42)

# Choques aleatórios
z = rng.normal(0, 1, size=(dias, simulacoes))

# Movimento Browniano Geométrico
retornos = (retorno_esperado - 0.5 * volatilidade ** 2) * dt + volatilidade * np.sqrt(dt) * z

precos = preco_inicial * np.exp(np.cumsum(retornos, axis=0))

# Adiciona o preço inicial no começo
precos = np.vstack([np.full(simulacoes, preco_inicial), precos])

# Gráfico
plt.figure(figsize=(12, 6))
plt.plot(precos[:, :50])
plt.title("Simulação Monte Carlo - Preço do Ativo")
plt.xlabel("Dias")
plt.ylabel("Preço")
plt.grid(True)
plt.show()

# Estatísticas finais
precos_finais = precos[-1]

print(f"Preço médio final: R$ {np.mean(precos_finais):.2f}")
print(f"Mediana final: R$ {np.median(precos_finais):.2f}")
print(f"Pior 5% dos cenários: R$ {np.percentile(precos_finais, 5):.2f}")
print(f"Melhor 5% dos cenários: R$ {np.percentile(precos_finais, 95):.2f}")
print(f"Probabilidade de terminar abaixo do inicial: {np.mean(precos_finais < preco_inicial) * 100:.2f}%")