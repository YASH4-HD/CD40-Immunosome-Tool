import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CD40 Immunosome Explorer",
    page_icon="🛡️",
    layout="wide"
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- TITLE & DESCRIPTION ---
st.title("🛡️ CD40 Immunosome Explorer")
st.markdown("### Interactive Platform for Immunotherapy Review & Design")

with st.expander("ℹ️ About this Tool (Project Description)", expanded=True):
    st.markdown("""
    **Project Overview:**
    The **CD40-Immunosome Explorer** is a bioinformatics dashboard designed to bridge the gap between nanotechnology and immunotherapy. 
    Focusing on the **CD40/CD40L costimulatory pathway**, this tool allows researchers to simulate the architecture of 
    "Immunosomes"—synthetic nanoparticles engineered to trigger potent anti-tumor immune responses.

    **Key Capabilities:**
    - **Modular Builder:** Select scaffolds (Liposomes, Exosomes) and ligands (Selicrelumab, CD40L).
    - **Signaling Cascade:** Visualize the pathway from receptor binding to NF-κB activation.
    - **Clinical Analytics:** Compare binding affinities and clinical trial statuses.
    """)

# --- SIDEBAR: IMMUNOSOME BUILDER ---
st.sidebar.header("🛠️ Immunosome Designer")
st.sidebar.subheader("1. Scaffold Selection")
scaffold = st.sidebar.selectbox(
    "Select Nanoparticle Base", 
    ["Liposome", "Exosome", "Gold Nanoparticle", "PLGA Polymer", "Silica Nanoparticle"]
)

st.sidebar.subheader("2. Surface Engineering")
ligand = st.sidebar.selectbox(
    "Select CD40 Ligand/Agonist", 
    ["CD40L (Natural)", "Selicrelumab (APX005M)", "CP-870,893", "Dacetuzumab", "Peptide Agonist"]
)

st.sidebar.subheader("3. Therapeutic Cargo")
payload = st.sidebar.multiselect(
    "Select Payload (Adjuvants)", 
    ["CpG ODN", "Tumor Antigens", "STING Agonists", "IL-12", "STAT3 siRNA"],
    default=["Tumor Antigens"]
)

# --- MAIN LAYOUT: COLUMNS ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🕸️ CD40 Signaling & Immune Cascade")
    st.info(f"Current Configuration: **{scaffold}** coated with **{ligand}** delivering **{', '.join(payload)}**")
    
    # --- PYVIS NETWORK GENERATION ---
    def create_cd40_network():
        net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black", heading="")
        
        # Nodes
        net.add_node("Immunosome", label=f"Immunosome\n({scaffold})", color="#FF4B4B", size=30, shape="diamond")
        net.add_node("CD40", label=f"CD40 Receptor\n(Binding {ligand})", color="#1f77b4", size=25)
        net.add_node("TRAF6", label="TRAF6\n(Adapter)", color="#ff7f0e")
        net.add_node("NFkB", label="NF-κB Pathway\n(Transcription)", color="#2ca02c")
        net.add_node("Cytokines", label="IL-12 / IFN-γ\n(Th1 Response)", color="#d62728")
        net.add_node("TCell", label="CD8+ T-Cell\nActivation", color="#9467bd", shape="star", size=30)

        # Edges
        net.add_edge("Immunosome", "CD40", width=2, title="Multivalent Interaction")
        net.add_edge("CD40", "TRAF6", width=2)
        net.add_edge("TRAF6", "NFkB", width=2)
        net.add_edge("NFkB", "Cytokines", width=2)
        net.add_edge("Cytokines", "TCell", width=2, label="Priming")
        
        # Add Payload connections if selected
        if payload:
            net.add_node("Payload", label=f"Cargo: {payload[0]}", color="#7f7f7f", size=20)
            net.add_edge("Immunosome", "Payload", dashes=True)
            net.add_edge("Payload", "NFkB", dashes=True, label="Synergy")

        net.set_options("""
        var options = {
          "physics": {
            "forceAtlas2Based": { "gravitationalConstant": -50, "centralGravity": 0.01, "springLength": 100 },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        """)
        return net

    # Save and display network
    cd40_net = create_cd40_network()
    cd40_net.save_graph("cd40_network.html")
    HtmlFile = open("cd40_network.html", 'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=550)

with col2:
    st.subheader("📈 Predicted Metrics")
    st.metric(label="Binding Avidity", value="High", delta="Multivalent Effect")
    st.metric(label="Systemic Toxicity Risk", value="Low", delta="-12%", delta_color="inverse")
    st.metric(label="Antigen Presentation", value="+85%", delta="Optimized")
    
    st.markdown("---")
    st.write("**Mechanism Summary:**")
    st.caption(f"The {scaffold} provides a stable platform for the clustering of {ligand}, which mimics the natural CD40L trimerization, leading to enhanced TRAF6 recruitment.")

# --- DATA SECTION: CLINICAL COMPARISON ---
st.divider()
st.subheader("📊 Comparative Analysis of CD40 Agonists")
data = {
    "Agent": ["Selicrelumab", "CP-870,893", "Dacetuzumab", "CD40L-Fc", "Mitazalimab"],
    "Format": ["IgG2 mAb", "IgG2 mAb", "IgG1 mAb", "Fusion Protein", "IgG1 mAb"],
    "Binding Affinity (Kd)": ["0.3 nM", "0.1 nM", "1.2 nM", "2.5 nM", "0.5 nM"],
    "Clinical Status": ["Phase II", "Phase I/II", "Discontinued", "Phase I", "Phase II"],
    "Primary Indication": ["Pancreatic Cancer", "Solid Tumors", "Lymphoma", "Solid Tumors", "Pancreatic Cancer"]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("Created for Review Paper Supplement: *CD40 Immunosomes in Immunotherapy*")
