"""
AREA 4 - VISUALIZACAO COMPUTACIONAL (Scientific / Data Visualization)
Aplicacao: visualizacao de um dataset cientifico multidimensional
(Iris dataset, 4 variaveis numericas, sem nenhuma natureza visual/espacial
intrinseca) transformado em graficos 3D e mapas de calor para permitir
compreensao humana de padroes.

Diferenca chave: a ENTRADA aqui e DADO ABSTRATO (nao e uma cena 3D como na
Sintese, nem uma imagem como no Processamento/Visao). A tarefa da
Visualizacao Computacional e projetar/mapear dados (que podem nao ter
nenhuma geometria natural) em uma representacao grafica que revele
estrutura, tendencias e relacoes.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

iris = load_iris()
X, y, names = iris.data, iris.target, iris.target_names

pca = PCA(n_components=3)
X3 = pca.fit_transform(X)

fig = plt.figure(figsize=(14, 6))

# (a) dispersao 3D apos reducao de dimensionalidade (PCA): dado abstrato -> geometria
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
colors = ["#e74c3c", "#2ecc71", "#3498db"]
for i, name in enumerate(names):
    m = y == i
    ax1.scatter(X3[m, 0], X3[m, 1], X3[m, 2], label=name, color=colors[i], s=45, alpha=0.85)
ax1.set_xlabel("PC1")
ax1.set_ylabel("PC2")
ax1.set_zlabel("PC3")
ax1.set_title("PCA 3D: 4 variaveis -> espaco visual")
ax1.legend()

# (b) mapa de calor de correlacao entre as variaveis originais
ax2 = fig.add_subplot(1, 2, 2)
corr = np.corrcoef(X.T)
im = ax2.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax2.set_xticks(range(4)); ax2.set_xticklabels(iris.feature_names, rotation=45, ha="right")
ax2.set_yticks(range(4)); ax2.set_yticklabels(iris.feature_names)
for i in range(4):
    for j in range(4):
        ax2.text(j, i, f"{corr[i,j]:.2f}", ha="center", va="center", fontsize=9)
ax2.set_title("Mapa de calor: correlacao entre variaveis")
fig.colorbar(im, ax=ax2, shrink=0.8)

plt.tight_layout()
plt.savefig("/home/claude/cv_areas/out_4_visualizacao.png", dpi=130)
print("Salvo -> out_4_visualizacao.png")
print("Variancia explicada pelos 3 componentes:", pca.explained_variance_ratio_.round(3))
