from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Union
from dotenv import load_dotenv
import os
import requests
import streamlit as st

load_dotenv()

# ─────────────────────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RateForge · Currency Intelligence",
    page_icon="⚡",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────
#  LLM & Tools
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    return ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=os.getenv("GROQ_API_KEY"),
    )

llm = get_llm()

@tool
def conversion_rate(present_currency: str, target_currency: str) -> float:
    """Get conversion rates between 2 currencies"""
    CURRENCY_CONVERTOR_KEY = os.getenv("CURRENCY_CONVERTOR_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_CONVERTOR_KEY}/pair/{present_currency}/{target_currency}"
    response = requests.get(url)
    return response.json()

@tool
def convert(amount: Union[float, str], from_currency: str, to_currency: str) -> float:
    """Convert an amount from one currency to another."""
    amount = float(amount)
    CURRENCY_CONVERTOR_KEY = os.getenv("CURRENCY_CONVERTOR_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_CONVERTOR_KEY}/pair/{from_currency}/{to_currency}"
    response = requests.get(url).json()
    rate = response["conversion_rate"]
    return amount * rate

system_prompt = """
You are a currency conversion assistant. You ONLY answer questions about currency conversion and exchange rates.

═══════════════════════════════════════════
RULE 1 — SCOPE
═══════════════════════════════════════════
Only respond to:
- Currency conversion (e.g. "100 USD to INR")
- Exchange rate queries (e.g. "USD to INR rate")
- General currency knowledge (e.g. "What currency does Japan use?")

For ANYTHING else → reply: "I can only help with currency conversion and exchange rates."

═══════════════════════════════════════════
RULE 2 — TOOL CALLING (NON-NEGOTIABLE)
═══════════════════════════════════════════
You have 2 tools: `convert` and `conversion_rate`

YOU MUST ALWAYS USE A TOOL for conversion and rate queries.
NEVER calculate or answer from memory. Your training data has outdated rates.

→ Query has a NUMBER  : call `convert`
→ Query has NO number : call `conversion_rate`

═══════════════════════════════════════════
RULE 3 — ONE TOOL PER QUERY
═══════════════════════════════════════════
- Never call both tools in one query
- Never chain tools (rate first, then convert)
- One query = one tool call, always

═══════════════════════════════════════════
RULE 4 — INPUT NORMALIZATION
═══════════════════════════════════════════
Always convert currency names to ISO codes:
- "dollars" → USD
- "rupees"  → INR
- "euros"   → EUR
- "pounds"  → GBP

═══════════════════════════════════════════
RULE 5 — RESPONSE FORMAT
═══════════════════════════════════════════
- Be concise and clear
- Always include currency units in the answer
- If inputs are missing or ambiguous, ask for clarification
- The tool result is the ONLY source of truth for the final amount.
- NEVER modify, round, or replace the tool's returned value.
- If the tool returns 9316.63, your answer MUST say 9316.63 — not any other number.

═══════════════════════════════════════════
FINAL RULE — TRUST THE TOOL
═══════════════════════════════════════════
The tool result is ground truth. 
Output it exactly. Never substitute your own value.
A wrong number is worse than no answer.

═══════════════════════════════════════════
EXAMPLES
═══════════════════════════════════════════
"100 USD to INR"            → call convert(100, USD, INR)
"how much is 50 euros in pounds" → call convert(50, EUR, GBP)
"USD to INR rate"           → call conversion_rate(USD, INR)
"what is euro to yen rate"  → call conversion_rate(EUR, JPY)
"what currency does Japan use" → answer directly, no tool needed
"who is the PM of India"    → refuse, out of scope
"""
llm_with_tools = llm.bind_tools([conversion_rate, convert])

# ─────────────────────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─────────────────────────────────────────────────────────────
#  Core logic
# ─────────────────────────────────────────────────────────────
def run_query(query: str) -> str:
    messages = [SystemMessage(system_prompt), HumanMessage(query)]
    ai_message = llm_with_tools.invoke(messages)
    messages.append(ai_message)

    if not ai_message.tool_calls:
        return ai_message.content

    tool_calls_map = {tc["name"]: tc for tc in ai_message.tool_calls}

    if "conversion_rate" in tool_calls_map:
        rate_result = conversion_rate.invoke(tool_calls_map["conversion_rate"])
        messages.append(rate_result)

    if "convert" in tool_calls_map:
        convert_result = convert.invoke(tool_calls_map["convert"])
        messages.append(convert_result)

    return llm.invoke(messages).content

# ─────────────────────────────────────────────────────────────
#  UI — Header
# ─────────────────────────────────────────────────────────────
st.title("⚡ RateForge")
st.caption("CURRENCY INTELLIGENCE  ·  REAL-TIME RATES  ·  180+ CURRENCIES  ·  LLAMA 4 SCOUT")
st.divider()

# ─────────────────────────────────────────────────────────────
#  Market snapshot strip
# ─────────────────────────────────────────────────────────────
st.caption("📡  POPULAR PAIRS — click any to query instantly")
snap1, snap2, snap3, snap4 = st.columns(4)

quick_query = None

with snap1:
    st.markdown("**USD / INR**")
    if st.button("Query →", key="snap1", use_container_width=True):
        quick_query = "What is the current conversion rate from USD to INR?"
with snap2:
    st.markdown("**EUR / USD**")
    if st.button("Query →", key="snap2", use_container_width=True):
        quick_query = "What is the current conversion rate from EUR to USD?"
with snap3:
    st.markdown("**GBP / JPY**")
    if st.button("Query →", key="snap3", use_container_width=True):
        quick_query = "What is the current conversion rate from GBP to JPY?"
with snap4:
    st.markdown("**AED / INR**")
    if st.button("Query →", key="snap4", use_container_width=True):
        quick_query = "What is the current conversion rate from AED to INR?"

st.divider()

# ─────────────────────────────────────────────────────────────
#  Quick conversion buttons — 2 rows
# ─────────────────────────────────────────────────────────────
st.caption("⚡  QUICK CONVERSIONS")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔁  100 USD → INR", use_container_width=True):
        quick_query = "How much is 100 USD in INR?"
with col2:
    if st.button("🔁  50 EUR → GBP", use_container_width=True):
        quick_query = "How much is 50 EUR in GBP?"
with col3:
    if st.button("🔁  1000 INR → AED", use_container_width=True):
        quick_query = "How much is 1000 INR in AED?"

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("📈  USD → INR rate", use_container_width=True):
        quick_query = "What is the current USD to INR exchange rate?"
with col5:
    if st.button("📈  EUR → JPY rate", use_container_width=True):
        quick_query = "What is the current EUR to JPY exchange rate?"
with col6:
    if st.button("📈  GBP → AED rate", use_container_width=True):
        quick_query = "What is the current GBP to AED exchange rate?"

st.divider()

# ─────────────────────────────────────────────────────────────
#  Chat history
# ─────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.caption("🗨️  CONVERSATION LOG")
    for role, text in st.session_state.chat_history:
        if role == "user":
            with st.chat_message("user", avatar="🧑‍💼"):
                st.write(text)
        else:
            with st.chat_message("assistant", avatar="⚡"):
                st.write(text)
    st.divider()

# ─────────────────────────────────────────────────────────────
#  Query input
# ─────────────────────────────────────────────────────────────
st.caption("💬  QUERY TERMINAL")

with st.form(key="query_form", clear_on_submit=True):
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            label="query",
            placeholder="e.g.  Convert 250 USD to SGD   |   What is CHF to INR rate?",
            label_visibility="collapsed",
        )
    with col_btn:
        submitted = st.form_submit_button("SEND ⚡", use_container_width=True)

# Handle quick button clicks
if quick_query:
    submitted = True
    user_input = quick_query

# ─────────────────────────────────────────────────────────────
#  Process & respond
# ─────────────────────────────────────────────────────────────
if submitted and user_input.strip():
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("🔄  Fetching live data..."):
        try:
            response = run_query(user_input)
        except Exception as e:
            response = f"⚠️ Something went wrong: {str(e)}"
    st.session_state.chat_history.append(("assistant", response))
    st.rerun()

elif submitted and not user_input.strip():
    st.warning("⚠️  Please enter a query before sending.")

# ─────────────────────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────────────────────
st.divider()
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.caption("🌍  180+ currencies supported")
with col_f2:
    st.caption("⚡  Powered by ExchangeRate API")
with col_f3:
    st.caption("🤖  LLaMA 4 Scout via Groq")

if st.session_state.chat_history:
    st.divider()
    if st.button("🗑️  Clear conversation", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()
