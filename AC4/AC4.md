# AC04 — Comparação dos modelos de iluminação Lambert, Phong e Blinn-Phong

**Aluno(a):** [Nome Sobrenome]
**Arquivo:** AC04_NomeSobrenome.blend
**Ferramenta:** Blender 4.5 LTS — motor de render Cycles (256 amostras)

## 1. Objetos e materiais aplicados

A cena da AP1 foi preservada: a palavra Ibmec, a composição e o enquadramento da câmera não foram alterados. Os testes foram feitos apenas nos três objetos autorais.

| Objeto autoral | Material aplicado | Modelo representado |
|---|---|---|
| [Objeto 1] | MAT_Lambert | Lambert (difuso) |
| [Objeto 2] | MAT_Phong | Phong (difuso + especular) |
| [Objeto 3] | MAT_BlinnPhong | Blinn-Phong (difuso + especular com vetor médio) |

No Outliner, as luzes foram reunidas na coleção **Luzes**. Os materiais têm nomes padronizados com o prefixo `MAT_` e estão marcados com *fake user*, para serem mantidos no arquivo.

## 2. Configuração da iluminação

| Parâmetro | Luz principal (`LUZ_Principal`) | Luz de preenchimento (`LUZ_Preenchimento`) |
|---|---|---|
| Tipo | Area | Area |
| Potência | 800 W | 120 W |
| Tamanho | 1,5 m | 4,0 m |
| Cor (RGB) | (1,00; 0,97; 0,92), branco levemente quente | (1,00; 1,00; 1,00), branco |
| Posição | centro dos objetos + (4; −4; 5) m, lateral e acima, cerca de 45° | centro dos objetos + (−5; −3; 2) m, lado oposto e mais baixa |
| Orientação | apontada para o centro dos três objetos | apontada para o centro dos três objetos |

A luz principal foi posicionada de lado e acima para criar uma transição clara entre as áreas iluminadas e as sombras e para gerar highlights visíveis nos objetos polidos. A luz de preenchimento é grande e fraca, para suavizar as sombras sem competir com a principal. Posição, intensidade, cor das luzes e enquadramento da câmera foram mantidos iguais em todas as imagens comparativas.

Posição e rotação absolutas (copiadas do texto `AC04_valores`): [preencher]

## 3. Parâmetros dos materiais

Todos os materiais usam o **Principled BSDF** com Metallic = 0. No Blender 4.5, a intensidade especular é controlada pelo parâmetro **IOR Level** (Specular > IOR Level).

| Material | Cor-base (RGB linear) | Roughness | IOR Level | Metallic |
|---|---|---|---|---|
| MAT_Lambert | (0,80; 0,10; 0,08), vermelho | 1,0 | 0,0 | 0,0 |
| MAT_Phong | (0,08; 0,25; 0,80), azul | 0,2 | 0,5 | 0,0 |
| MAT_BlinnPhong | (0,10; 0,65; 0,15), verde | 0,1 | 0,8 | 0,0 |

As cores-base são distintas para facilitar a identificação de cada material nas imagens.

## 4. Comparação das aparências observadas

**MAT_Lambert.** A superfície tem aparência totalmente fosca. O brilho varia apenas com o ângulo entre a superfície e a luz: as faces voltadas para a luz principal ficam mais claras e as demais escurecem de forma gradual. Não há highlight visível, e a aparência não muda quando o ponto de vista muda. Esse é o comportamento previsto pelo modelo de Lambert, em que a intensidade depende só de N·L.

**MAT_Phong.** A cor-base continua sendo a componente dominante, mas aparece um brilho especular concentrado nas regiões em que a direção da reflexão da luz se aproxima da direção da câmera. Com rugosidade 0,2, o highlight é bem definido, porém ainda tem bordas suaves e uma área moderada. A superfície parece polida, como um plástico acetinado.

**MAT_BlinnPhong.** Com rugosidade 0,1 e IOR Level 0,8, este é o material de aspecto mais polido. O highlight é o menor, o mais intenso e o de contorno mais nítido entre os três, e a superfície também reflete um pouco do ambiente.

**Influência do ângulo da luz.** Nos testes com a luz principal girada temporariamente, o MAT_Lambert só mudou na distribuição de claro e escuro. Nos materiais especulares, os highlights mudaram de posição e de forma. Com iluminação rasante, os reflexos ficaram mais alongados e o efeito Fresnel deixou as bordas mais claras. Ao final dos testes, a luz foi restaurada à configuração original.

**Rugosidade.** A rugosidade foi o parâmetro que mais diferenciou os materiais. Quanto menor o valor, menor e mais concentrado o highlight. O IOR Level controlou principalmente a intensidade do reflexo, e não o seu tamanho.

[Ajustar este texto conforme o que aparece nos seus renders.]

## 5. Limitação: aproximações no Principled BSDF

O Principled BSDF do Blender 4.5 é um shader baseado em princípios físicos. Ele usa um modelo de microfacetas (GGX), com conservação de energia e efeito Fresnel. Ele **não implementa literalmente** as equações clássicas:

- **Lambert:** I = k_d · max(0, N·L)
- **Phong:** I = k_d · (N·L) + k_s · (R·V)ⁿ
- **Blinn-Phong:** I = k_d · (N·L) + k_s · (N·H)ⁿ, com H = (L + V) / |L + V|

Os parâmetros Roughness e IOR Level não correspondem diretamente ao expoente de brilho *n* nem ao coeficiente especular *k_s*. Por isso, os materiais MAT_Phong e MAT_BlinnPhong são **aproximações visuais**, e a diferença entre eles na cena vem dos valores de rugosidade e intensidade especular escolhidos, e não de uma troca real de equação. Na teoria, com o mesmo expoente, o Blinn-Phong produz um highlight *mais largo* que o Phong, e precisa de um expoente cerca de quatro vezes maior para ficar com aparência parecida. Na cena, o MAT_BlinnPhong recebeu rugosidade menor justamente para tornar a comparação visível.

O MAT_Lambert com rugosidade 1,0 e IOR Level 0 é a configuração mais próxima do modelo clássico. Uma alternativa ainda mais direta é o nó Diffuse BSDF com Roughness 0.

## 6. Imagens

- `AC04_render_final.png` — render final da cena, com a palavra Ibmec legível e os três objetos autorais visíveis.
- `AC04_comparativo.png` — os três objetos e seus materiais sob a mesma iluminação.
- `AC04_teste_angulo.png` (opcional) — teste com a luz principal girada.
