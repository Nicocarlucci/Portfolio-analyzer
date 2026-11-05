import numpy as np
from scipy.optimize import minimize

def optimize_portfolio(rendimenti_annualizzati, covarianza, risk_free):
    """Performs portfolio optimization for Max Sharpe and Min Volatility."""
    n_tickers = len(rendimenti_annualizzati)
    bounds = [(0, 1) for _ in range(n_tickers)]
    constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
    init_guess = [1 / n_tickers for _ in range(n_tickers)]

    # 1. Max Sharpe Ratio
    def negativo_sharpe(pesi):
        rend = np.dot(rendimenti_annualizzati, pesi)
        vol = np.sqrt(np.dot(pesi.T, np.dot(covarianza, pesi)))
        return -(rend - risk_free) / vol

    res_sharpe = minimize(negativo_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)

    # 2. Min Volatility
    def min_vol(pesi):
        return np.sqrt(np.dot(pesi.T, np.dot(covarianza, pesi)))

    res_vol = minimize(min_vol, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)

    metrics_optimized = {
        "max_sharpe_weights": res_sharpe.x,
        "max_sharpe_value": -res_sharpe.fun,
        "min_vol_weights": res_vol.x,
        "min_vol_value": res_vol.fun
    }

    return metrics_optimized