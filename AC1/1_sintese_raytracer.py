"""
AREA 1 - SINTESE DE IMAGENS (COMPUTACAO GRAFICA)
Aplicacao: Ray Tracer simples (Whitted-style ray tracing)

Conceito da area: partir de um MODELO 3D (geometria, materiais, luzes, camera)
descrito matematicamente e GERAR uma imagem 2D que ainda nao existe.
E o processo inverso da Visao Computacional: aqui criamos pixels a partir
de uma descricao da cena (sintese), nao extraimos informacao de uma imagem
ja existente.

Algoritmo classico de ray tracing (baseado no algoritmo padrao descrito por
Whitted 1980, amplamente reproduzido em repositorios publicos de raytracers
educacionais em Python, ex: "Ray Tracing in One Weekend" / raytracer minimalista
de Cyrille Rossant). Implementacao propria abaixo, do zero, em numpy puro.
"""
import numpy as np
from PIL import Image
import time

W, H = 480, 320

def normalize(v):
    return v / np.linalg.norm(v)

class Sphere:
    def __init__(self, center, radius, color, spec=0.6, refl=0.25):
        self.center = np.array(center, dtype=float)
        self.radius = radius
        self.color = np.array(color, dtype=float)
        self.spec = spec
        self.refl = refl

    def intersect(self, O, D):
        # Interseccao raio-esfera (equacao quadratica)
        OC = O - self.center
        b = 2 * np.dot(D, OC)
        c = np.dot(OC, OC) - self.radius ** 2
        disc = b ** 2 - 4 * c
        if disc > 0:
            distSqrt = np.sqrt(disc)
            q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
            t0 = q
            t1 = c / q if q != 0 else 1e9
            t0, t1 = min(t0, t1), max(t0, t1)
            if t1 >= 0:
                return t1 if t0 < 0 else t0
        return np.inf

scene = [
    Sphere([-0.6, 0.1, 1.2], 0.6, [0.85, 0.15, 0.15]),   # esfera vermelha
    Sphere([0.9, -0.15, 2.3], 0.5, [0.15, 0.35, 0.9]),   # esfera azul
    Sphere([0.0, -9999.5, 0.0], 9999.0, [0.35, 0.35, 0.35]),  # "chao"
]

L = np.array([5.0, 5.0, -3.0])       # posicao da luz
O = np.array([0.0, 0.35, -1.0])      # posicao da camera
color_bg = np.array([0.55, 0.75, 0.95])
ambient = 0.05
light_color = np.array([1.0, 1.0, 1.0])

def trace_ray(O, D, depth=0):
    t_min, obj_min = np.inf, None
    for obj in scene:
        t = obj.intersect(O, D)
        if t < t_min:
            t_min, obj_min = t, obj
    if obj_min is None:
        return color_bg
    P = O + t_min * D                       # ponto de interseccao
    N = normalize(P - obj_min.center)       # normal da superficie
    toL = normalize(L - P)
    toO = normalize(O - P)

    # sombra: lanca raio secundario em direcao a luz
    shadow = False
    for obj in scene:
        if obj is obj_min:
            continue
        t_s = obj.intersect(P + N * 1e-4, toL)
        if t_s < np.inf:
            shadow = True
            break

    col = ambient * obj_min.color
    if not shadow:
        # difuso (Lambert) + especular (Blinn-Phong)
        diff = max(np.dot(N, toL), 0.0)
        col = col + obj_min.color * diff * light_color
        H_ = normalize(toL + toO)
        spec = max(np.dot(N, H_), 0.0) ** 60
        col = col + obj_min.spec * spec * light_color

    # reflexao recursiva (efeito espelhado, limitado a 2 niveis)
    if depth < 2 and obj_min.refl > 0:
        R = D - 2 * np.dot(D, N) * N
        col = col + obj_min.refl * trace_ray(P + N * 1e-4, normalize(R), depth + 1)
    return col

t0 = time.time()
img = np.zeros((H, W, 3))
ratio = W / H
for j, y in enumerate(np.linspace(1, -1, H)):
    for i, x in enumerate(np.linspace(-1, 1, W)):
        D = normalize(np.array([x * ratio, y, 1.0]) - np.array([0, 0, -1]))
        col = trace_ray(O, D)
        img[j, i] = np.clip(col, 0, 1)

Image.fromarray((img * 255).astype(np.uint8)).save("/home/claude/cv_areas/out_1_sintese.png")
print(f"Renderizado em {time.time()-t0:.2f}s -> out_1_sintese.png")
