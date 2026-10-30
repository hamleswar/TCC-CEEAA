from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg

# INICIALIZAÇÃO DA POPULAÇÃO
"""
1 - inicializar com valores aleatórios
2 - população pequena explora poucas soluções e podemos cair em um máximo local
3 - populações maiores aumentam as chances de encontrar o máximo global
"""
@dataclass
class besouro:
    R: float
    G: float
    B: float

def inicializar_populacao(N):
    populacao = [
        besouro(
            R = np.random.uniform(0,1),
            G = np.random.uniform(0,1),
            B = np.random.uniform(0,1),
        )
        for _ in range(N)
    ]

    return populacao

def mostrar_cor(individuo, caminho_imagem):
    cor = np.array([individuo.R, individuo.G, individuo.B])

    img = mpimg.imread(caminho_imagem)

    if img.max() > 1:
        img = img / 255.0

    h, w = img.shape[:2]
    fundo = np.ones((h, w, 3)) * cor

    mascara = np.mean(img[:, :, :3], axis=2) < 0.3

    saida = fundo.copy()
    saida[mascara] = [0, 0, 0]

    fig, ax = plt.subplots(figsize=(3, 3))
    ax.imshow(saida)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"RGB = {tuple(round(c, 2) for c in cor)}")
    plt.show()

populacao = inicializar_populacao(200)

def mostrar_populacao(populacao, colunas=5):

    N = len(populacao)
    linhas = int(np.ceil(N / colunas))

    # Figura cresce verticalmente conforme a população
    fig = Figure(
        figsize=(10, linhas * 0.8),
        dpi=100
    )

    axes = fig.subplots(linhas, colunas, squeeze=False)
    axes = axes.flatten()

    for i, individuo in enumerate(populacao):

        cor = (individuo.R, individuo.G, individuo.B)

        ax = axes[i]
        ax.set_facecolor(cor)

        ax.set_xticks([])
        ax.set_yticks([])

        ax.text(
            0.5, 0.5, str(i),
            ha="center",
            va="center",
            transform=ax.transAxes,
            color="white" if np.mean(cor) < 0.5 else "black"
        )

    # Ocultar posições vazias
    for ax in axes[N:]:
        ax.axis("off")

    fig.subplots_adjust(
        left=0.03,
        right=0.97,
        top=0.995,
        bottom=0.005,
        hspace=0.35,
        wspace=0.2
    )

    # Janela
    janela = tk.Tk()
    janela.title("População de Besouros")
    janela.geometry("1050x700")

    # Área com rolagem
    frame = tk.Frame(janela)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(
        frame,
        orient=tk.VERTICAL,
        command=canvas.yview
    )

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Inserir gráfico
    grafico = FigureCanvasTkAgg(fig, master=canvas)
    grafico.draw()

    widget = grafico.get_tk_widget()
    canvas.create_window((0, 0), window=widget, anchor="nw")

    janela.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Rolagem com o mouse
    def rolar(event):
        direcao = -1 if event.delta > 0 else 1
        canvas.yview_scroll(direcao * 3, "units")

    janela.bind_all("<MouseWheel>", rolar)

    janela.mainloop()

# mostrar_populacao(populacao)
individuo = besouro(255,255,255)

mostrar_cor(individuo, "besouro.png")