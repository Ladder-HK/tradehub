import streamlit as st
import pandas as pd
import plotly.express as px
import uuid
import random
from datetime import datetime
import io
import zipfile

def export_all_data():

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zf:

        datasets = {

            "platform_summary.csv":
            summary,

            "invoices.csv":
            pd.DataFrame(st.session_state.invoices),

            "oracle_events.csv":
            pd.DataFrame(st.session_state.oracle_events),

            "blockchain_ledger.csv":
            pd.DataFrame(st.session_state.ledger),

            "settlements.csv":
            pd.DataFrame(st.session_state.settlements),

            "kyb_registry.csv":
            pd.DataFrame(st.session_state.kyb)
        }


        for filename, df in datasets.items():

            csv_data = df.to_csv(
                index=False
            )

            zf.writestr(
                filename,
                csv_data
            )

    zip_buffer.seek(0)

    return zip_buffer

# --------------------------------------------------
# CSV EXPORT HELPER
# --------------------------------------------------

def download_csv(data, filename, label):
    if len(data) > 0:
        df = pd.DataFrame(data)

        st.download_button(
            label=label,
            data=df.to_csv(index=False),
            file_name=filename,
            mime="text/csv"
        )

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Ladder Street Trade Data Hub",
    page_icon="🌐",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

for key in [
    "invoices",
    "oracle_events",
    "ledger",
    "settlements",
    "kyb"
]:
    if key not in st.session_state:
        st.session_state[key] = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🌐 Ladder Street")

page = st.sidebar.radio(
    "Platform Modules",
    [
        "Dashboard",
        "🏢 ERP Integration",
        "📄 E-Fapiao Verification",
        "🔮 Data Oracles",
        "🌐 Trade Data Hub",
        "🔗 Blockchain",
        "🏦 Capital Markets",
        "🪙 Stablecoin Settlement",
        "📊 Risk Dashboard",
        "🔐 KYC / KYB",
        "📈 Investor Reporting"
    ]
)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.title("🌐 Ladder Street Trade Data Hub")

    st.markdown("""
    **Trusted Trade Data • Trusted Capital • Trusted Payments**
    """)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Invoices",
        len(st.session_state.invoices)
    )

    c2.metric(
        "Oracle Events",
        len(st.session_state.oracle_events)
    )

    c3.metric(
        "Blockchain Records",
        len(st.session_state.ledger)
    )

    c4.metric(
        "Stablecoin Settlements",
        len(st.session_state.settlements)
    )

    st.divider()

    st.subheader("Platform Architecture")

    st.code("""
ERP Systems
     ↓
E-Fapiao Verification
     ↓
Trade Data Hub
     ↓
Data Oracles
     ↓
Blockchain Trust Layer
     ↓
Capital Markets
     ↓
Stablecoin Settlement
""")

st.subheader("Data Exports")

summary = pd.DataFrame({

    "Metric": [

        "Invoices",
        "Oracle Events",
        "Blockchain Records",
        "Settlements",
        "KYB Entities"

    ],

    "Value": [

        len(st.session_state.invoices),

        len(st.session_state.oracle_events),

        len(st.session_state.ledger),

        len(st.session_state.settlements),

        len(st.session_state.kyb)
    ]
})

st.divider()

st.subheader("📦 Export Platform Data")

zip_file = export_all_data()

st.download_button(
    label="⬇️ Export Entire Platform",
    data=zip_file,
    file_name="LadderStreet_Export.zip",
    mime="application/zip"
)

st.subheader("Platform Summary")

st.dataframe(summary)

summary = pd.DataFrame({

    "Metric": [

        "Invoices",
        "Oracle Events",
        "Blockchain Records",
        "Settlements",
        "KYB Entities"

    ],

    "Value": [

        len(st.session_state.invoices),

        len(st.session_state.oracle_events),

        len(st.session_state.ledger),

        len(st.session_state.settlements),

        len(st.session_state.kyb)

    ]
})

st.dataframe(summary)


summary = pd.DataFrame({

    "Metric": [
        "Invoices",
        "Oracle Events",
        "Blockchain Records",
        "Settlements",
        "KYB Entities"
    ],

    "Value": [
        len(st.session_state.invoices),
        len(st.session_state.oracle_events),
        len(st.session_state.ledger),
        len(st.session_state.settlements),
        len(st.session_state.kyb)
    ]
})

