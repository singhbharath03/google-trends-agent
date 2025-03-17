# Google Trends Trading Agent

This repository contains a trading agent application that uses Google Trends data and LLM-based decision making to trade attention tokens. The application is built with FastAPI.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Solana wallet

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/singhbharath03/google-trends-agent
cd google-trends-agent
```

### 2. Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install using requirements.txt
pip install -r requirements.txt
```

### 4. Create a .env File

Create a `.env` file in the root directory with the following variables:

```
DEBUG_MODE=True
PRIVATE_KEY=your-solana-private-key
GROQ_API_KEY=your-groq-api-key
SERP_API_KEY=your-serp-api-key
```

## Running the Application

```bash
python main.py
```

Or you can use uvicorn directly:

```bash
uvicorn main:app --reload
```

The application will be available at http://localhost:8000

## API Endpoints

- `POST /trade/buy`: Buy tokens with the specified wallet
- `POST /trade/sell`: Sell tokens from the specified wallet
- `POST /trade/llm`: Trigger the LLM agent to make trading decisions based on Google Trends data

## Request Format

For buy/sell operations:

```json
{
  "wallet_address": "your-wallet-address",
  "mint": "token-mint-address",
  "amount_with_decimals": 1000000
}
```

## Components

- `main.py`: FastAPI application and endpoints
- `llm.py`: LLM agent integration using Groq
- `serpa_api.py`: Google Trends data fetching via SERP API
- `config.py`: Application configuration
- `trade/`: Trading related modules
  - `trader.py`: Trading functions
  - `keypair.py`: Solana wallet utilities
  - `swap_transaction.py`: Transaction handling
  - `token_account.py`: Token account operations
- `tools/`: Utility tools for the application

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc 