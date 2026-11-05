from visualizer import lineplot, drawdown_plot, hist_returns, heatmap_correlation, scatter_portf_vs_benchmark
from metrics import calculate_metrics
from data_loader import download_data
from optimizer import optimize_portfolio
import numpy as np
import pandas as pd

# ============================================================
# PARAMETRI
# ============================================================

total_years = "20y"

tickers_input = input(" Enter your portfolio tickers: ").upper().strip()
tickers = [t.upper().strip() for t in tickers_input.split(",")]

index = input("Enter the index to use in the analysis: ").upper().strip()

while True:
    pesi = []


    for ticker in tickers:
        while True:
            peso_input = input(f"Peso di {ticker}: ")

            try:
                peso = float(peso_input)

                if peso > 1:
                    peso = peso/100

                if 0 <= peso <= 1:
                    pesi.append(peso)
                    break

                else:
                    print(" Il peso deve essere compreso tra 0 e 100%")

            except ValueError:
                print("Inserisci un valore valido")

    if abs(sum(pesi) - 1) > 0.001:
        print("La somma dei pesi deve essere 1 (o 100%)")
        print(f"Somma attuale: {sum(pesi)*100:.1f}%")

    else:
        pesi = np.array(pesi)
        break


# ===============================
# DOWNLOAD THE DATA
# ===============================
prezzi, benchmark = download_data(tickers, index, total_years)
risk_free = 0.04

# =======================================
# DOWNLOAD THE METRICS
# =======================================

metrics_assets_df, metrics_portfolio_df, alpha_capm, beta, correlazione_assets, covarianza, alpha, prezzi_benchmark, prezzi_portfolio, prezzi_assets, portfolio_returns, returns_benchmark_aligned, portfolio_aligned, rendimenti_annualizzati = calculate_metrics (tickers, prezzi, benchmark, pesi, risk_free)

sharpe_portfolio = metrics_portfolio_df["Sharpe"]
sortino_ratio_portfolio = metrics_portfolio_df["Sortino"]
calmar_ratio_portfolio = metrics_portfolio_df["Calmar"]
var_95_portfolio = metrics_portfolio_df["VaR 95 (%)"]
cvar_95_portfolio = metrics_portfolio_df["CVaR 95 (%)"]
tracking_error = metrics_portfolio_df["Tracking Error"]
max_drawdown_portfolio = metrics_portfolio_df["Max DD (%)"]
information_ratio = metrics_portfolio_df["Information Error"]
volatilita_annualizzata_portfolio = metrics_portfolio_df["Volatilita (%)"]
rendimento_portoflio_annualizzato = metrics_portfolio_df["Rend Annuo (%)"]

# =============================
# PRINTING
# =============================
print("=" * 70)
print("METRICHE PORTFOLIO")
print("=" * 70)
print(f"Rendimento annualizzato:  {rendimento_portoflio_annualizzato*100:.2f}%")
print(f"Volatilità:               {volatilita_annualizzata_portfolio*100:.2f}%")
print(f"Sharpe Ratio:             {sharpe_portfolio:.2f}")
print(f"Sortino Ratio:            {sortino_ratio_portfolio:.2f}")
print(f"Max Drawdown:             {max_drawdown_portfolio:.2f}%")
print(f"Calmar Ratio:             {calmar_ratio_portfolio:.2f}")
print(f"VaR 95%:                  {var_95_portfolio*100:.2f}%")
print(f"CVaR 95%:                 {cvar_95_portfolio*100:.2f}%")
print(f"Beta (vs S&P 500):        {beta:.3f}")
print(f"Tracking Error:           {tracking_error*100:.2f}%")
print(f"Information Ratio:        {information_ratio:.3f}")
print(f"Alpha CAMP:               {(alpha_capm * 100):.2f}%")
print(f"Alpha:                    {(alpha * 100):.2f}%")
print("")
print("=" * 70)
print("DATI SUI SINGOLI ASSETS")
print("=" * 70)


print(metrics_assets_df.round(len(tickers)))

# ======================
# PRINTING THE GRAPHS
# =======================
lineplot(prezzi_assets, prezzi_portfolio, prezzi_benchmark)
drawdown_plot(prezzi_portfolio)
hist_returns(portfolio_returns,var_95_portfolio, cvar_95_portfolio)
heatmap_correlation(correlazione_assets)
scatter_portf_vs_benchmark(returns_benchmark_aligned, portfolio_aligned, beta)

# PRINT OPTIMIZATION METRICS
metrics_optimized = optimize_portfolio(rendimenti_annualizzati, covarianza, risk_free)

print("" * 50)
print("=" * 70)
print(("METRICS FOR OPTIMIZED SHARPE RATIO"))
print("-"* 50)
for i in range(len(tickers)):
    print(f"{tickers[i]}'s Weight: {metrics_optimized["max_sharpe_weights"][i] * 100}%")
print(f"Sharpe ratio using these weights: {metrics_optimized["max_sharpe_value"]:.2f}")

print("="* 50)

print(("METRICS FOR MIN VOLATILITY"))
print("-"* 50)
for i in range(len(tickers)):
    print(f"{tickers[i]}'s Weight: {metrics_optimized["min_vol_weights"][i] * 100}%")
print(f"Volatility using these weights: {metrics_optimized["min_vol_value"]:.2f}")


