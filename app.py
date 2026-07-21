"""
Apex Bank — Modern American Neo-Banking Web Portal
-----------------------------------------------------
Premium dark navy + emerald + gold color system.
Session-based login, transaction history, transfers between
accounts, and a real dashboard — original business rules preserved.
"""

import json
import random
import string
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------- #
# Page Setup
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="Apex Bank — Banking, reimagined",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATABASE_FILE = "database.json"
DEPOSIT_LIMIT = 10_000
BRAND = "Apex Bank"

# --------------------------------------------------------------------------- #
# Visual Design System & Custom CSS  —  Navy / Emerald / Gold
# --------------------------------------------------------------------------- #
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #E7ECF3;
    }
    .stApp {
        background: radial-gradient(circle at top left, #101B2D 0%, #0B1420 55%, #070C14 100%);
    }
    h1, h2, h3, h4, h5, h6 { color: #F1F5F9 !important; }
    p, span, label, .stMarkdown { color: #C7D0DC; }

    /* ---------- Generic surfaces ---------- */
    .apex-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 10px 30px -8px rgba(0,0,0,0.45);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    .apex-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 32px -10px rgba(16, 185, 129, 0.18);
        border-color: rgba(16, 185, 129, 0.35);
    }

    /* ---------- Virtual card (premium metal-card look) ---------- */
    .virtual-card {
        background: linear-gradient(135deg, #04120C 0%, #0B3B2E 45%, #146356 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 26px;
        padding: 30px;
        color: #F8FAFC;
        box-shadow: 0 25px 45px -12px rgba(4, 18, 12, 0.65);
        position: relative;
        overflow: hidden;
        margin-bottom: 22px;
    }
    .virtual-card::before {
        content: '';
        position: absolute;
        top: -60%; right: -25%;
        width: 300px; height: 300px;
        background: rgba(212, 175, 55, 0.10);
        border-radius: 50%;
    }
    .virtual-card::after {
        content: '';
        position: absolute;
        bottom: -70px; left: -40px;
        width: 220px; height: 220px;
        background: rgba(16, 185, 129, 0.08);
        border-radius: 50%;
    }
    .chip {
        width: 46px; height: 34px;
        background: linear-gradient(135deg, #F5D67A 0%, #C89A2C 100%);
        border-radius: 7px;
        box-shadow: inset 0 0 4px rgba(0,0,0,0.35);
    }
    .card-number { font-family: 'Courier New', monospace; letter-spacing: 3px; font-size: 1.15rem; font-weight: 700; color: #F5E6B8; }

    /* ---------- Metrics ---------- */
    .metric-title { font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #7C8CA3; margin-bottom: 6px; }
    .metric-value-lg { font-size: 2.1rem; font-weight: 800; color: #F1F5F9; letter-spacing: -0.02em; }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #0D9268 100%) !important;
        color: #06110C !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.7rem 1.4rem !important;
        font-weight: 800 !important;
        font-size: 0.94rem !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.30) !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 10px 24px rgba(16, 185, 129, 0.42) !important; }

    /* ---------- Inputs ---------- */
    .stTextInput input, .stNumberInput input {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        padding: 10px 14px !important;
        background-color: rgba(255,255,255,0.04) !important;
        color: #F1F5F9 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.20) !important;
    }
    .stTabs [data-baseweb="tab"] { color: #9AA7B8; }
    .stTabs [aria-selected="true"] { color: #10B981 !important; }

    /* ---------- Badges & pills ---------- */
    .pill-tag {
        background: rgba(16, 185, 129, 0.12); color: #34D399;
        font-size: 0.72rem; font-weight: 800; padding: 6px 14px; border-radius: 30px;
        letter-spacing: 0.06em; text-transform: uppercase; display: inline-block; margin-bottom: 10px;
    }
    .badge-green { background: rgba(16,185,129,0.15); color: #34D399; padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; }
    .badge-red { background: rgba(248,113,113,0.15); color: #F87171; padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; }
    .badge-blue { background: rgba(212,175,55,0.15); color: #E8C766; padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.75rem; }

    /* ---------- Quick action tiles ---------- */
    .quick-action-btn { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 18px 10px; text-align: center; transition: all .2s ease; }
    .quick-action-btn:hover { border-color: #10B981; background: rgba(16,185,129,0.08); }

    /* ---------- Avatar ---------- */
    .avatar {
        width: 46px; height: 46px; border-radius: 50%;
        background: linear-gradient(135deg, #10B981, #146356);
        color: #06110C; display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: 1.05rem; flex-shrink: 0;
    }

    /* ---------- Transaction rows ---------- */
    .tx-row { display: flex; align-items: center; justify-content: space-between; padding: 14px 4px; border-bottom: 1px solid rgba(255,255,255,0.06); }
    .tx-row:last-child { border-bottom: none; }
    .tx-icon { width: 38px; height: 38px; border-radius: 12px; display:flex; align-items:center; justify-content:center; font-size:1.1rem; margin-right: 12px; }

    /* ---------- Landing hero ---------- */
    .landing-hero {
        background: linear-gradient(135deg, #04120C 0%, #0B3B2E 40%, #146356 75%, #1B7A63 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 28px; padding: 46px 42px; color: #F8FAFC; margin-bottom: 20px;
        box-shadow: 0 25px 45px -15px rgba(4, 18, 12, 0.6);
    }
    .landing-hero h1 { font-size: 2.3rem; font-weight: 900; margin: 0 0 10px 0; letter-spacing: -0.02em; color: #F8FAFC !important; }
    .landing-hero p { font-size: 1.05rem; opacity: 0.92; max-width: 480px; color: #DCEFE7; }
    .feature-chip { display:flex; align-items:center; gap:10px; margin-top: 14px; font-size: 0.92rem; opacity: 0.95; color: #DCEFE7;}

    section[data-testid="stSidebar"] {
        background: #080D16;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Persistence Helpers
# --------------------------------------------------------------------------- #
def load_data() -> list:
    try:
        if Path(DATABASE_FILE).exists():
            with open(DATABASE_FILE) as fs:
                content = fs.read().strip()
                data = json.loads(content) if content else []
                for u in data:
                    u.setdefault("transactions", [])
                return data
    except Exception as err:
        st.error(f"Failed to read database engine: {err}")
    return []


def save_data(data: list) -> None:
    with open(DATABASE_FILE, "w") as fs:
        fs.write(json.dumps(data, indent=4))


def generate_accountno() -> str:
    char = random.choices(string.ascii_uppercase, k=4)
    digits = random.choices(string.digits, k=8)
    return "".join(char + digits)


def mask_acc(acc_no: str) -> str:
    return f"•••• •••• {acc_no[-4:]}" if len(acc_no) >= 4 else acc_no


def find_user(data, acc_no: str, pin: int):
    matches = [i for i in data if i["pin"] == pin and i["accountno."] == acc_no]
    return matches[0] if matches else None


def find_by_accno(data, acc_no: str):
    matches = [i for i in data if i["accountno."] == acc_no]
    return matches[0] if matches else None


def log_tx(user: dict, tx_type: str, amount: float, note: str = ""):
    user.setdefault("transactions", []).insert(
        0,
        {
            "type": tx_type,
            "amount": amount,
            "balance_after": user["balance"],
            "note": note,
            "time": datetime.now().strftime("%b %d, %Y · %I:%M %p"),
        },
    )


# --------------------------------------------------------------------------- #
# Core Business Logic Engine
# --------------------------------------------------------------------------- #
def create_account(name, age, mail, number, pin):
    if len(str(pin)) != 4:
        return False, "Security PIN must be exactly 4 digits.", None
    if age < 18:
        return False, "Minors cannot open an account (must be 18+).", None

    info = {
        "name": name, "age": age, "mail": mail, "balance": 0,
        "accountno.": generate_accountno(), "number": number, "pin": pin,
        "opened": datetime.now().strftime("%b %d, %Y"), "transactions": [],
    }
    st.session_state.data.append(info)
    save_data(st.session_state.data)
    return True, "Account successfully activated!", info


def deposit_money(data, acc_no, pin, amount):
    user = find_user(data, acc_no, pin)
    if not user:
        return False, "Invalid account number or PIN code."
    if amount > DEPOSIT_LIMIT or amount <= 0:
        return False, f"Deposit limit exception: amount must be between ₹1 and ₹{DEPOSIT_LIMIT:,}."
    user["balance"] += amount
    log_tx(user, "deposit", amount, "Cash deposit")
    save_data(data)
    return True, f"Successfully deposited ₹{amount:,.2f}."


def withdraw_money(data, acc_no, pin, amount):
    user = find_user(data, acc_no, pin)
    if not user:
        return False, "Invalid account number or PIN code."
    if amount > user["balance"] or amount <= 0:
        return False, "Transaction declined: insufficient balance or invalid amount."
    user["balance"] -= amount
    log_tx(user, "withdraw", amount, "Cash withdrawal")
    save_data(data)
    return True, f"Successfully debited ₹{amount:,.2f}."


def transfer_money(data, from_acc, pin, to_acc, amount):
    sender = find_user(data, from_acc, pin)
    if not sender:
        return False, "Invalid account number or PIN code."
    if to_acc == from_acc:
        return False, "You cannot transfer money to your own account."
    receiver = find_by_accno(data, to_acc)
    if not receiver:
        return False, "Recipient account number was not found."
    if amount <= 0 or amount > sender["balance"]:
        return False, "Transfer declined: insufficient balance or invalid amount."

    sender["balance"] -= amount
    receiver["balance"] += amount
    log_tx(sender, "transfer_out", amount, f"To {mask_acc(to_acc)}")
    log_tx(receiver, "transfer_in", amount, f"From {mask_acc(from_acc)}")
    save_data(data)
    return True, f"₹{amount:,.2f} sent to {mask_acc(to_acc)}."


def update_details(data, acc_no, pin, new_name, new_mail, new_number, new_pin):
    user = find_user(data, acc_no, pin)
    if not user:
        return False, "Invalid account number or PIN code."
    if new_name:
        user["name"] = new_name
    if new_mail:
        user["mail"] = new_mail
    if new_number:
        user["number"] = int(new_number)
    if new_pin:
        user["pin"] = int(new_pin)
    save_data(data)
    return True, "Account profile updated successfully."


def delete_user(data, acc_no, pin, confirm):
    user = find_user(data, acc_no, pin)
    if not user:
        return False, "Invalid account number or PIN code."
    if not confirm:
        return False, "Account deletion requires explicit checkbox confirmation."
    data.remove(user)
    save_data(data)
    return True, "Account permanently closed and removed."


# --------------------------------------------------------------------------- #
# Session State
# --------------------------------------------------------------------------- #
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "auth" not in st.session_state:
    st.session_state.auth = None
if "reveal_acc" not in st.session_state:
    st.session_state.reveal_acc = False
if "flash" not in st.session_state:
    st.session_state.flash = None


def flash(kind, msg):
    st.session_state.flash = (kind, msg)


def show_flash():
    if st.session_state.flash:
        kind, msg = st.session_state.flash
        getattr(st, kind)(msg)
        st.session_state.flash = None


def current_user():
    if not st.session_state.auth:
        return None, None
    data = load_data()
    user = find_user(data, st.session_state.auth["accountno."], st.session_state.auth["pin"])
    return user, data


def greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"


TX_ICON = {
    "deposit": ("💰", "rgba(16,185,129,0.15)", "#34D399"),
    "withdraw": ("🏧", "rgba(248,113,113,0.15)", "#F87171"),
    "transfer_out": ("📤", "rgba(212,175,55,0.15)", "#E8C766"),
    "transfer_in": ("📥", "rgba(16,185,129,0.15)", "#34D399"),
}

# --------------------------------------------------------------------------- #
# Header helper
# --------------------------------------------------------------------------- #
def render_header(title, subtitle, tag="APEX BANK"):
    st.markdown(
        f"""
        <div style="margin-bottom: 22px;">
            <span class="pill-tag">{tag}</span>
            <h1 style="font-size: 1.9rem; font-weight: 900; margin: 4px 0;">{title}</h1>
            <p style="font-size: 0.95rem; margin: 0;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# LANDING (logged out)
# --------------------------------------------------------------------------- #
def page_landing():
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown(
            """
            <div class="landing-hero">
                <span class="pill-tag" style="background:rgba(212,175,55,0.15); color:#E8C766;">TRUSTED BY 2M+ CUSTOMERS</span>
                <h1>Banking that feels effortless.</h1>
                <p>Open an account in minutes, send money instantly, and track every dollar
                with a dashboard built for real life.</p>
                <div class="feature-chip">✅ &nbsp; FDIC-style deposit protection (demo)</div>
                <div class="feature-chip">⚡ &nbsp; Instant transfers between Apex accounts</div>
                <div class="feature-chip">🔒 &nbsp; PIN-secured, encrypted account records</div>
                <div class="feature-chip">📊 &nbsp; Real-time spending & balance insights</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="apex-card">
                <div class="metric-title">Community snapshot</div>
                <div style="display:flex; gap:32px; margin-top:6px;">
                    <div><div class="metric-value-lg" style="font-size:1.6rem;">{len(st.session_state.data)}</div><span style="color:#7C8CA3; font-size:0.8rem;">Active accounts</span></div>
                    <div><div class="metric-value-lg" style="font-size:1.6rem;">₹{sum(u['balance'] for u in st.session_state.data):,.0f}</div><span style="color:#7C8CA3; font-size:0.8rem;">Total on deposit</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        tab_login, tab_signup = st.tabs(["🔐 Sign In", "✨ Open an Account"])

        with tab_login:
            st.subheader("Welcome back")
            with st.form("login_form"):
                acc_no = st.text_input("Account number", placeholder="e.g. ABCD12345678").strip().upper()
                pin = st.text_input("4-digit PIN", type="password", max_chars=4)
                submitted = st.form_submit_button("Sign In")
            if submitted:
                if not acc_no or not pin.isdigit() or len(pin) != 4:
                    st.error("Enter a valid account number and 4-digit PIN.")
                else:
                    data = load_data()
                    user = find_user(data, acc_no, int(pin))
                    if user:
                        st.session_state.data = data
                        st.session_state.auth = {"accountno.": acc_no, "pin": int(pin)}
                        flash("success", f"{greeting()}, {user['name']}! 👋")
                        st.rerun()
                    else:
                        st.error("Invalid account number or PIN.")

        with tab_signup:
            st.subheader("Join Apex Bank")
            with st.form("create_account_form", clear_on_submit=True):
                name = st.text_input("Full name", placeholder="e.g. Alex Morgan")
                c_a, c_b = st.columns(2)
                with c_a:
                    age = st.number_input("Age", min_value=0, max_value=120, value=21)
                with c_b:
                    pin = st.text_input("Create 4-digit PIN", type="password", max_chars=4, placeholder="****")
                mail = st.text_input("Email address", placeholder="alex@domain.com")
                number = st.text_input("10-digit phone number", placeholder="9876543210")
                submitted = st.form_submit_button("✨ Create My Account")

            if submitted:
                errors = []
                if not name.strip():
                    errors.append("Full name is required.")
                if not mail.strip() or "@" not in mail or "." not in mail:
                    errors.append("Please provide a valid email address.")
                if not number.strip().isdigit() or len(number.strip()) != 10:
                    errors.append("Phone number must contain exactly 10 digits.")
                if not pin.isdigit() or len(pin) != 4:
                    errors.append("PIN must be exactly 4 numeric digits.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    with st.spinner("Generating account credentials..."):
                        success, message, info = create_account(
                            name.strip(), int(age), mail.strip(), int(number), int(pin)
                        )
                    if success:
                        st.success(message)
                        st.balloons()
                        st.markdown(
                            f"""
                            <div class="apex-card" style="border-color:#10B981;">
                                <h4 style="color:#34D399; margin-top:0;">🎉 Welcome to Apex Bank!</h4>
                                <p style="margin-bottom:4px;"><b>Your new account number:</b></p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.code(info["accountno."])
                        st.caption("Save this along with your PIN — you'll need both to sign in.")
                    else:
                        st.warning(message)


# --------------------------------------------------------------------------- #
# AUTHENTICATED APP
# --------------------------------------------------------------------------- #
def page_overview(user, data):
    total_tx = user.get("transactions", [])
    acc_display = user["accountno."] if st.session_state.reveal_acc else mask_acc(user["accountno."])

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(
            f"""
            <div class="virtual-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:800; letter-spacing:0.12em; font-size:0.85rem; color:#E8C766;">APEX PLATINUM</span>
                    <span style="font-weight:900; font-style:italic; color:#F5E6B8;">VISA</span>
                </div>
                <div class="chip" style="margin-top:22px;"></div>
                <div class="card-number" style="margin: 16px 0 6px 0;">{acc_display}</div>
                <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#DCEFE7; margin-top: 14px;">
                    <span>{user['name'].upper()}</span>
                    <span>MEMBER SINCE {user.get('opened', 'N/A')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        b1, b2 = st.columns(2)
        with b1:
            if st.button(("🙈 Hide" if st.session_state.reveal_acc else "👁️ Reveal") + " account number"):
                st.session_state.reveal_acc = not st.session_state.reveal_acc
                st.rerun()
        with b2:
            if st.session_state.reveal_acc:
                st.code(user["accountno."])
            else:
                st.caption("Tap reveal to copy your full account number.")

    with col2:
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(
                f"""<div class="apex-card"><div class="metric-title">Available Balance</div>
                <div class="metric-value-lg">₹{user['balance']:,.2f}</div>
                <span class="badge-green">● Active</span></div>""",
                unsafe_allow_html=True,
            )
        with m2:
            monthly_in = sum(t["amount"] for t in total_tx if t["type"] in ("deposit", "transfer_in"))
            st.markdown(
                f"""<div class="apex-card"><div class="metric-title">Lifetime Deposits</div>
                <div class="metric-value-lg" style="font-size:1.6rem;">₹{monthly_in:,.0f}</div>
                <span class="badge-blue">● All time</span></div>""",
                unsafe_allow_html=True,
            )

    st.markdown("### Quick actions")
    labels = [("💸", "Send"), ("💰", "Deposit"), ("🏧", "Withdraw"), ("📄", "Statements"), ("⚙️", "Settings"), ("🔒", "Security")]
    cols = st.columns(6)
    for c, (icon, label) in zip(cols, labels):
        with c:
            st.markdown(
                f"""<div class="quick-action-btn"><div style="font-size:1.4rem; margin-bottom:4px;">{icon}</div>
                <div style="font-size:0.85rem; font-weight:700; color:#E7ECF3;">{label}</div></div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Balance trend")
    if total_tx:
        df = pd.DataFrame(list(reversed(total_tx)))
        st.line_chart(df.set_index(pd.RangeIndex(1, len(df) + 1))["balance_after"], color="#10B981")
    else:
        st.info("Make your first deposit to start seeing your balance trend here.")


def page_transactions(user):
    render_header("Transaction History", "Every deposit, withdrawal, and transfer on your account", "ACTIVITY")
    tx = user.get("transactions", [])
    if not tx:
        st.info("No transactions yet. Deposit some funds to get started!")
        return

    for t in tx:
        icon, bg, fg = TX_ICON.get(t["type"], ("💳", "rgba(255,255,255,0.06)", "#C7D0DC"))
        sign = "+" if t["type"] in ("deposit", "transfer_in") else "−"
        label = {
            "deposit": "Cash Deposit", "withdraw": "Cash Withdrawal",
            "transfer_out": "Transfer Sent", "transfer_in": "Transfer Received",
        }.get(t["type"], t["type"].title())
        st.markdown(
            f"""
            <div class="tx-row">
                <div style="display:flex; align-items:center;">
                    <div class="tx-icon" style="background:{bg};">{icon}</div>
                    <div>
                        <div style="font-weight:700; font-size:0.95rem; color:#F1F5F9;">{label}</div>
                        <div style="color:#7C8CA3; font-size:0.78rem;">{t['time']} · {t.get('note','')}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:800; color:{fg};">{sign} ₹{t['amount']:,.2f}</div>
                    <div style="color:#7C8CA3; font-size:0.75rem;">Bal: ₹{t['balance_after']:,.2f}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    df = pd.DataFrame(tx)
    with st.expander("📥 Export as table"):
        st.dataframe(df[["time", "type", "amount", "balance_after", "note"]], use_container_width=True, hide_index=True)


def page_move_money(user, data):
    render_header("Move Money", "Deposit, withdraw, or transfer to another Apex account", "PAYMENTS")
    tab_dep, tab_wd, tab_transfer = st.tabs(["💰 Deposit", "🏧 Withdraw", "💸 Transfer"])

    with tab_dep:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            with st.form("deposit_form"):
                amount = st.number_input("Deposit amount (₹)", min_value=0, max_value=DEPOSIT_LIMIT, step=100, value=1000)
                submitted = st.form_submit_button("💳 Deposit Funds")
            if submitted:
                with st.spinner("Processing deposit..."):
                    success, message = deposit_money(data, user["accountno."], user["pin"], int(amount))
                st.success(message) if success else st.error(message)
                if success:
                    st.rerun()
        with col2:
            st.markdown(
                f"""<div class="apex-card"><h4 style="margin-top:0;">⚠️ Deposit limits</h4>
                <p style="color:#7C8CA3; font-size:0.85rem;">Single online deposits are capped at ₹{DEPOSIT_LIMIT:,} for security.</p></div>""",
                unsafe_allow_html=True,
            )

    with tab_wd:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            with st.form("withdraw_form"):
                amount = st.number_input("Withdrawal amount (₹)", min_value=0, step=100, value=500)
                submitted = st.form_submit_button("🏧 Cash Out")
            if submitted:
                with st.spinner("Authorizing with vault..."):
                    success, message = withdraw_money(data, user["accountno."], user["pin"], int(amount))
                st.success(message) if success else st.error(message)
                if success:
                    st.rerun()
        with col2:
            st.markdown(
                f"""<div class="apex-card"><h4 style="margin-top:0;">🔒 Current balance</h4>
                <p style="font-size:1.4rem; font-weight:800; color:#34D399;">₹{user['balance']:,.2f}</p></div>""",
                unsafe_allow_html=True,
            )

    with tab_transfer:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            with st.form("transfer_form"):
                to_acc = st.text_input("Recipient account number").strip().upper()
                amount = st.number_input("Amount to send (₹)", min_value=0, step=100, value=500)
                submitted = st.form_submit_button("💸 Send Money")
            if submitted:
                if not to_acc:
                    st.error("Enter a recipient account number.")
                else:
                    with st.spinner("Sending money..."):
                        success, message = transfer_money(data, user["accountno."], user["pin"], to_acc, int(amount))
                    st.success(message) if success else st.error(message)
                    if success:
                        st.rerun()
        with col2:
            st.markdown(
                """<div class="apex-card"><h4 style="margin-top:0;">⚡ Instant transfers</h4>
                <p style="color:#7C8CA3; font-size:0.85rem;">Money sent to another Apex Bank account arrives instantly, 24/7.</p></div>""",
                unsafe_allow_html=True,
            )


def page_profile(user, data):
    render_header("Profile & Settings", "Manage your personal information", "SETTINGS")
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.markdown(
            f"""
            <div class="apex-card">
                <div style="display:flex; align-items:center; gap:14px; margin-bottom:14px;">
                    <div class="avatar">{user['name'][:1].upper()}</div>
                    <div><div style="font-weight:800; font-size:1.05rem; color:#F1F5F9;">{user['name']}</div>
                    <div style="color:#7C8CA3; font-size:0.82rem;">Member since {user.get('opened','N/A')}</div></div>
                </div>
                <p>📧 <b>Email:</b> {user['mail']}</p>
                <p>📱 <b>Phone:</b> {user['number']}</p>
                <p>🎂 <b>Age:</b> {user['age']}</p>
                <p>🔢 <b>Account:</b> {mask_acc(user['accountno.'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.subheader("Update information")
        st.caption("Leave a field blank to keep it unchanged.")
        with st.form("update_form"):
            new_name = st.text_input("New name")
            new_mail = st.text_input("New email")
            new_number = st.text_input("New phone number", max_chars=10)
            new_pin = st.text_input("New 4-digit PIN", type="password", max_chars=4)
            submitted = st.form_submit_button("💾 Save Changes")

        if submitted:
            errors = []
            if new_number and (not new_number.isdigit() or len(new_number) != 10):
                errors.append("New phone number must be exactly 10 digits.")
            if new_pin and (not new_pin.isdigit() or len(new_pin) != 4):
                errors.append("New PIN must be exactly 4 digits.")
            if new_mail and ("@" not in new_mail or "." not in new_mail):
                errors.append("Please enter a valid email address.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                success, message = update_details(
                    data, user["accountno."], user["pin"], new_name.strip(), new_mail.strip(), new_number.strip(), new_pin.strip()
                )
                if success:
                    if new_pin.strip():
                        st.session_state.auth["pin"] = int(new_pin.strip())
                    flash("success", message)
                    st.rerun()
                else:
                    st.error(message)


def page_security(user, data):
    render_header("Security Center", "Manage account safety and closure", "DANGER ZONE")
    st.markdown(
        """<div class="apex-card"><h4 style="margin-top:0;">🔒 Account protection</h4>
        <p style="color:#7C8CA3; font-size:0.88rem;">Your account is protected by a 4-digit PIN.
        Update it any time from the Profile tab if you suspect it's been compromised.</p></div>""",
        unsafe_allow_html=True,
    )
    st.error("⚠️ Danger Zone: closing your account permanently deletes it and cannot be undone.")
    confirm = st.checkbox("I understand this will permanently delete my account.")
    if st.button("🗑️ Close My Account", disabled=not confirm):
        success, message = delete_user(data, user["accountno."], user["pin"], confirm)
        if success:
            st.session_state.auth = None
            flash("success", message)
            st.rerun()
        else:
            st.error(message)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    with st.sidebar:
        st.markdown(
            f"""<div style="padding:10px 0 20px 0;">
            <h2 style="margin:0; color:#34D399; font-weight:900; letter-spacing:-0.03em;">🏦 {BRAND.upper()}</h2>
            <span style="color:#7C8CA3; font-size:0.8rem; font-weight:600;">Banking, reimagined</span></div>""",
            unsafe_allow_html=True,
        )

        if st.session_state.auth:
            user, data = current_user()
            if user:
                st.markdown(
                    f"""<div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
                    <div class="avatar">{user['name'][:1].upper()}</div>
                    <div><div style="font-weight:800; color:#F1F5F9;">{user['name']}</div>
                    <div style="color:#7C8CA3; font-size:0.78rem;">{mask_acc(user['accountno.'])}</div></div></div>""",
                    unsafe_allow_html=True,
                )
                if st.button("🚪 Log Out", use_container_width=True):
                    st.session_state.auth = None
                    flash("success", "You have been logged out.")
                    st.rerun()

        st.markdown("---")
        st.caption(f"📂 Database: `{DATABASE_FILE}`")
        st.caption(f"👥 Registered accounts: **{len(st.session_state.data)}**")

    show_flash()

    if not st.session_state.auth:
        page_landing()
        return

    user, data = current_user()
    if not user:
        st.error("Your session is no longer valid. Please sign in again.")
        st.session_state.auth = None
        st.stop()

    st.markdown(
        f"<h2 style='font-weight:900; margin-bottom:2px;'>{greeting()}, {user['name'].split()[0]} 👋</h2>"
        f"<p style='color:#7C8CA3; margin-top:0;'>Here's what's happening with your money today.</p>",
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["🏠 Overview", "💸 Move Money", "🧾 Transactions", "👤 Profile", "🔒 Security"])
    with tabs[0]:
        page_overview(user, data)
    with tabs[1]:
        page_move_money(user, data)
    with tabs[2]:
        page_transactions(user)
    with tabs[3]:
        page_profile(user, data)
    with tabs[4]:
        page_security(user, data)


if __name__ == "__main__":
    main()