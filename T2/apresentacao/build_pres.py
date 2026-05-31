"""Gera apresentacao.pdf — slides em paisagem para a apresentacao de 5 min."""
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

PAGE = landscape(A4)
W, H = PAGE

# paleta (tons de azul, alinhada ao material da disciplina)
BLUE = colors.HexColor("#1f6fb2")
DARK = colors.HexColor("#1b3a5b")
LIGHT = colors.HexColor("#eef4fa")
GREY = colors.HexColor("#444444")

title_style = ParagraphStyle(
    "title", fontName="Helvetica-Bold", fontSize=30, textColor=DARK,
    leading=34, alignment=TA_LEFT)
sub_style = ParagraphStyle(
    "sub", fontName="Helvetica-Bold", fontSize=15, textColor=BLUE, leading=20)
body_style = ParagraphStyle(
    "body", fontName="Helvetica", fontSize=14, textColor=GREY, leading=21)
bullet_style = ParagraphStyle(
    "bullet", fontName="Helvetica", fontSize=14, textColor=GREY, leading=21,
    leftIndent=16, bulletIndent=2)
small = ParagraphStyle(
    "small", fontName="Helvetica", fontSize=11, textColor=GREY, leading=16)
code_style = ParagraphStyle(
    "code", fontName="Courier", fontSize=11.5, textColor=DARK, leading=16,
    backColor=LIGHT, leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4)


def header(c, kicker):
    c.setFillColor(BLUE)
    c.rect(0, H - 1.0 * cm, W, 1.0 * cm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1.5 * cm, H - 0.68 * cm, kicker)
    c.setFont("Helvetica", 10)
    c.drawRightString(W - 1.5 * cm, H - 0.68 * cm,
                      "Resolução de Problemas com Grafos — Unidade 3")


def footer(c, n):
    c.setFillColor(GREY)
    c.setFont("Helvetica", 9)
    c.drawString(1.5 * cm, 0.6 * cm, "Codeforces 449B — Jzzhu and Cities")
    c.drawRightString(W - 1.5 * cm, 0.6 * cm, f"{n}")


def flow(c, items, x, y, w, h):
    """Desenha uma sequencia de Paragraphs num frame."""
    fr = Frame(x, y, w, h, leftPadding=0, rightPadding=0,
               topPadding=0, bottomPadding=0, showBoundary=0)
    fr.addFromList(list(items), c)


def bullets(texts, style=bullet_style):
    return [Paragraph("• " + t, style) for t in texts]


c = canvas.Canvas("apresentacao.pdf", pagesize=PAGE)

# ---------------- Slide 1: capa ----------------
c.setFillColor(BLUE)
c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 13)
c.drawString(1.5 * cm, H - 2.0 * cm, "CENTRO DE CIÊNCIAS TECNOLÓGICAS")
c.setFont("Helvetica-Bold", 40)
c.drawString(1.5 * cm, H / 2 + 1.2 * cm, "Jzzhu and Cities")
c.setFont("Helvetica", 20)
c.drawString(1.5 * cm, H / 2 - 0.2 * cm,
             "Caminhos mínimos com Dijkstra e análise de arestas redundantes")
c.setFont("Helvetica", 14)
c.drawString(1.5 * cm, H / 2 - 1.6 * cm, "Codeforces 449B  •  Grupo F  •  Python 3")
c.setFont("Helvetica", 12)
c.drawString(1.5 * cm, 1.4 * cm, "Trabalho Prático 2  —  Prof. Me. Ricardo Carubbi")
c.showPage()

# ---------------- Slide 2: problema + modelagem ----------------
header(c, "1 · PROBLEMA E MODELAGEM")
c.setFillColor(DARK)
left = [
    Paragraph("O problema", sub_style),
    Paragraph("n cidades, capital = cidade 1. Há <b>estradas</b> "
              "bidirecionais (peso x) e <b>rotas de trem</b> ligando a capital "
              "a uma cidade (peso y).", body_style),
    Paragraph("Queremos fechar o <b>máximo de rotas de trem</b> sem que a "
              "distância mínima de nenhuma cidade até a capital mude.", body_style),
    Paragraph("Modelagem como grafo", sub_style),
]
left += bullets([
    "<b>Vértices:</b> as n cidades; origem s = 1.",
    "<b>Arestas-estrada:</b> (u, v) bidirecional, peso x.",
    "<b>Arestas-trem:</b> (1, c) bidirecional, peso y.",
    "Grafo não-direcionado ⇒ distância cidade→capital = capital→cidade.",
    "Pesos ≥ 1 (não negativos) ⇒ Dijkstra é aplicável.",
])
flow(c, left, 1.5 * cm, 1.3 * cm, 14.5 * cm, H - 3.2 * cm)

