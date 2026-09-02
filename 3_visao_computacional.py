"""
AREA 3 - VISAO COMPUTACIONAL (VISAO ARTIFICIAL)
Aplicacao: deteccao de face com classificador Haar Cascade (Viola-Jones,
2001) - classificador pre-treinado publico, distribuido dentro do proprio
pacote OpenCV (haarcascade_frontalface_default.xml).

Diferenca chave em relacao ao Processamento de Imagens: a saida NAO e mais
uma imagem, e sim uma INTERPRETACAO/DECISAO simbolica sobre o conteudo da
cena ("ha um rosto humano nesta regiao [x,y,w,h]"). A VC tenta replicar uma
capacidade cognitiva (reconhecer/entender), enquanto o processamento de
imagens apenas transforma pixels.
"""
import cv2
from skimage import data
import matplotlib.pyplot as plt

img_rgb = data.astronaut()
img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# classificador pre-treinado publico, incluso no OpenCV
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
print(f"Rostos detectados: {len(faces)}")

out = img_rgb.copy()
for (x, y, w, h) in faces:
    cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 4)
    cv2.putText(out, "face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 0), 2)

plt.figure(figsize=(6, 6))
plt.imshow(out)
plt.title(f"Deteccao de face (Haar Cascade / Viola-Jones) - {len(faces)} face(s)")
plt.axis("off")
plt.tight_layout()
plt.savefig("/home/claude/cv_areas/out_3_visao.png", dpi=130)
print("Salvo -> out_3_visao.png")
