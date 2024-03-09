# Arbitrage Analysis in the Sports Betting Market

## Description

This project aims to explore arbitrage opportunities within the sports betting market by automating the analysis of bookmakers' odds. It seeks to identify profitable bets across various sports events, leveraging data management and statistical analysis techniques.

## Features

- **Automated Data Management**: Utilizes scripts to process and analyze betting odds data retrieved from The ODDs API and OddsAPI1 via RAPID API.
- **Arbitrage Detection**: Employs algorithms to detect arbitrage opportunities by scrutinizing disparities in bookmakers' odds.
- **Arbitrage Analysis**: Engages in arbitrage analysis, including the estimation of general densities for sports odds and the comparison with financial market data, specifically ticker data from Yahoo Finance.


## Installation

Ensure you have Conda or Mamba installed on your system. To set up the project environment:

```console
$ conda env create --file environment.yml --name arbitrage_analysis
$ conda activate arbitrage_analysis
```

## Building the Project

Activate the project environment and execute the following command to build the project:

```console
$ pytask
```