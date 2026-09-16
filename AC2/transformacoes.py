import numpy as np
import matplotlib.pyplot as plt
import os

OUT = "/home/claude/plots"
os.makedirs(OUT, exist_ok=True)


def plot_shapes(original, transformed, title, filename, is_point=False):
    plt.figure(figsize=(5, 5))
    if is_point:
        plt.scatter(*original[0], color="tab:blue", s=80, label="Original", zorder=3)
        plt.scatter(*transformed[0], color="tab:red", s=80, label="Transformado", zorder=3)
        plt.annotate(f"P{tuple(np.round(original[0],2))}", original[0],
                     textcoords="offset points", xytext=(8, 8))
        plt.annotate(f"P'{tuple(np.round(transformed[0],2))}", transformed[0],
                     textcoords="offset points", xytext=(8, -12))
    else:
        orig_closed = np.vstack([original, original[0]])
        trans_closed = np.vstack([transformed, transformed[0]])
        plt.plot(orig_closed[:, 0], orig_closed[:, 1], "o-", color="tab:blue", label="Original")
        plt.plot(trans_closed[:, 0], trans_closed[:, 1], "o--", color="tab:red", label="Transformado")

    plt.axhline(0, color="gray", linewidth=0.8)
    plt.axvline(0, color="gray", linewidth=0.8)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.axis("equal")
    plt.savefig(f"{OUT}/{filename}", dpi=120, bbox_inches="tight")
    plt.close()


def rotate(points, angle_deg, clockwise=False):
    theta = np.radians(angle_deg)
    if clockwise:
        theta = -theta
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    return points @ R.T


results = {}

# Exercício 1: Translação simples
P1 = np.array([[2, 3]])
P1t = P1 + np.array([4, -2])
plot_shapes(P1, P1t, "Exercício 1 - Translação Simples", "ex1.png", is_point=True)
results["ex1"] = P1t[0]

# Exercício 2: Escala uniforme
tri2 = np.array([[1, 1], [3, 1], [2, 4]])
tri2s = tri2 * 2
plot_shapes(tri2, tri2s, "Exercício 2 - Escala Uniforme (fator 2)", "ex2.png")
results["ex2"] = tri2s

# Exercício 3: Escala não uniforme
tri3s = tri2 * np.array([2, 0.5])
plot_shapes(tri2, tri3s, "Exercício 3 - Escala Não Uniforme (2x, 0.5y)", "ex3.png")
results["ex3"] = tri3s

# Exercício 4: Rotação em torno da origem
P4 = np.array([[1, 0]])
P4r = rotate(P4, 90, clockwise=False)
plot_shapes(P4, P4r, "Exercício 4 - Rotação 90° Anti-horário", "ex4.png", is_point=True)
results["ex4"] = P4r[0]

# Exercício 5: Rotação de um polígono
quad5 = np.array([[1, 1], [1, 4], [4, 4], [4, 1]])
quad5r = rotate(quad5, 45, clockwise=True)
plot_shapes(quad5, quad5r, "Exercício 5 - Rotação 45° Horário", "ex5.png")
results["ex5"] = quad5r

# Exercício 6: Reflexão simples (eixo y)
P6 = np.array([[2, 5]])
P6r = P6 * np.array([-1, 1])
plot_shapes(P6, P6r, "Exercício 6 - Reflexão em relação ao eixo Y", "ex6.png", is_point=True)
results["ex6"] = P6r[0]

# Exercício 7: Reflexão de um triângulo (eixo x)
tri7 = np.array([[2, 3], [4, 3], [3, 5]])
tri7r = tri7 * np.array([1, -1])
plot_shapes(tri7, tri7r, "Exercício 7 - Reflexão em relação ao eixo X", "ex7.png")
results["ex7"] = tri7r

# Exercício 8: Cisalhamento horizontal
P8 = np.array([[2, 3]])
k = 2
Shear = np.array([[1, k], [0, 1]])
P8s = P8 @ Shear.T
plot_shapes(P8, P8s, "Exercício 8 - Cisalhamento Horizontal (k=2)", "ex8.png", is_point=True)
results["ex8"] = P8s[0]

# Exercício 9: Composição de transformações
P9 = np.array([[3, 2]])
P9_1 = P9 + np.array([1, -1])           # translação
P9_2 = rotate(P9_1, 90, clockwise=False)  # rotação
P9_3 = P9_2 * 2                          # escala
plot_shapes(P9, P9_3, "Exercício 9 - Composição de Transformações", "ex9.png", is_point=True)
results["ex9"] = P9_3[0]
results["ex9_steps"] = (P9_1[0], P9_2[0], P9_3[0])

# Exercício 10: Combinação de transformações em uma figura
rect10 = np.array([[1, 1], [5, 1], [5, 3], [1, 3]])
r10_1 = rect10 + np.array([-2, 3])            # translação
r10_2 = r10_1 * np.array([1.5, 0.5])          # escala não uniforme
r10_3 = r10_2 * np.array([-1, 1])             # reflexão eixo y
plot_shapes(rect10, r10_3, "Exercício 10 - Combinação de Transformações", "ex10.png")
results["ex10"] = r10_3

# Impressão dos resultados no console
print("=== RESULTADOS ===")
for k_, v in results.items():
    print(k_, ":", v)
