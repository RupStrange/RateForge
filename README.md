# ⚡ RateForge · Currency Intelligence

An AI-powered currency conversion assistant that handles real-time exchange rates and conversions through natural language — powered by LLaMA 4 Scout via Groq inference.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red?style=flat-square&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA--4--Scout-black?style=flat-square)
![API](https://img.shields.io/badge/Rates-ExchangeRate--API-orange?style=flat-square)

---

## 🚀 Demo

🔗 **Live App:** https://rateforge-rupstrange-app.streamlit.app/

Screenshot 1:
<img width="800" height="810" alt="image" src="https://github.com/user-attachments/assets/9899e292-ea0f-422a-9024-cdfc7c664704" />

Screenshot 2:
<img width="787" height="663" alt="image" src="https://github.com/user-attachments/assets/d3f03fc3-53b4-4193-89a9-f57ea43b34fb" />

---

## ✨ Features

- 💬 Natural language queries — ask in plain English, no special syntax needed
- 🔁 Smart tool routing — automatically picks the right tool (rate lookup vs. conversion)
- 📡 Real-time rates — live data fetched from ExchangeRate API on every query
- ⚡ Quick-action buttons — one-click queries for popular currency pairs
- 🌍 180+ currencies supported — full ISO 4217 coverage
- 🗨️ Conversation history — scrollable chat log with clear option
- 🚫 Scope control — politely refuses off-topic questions

---

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| Frontend | Streamlit |
| LLM | Meta LLaMA 4 Scout 17B (via Groq) |
| LLM Framework | LangChain (`langchain_groq`) |
| Exchange Rates | ExchangeRate API v6 |
| Config | `python-dotenv` |

---

## 🧠 How It Works

RateForge uses **LangChain tool calling** with two specialized tools:

| Tool | Triggered when |
|------|---------------|
| `conversion_rate` | Query has **no amount** — e.g. *"USD to INR rate?"* |
| `convert` | Query has a **numeric amount** — e.g. *"Convert 100 USD to INR"* |

**Flow:**

```
User query → LLaMA 4 Scout decides which tool to call
    ↳ conversion_rate → fetches live rate → LLM formats response
    ↳ convert → fetches rate + multiplies amount → LLM formats response
    ↳ no tool call → LLM answers directly (e.g. off-topic refusal)
```

The system prompt enforces strict tool routing — the LLM is never allowed to call both tools for a single query.

---

## 🗂️ Project Structure

```
rateforge/
│
├── app.py              # Streamlit UI + LangChain logic (main entry point)
│
├── .env                # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/rateforge.git
cd rateforge
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your API keys**

Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
CURRENCY_CONVERTOR_KEY=your_exchangerate_api_key_here
```

- Get a free Groq API key at [https://console.groq.com](https://console.groq.com)
- Get a free ExchangeRate API key at [https://www.exchangerate-api.com](https://www.exchangerate-api.com)

---

## ▶️ Usage

```bash
streamlit run app.py
```

Then:
1. Use the **quick-action buttons** for instant popular pair lookups
2. Or type any natural language query in the **Query Terminal**
3. Hit **SEND ⚡** and get a live, AI-formatted response

**Example queries:**
```
Convert 250 USD to SGD
What is the CHF to INR exchange rate?
How much is 1000 JPY in EUR?
What currency does Brazil use?
```

---

## ⚠️ Known Limitations

- Dependent on Groq API and ExchangeRate API availability
- LLaMA 4 Scout may occasionally misroute tool selection on ambiguous queries
- No conversation memory across sessions — history resets on page refresh

---

## 🔮 Future Improvements

- 📊 Historical rate charts using Matplotlib or Plotly
- 🔔 Rate alert system — notify when a pair crosses a threshold
- 💾 Export conversation history as CSV or PDF
- 🌐 Multi-turn context — remember currencies mentioned earlier in chat
- 🗺️ Currency map — visual world map highlighting selected currencies

---

## 📦 Requirements

```
langchain
langchain-groq
langchain-core
streamlit
requests
python-dotenv
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create your branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with ⚡ by <a href="https://github.com/your-username">your-username</a></p>
