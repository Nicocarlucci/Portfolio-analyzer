Quantitative Portfolio Risk & Optimization Analyzer

A comprehensive Python toolkit designed for quantitative portfolio management, risk analysis, and asset allocation. This application automates historical data retrieval, calculates institutional-grade risk metrics, generates performance visualizations, and solves for optimal portfolio weights using Markowitz Modern Portfolio Theory.

🌟 Key Features

Automated Data Retrieval: Dynamically pulls historical price data for custom tickers and benchmark indices (S&P 500) via yfinance.

Institutional Risk Metrics: Computes Sharpe Ratio, Sortino Ratio, Calmar Ratio, Maximum Drawdown, Value at Risk (VaR 95%), and Conditional Value at Risk (CVaR 95% / Expected Shortfall).

Benchmark Analytics: Evaluates portfolio performance relative to market benchmarks using CAPM Beta, Alpha, Tracking Error, and Information Ratio.

Portfolio Optimization: Uses non-linear mathematical optimization (scipy.optimize) to calculate:

Tangency Portfolio: Maximizes Sharpe Ratio under weight constraints.

Global Minimum Variance (GMV): Minimizes total portfolio risk.

Maximum Return Portfolio: Maximizes annual return expectations.

Visual Diagnostics: Plots cumulative performance, historical drawdowns, return distribution histograms with risk limits, asset correlation heatmaps, and regression scatter plots.

🚀 Getting Started

Prerequisites

Make sure you have Python installed on your system. Install the required dependencies using pip:

pip install yfinance pandas numpy matplotlib seaborn scipy


Installation & Execution

Clone the repository:

git clone https://github.com/Nicocarlucci/Portfolio-analyzer.git
cd Portfolio-analyzer


Run the script:

python main.py


Input Parameters:

Enter target asset tickers separated by commas (e.g., AAPL, MSFT, GOOGL, NVDA).

Specify individual weight allocations for each asset.

📊 Summary Output Example

======================================================================
METRICHE PORTFOLIO
======================================================================
Rendimento totale:        142.50%
Rendimento annualizzato:  12.40%
Volatilità:               15.20%
Sharpe Ratio:             0.55
Sortino Ratio:            0.82
Max Drawdown:             -22.10%
Calmar Ratio:             0.56
VaR 95%:                  -1.85%
CVaR 95%:                 -2.90%
Beta (vs S&P 500):        1.050
Tracking Error:           4.30%
Information Ratio:        0.420
======================================================================


🛠️ Built With

Python - Core programming language.

Pandas & NumPy - Data manipulation and vector math.

SciPy - Non-linear optimization algorithms (scipy.optimize.minimize).

yfinance - Financial market data downloader.

Matplotlib & Seaborn - Data visualization libraries.

📜 License

Distributed under the MIT License. See LICENSE for more information.