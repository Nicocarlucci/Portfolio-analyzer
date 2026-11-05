import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



def lineplot(prezzi_assets, prezzi_portfolio, prezzi_benchmark):

    # ============================================================
    # GRAFICO 1: ANDAMENTO CUMULATIVO
    # ============================================================
    fig, ax = plt.subplots(figsize=(14, 8))


    for column in prezzi_assets.columns:
        ax.plot(prezzi_assets.index, prezzi_assets[column], 
                label=column, linewidth=1.3, alpha=0.7)

    ax.plot(prezzi_portfolio.index, prezzi_portfolio, 
            label="PORTFOLIO", linewidth=2.5, color="blue")

    ax.plot(prezzi_benchmark.index, prezzi_benchmark, 
            label="S&P 500", linewidth=2, linestyle="--", color="green")

    ax.set_title("Andamento Cumulativo: Portfolio vs S&P 500 (Base 100)", 
                fontsize=15, fontweight="bold", pad=10)
    ax.set_xlabel("Data", fontsize=11)
    ax.set_ylabel("Valore (Base 100)", fontsize=11)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def drawdown_plot(prezzi_portfolio):
    # ============================================================
    # GRAFICO 2: DRAWDOWN PORTFOLIO
    # ============================================================
    fig, ax = plt.subplots(figsize=(14, 6))

    picco = prezzi_portfolio.cummax()
    drawdown = ((prezzi_portfolio - picco) / picco) * 100

    ax.fill_between(prezzi_portfolio.index, drawdown, 0, color="red", alpha=0.4)
    ax.plot(prezzi_portfolio.index, drawdown, color="darkred", linewidth=1)

    ax.set_title("Drawdown del Portfolio", fontsize=14, fontweight="bold")
    ax.set_xlabel("Data", fontsize=11)
    ax.set_ylabel("Drawdown (%)", fontsize=11)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def hist_returns(portfolio_returns,var_95_portfolio, cvar_95_portfolio):
    # ============================================================
    # GRAFICO 3: ISTOGRAMMA RENDIMENTI con VaR e CVaR
    # ============================================================
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.hist(portfolio_returns * 100, bins=60, color="skyblue", 
            edgecolor="black", alpha=0.7, density=True)

    ax.axvline(var_95_portfolio * 100, color="red", linewidth=2.5, 
            linestyle="--", label=f"VaR 95%: {var_95_portfolio*100:.2f}%")
    ax.axvline(cvar_95_portfolio * 100, color="darkred", linewidth=2.5, 
            label=f"CVaR 95%: {cvar_95_portfolio*100:.2f}%")
    ax.axvline(0, color="grey", linewidth=1, linestyle="-", alpha=0.5)

    ax.set_title("Distribuzione Rendimenti Giornalieri del Portfolio", 
                fontsize=14, fontweight="bold")
    ax.set_xlabel("Rendimento Giornaliero (%)", fontsize=11)
    ax.set_ylabel("Densità", fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()



def heatmap_correlation(correlazione_assets):
    
    # ============================================================
    # GRAFICO 4: HEATMAP C:ORRELAZIONE
    # ============================================================

    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(
        correlazione_assets,
        annot=True,
        cmap="coolwarm",
        vmin=-1, vmax=1,
        linewidths=1,
        ax=ax,
        fmt=".2f",
        square=True,
        cbar_kws={"shrink": 0.8}
    )

    ax.set_title("Matrice di Correlazione", fontsize=14, fontweight="bold", pad=10)
    plt.tight_layout()
    plt.show()


def scatter_portf_vs_benchmark (returns_benchmark_aligned, portfolio_aligned, beta):
    # ============================================================
    # GRAFICO 5: SCATTER PLOT vs BENCHMARK
    # ============================================================
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.scatter(returns_benchmark_aligned * 100, portfolio_aligned * 100, 
            alpha=0.4, s=15, color="steelblue")

    # Linea di regressione (Beta)
    x = np.linspace(returns_benchmark_aligned.min() * 100, returns_benchmark_aligned.max() * 100, 100)
    y = beta * x
    ax.plot(x, y, color="red", linewidth=2.5, label=f"Beta = {beta:.3f}")

    ax.axhline(0, color="grey", linewidth=0.8, alpha=0.5)
    ax.axvline(0, color="grey", linewidth=0.8, alpha=0.5)

    ax.set_xlabel("S&P 500 (%)", fontsize=12)
    ax.set_ylabel("Portfolio (%)", fontsize=12)
    ax.set_title("Portfolio vs S&P 500 - Scatter Plot", 
                fontsize=14, fontweight="bold")
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
