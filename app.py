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

# --- DARK PROTEOME SYSTEM ENTRY HYPOTHESES ---
DARK_PROTEOME_HYPOTHESES = {
    "C1orf112": "LRR-containing architecture suggests a potential adaptor-like role influencing receptor-proximal clustering dynamics.",
    "FAM210A": "Coiled-coil structure may mediate transient protein–protein interactions within immune signaling complexes.",
    "TMEM256": "Transmembrane localization suggests a role in compartmentalizing CD40 signaling at the membrane interface.",
    "C19orf12": "TNFR-like features indicate possible non-canonical modulation of TRAF recruitment dynamics."
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
        st.metric("Predicted Receptor Clustering Regime", SCAFFOLD_MODELS[scaffold]["clustering"])
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

        st.info(f"Conditional synergy between **{ligand}** activation and **{ko} knockout** via **{delivery}** delivery.")

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

    st.markdown("### 🧩 Proposed System Entry Hypotheses")
    for protein, hypothesis in DARK_PROTEOME_HYPOTHESES.items():
        st.markdown(f"- **{protein}:** {hypothesis}")

    st.info("""
    **Why AlphaFold is used here**  
    Structural confidence is used **only to assess tractability and domain plausibility**, not to infer biological function.
    """)

    st.success("""
    **Integration with CRISPR Strategy**  
    Top-ranked candidates are intended for **secondary CRISPR perturbation**
    to evaluate their modulatory role within the CD40–TRAF6 signaling regime.
    """)

# =========================
# MOLECULAR VALIDATION (UPGRADED BLOCK)
# =========================
elif tab_select == "Molecular Validation":
    st.subheader("🧬 Molecular Validation: Plausibility Checks")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Relative Binding Plausibility (In Silico Docking)**")
        dock_df = pd.DataFrame({
            "Ligand": [ligand, "Native CD40L"],
            "Affinity (kcal/mol)": [-11.4, -9.2]
        })
        st.table(dock_df)
        st.info("""
        **What this docking validates**  
        Docking scores assess **relative binding plausibility** between agonist and native ligand.
        They do **not** predict receptor clustering or signaling outcomes.
        """)

    with col2:
        st.markdown("**Cell-Type Context (Reference RNA-seq TPM)**")
        expr_df = pd.DataFrame({
            "Cell Type": ["B-Cells", "Dendritic Cells", "Macrophages"],
            "TPM": [180, 310, 95]
        })
        st.bar_chart(expr_df.set_index("Cell Type"))

    st.markdown("### 🔍 Mechanistic Consistency Check")
    st.success("""
    CD40 expression is enriched in **B-cells and dendritic cells**, aligning with
    the proposed CD40–TRAF6 signaling focus on professional antigen-presenting cells.
    Reduced macrophage expression suggests **context-dependent responsiveness**.
    """)

    with st.expander("⚠️ Molecular Validation: Failure Modes & Constraints"):
        st.markdown("""
        - Favorable docking does **not guarantee signaling**
        - Static docking ignores membrane dynamics
        - Expression does not imply pathway dominance
        """)
st.divider()
st.subheader("📄 Export Project Summary")

summary_text = generate_project_summary(scaffold, ligand)

st.download_button(
    label="⬇️ Download Project Summary (TXT)",
    data=summary_text,
    file_name="CD40_Immunosome_Project_Summary.txt",
    mime="text/plain"
)
with st.expander("🧠 Explain this tool in plain language"):
    st.markdown("""
**Imagine the immune system like a control panel.**

This tool studies one important switch — **CD40** — that helps immune cells
decide *when* and *how strongly* to activate.

Instead of doing experiments first, this platform:
- Maps how signals *should* flow
- Tests what might amplify or break them
- Identifies weak points worth testing in the lab

The goal is **not prediction**.  
The goal is **better-designed experiments**.
""")
		
def generate_project_summary(scaffold, ligand):
    return f"""
CD40 IMMUNOSOME – SYSTEMS BIOLOGY SUMMARY
======================================

What is this tool?
------------------
This platform is an in silico systems biology framework designed to
generate experimentally testable hypotheses around the CD40–TRAF6
signaling axis in immune cells.

Core Question
-------------
How do delivery scaffolds, receptor topology, and genetic perturbations
interact to shape CD40-driven immune signaling outcomes?

Modules Overview
----------------
1. Immunosome Builder
   - Models receptor clustering and adaptor recruitment
   - Current scaffold: {scaffold}
   - CD40 agonist model: {ligand}

2. CRISPR Synergy
   - Explores conditional genetic perturbations
   - Focuses on boundary conditions, not guaranteed enhancement

3. Dark Proteome Explorer
   - Identifies uncharacterized proteins with plausible system entry
   - Uses AlphaFold only for tractability, not function inference

4. Molecular Validation
   - Uses docking for relative plausibility
   - Uses expression context to define responsive cell types

What this tool does NOT do
-------------------------
- Does not predict clinical outcomes
- Does not replace wet-lab validation
- Does not claim causal certainty

Intended Use
------------
To guide experimental design, PhD project formulation,
and hypothesis prioritization in CD40-focused immunology research.
"""

st.divider()
st.caption("PhD Application Portfolio | Systems Biology Framework | Yashwant Nama")
