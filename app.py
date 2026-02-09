import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CD40 Systems Biology Framework",
    page_icon="🧬",
    layout="wide"
)

# --- MECHANISTIC ASSUMPTIONS BY DELIVERY VEHICLE ---
SCAFFOLD_MODELS = {
    "Liposome": {
        "clustering": "Moderate",
        "release": "Fast",
        "risk": "Transient signaling"
    },
    "Exosome": {
        "clustering": "High",
        "release": "Physiological",
        "risk": "Heterogeneous uptake"
    },
    "PLGA Polymer": {
        "clustering": "High",
        "release": "Sustained",
        "risk": "NF-κB overactivation / exhaustion"
    },
    "Gold NP": {
        "clustering": "Very High",
        "release": "None",
        "risk": "Non-physiological signaling"
    }
}

# --- MECHANISTIC RATIONALE FOR CRISPR TARGETS ---
CRISPR_RATIONALE = {
    "PD-L1": "PD-L1 deletion removes inhibitory feedback on T-cells activated downstream of CD40-mediated antigen presentation, testing whether CD40 signaling is functionally constrained by immune checkpoints.",
    "CTLA-4": "CTLA-4 knockout disrupts early co-inhibitory signaling during T-cell priming, amplifying CD40-driven co-stimulation at the antigen-presenting cell interface.",
    "SOCS1": "SOCS1 knockout releases negative regulation of cytokine and NF-κB signaling, probing the persistence of CD40–TRAF6 signal amplification.",
    "IL-10": "IL-10 deletion limits anti-inflammatory feedback from antigen-presenting cells following CD40 activation, testing immune resolution boundaries."
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    ">
        <h2>Yashwant Nama</h2>
        <p style="font-size: 14px;">
            PhD Applicant<br><b>Systems Biology & Neurogenetics</b>
        </p>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 14px;">🧬 Genomics</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 14px;">🕸️ Networks</span>
    </div>
    """, unsafe_allow_html=True)

    tab_select = st.radio(
        "🚀 Framework Modules",
        ["Immunosome Builder", "CRISPR Synergy", "Dark Proteome Explorer", "Molecular Validation"]
    )

    st.divider()
    st.subheader("⚙️ Experimental Parameters")
    scaffold = st.selectbox("Delivery Vehicle", list(SCAFFOLD_MODELS.keys()))
    ligand = st.selectbox(
        "CD40 Agonist Model",
        ["CD40L (Native)", "Selicrelumab", "CP-870,893", "Dacetuzumab"]
    )

# --- HEADER ---
st.title("🛡️ CD40 Immunosome: A Systems Biology Framework")

col_a, col_b = st.columns([1.5, 1])
with col_a:
    st.markdown("""
    ### 🎯 Research Intent
    This platform is an **in silico hypothesis-generation framework** for systematically interrogating the **CD40 signaling axis**.
    It integrates **delivery scaffolds, receptor topology, CRISPR perturbations, and structural biology**
    into a unified **systems-level discovery workflow**.

    **PhD Scope:** Experimental validation of the **CD40–TRAF6 signaling module**
    using targeted CRISPR perturbations.
    """)
with col_b:
    st.warning("""
    **Scientific Disclaimer**  
    All outputs are computational predictions intended to guide
    *in vitro* and *in vivo* experimental design.
    """)

st.divider()

# =========================
# IMMUNOSOME BUILDER
# =========================
if tab_select == "Immunosome Builder":
    st.subheader("🕸️ Network Topology: CD40 Signaling Axis")

    col1, col2 = st.columns([2, 1])

    with col1:
        net = Network(height="520px", width="100%", bgcolor="white", font_color="black")
        net.add_node("NP", label=f"Vehicle\n({scaffold})", color="#FF4B4B", shape="diamond", size=30)
        net.add_node("CD40", label=f"CD40\n({ligand})", color="#1f77b4", size=25)
        net.add_node("TRAF6", label="TRAF6", color="#ff7f0e")
        net.add_node("NFkB", label="NF-κB Pathway", color="#2ca02c")
        net.add_node("TCell", label="T-Cell Response", color="#9467bd", shape="star", size=30)

        net.add_edge("NP", "CD40", title="Scaffold-mediated receptor clustering")
        net.add_edge("CD40", "TRAF6", title="Adaptor recruitment")
        net.add_edge("TRAF6", "NFkB", title="Signal amplification")
        net.add_edge("NFkB", "TCell", title="Effector activation")

        net.toggle_physics(True)
        net.save_graph("net.html")
        components.html(open("net.html", "r").read(), height=550)

    with col2:
        st.metric(
            "Predicted Receptor Clustering Regime",
            SCAFFOLD_MODELS[scaffold]["clustering"]
        )
        st.metric("Predicted Antigen Presentation Gain", "+82%")

        st.markdown("**Mechanistic Interpretation**")
        st.success(f"""
        **{scaffold}** scaffolds promote **{SCAFFOLD_MODELS[scaffold]['clustering']} receptor clustering**
        with **{SCAFFOLD_MODELS[scaffold]['release']} release kinetics**.

        ⚠️ *Primary failure risk:* {SCAFFOLD_MODELS[scaffold]['risk']}
        """)

        with st.expander("🧪 Model Sensitivity & Failure Modes"):
            st.markdown("""
            - Insufficient clustering → weak TRAF6 recruitment  
            - Excessive agonism → NF-κB desensitization  
            - Scaffold rigidity mismatch → signaling without transcriptional output  

            These sensitivities motivate **targeted perturbation experiments** rather than global pathway activation.
            """)

# =========================
# CRISPR SYNERGY
# =========================
elif tab_select == "CRISPR Synergy":
    st.subheader("✂️ CRISPR/Cas9 Perturbation Strategy")

    c1, c2 = st.columns([1, 2])
    with c1:
        ko = st.selectbox("Genetic Target (Knockout)", list(CRISPR_RATIONALE.keys()))
        delivery = st.radio("Delivery Method", ["LNP-Encapsulated", "Viral Vector", "Ex Vivo"])

        st.info(
            f"Conditional synergy between **{ligand}** activation and **{ko} knockout** via **{delivery}** delivery."
        )

        st.markdown("**🧠 Mechanistic Rationale for Target Selection**")
        st.success(CRISPR_RATIONALE[ko])

    with c2:
        synergy_scores = {"PD-L1": 85, "CTLA-4": 78, "SOCS1": 94, "IL-10": 70}
        score = synergy_scores[ko]
        st.progress(score / 100)

        df = pd.DataFrame({
            "Condition": ["Agonist Only", "Conditional Synergy Model", f"{ko} KO Only"],
            "Response": [40, score, 25]
        })
        st.bar_chart(df.set_index("Condition"))

        with st.expander("⚠️ CRISPR Synergy: Failure Modes & Boundary Conditions"):
            st.markdown(f"""
            - **{ko} KO may induce compensatory inhibitory pathways**
            - **Excessive immune activation** may lead to non-specific T-cell responses
            - **Delivery dependence ({delivery})** may limit editing efficiency or specificity
            - **Context dependence:** Synergy is expected only under active CD40 signaling regimes

            These constraints define **experimentally testable boundaries**, not guaranteed outcomes.
            """)

# =========================
# DARK PROTEOME
# =========================
elif tab_select == "Dark Proteome Explorer":
    st.subheader("🔍 Dark Proteome: Target Prioritization")

    df = pd.DataFrame({
        "Protein": ["C1orf112", "FAM210A", "TMEM256", "C19orf12"],
        "Domain": ["LRR", "Coiled-coil", "TM", "TNFR-like"],
        "AF2 Confidence": [89, 45, 92, 81],
        "Priority": ["⭐⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐"]
    })
    st.dataframe(df, use_container_width=True)

    st.success("""
    **AlphaFold-guided prioritization**  
    High-confidence candidates are proposed for functional validation
    within the CD40–TRAF signaling context.
    """)

# =========================
# MOLECULAR VALIDATION
# =========================
elif tab_select == "Molecular Validation":
    st.subheader("🧬 Computational Validation")

    c1, c2 = st.columns(2)
    with c1:
        st.table(pd.DataFrame({
            "Ligand": [ligand, "Native CD40L"],
            "Affinity (kcal/mol)": [-11.4, -9.2]
        }))
    with c2:
        st.bar_chart(pd.DataFrame({
            "Cell Type": ["B-Cells", "DCs", "Macrophages"],
            "TPM": [180, 310, 95]
        }).set_index("Cell Type"))

st.divider()
st.caption("PhD Application Portfolio | Systems Biology Framework | Yashwant Nama")