st.subheader("Platform Summary")

st.dataframe(summary)

st.divider()

st.subheader(
    "📦 Platform Export"
)

st.markdown(
    """
    Download all trade,
    settlement, compliance,
    oracle and blockchain data.
    """
)

zip_file = export_all_data()

st.download_button(

    label="⬇️ Export Entire Platform",

    data=zip_file,

    file_name=(
        "LadderStreet_"
        "TradeDataHub_Export.zip"
    ),

    mime="application/zip"
)

summary = pd.DataFrame({

    "Metric": [

        "Invoices",
        "Oracle Events",
        "Blockchain Records",
        "Settlements",
        "KYB Entities"

    ],

    "Value": [

        len(st.session_state.invoices),

        len(st.session_state.oracle_events),

        len(st.session_state.ledger),

        len(st.session_state.settlements),

        len(st.session_state.kyb)
    ]
})

# --------------------------------------------------
# ERP
# --------------------------------------------------
if page == "Dashboard":
    st.title("Dashboard")

if page == "🏢 ERP Integration":

    st.header("🏢 ERP Integration Layer")

    uploaded = st.file_uploader(
        "Upload ERP CSV",
        type="csv"
    )

    if uploaded:

        df = pd.read_csv(uploaded)

        st.success("ERP File Imported")

        st.dataframe(df)

# --------------------------------------------------
# E-FAPIAO
# --------------------------------------------------

elif page == "📄 E-Fapiao Verification":

    st.header("📄 E-Fapiao Verification")

    seller = st.text_input("Seller")

    buyer = st.text_input("Buyer")

    amount = st.number_input(
        "Invoice Amount",
        min_value=0.0
    )

    if st.button("Verify Invoice"):

        invoice_id = str(uuid.uuid4())[:8]

        verified = random.choice(
            [True, True, True, False]
        )

        invoice = {
            "Invoice ID": invoice_id,
            "Seller": seller,
            "Buyer": buyer,
            "Amount": amount,
            "Verified": verified
        }

        st.session_state.invoices.append(invoice)

        if verified:
            st.success(
                f"✅ Invoice {invoice_id} Verified"
            )
        else:
            st.error(
                f"❌ Invoice {invoice_id} Rejected"
            )

    if st.session_state.invoices:
        invoice_df = pd.DataFrame(
            st.session_state.invoices
        )

        st.dataframe(invoice_df)

        download_csv(
            st.session_state.invoices,
            "invoices.csv",
            "⬇️ Export Invoices CSV"
        )

# --------------------------------------------------
# ORACLES
# --------------------------------------------------

elif page == "🔮 Data Oracles":

    st.header("🔮 Data Oracle Services")

    oracle_event = st.selectbox(
        "Select Event",
        [
            "Shipment Created",
            "Customs Cleared",
            "Port Arrival",
            "Goods Delivered",
            "Payment Triggered"
        ]
    )

    if st.button("Publish Event"):

        event = {

            "Event":
            oracle_event,

            "Timestamp":
            datetime.now()
        }

        st.session_state.oracle_events.append(
            event
        )

        st.success("Oracle Event Recorded")

    if st.session_state.oracle_events:

        st.dataframe(
            pd.DataFrame(
                st.session_state.oracle_events
            )
        )

        download_csv(
            st.session_state.oracle_events,
            "oracle_events.csv",
            "⬇️ Export Oracle Events"
        )

# --------------------------------------------------
# TRADE HUB
# --------------------------------------------------

elif page == "🌐 Trade Data Hub":

    st.header("🌐 Trade Data Hub")

    if st.session_state.invoices:

        trade_df = pd.DataFrame(
            st.session_state.invoices
        )

    st.dataframe(trade_df)

    download_csv(
        st.session_state.invoices,
        "trade_hub.csv",
        "⬇️ Export Trade Hub"
    )

# --------------------------------------------------
# BLOCKCHAIN
# --------------------------------------------------

