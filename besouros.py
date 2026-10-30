from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tkinter as tk

from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


@dataclass
class besouro:
    R: float
    G: float
    B: float


def inicializar_populacao(N):

    populacao = [
        besouro(
            R=np.random.uniform(0, 1),
            G=np.random.uniform(0, 1),
            B=np.random.uniform(0, 1)
        )
        for _ in range(N)
    ]

    return populacao


def mostrar_cor(individuo, caminho_imagem="besouro.png"):

    cor = np.array([
        individuo.R,
        individuo.G,
        individuo.B
    ])

    caminho = Path(__file__).resolve().parent / caminho_imagem
    img = mpimg.imread(caminho)

    saida = np.zeros_like(img)
    saida[:, :, :3] = cor
    saida[:, :, 3] = img[:, :, 3]

    fig, ax = plt.subplots(figsize=(3, 3))

    ax.set_facecolor("white")
    ax.imshow(saida)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(f"RGB = {tuple(round(c, 2) for c in cor)}")

    plt.show()


def mostrar_populacao(populacao, colunas=5, caminho_imagem="besouro.png"):

    N = len(populacao)

    if N == 0:
        return

    linhas = int(np.ceil(N / colunas))

    caminho = Path(__file__).resolve().parent / caminho_imagem
    imagem = Image.open(caminho).convert("RGBA")
    imagem = imagem.resize((150, 150), Image.Resampling.LANCZOS)

    img = np.asarray(imagem) / 255.0
    alpha = img[:, :, 3]

    fig = Figure(
        figsize=(10, linhas * 1.6),
        dpi=100
    )

    axes = fig.subplots(linhas, colunas, squeeze=False).flatten()

    for i, individuo in enumerate(populacao):

        cor = np.array([
            individuo.R,
            individuo.G,
            individuo.B
        ])

        saida = np.zeros((150, 150, 4))
        saida[:, :, :3] = cor
        saida[:, :, 3] = alpha

        ax = axes[i]
        ax.set_facecolor("white")
        ax.imshow(saida)

        ax.set_xticks([])
        ax.set_yticks([])

        ax.set_title(f"Indivíduo {i}", fontsize=9)

        ax.set_xlabel(
            f"({individuo.R:.2f}, {individuo.G:.2f}, {individuo.B:.2f})",
            fontsize=8,
            labelpad=5
        )

    for ax in axes[N:]:
        ax.axis("off")

    fig.subplots_adjust(
        left=0.03,
        right=0.97,
        top=0.99,
        bottom=0.01,
        hspace=0.65,
        wspace=0.2
    )

    janela = tk.Tk()
    janela.title("População de Besouros")
    janela.geometry("1050x700")

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

    grafico = FigureCanvasTkAgg(fig, master=canvas)
    grafico.draw()

    widget = grafico.get_tk_widget()
    canvas.create_window((0, 0), window=widget, anchor="nw")

    janela.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    def rolar(event):
        direcao = -1 if event.delta > 0 else 1
        canvas.yview_scroll(direcao * 3, "units")

    janela.bind_all("<MouseWheel>", rolar)

    janela.mainloop()