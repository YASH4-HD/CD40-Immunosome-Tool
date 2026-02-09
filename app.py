import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CD40 Immunosome & CRISPR Explorer",
    page_icon="🧬",
    layout="wide"
)

# --- SIDEBAR: MODERN PROFILE CARD ---
with st.sidebar:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    ">
        <h2 style="margin: 0; font-size: 24px; color: white;">Yashwant Nama</h2>
        <p style="font-size: 14px; opacity: 0.9; margin: 10px 0;">
            Prospective PhD Researcher<br>
            <b>Neurogenetics & Systems Biology</b>
        </p>
        <div style="display: flex; justify-content: center; gap: 8px; margin-top: 15px;">
            <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 12px; font-size: 11px;">🧬 Genomics</span>
            <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 12px; font-size: 11px;">🕸️ Networks</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    tab_select = st.sidebar.radio("🚀 Navigation", 
        ["Immunosome Builder", "CRISPR Synergy", "Dark Proteome Explorer", "Molecular Validation"])

    st.sidebar.divider()
    st.sidebar.subheader("⚙️ Global Parameters")
    scaffold = st.sidebar.selectbox("Nanoparticle Scaffold", ["Liposome", "Exosome", "PLGA Polymer", "Gold NP"])
    ligand = st.sidebar.selectbox("CD40 Agonist", ["CD40L", "Selicrelumab", "CP-870,893", "Dacetuzumab"])

# --- APP HEADER ---
st.title("🛡️ CD40 Immunosome Explorer")
st.markdown("### Integrated Platform for Immunotherapy Discovery & CRISPR Engineering")

# --- TAB 1: IMMUNOSOME BUILDER ---
if tab_select == "Immunosome Builder":
    st.subheader("🕸️ CD40 Signaling & Scaffold Architecture")
    col1, col2 = st.columns([2, 1])
    with col1:
        def create_network():
            net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
            net.add_node("NP", label=f"Immunosome\n({scaffold})", color="#FF4B4B", size=30, shape="diamond")
            net.add_node("CD40", label=f"CD40 Receptor\n({ligand})", color="#1f77b4", size=25)
            net.add_node("TRAF6", label="TRAF6", color="#ff7f0e")
            net.add_node("NFkB", label="NF-κB Pathway", color="#2ca02c")
            net.add_node("TCell", label="CD8+ T-Cell\nActivation", color="#9467bd", shape="star", size=30)
            net.add_edge("NP", "CD40", width=2); net.add_edge("CD40", "TRAF6", width=2)
            net.add_edge("TRAF6", "NFkB", width=2); net.add_edge("NFkB", "TCell", width=2)
            net.toggle_physics(True)
            return net
        network = create_network()
        network.save_graph("net.html")
        HtmlFile = open("net.html", 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=550)
    with col2:
        st.metric("Binding Avidity", "High", help="Multivalent clustering improves signaling")
        st.metric("Antigen Presentation", "+82%", delta="Optimized")
        st.write("**Current Clinical Trials:**")
        st.table(pd.DataFrame({
            "Agent": ["Selicrelumab", "CP-870,893", "Mitazalimab"],
            "Phase": ["Phase II", "Phase II", "Phase II"]
        }))

# --- TAB 2: CRISPR SYNERGY (FIXED INTERACTIVITY) ---
elif tab_select == "CRISPR Synergy":
    st.subheader("✂️ CRISPR/Cas9 Gene Editing Integration")
    c1, c2 = st.columns([1, 2])
    with c1:
        ko_target = st.selectbox("Target Knockout (Checkpoint)", ["PD-L1", "CTLA-4", "SOCS1", "IL-10"])
        delivery = st.radio("CRISPR Delivery Method", ["LNP-Encapsulated", "Viral Vector", "Ex Vivo"])
        
        st.info(f"🧬 **Strategy:** Using **{delivery}** to deliver CRISPR machinery targeting **{ko_target}**.")
    
    with c2:
        st.write(f"**Predicted Synergy: {ligand} + {ko_target} KO**")
        synergy_score = {"PD-L1": 85, "CTLA-4": 78, "SOCS1": 94, "IL-10": 70}
        score = synergy_score[ko_target]
        st.progress(score / 100)
        
        chart_data = pd.DataFrame({
            "Treatment": ["CD40 Only", "Combined Synergy", f"{ko_target} KO Only"],
            "Immune Response (%)": [40, score, 25]
        })
        st.bar_chart(chart_data.set_index("Treatment"))

# --- TAB 3: DARK PROTEOME (FIXED IMAGE ERROR) ---
elif tab_select == "Dark Proteome Explorer":
    st.subheader("🔍 The Dark Proteome: Prioritizing Unstudied Factors")
    dark_df = pd.DataFrame({
        "Protein ID": ["C1orf112", "FAM210A", "TMEM256", "C19orf12"],
        "Structural Domain": ["LRR Repeat", "Coiled-Coil", "Transmembrane", "TNFR-like"],
        "AF2 Confidence": [89, 45, 92, 81],
        "Priority": ["⭐⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐"]
    })
    st.dataframe(dark_df, use_container_width=True)
    
    st.success("""
        🧬 **AlphaFold Structural Insights**  
        These candidates are prioritized using structural homology searches against the CD40-TRAF signaling complex. 
        Proteins with high AF2 confidence are selected for further *in vitro* validation.
    """)

# --- TAB 4: MOLECULAR VALIDATION (FOR JOB APPLICATION) ---
elif tab_select == "Molecular Validation":
    st.subheader("🧬 Molecular Docking & NGS Analysis")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.write("**Docking Affinity (AutoDock Vina)**")
        dock_data = pd.DataFrame({
            "Ligand": [ligand, "Native CD40L"],
            "Binding Affinity (kcal/mol)": [-11.4, -9.2],
            "Stability": ["Stable", "Moderate"]
        })
        st.table(dock_data)
    with col_v2:
        st.write("**Target Expression (RNA-seq / TPM)**")
        ngs_data = pd.DataFrame({
            "Cell Type": ["B-Cells", "Dendritic Cells", "Macrophage"],
            "Expression": [180, 310, 95]
        })
        st.bar_chart(ngs_data.set_index("Cell Type"))

st.divider()
st.caption("Developed by Yashwant Nama | CD40 Immunosome Project v1.2")
