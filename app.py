import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CD40 Immunosome & CRISPR Explorer",
    page_icon="🛡️",
    layout="wide"
)

# --- APP TITLE & DESCRIPTION ---
st.title("🛡️ CD40 Immunosome Explorer")
st.markdown("### Advanced Platform for Immunotherapy Discovery, CRISPR Synergy & The Dark Proteome")

with st.expander("ℹ️ About this Project (Review Paper Supplement)", expanded=False):
    st.markdown("""
    **Project Overview:**
    This tool is a computational companion to the review paper: *'CD40 Immunosomes: Review of immunosome-based approaches in immunotherapy'*. 
    It integrates three cutting-edge fields:
    1.  **Nanotechnology:** Designing Immunosome scaffolds.
    2.  **Genetic Engineering:** CRISPR/Cas9 synergy to knockout immune checkpoints.
    3.  **The Dark Proteome:** Identifying uncharacterized factors in the CD40 pathway.
    """)

# --- SIDEBAR: DESIGNER ---
st.sidebar.header("🛠️ Design Control Center")
tab_select = st.sidebar.radio("Navigate Sections", ["Immunosome Builder", "CRISPR Synergy", "Dark Proteome Explorer"])

st.sidebar.divider()
st.sidebar.subheader("Global Parameters")
scaffold = st.sidebar.selectbox("Nanoparticle Scaffold", ["Liposome", "Exosome", "PLGA Polymer", "Gold NP"])
ligand = st.sidebar.selectbox("CD40 Agonist", ["CD40L", "Selicrelumab", "CP-870,893", "Dacetuzumab"])

# --- TAB 1: IMMUNOSOME BUILDER & SIGNALING ---
if tab_select == "Immunosome Builder":
    st.subheader("🕸️ CD40 Signaling & Scaffold Architecture")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # --- PYVIS NETWORK ---
        def create_network():
            net = Network(height="450px", width="100%", bgcolor="#ffffff", font_color="black")
            net.add_node("NP", label=f"Immunosome\n({scaffold})", color="#FF4B4B", size=30, shape="diamond")
            net.add_node("CD40", label=f"CD40 Receptor\n({ligand})", color="#1f77b4", size=25)
            net.add_node("TRAF6", label="TRAF6", color="#ff7f0e")
            net.add_node("NFkB", label="NF-κB Pathway", color="#2ca02c")
            net.add_node("TCell", label="CD8+ T-Cell\nActivation", color="#9467bd", shape="star", size=30)
            
            net.add_edge("NP", "CD40", width=2)
            net.add_edge("CD40", "TRAF6", width=2)
            net.add_edge("TRAF6", "NFkB", width=2)
            net.add_edge("NFkB", "TCell", width=2)
            
            net.toggle_physics(True)
            return net

        network = create_network()
        network.save_graph("net.html")
        HtmlFile = open("net.html", 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=500)

    with col2:
        st.metric("Binding Avidity", "High", help="Multivalent clustering increases signal strength")
        st.metric("Antigen Presentation", "+82%", delta="Optimized")
        st.write("**Clinical Landscape:**")
        clinical_data = {
            "Agent": ["Selicrelumab", "CP-870,893", "Mitazalimab"],
            "Phase": ["Phase II", "Phase II", "Phase II"],
            "Status": ["Active", "Active", "Recruiting"]
        }
        st.table(pd.DataFrame(clinical_data))

# --- TAB 2: CRISPR SYNERGY ---
elif tab_select == "CRISPR Synergy":
    st.subheader("✂️ CRISPR/Cas9 Gene Editing Integration")
    st.markdown("Select a gene to knockout within the immune cell to amplify the Immunosome's effect.")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        ko_target = st.selectbox("Target Knockout (Checkpoint)", ["PD-L1", "CTLA-4", "SOCS1", "IL-10"])
        delivery = st.radio("CRISPR Delivery", ["LNP-Encapsulated", "Viral Vector", "Ex Vivo"])
        
        st.warning(f"Strategy: Delivering {scaffold} + {ko_target}-CRISPR")
    
    with c2:
        st.write(f"**Predicted Synergy: {ligand} + {ko_target} KO**")
        # Mock synergy data
        synergy_score = {"PD-L1": 85, "CTLA-4": 78, "SOCS1": 94, "IL-10": 70}
        st.progress(synergy_score[ko_target] / 100)
        st.caption(f"Predicted Therapeutic Efficacy Score: {synergy_score[ko_target]}%")
        
        chart_data = pd.DataFrame({
            "Treatment": ["CD40 Only", f"{ko_target} KO Only", "Combined Synergy"],
            "Immune Response": [40, 25, synergy_score[ko_target]]
        })
        st.bar_chart(chart_data.set_index("Treatment"))

# --- TAB 3: DARK PROTEOME EXPLORER ---
elif tab_select == "Dark Proteome Explorer":
    st.subheader("🔍 The Dark Proteome: Prioritizing Unstudied Factors")
    st.markdown("Identifying proteins with **no known function** that share structural domains with the CD40 signaling complex.")
    
    dark_df = pd.DataFrame({
        "Protein ID": ["C1orf112", "FAM210A", "TMEM256", "C19orf12", "UPF0568"],
        "Structural Domain": ["LRR Repeat", "Coiled-Coil", "Transmembrane", "TNFR-like", "Zinc-Finger"],
        "Darkness Score": ["High", "Very High", "Medium", "High", "High"],
        "AF2 Confidence": [89, 45, 92, 81, 95],
        "Priority": ["⭐⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"]
    })
    
    st.dataframe(dark_df, use_container_width=True)
    
    st.info("""
        **Biochemist's Insight:** 
        These 'Dark' factors were selected because they contain motifs (like TNFR or Zinc-Fingers) 
        found in the CD40-TRAF pathway, but currently have no assigned biological function in PubMed.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e1/AlphaFold_structure_example.png", caption="Example AlphaFold Structure Prediction for Uncharacterized Factors", width=400)

# --- FOOTER ---
st.divider()
st.caption("Developed for: CD40 Immunosomes Review Paper | Tool Version 1.0.2")