right = [
    Paragraph("Restrição que define a solução", sub_style),
    Paragraph("Um trem para a cidade c só é necessário quando é a "
              "<b>única</b> forma de manter a distância mínima de c. "
              "Caso contrário, pode ser fechado.", body_style),
    Paragraph("Limites", sub_style),
]
right += bullets([
    "n ≤ 10⁵ ;  m ≤ 3·10⁵ ;  k ≤ 10⁵",
    "x, y ≤ 10⁹  (somas cabem em inteiros grandes).",
    "Conectividade garantida pelo enunciado.",
])
flow(c, right, 16.8 * cm, 1.3 * cm, W - 16.8 * cm - 1.5 * cm, H - 3.2 * cm)
footer(c, 2)
c.showPage()

# ---------------- Slide 3: estrategia / Dijkstra ----------------
header(c, "2 · ESTRATÉGIA COM DIJKSTRA")
items = [
    Paragraph("Um único Dijkstra a partir da capital", sub_style),
    Paragraph("Rodamos Dijkstra sobre estradas + a <b>menor</b> rota-trem de "
              "cada cidade. A fila de prioridade mínima escolhe sempre o "
              "vértice de menor distTo[]; cada aresta é relaxada uma vez.", body_style),
    Paragraph("Decisão de cada rota-trem (peso y para a cidade c):", sub_style),
]
items += bullets([
    "<b>Por cidade só a menor rota importa</b> — as demais já são fechadas.",
    "<b>y &gt; dist[c]</b> → o trem nem atinge o mínimo → fecha.",
    "<b>y = dist[c]</b> e alguma <b>estrada</b> atinge dist[c] → redundante → fecha.",
    "<b>y = dist[c]</b> e nenhuma estrada atinge dist[c] → única forma → mantém.",
])
items += [
    Paragraph("A contagem de estradas que realizam dist[c] (cnt_road[c]) é feita "
              "numa varredura O(V+E) após o Dijkstra.", small),
    Paragraph("relax:  if dist[v] + peso(v,w) &lt; dist[w]: dist[w] = dist[v] + peso(v,w)", code_style),
]
flow(c, items, 1.5 * cm, 1.3 * cm, W - 3.0 * cm, H - 3.2 * cm)
footer(c, 3)
c.showPage()

# ---------------- Slide 4: complexidade e casos especiais ----------------
header(c, "3 · COMPLEXIDADE E CASOS ESPECIAIS")
left = [
    Paragraph("Complexidade", sub_style),
    Paragraph("V = n,  E = m,  k rotas de trem.", body_style),
]
left += bullets([
    "Construção + pré-filtragem dos trens: O(V+E+k).",
    "Dijkstra (heap binário): O((V+E) log V).",
    "Varredura final e decisão: O(V+E+k).",
])
left += [
    Paragraph("<b>Tempo total: O((V+E) log V + k).</b>", body_style),
    Paragraph("<b>Espaço: O(V+E)</b> (grafo em CSR + vetores).", body_style),
]
flow(c, left, 1.5 * cm, 1.3 * cm, 14.5 * cm, H - 3.2 * cm)

right = [
    Paragraph("Casos especiais", sub_style),
]
right += bullets([
    "Estradas/trens paralelos: mantém-se a melhor de cada.",
    "Empate trem = estrada: fecha o trem.",
    "Vários trens mínimos iguais sem estrada: mantém só um.",
    "Pesos grandes (≤10⁹): inteiros do Python, sem overflow.",
    "Toda cidade alcança a capital (sem inalcançáveis).",
])
right += [
    Paragraph("Validação: 5069 casos contra força-bruta que testa todos os "
              "subconjuntos de trens — 0 divergências.", small),
]
flow(c, right, 16.8 * cm, 1.3 * cm, W - 16.8 * cm - 1.5 * cm, H - 3.2 * cm)
footer(c, 4)
c.showPage()

# ---------------- Slide 5: conclusao ----------------
header(c, "4 · CONCLUSÃO")
items = [
    Paragraph("Resumo", sub_style),
]
items += bullets([
    "Dijkstra padrão sobre o grafo combinado resolve as distâncias.",
    "A pergunta vira uma análise local: cada trem é necessário só se for a "
    "única forma de manter dist[c].",
    "Solução O((V+E) log V + k), dentro do limite de 2 s mesmo em Python.",
])
items += [
    Paragraph("Por que Dijkstra (e não Bellman-Ford)?", sub_style),
    Paragraph("Todos os pesos são não-negativos, então não há ciclos negativos; "
              "Dijkstra é correto e mais rápido — O((V+E) log V) vs O(V·E).", body_style),
    Paragraph("Obrigado!", title_style),
]
flow(c, items, 1.5 * cm, 1.3 * cm, W - 3.0 * cm, H - 3.2 * cm)
footer(c, 5)
c.showPage()

c.save()
print("apresentacao.pdf gerado")
