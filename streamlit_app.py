import streamlit as st
import requests
import json
import time
from datetime import datetime
from requests.auth import HTTPBasicAuth

# --- Page Configuration ---
st.set_page_config(
    page_title="Ogury One API",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS Styling matching styles.css ---
st.markdown("""
<style>
    /* Background & Global */
    .stApp {
        background-color: #f9fafb;
        background-image: 
            radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.05) 0px, transparent 50%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide native sidebar and its toggle controller */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1600px;
    }

    /* Style the main containers inside columns as glass cards */
    div[data-testid="column"]:nth-of-type(1) > div > [data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="column"]:nth-of-type(2) > div > [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        padding: 1.5rem !important;
        overflow: hidden !important;
    }

    /* Target Terminal column separately for dark card look */
    div[data-testid="column"]:nth-of-type(3) > div > [data-testid="stVerticalBlockBorderWrapper"] {
        background: #181e29 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
        padding: 1.0rem 1.2rem !important;
        overflow: hidden !important;
    }

    /* Sidebar title styling */
    .logo-container h2 {
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #111827;
        margin-top: 0px;
        margin-bottom: 1.5rem;
    }
    .logo-container h2 span {
        color: #2563eb;
    }

    .sidebar-section-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6b7280;
        margin-bottom: 0.6rem;
        margin-top: 1.2rem;
        font-weight: 600;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        padding-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #6b7280 !important;
        padding: 0.5rem 1.0rem !important;
        font-size: 0.95rem !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        background: rgba(37, 99, 235, 0.05) !important;
        font-weight: 600 !important;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* Node Headers */
    .node-header {
        color: #2563eb;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1rem;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600;
        border-bottom: 1px solid rgba(0,0,0,0.08);
        padding-bottom: 0.5rem;
    }

    /* Custom request builder divider */
    .custom-request-divider {
        border-top: 1px dashed rgba(0, 0, 0, 0.08);
        margin-top: 1.0rem;
        margin-bottom: 1.0rem;
        height: 1px;
    }

    /* Action Buttons - Unified and Strict No Wrap */
    .stButton > button {
        background: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        padding: 0.3rem 0.2rem !important;
        font-size: 0.70rem !important;
        font-weight: 500 !important;
        white-space: nowrap !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        min-height: 38px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    .stButton > button:hover {
        background: #f9fafb !important;
        border-color: #2563eb !important;
        color: #2563eb !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    /* Primary Button (Send/Generate) */
    .stButton > button[kind="primary"] {
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
    }

    /* Terminal buttons styling */
    div[data-testid="column"]:nth-of-type(3) button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #e5e7eb !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-size: 10px !important;
        min-height: 24px !important;
        height: 24px !important;
        padding: 2px 6px !important;
    }
    div[data-testid="column"]:nth-of-type(3) button:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
    }

    
    /* Subtle User Manual Link styling */
    .manual-download-btn > button {
        background: transparent !important;
        border: none !important;
        color: #6b7280 !important;
        font-size: 0.75rem !important;
        padding: 0 !important;
        min-height: auto !important;
        height: auto !important;
        box-shadow: none !important;
        justify-content: flex-start !important;
        margin-bottom: 1.5rem !important;
        margin-top: -1.0rem !important;
    }
    .manual-download-btn > button:hover {
        color: #2563eb !important;
        background: transparent !important;
        transform: none !important;
        text-decoration: underline !important;
    }

    /* Status Badge */
    .status-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        background: rgba(241, 245, 249, 0.8);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 500;
    }
    .indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }
    .connected { background-color: #10b981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }
    .disconnected { background-color: #ef4444; }

    /* Custom scrollbars inside Streamlit containers */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
    div[data-testid="column"]:nth-of-type(3) ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'token' not in st.session_state:
    st.session_state.token = None
if 'expires_at' not in st.session_state:
    st.session_state.expires_at = None
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Helper Functions ---
def get_ogury_token(client_id, client_secret):
    url = "https://api.ogury.com/oauth2/token"
    payload = {"grant_type": "client_credentials"}
    auth = HTTPBasicAuth(client_id, client_secret)
    try:
        response = requests.post(url, data=payload, auth=auth, timeout=15)
        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data.get("access_token")
            expires_in = data.get("expires_in", 3600)
            st.session_state.expires_at = time.time() + expires_in
            return True, "Authentication successful."
        else:
            return False, f"Auth Failed ({response.status_code}): {response.text}"
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

def call_ogury_api(endpoint, method="GET", payload=None, params=None):
    if not st.session_state.token:
        st.error("Missing Authentication Token. Please generate a token first.")
        return

    url = f"https://api.ogury.com/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {st.session_state.token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=payload,
            params=params,
            timeout=30
        )
        
        try:
            result = response.json()
        except:
            result = {"text": response.text}
            
        st.session_state.last_response = {
            "status": response.status_code,
            "url": url,
            "method": method,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "data": result
        }
        
        # Add to history
        st.session_state.history.insert(0, f"{method} {endpoint}")
        if len(st.session_state.history) > 10:
            st.session_state.history.pop()
            
    except Exception as e:
        st.error(f"Request failed: {str(e)}")

# --- Callbacks ---
def set_demo(method, endpoint, payload=None):
    st.session_state.demo_method = method
    st.session_state.demo_endpoint = endpoint
    if payload:
        st.session_state.demo_payload = json.dumps(payload, indent=2)
    else:
        st.session_state.demo_payload = ""

if 'demo_method' not in st.session_state: st.session_state.demo_method = "GET"
if 'demo_endpoint' not in st.session_state: st.session_state.demo_endpoint = ""
if 'demo_payload' not in st.session_state: st.session_state.demo_payload = ""

# --- Main UI Layout (3 Columns Aligned Perfectly at the Bottom) ---
col_sidebar, col_playground, col_terminal = st.columns([0.8, 2.0, 1.2])

# Column 1: Configuration & Status Sidebar Card
with col_sidebar:
    with st.container(height=680):
        
        import base64
        manual_b64 = ""
        try:
            # User Manual Download Button
            with open("User_Manual.md", "r", encoding="utf-8") as f:
                manual_content = f.read()
                manual_b64 = base64.b64encode(manual_content.encode("utf-8")).decode("utf-8")
        except FileNotFoundError:
            manual_b64 = ""
            
        st.markdown(f"""
            <div class="logo-container" style="margin-bottom: 1.5rem;">
                <h2 style="margin-bottom: 0.2rem;">Ogury <span>One API</span></h2>
                <a href="data:text/markdown;base64,{manual_b64}" download="Ogury_One_API_User_Manual.md" style="color: #6b7280; font-size: 0.8rem; text-decoration: none; display: inline-block;">
                    📖  User Manual
                </a>
            </div>
        """, unsafe_allow_html=True)

        
        st.markdown("<div class='sidebar-section-title'>CONFIGURATION</div>", unsafe_allow_html=True)
        client_id = st.text_input("Client ID", placeholder="Enter Client ID", label_visibility="collapsed")
        client_secret = st.text_input("Client Secret", type="password", placeholder="Enter Client Secret", label_visibility="collapsed")
        
        if st.button("Generate Token", type="primary", use_container_width=True):
            if client_id and client_secret:
                success, msg = get_ogury_token(client_id, client_secret)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Please enter credentials.")

        st.markdown("<div class='sidebar-section-title'>STATUS</div>", unsafe_allow_html=True)
        if st.session_state.token:
            st.markdown(f"""
            <div class="status-badge">
                <span class="indicator connected"></span>
                <span>Authenticated</span>
            </div>
            """, unsafe_allow_html=True)
            remaining = int(st.session_state.expires_at - time.time())
            if remaining > 0:
                st.caption(f"Expires in: {remaining // 60}m {remaining % 60}s")
            else:
                st.session_state.token = None
                st.rerun()
        else:
            st.markdown("""
            <div class="status-badge">
                <span class="indicator disconnected"></span>
                <span>Not Authenticated</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='sidebar-section-title'>HISTORY</div>", unsafe_allow_html=True)
        if not st.session_state.history:
            st.caption("No requests yet")
        for item in st.session_state.history:
            st.caption(item)

# Column 2: Playground & Custom Request Builder Card
with col_playground:
    with st.container(height=680):
        # Tabs scrollable wrapper to keep custom builder stationary at the bottom
        with st.container(height=390, border=False):
            tab1, tab2, tab3, tab4 = st.tabs(["Personas", "Accounts & Brands", "Deals & DSPs", "Reporting"])

            with tab1:
                st.markdown('<div class="node-header">Node: Personas</div>', unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns([1.1, 1.2, 1.2, 1.3])
                c1.button("GET Persona", on_click=set_demo, args=("GET", "v1/personas"), use_container_width=True)
                c2.button("GET Basic Persona", on_click=set_demo, args=("GET", "v1/personas?personaType=basic-persona"), use_container_width=True)
                c3.button("GET Vertical: Tech", on_click=set_demo, args=("GET", "v1/personas?category=interest&vertical=technology"), use_container_width=True)
                c4.button("GET Persona by ID", on_click=set_demo, args=("GET", "v1/personas/7781"), use_container_width=True)

                col_my_pers, col_comb = st.columns([2.5, 1.5])
                with col_my_pers:
                    st.markdown('<div class="node-header">Node: My Personas</div>', unsafe_allow_html=True)
                    demo_payload_save = {"country": "US", "expression": {"operands": [7781, 7781], "operator": "AND"}, "age": ["18-24"], "gender": "all", "metrics": ["deviceReach"], "name": "Demo Audience", "brief": "Demo audience using persona 7781", "accountId": "001N200000CJPR9IAP", "brandId": "001N200000CvCjvIAF", "owner": "dev@example.com"}
                    st.button("POST Save Persona", on_click=set_demo, args=("POST", "v1/personas/my-personas", demo_payload_save), use_container_width=True)
                
                with col_comb:
                    st.markdown('<div class="node-header">Node: Combine</div>', unsafe_allow_html=True)
                    demo_payload_combine = {"country": "US", "expression": {"operands": [7781, 7781], "operator": "AND"}, "age": ["18-24"], "gender": "all", "metrics": ["deviceReach", "socioDemo"]}
                    st.button("POST Combine", on_click=set_demo, args=("POST", "v1/personas/combine", demo_payload_combine), use_container_width=True)

                col_trans, col_countries = st.columns([2.5, 1.5])
                with col_trans:
                    st.markdown('<div class="node-header">Node: Translate</div>', unsafe_allow_html=True)
                    ct1, ct2 = st.columns(2)
                    payload_trans_text = {"format": "default", "input": {"brief": "Tech enthusiasts who travel frequently", "country": "US"}}
                    ct1.button("POST Translate (Text)", on_click=set_demo, args=("POST", "v1/personas/translate", payload_trans_text), use_container_width=True)
                    payload_trans_pql = {
                        "format": "pql",
                        "input": {
                            "pql": "INTEREST(technology) AND GEOGRAPHY(US)",
                            "country": "US"
                        }
                    }
                    ct2.button("POST Translate (PQL)", on_click=set_demo, args=("POST", "v1/personas/translate", payload_trans_pql), use_container_width=True)
                
                with col_countries:
                    st.markdown('<div class="node-header">Node: Countries</div>', unsafe_allow_html=True)
                    st.button("GET Countries", on_click=set_demo, args=("GET", "v1/personas/countries"), use_container_width=True)

            with tab2:
                st.markdown('<div class="node-header">Node: Accounts</div>', unsafe_allow_html=True)
                st.button("GET All Accounts", on_click=set_demo, args=("GET", "v1/accounts"), use_container_width=True)
                
                st.markdown('<div class="node-header">Node: Brands</div>', unsafe_allow_html=True)
                st.button("GET All Brands", on_click=set_demo, args=("GET", "v1/brands"), use_container_width=True)

            with tab3:
                st.markdown('<div class="node-header">Node: Deals</div>', unsafe_allow_html=True)
                d1, d2, d3, d4 = st.columns(4)
                d1.button("GET List Deals", on_click=set_demo, args=("GET", "v1/deals"), use_container_width=True)
                d2.button("GET Deal by ID", on_click=set_demo, args=("GET", "v1/deals/DEAL_ID_HERE"), use_container_width=True)
                
                payload_deal_create = {"type": "PD", "name": "My New Deal", "accountId": "001N200000CJPR9IAP", "brandId": "001N200000CvCjvIAF", "seatId": "ENTER_YOUR_SEAT_ID", "dspId": "4", "startDate": "2026-06-04", "endDate": "2026-07-04", "price": {"amount": 1.5, "currency": "USD"}}
                d3.button("POST Create Deal", on_click=set_demo, args=("POST", "v1/deals", payload_deal_create), use_container_width=True)
                payload_deal_update = {"name": "Updated Deal Name", "bid": 10.5, "budget": 2000}
                d4.button("PUT Update Deal", on_click=set_demo, args=("PUT", "v1/deals/DEAL_ID_HERE", payload_deal_update), use_container_width=True)

                st.markdown('<div class="node-header">Node: DSPs</div>', unsafe_allow_html=True)
                ds1, _ = st.columns([1, 3])
                ds1.button("GET List DSPs", on_click=set_demo, args=("GET", "v1/dsps"), use_container_width=True)

            with tab4:
                r1, r2 = st.columns(2)
                start_date = r1.date_input("Start Date", value=datetime(2026, 5, 1))
                end_date = r2.date_input("End Date", value=datetime.now())
                
                c1, c2, c3, c4 = st.columns(4)
                rep_acc = c1.text_input("Account ID(s)", value="001N200000CJPR9IAP")
                rep_brand = c2.text_input("Brand ID(s)", value="001N200000CvCjvIAF")
                rep_camp = c3.text_input("Campaign ID(s)", placeholder="e.g. 166727")
                rep_country = c4.text_input("Country Code (ISO)", placeholder="e.g. SG, FR, US")

                def run_report_demo(node):
                    params = {
                        "startDate": start_date.strftime("%Y-%m-%d"),
                        "endDate": end_date.strftime("%Y-%m-%d")
                    }
                    if rep_acc: params["accountIds"] = rep_acc
                    if rep_brand:
                        if node == "creatives": params["brandIds"] = rep_brand
                        else: params["brandId"] = rep_brand
                    if rep_camp:
                        if node == "creatives": params["campaignIds"] = rep_camp
                        else: params["campaignId"] = rep_camp
                    if rep_country: params["country"] = rep_country
                    
                    qs = "&".join([f"{k}={v}" for k, v in params.items()])
                    endpoint = f"v1/reporting/{node}?{qs}"
                    
                    # Update demo builder
                    set_demo("GET", endpoint)
                    # Run query
                    call_ogury_api(f"v1/reporting/{node}", params=params)

                st.markdown('<div class="node-header">Reporting Nodes</div>', unsafe_allow_html=True)
                rg1, rg2, rg3, rg4 = st.columns(4)
                rg1.button("GET Account", on_click=run_report_demo, args=("account",), use_container_width=True)
                rg2.button("GET Campaigns", on_click=run_report_demo, args=("campaigns",), use_container_width=True)
                rg3.button("GET Creatives", on_click=run_report_demo, args=("creatives",), use_container_width=True)
                rg4.button("GET Geography", on_click=run_report_demo, args=("geography",), use_container_width=True)
                
                rg5, rg6, rg7, _ = st.columns(4)
                rg5.button("GET Region", on_click=run_report_demo, args=("region",), use_container_width=True)
                rg6.button("GET Devices", on_click=run_report_demo, args=("devices",), use_container_width=True)
                rg7.button("GET Daily", on_click=run_report_demo, args=("daily",), use_container_width=True)

        st.markdown('<div class="custom-request-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem; font-weight:600; margin-bottom:0.6rem; color:#111827;">Custom Request Builder</div>', unsafe_allow_html=True)
        
        # Custom Request Builder Inputs bound to session state directly via keys
        cm_col, ce_col, cb_col = st.columns([1.5, 3.5, 1.3])
        method = cm_col.selectbox("Method", ["GET", "POST", "PUT", "DELETE"], key="demo_method", label_visibility="collapsed")
        endpoint = ce_col.text_input("Endpoint", placeholder="e.g., v1/personas?country=US", key="demo_endpoint", label_visibility="collapsed")
        
        if cb_col.button("Send", type="primary", use_container_width=True):
            payload = None
            if st.session_state.demo_payload:
                try: payload = json.loads(st.session_state.demo_payload)
                except: st.error("Invalid JSON")
            if endpoint: call_ogury_api(endpoint, method=method, payload=payload)
            
        payload_str = st.text_area("Payload", placeholder='{"optional_json_payload": "here"}', key="demo_payload", label_visibility="collapsed", height=95)

# Column 3: Terminal Output Panel Card
with col_terminal:
    with st.container(height=680):
        # Header Row mimicking a real terminal title bar
        th1, th2, th3 = st.columns([3.0, 2.0, 1.4])
        th1.markdown("""
            <div style="display:flex; align-items:center; gap:8px; height:100%; padding-top:6px; white-space:nowrap;">
                <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ff5f56;"></span>
                <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ffbd2e;"></span>
                <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#27c93f;"></span>
                <span style="margin-left:6px; color: #9ca3af; font-family: monospace; font-size:12px;">Response Output</span>
            </div>
        """, unsafe_allow_html=True)

        res = st.session_state.last_response
        if res:
            json_str = json.dumps(res['data'], indent=2)
            with th2:
                st.download_button(label="Download", data=json_str, file_name=f"ogury_res_{res['timestamp'].replace(':','_')}.json", mime="application/json", use_container_width=True)
            with th3:
                if st.button("Clear", use_container_width=True):
                    st.session_state.last_response = None
                    st.rerun()
        else:
            with th2:
                st.button("Download", disabled=True, use_container_width=True)
            with th3:
                if st.button("Clear", use_container_width=True):
                    st.session_state.last_response = None
                    st.rerun()

        st.markdown("<hr style='margin: 0.5rem 0; border: 0; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

        # The actual scrolling container for the response content
        with st.container(height=560, border=False):
            if res:
                st.markdown(f"""
                <div style='background-color: rgba(37, 99, 235, 0.1); border-left: 4px solid #2563eb; padding: 6px 10px; border-radius: 4px; color: #e5e7eb; font-family: monospace; font-size: 11px; margin-bottom: 8px; word-break: break-all;'>
                    <strong style='color:#60a5fa;'>{res['method']}</strong> {res['url']} <br/>
                    <span style='color: {'#34d399' if str(res['status']).startswith('2') else '#f87171'};'>[{res['status']}]</span> | <span style='color:#9ca3af;'>{res['timestamp']}</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<style>div[data-testid='stJson'] { font-size: 11px !important; }</style>", unsafe_allow_html=True)
                st.json(res['data'])
            else:
                st.code("// Waiting for requests...", language="javascript")
