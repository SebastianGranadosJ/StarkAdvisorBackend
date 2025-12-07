# 🌐 Financial Intelligence Hub – Backend  
*A centralized platform for smarter, data-driven financial decisions.*

This backend powers a financial analytics platform designed to centralize market information and help users make informed investment decisions.  
It aggregates financial news through web scraping, processes market data for stocks, ETFs, and currencies, computes technical indicators, recommends daily trading opportunities, and provides a multilingual AI chatbot capable of answering questions about both the platform and the financial world.

---

## 🚀 Key Features

- **Financial News Aggregation** from multiple sources using web scraping.  
- **Market Charts & Indicators** for stocks, ETFs, and forex — all market data sourced from **Yahoo Finance** (price history, RSI, MA, volatility, etc.).  
- **Trade of the Day Engine** recommending the strongest opportunities of the day based on RSI-driven analysis, enriched with insights from a **third-party financial analysis provider**.  
- **AI Chatbot (EN/ES)** trained with NLP/ML models to answer financial and platform-related questions.  
- **Centralized API** serving all data to the React frontend.  
---

## 🧰 Tech Stack

### Backend & Infrastructure
- **Python · Django**
- **AWS EC2**, **AWS CloudFront**
- **PostgreSQL (AWS Aurora)**  
- **MongoDB Atlas**
- **Redis** (cache & session management)

### AI / NLP
- **Hugging Face Transformers**
- **Multilingual BERT**
- **SpaCy**
- **Scikit-Learn**

### Frontend
- **React + TypeScript**

---

