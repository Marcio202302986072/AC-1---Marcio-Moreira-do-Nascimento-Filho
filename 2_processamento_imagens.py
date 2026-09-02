"""
AREA 2 - PROCESSAMENTO DE IMAGENS
Aplicacao: pipeline classico de filtros (OpenCV) sobre uma imagem real ja
existente (foto). Diferente da Sintese, aqui a ENTRADA e a SAIDA sao ambas
imagens (imagem -> imagem). Nao ha interpretacao/decisao sobre o conteudo
(isso seria Visao Computacional): apenas transformacoes matematicas de
pixel a pixel ou de vizinhanca (convolucao, equalizacao de histograma etc).
"""
import cv2
import numpy as np
from skimage import data
import matplotlib.pyplot as plt

# imagem de exemplo padrao, ja embutida no scikit-image (foto real)
img_rgb = data.astronaut()
img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# 1) suavizacao (filtro de convolucao Gaussiano) - reduz ruido
blur = cv2.GaussianBlur(img_bgr, (15, 15), 0)

# 2) deteccao de bordas (Canny) - realca transicoes de intensidade
edges = cv2.Canny(gray, 100, 200)

# 3) equalizacao de histograma - realca contraste
eq = cv2.equalizeHist(gray)

# 4) operador morfologico (realce/erosao) sobre as bordas
kernel = np.ones((3, 3), np.uint8)
edges_dilated = cv2.dilate(edges, kernel, iterations=1)

fig, axs = plt.subplots(2, 3, figsize=(14, 9))
titles = ["Original", "Escala de cinza", "Desfoque Gaussiano (convolucao)",
          "Bordas - Canny", "Bordas dilatadas (morfologia)", "Equalizacao de histograma"]
imgs = [img_rgb, gray, cv2.cvtColor(blur, cv2.COLOR_BGR2RGB), edges, edges_dilated, eq]
cmaps = [None, "gray", None, "gray", "gray", "gray"]

for ax, im, t, cm in zip(axs.ravel(), imgs, titles, cmaps):
    ax.imshow(im, cmap=cm)
    ax.set_title(t, fontsize=11)
    ax.axis("off")

plt.tight_layout()
plt.savefig("/home/claude/cv_areas/out_2_processamento.png", dpi=130)
print("Salvo -> out_2_processamento.png")