elif page == "🔗 Blockchain":

    st.header("🔗 Blockchain Trust Layer")

    if st.button("Create Blockchain Record"):

        tx = {

            "TX ID":
            str(uuid.uuid4()),

            "Timestamp":
            str(datetime.now())
        }

        st.session_state.ledger.append(tx)

        st.success("Record Written")

    if st.session_state.ledger:

        ledger_df = pd.DataFrame(
            st.session_state.ledger
        )

        st.dataframe(ledger_df)

        download_csv(
            st.session_state.ledger,
            "blockchain_ledger.csv",
            "⬇️ Export Blockchain Ledger"
        )

# --------------------------------------------------
# CAPITAL MARKETS
# --------------------------------------------------

elif page == "🏦 Capital Markets":

    st.header("🏦 Capital Markets Module")

    pool = st.text_input(
        "Funding Pool Name"
    )

    value = st.number_input(
        "Pool Value (USD)"
    )

    yield_rate = st.slider(
        "Target Yield %",
        1,
        15,
        8
    )

    if st.button("Create Pool"):

        st.success(
            f"Created {pool}"
        )

        st.metric(
            "Target Yield",
            f"{yield_rate}%"
        )

# --------------------------------------------------
# STABLECOINS
# --------------------------------------------------

elif page == "🪙 Stablecoin Settlement":

    st.header("🪙 Stablecoin Settlement")

    coin = st.selectbox(
        "Stablecoin",
        [
            "HKD",
            "AUD",
            "USD"
        ]
    )

    amount = st.number_input(
        "Payment Value"
    )

    if st.button("Execute Settlement"):

        tx = {

            "TX ID":
            str(uuid.uuid4()),

            "Currency":
            coin,

            "Amount":
            amount,

            "Status":
            "SETTLED"
        }

        st.session_state.settlements.append(tx)

        st.success("Settlement Complete")

    if st.session_state.settlements:

        settlement_df = pd.DataFrame(
            st.session_state.settlements
        )

        st.dataframe(settlement_df)

        download_csv(
            st.session_state.settlements,
            "stablecoin_settlements.csv",
            "⬇️ Export Settlements"
        )

# --------------------------------------------------
# RISK
# --------------------------------------------------

elif page == "📊 Risk Dashboard":

    st.header("📊 Risk Dashboard")

    trust_score = random.randint(
        70,
        98
    )

    st.metric(
        "Trade Trust Score",
        trust_score
    )

    risk_df = pd.DataFrame({

        "Risk Factor":
        [
            "Counterparty",
            "Country",
            "Invoice",
            "Settlement"
        ],

        "Score":
        [
            random.randint(70,100),
            random.randint(70,100),
            random.randint(70,100),
            random.randint(70,100)
        ]
    })

    fig = px.bar(
        risk_df,
        x="Risk Factor",
        y="Score",
        color="Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# KYC
# --------------------------------------------------

elif page == "🔐 KYC / KYB":

    st.header("🔐 Identity / KYB")

    company = st.text_input(
        "Company Name"
    )

    jurisdiction = st.text_input(
        "Jurisdiction"
    )

    reg = st.text_input(
        "Registration Number"
    )

    if st.button("Approve Entity"):

        st.session_state.kyb.append({

            "Company":
            company,

            "Jurisdiction":
            jurisdiction,

            "Registration":
            reg
        })

        st.success(
            f"{company} Approved"
        )

    if st.session_state.kyb:

        kyb_df = pd.DataFrame(
            st.session_state.kyb
        )

        st.dataframe(kyb_df)

        download_csv(
            st.session_state.kyb,
            "kyb_registry.csv",
            "⬇️ Export KYB Registry"
        )

# --------------------------------------------------
# INVESTOR REPORTING
# --------------------------------------------------

elif page == "📈 Investor Reporting":

    st.header("📈 Portfolio Reporting")

    portfolio_value = max(
        len(st.session_state.invoices)
        * 100000,
        1000000
    )

    st.metric(
        "Portfolio Value",
        f"${portfolio_value:,.0f}"
    )

    report_df = pd.DataFrame({

        "Metric":
        [
            "Yield",
            "Collections",
            "Performance"
        ],

        "Value":
        [
            8.2,
            96,
            93
        ]
    })

    fig = px.bar(
        report_df,
        x="Metric",
        y="Value"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    download_csv(
    report_df.to_dict("records"),
    "investor_report.csv",
    "⬇️ Export Investor Report"
)