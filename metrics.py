import pandas as pd
import numpy as np


def calculate_metrics (tickers, prezzi, benchmark, pesi, risk_free):

    returns = prezzi.pct_change().dropna()
    returns_benchmark = benchmark.pct_change().dropna()

    # Portfolio returns
    portfolio_returns = pd.Series(np.dot(returns, pesi), index=returns.index, name="Portfolio")

    # Allineamento portfolio vs benchmark
    df_allineato = pd.DataFrame({
        "Portfolio": portfolio_returns,
        "Benchmark": returns_benchmark
    }).dropna()

    df_allineato = pd.concat([df_allineato, returns], axis = 1).dropna()

    portfolio_aligned = df_allineato["Portfolio"]
    returns_benchmark_aligned = df_allineato["Benchmark"]
    assets_returns_aligned = df_allineato.loc[:, tickers]

    # Prezzi cumulativi per i grafici
    prezzi_benchmark = 100 * (1 + returns_benchmark_aligned).cumprod()
    prezzi_portfolio = 100 * (1 + portfolio_aligned).cumprod()
    prezzi_assets = 100 * (1 + assets_returns_aligned).cumprod()

    # ============================================================
    # METRICHE PORTFOLIO vs BENCHMARK
    # ============================================================
    # Beta
    cov_portfolio_benchmark = portfolio_aligned.cov(returns_benchmark_aligned)
    var_benchmark = returns_benchmark_aligned.var()
    beta = cov_portfolio_benchmark / var_benchmark

    # Tracking Error
    differenza = portfolio_aligned - returns_benchmark_aligned
    tracking_error = differenza.std() * np.sqrt(252)

    # Information Ratio
    rendimento_eccesso = portfolio_aligned.mean() - returns_benchmark_aligned.mean()
    rendimento_eccesso_annuo = rendimento_eccesso * 252
    information_ratio = rendimento_eccesso_annuo / tracking_error

    # ============================================================
    # METRICHE SINGOLI ASSET
    # ============================================================
    rendimenti_annualizzati = (1 + returns.mean()) ** 252 - 1
    volatilita_annualizzata = returns.std() * np.sqrt(252)
    varianza_annualizzata = volatilita_annualizzata ** 2

    sharpe = (rendimenti_annualizzati - risk_free) / volatilita_annualizzata

    picco = prezzi.cummax()
    drawdown = ((prezzi - picco) / picco)
    max_drawdown = drawdown.min()
    calmar_ratio = (rendimenti_annualizzati - risk_free) / abs(max_drawdown)

    volatilita_neg = returns[returns < 0].std() * np.sqrt(252)
    sortino_ratio = (rendimenti_annualizzati - risk_free) / volatilita_neg

    # VaR e CVaR per ogni asset
    var_95 = returns.apply(lambda x: np.percentile(x, 5))
    cvar_95 = returns.apply(lambda x: x[x <= np.percentile(x, 5)].mean())

    # ============================================================
    # METRICHE PORTFOLIO
    # ============================================================
    rendimento_giornaliero_medio = portfolio_returns.mean()
    rendimento_portoflio_annualizzato = (1 + rendimento_giornaliero_medio) ** 252 - 1

    volatilita_annualizzata_portfolio = portfolio_returns.std() * np.sqrt(252)
    sharpe_portfolio = (rendimento_portoflio_annualizzato - risk_free) / volatilita_annualizzata_portfolio

    picco_port = prezzi_portfolio.cummax()
    drawdown_portfolio = ((prezzi_portfolio - picco_port) / picco_port) * 100
    max_drawdown_portfolio = drawdown_portfolio.min()
    calmar_ratio_portfolio = (rendimento_portoflio_annualizzato - risk_free) / abs(max_drawdown_portfolio / 100)

    volatilita_neg_portfolio = portfolio_returns[portfolio_returns < 0].std() * np.sqrt(252)
    sortino_ratio_portfolio = (rendimento_portoflio_annualizzato - risk_free) / volatilita_neg_portfolio

    var_95_portfolio = np.percentile(portfolio_returns, 5)
    cvar_95_portfolio = portfolio_returns[portfolio_returns <= var_95_portfolio].mean()


    # ============================================================
    # MATRICE COVARIANZA, CORRELAZIONE, CONTRIBUZIONE RISCHIO
    # ============================================================
    covarianza = returns.cov() * 252
    varianza_portfolio = np.dot(pesi.T, np.dot(covarianza, pesi))
    correlazione_assets = returns.corr()

    rischio_marginale = np.dot(covarianza, pesi)
    rischio_pesato = rischio_marginale * pesi
    contributo_al_rischio = (rischio_pesato / varianza_portfolio) * 100

    indice_max = np.argmax(contributo_al_rischio)
    nome_asset = tickers[indice_max]
    maggiore = contributo_al_rischio[indice_max]


    # ALPHA 
    rendimento_portfolio = (1 + portfolio_returns.mean()) ** 252 - 1
    rendimento_benchmark = (1 + returns_benchmark_aligned.mean()) ** 252 - 1

    # Alpha del CAPM
    alpha_capm = rendimento_portfolio - (risk_free + beta * (rendimento_benchmark - risk_free))
    # Alpha Generale
    alpha = (prezzi_portfolio.iloc[-1] - prezzi_benchmark.iloc[-1]) / prezzi_benchmark.iloc[-1]

    metrics_assets_df = pd.DataFrame({
    "Peso (%)": pesi * 100,
    "Rend Annuo (%)": rendimenti_annualizzati * 100,
    "Volatilita (%)": volatilita_annualizzata * 100,
    "Sharpe": sharpe,
    "Max DD (%)": max_drawdown * 100,
    "Sortino": sortino_ratio,
    "Calmar": calmar_ratio,
    "VaR 95 (%)": var_95 * 100,
    "CVaR 95 (%)": cvar_95 * 100,
    }, index=tickers)


    metrics_portfolio_df = {
        "Tracking Error": tracking_error,
        "Information Error": information_ratio,
        "VaR 95 (%)": var_95_portfolio,
        "CVaR 95 (%)": cvar_95_portfolio,
        "Sortino": sortino_ratio_portfolio,
        "Calmar": calmar_ratio_portfolio,
        "Sharpe": sharpe_portfolio,
        "Max DD (%)": max_drawdown_portfolio, 
        "Volatilita (%)": volatilita_annualizzata_portfolio, 
        "Rend Annuo (%)": rendimento_portoflio_annualizzato}

    return metrics_assets_df, metrics_portfolio_df, alpha_capm, beta, correlazione_assets, covarianza, alpha, prezzi_benchmark, prezzi_portfolio, prezzi_assets, portfolio_returns, returns_benchmark_aligned, portfolio_aligned, rendimenti_annualizzati

