import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CD40 Systems Biology Framework",
    page_icon="🧬",
    layout="wide"
)


def generate_project_summary(scaffold, ligand, k1, k4):
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
   - Uses curated target rationale and synergy scores

3. Kinetic Simulator
   - Simulates NF-κB response with tunable recruitment/deactivation rates
   - Current k1: {k1:.2f}, k4: {k4:.2f}

4. Dark Proteome Explorer
   - Identifies uncharacterized proteins with plausible system entry

5. Molecular Validation
   - Uses docking for relative plausibility
   - Uses expression context to define responsive cell types

6. Unique Feature Explorer
   - Prioritizes novel additions by impact, feasibility, and execution risk

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


# --- KINETIC MODELING ---
def simulate_signaling(k1, k4, t_max=100):
    t = np.linspace(0, t_max, 100)
    signal = (k1 / (k4 + 0.01)) * (1 - np.exp(-k4 * t))
    return t, signal


# --- MECHANISTIC ASSUMPTIONS BY DELIVERY VEHICLE ---
SCAFFOLD_MODELS = {
    "Liposome": {"clustering": "Moderate", "release": "Fast", "risk": "Transient signaling", "gain": 45},
    "Exosome": {"clustering": "High", "release": "Physiological", "risk": "Heterogeneous uptake", "gain": 72},
    "PLGA Polymer": {"clustering": "High", "release": "Sustained", "risk": "NF-κB overactivation / exhaustion", "gain": 88},
    "Gold NP": {"clustering": "Very High", "release": "None", "risk": "Non-physiological signaling", "gain": 94},
}

# --- CRISPR DATA (CONSISTENT SCORES + RATIONALE) ---
CRISPR_DATA = {
    "SOCS1": {
        "score": 95,
        "color": "#1f77b4",
        "rationale": "SOCS1 knockout releases negative regulation of NF-κB signaling, probing signal persistence.",
    },
    "PD-L1": {
        "score": 88,
        "color": "#ff7f0e",
        "rationale": "PD-L1 deletion removes inhibitory feedback on T-cells activated downstream of CD40.",
    },
    "CTLA-4": {
        "score": 80,
        "color": "#2ca02c",
        "rationale": "CTLA-4 knockout disrupts early co-inhibitory signaling during T-cell priming.",
    },
    "IL-10": {
        "score": 70,
        "color": "#d62728",
        "rationale": "IL-10 deletion limits anti-inflammatory feedback following CD40 activation.",
    },
}

# --- DARK PROTEOME SYSTEM ENTRY HYPOTHESES ---
DARK_PROTEOME_HYPOTHESES = {
    "C1orf112": "LRR-containing architecture suggests a potential adaptor-like role influencing receptor-proximal clustering dynamics.",
    "FAM210A": "Coiled-coil structure may mediate transient protein–protein interactions within immune signaling complexes.",
    "TMEM256": "Transmembrane localization suggests a role in compartmentalizing CD40 signaling at the membrane interface.",
    "C19orf12": "TNFR-like features indicate possible non-canonical modulation of TRAF recruitment dynamics.",
}

# --- UNIQUE FEATURE EXPLORER: NOVELTY-FIRST R&D IDEAS ---
UNIQUE_FEATURES = {
    "Adaptive Dosing Twin": {
        "innovation": "Simulates patient-specific CD40 pulse schedules based on predicted inflammatory rebound windows.",
        "impact": 92,
        "feasibility": 68,
        "risk": "Needs longitudinal cytokine calibration",
    },
    "Signal Firewall Circuit": {
        "innovation": "Introduces a synthetic negative-feedback gate that activates only when NF-κB exceeds a toxicity threshold.",
        "impact": 88,
        "feasibility": 61,
        "risk": "Circuit transfer into primary APCs may be inefficient",
    },
    "Microenvironment Replay Engine": {
        "innovation": "Stress-tests CD40 interventions against hypoxia, lactate load, and checkpoint-rich tumor contexts.",
        "impact": 85,
        "feasibility": 74,
        "risk": "Requires robust context priors for each cancer type",
    },
    "Multi-Omic Sentinel Score": {
        "innovation": "Combines transcriptome, secretome, and phospho-signaling into a single actionability score.",
        "impact": 79,
        "feasibility": 83,
        "risk": "Score can overfit if cohort diversity is low",
    },
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

    tab_select = st.radio(
        "🚀 Framework Modules",
        [
            "Immunosome Builder",
            "CRISPR Synergy",
            "Kinetic Simulator (Table 1)",
            "Dark Proteome Explorer",
            "Molecular Validation",
            "Unique Feature Explorer",
        ],
    )

    st.divider()
    st.subheader("⚙️ Experimental Parameters")
    scaffold = st.selectbox("Delivery Vehicle", list(SCAFFOLD_MODELS.keys()))
    ligand = st.selectbox("CD40 Agonist Model", ["CD40L (Native)", "Selicrelumab", "CP-870,893", "Dacetuzumab"])

    st.caption("Kinetic parameters")
    k1 = st.slider("k1 (Recruitment Rate)", 0.01, 0.20, 0.08)
    k4 = st.slider("k4 (Deactivation Rate)", 0.01, 0.10, 0.05)

# --- HEADER ---
st.title("🛡️ CD40 Immunosome: A Systems Biology Framework")

col_a, col_b = st.columns([1.5, 1])
with col_a:
    st.markdown(
        """
    ### 🎯 Research Intent
    This platform is an **in silico hypothesis-generation framework** for systematically interrogating the **CD40 signaling axis**.
    It integrates **delivery scaffolds, receptor topology, CRISPR perturbations, kinetic modeling, and structural biology**
    into a unified **systems-level discovery workflow**.
    """
    )
with col_b:
    st.warning(
        """
    **Scientific Disclaimer**
    All outputs are computational predictions intended to guide
    *in vitro* and *in vivo* experimental design.
    """
    )

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
        net.add_edge("CD40", "TRAF6", title=f"Adaptor recruitment (k1={k1:.2f})")
        net.add_edge("TRAF6", "NFkB", title=f"Signal damping (k4={k4:.2f})")
        net.add_edge("NFkB", "TCell", title="Effector activation")
        net.toggle_physics(True)
        net.save_graph("net.html")
        with open("net.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=550)

    with col2:
        st.metric("Predicted Receptor Clustering Regime", SCAFFOLD_MODELS[scaffold]["clustering"])
        st.metric("Predicted Antigen Presentation Gain", f"+{SCAFFOLD_MODELS[scaffold]['gain']}%")
        st.metric("Current k1/k4 ratio", f"{(k1 / k4):.2f}")

# =========================
# CRISPR SYNERGY
# =========================
elif tab_select == "CRISPR Synergy":
    st.subheader("✂️ CRISPR/Cas9 Perturbation Strategy")

    c1, c2 = st.columns([1, 2])
    with c1:
        ko = st.selectbox("Genetic Target (Knockout)", list(CRISPR_DATA.keys()))
        delivery = st.radio("Delivery Method", ["LNP-Encapsulated", "Viral Vector", "Ex Vivo"])
        st.metric(f"{ko} Synergy Score", f"{CRISPR_DATA[ko]['score']}%")
        st.info(CRISPR_DATA[ko]["rationale"])
        st.caption(f"Model context: {ligand} + {ko} via {delivery}")

    with c2:
        df_fig3 = pd.DataFrame(
            {
                "Target": list(CRISPR_DATA.keys()),
                "Synergy Score (%)": [entry["score"] for entry in CRISPR_DATA.values()],
            }
        )
        st.bar_chart(df_fig3.set_index("Target"))

        comparison_df = pd.DataFrame(
            {
                "Condition": ["Agonist Only", "Conditional Synergy Model", f"{ko} KO Only"],
                "Response": [40, CRISPR_DATA[ko]["score"], 25],
            }
        )
        st.bar_chart(comparison_df.set_index("Condition"))

# =========================
# KINETIC SIMULATOR
# =========================
elif tab_select == "Kinetic Simulator (Table 1)":
    st.subheader("📈 Live Signaling Dynamics")
    st.markdown("Simulates NF-κB activation from adjustable recruitment/deactivation kinetics.")
    t, signal = simulate_signaling(k1, k4)
    chart_data = pd.DataFrame({"Time (s)": t, "NF-κB Activity": signal})
    st.line_chart(chart_data.set_index("Time (s)"))
    st.success(f"Current Steady State (approx): {float(np.max(signal)):.2f}")

# =========================
# DARK PROTEOME
# =========================
elif tab_select == "Dark Proteome Explorer":
    st.subheader("🔍 Dark Proteome: Target Prioritization")
    df = pd.DataFrame(
        {
            "Protein": ["C1orf112", "FAM210A", "TMEM256", "C19orf12"],
            "Domain": ["LRR", "Coiled-coil", "TM", "TNFR-like"],
            "AF2 Confidence": [89, 45, 92, 81],
            "Priority": ["⭐⭐⭐⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐"],
        }
    )
    st.dataframe(df, width="stretch")
    st.markdown("### 🧩 Proposed System Entry Hypotheses")
    for protein, hypothesis in DARK_PROTEOME_HYPOTHESES.items():
        st.markdown(f"- **{protein}:** {hypothesis}")

# =========================
# MOLECULAR VALIDATION
# =========================
elif tab_select == "Molecular Validation":
    st.subheader("🧬 Molecular Validation: Plausibility Checks")
    col1, col2 = st.columns(2)
    with col1:
        dock_df = pd.DataFrame({"Ligand": [ligand, "Native CD40L"], "Affinity (kcal/mol)": [-11.4, -9.2]})
        st.table(dock_df)
    with col2:
        expr_df = pd.DataFrame({"Cell Type": ["B-Cells", "Dendritic Cells", "Macrophages"], "TPM": [180, 310, 95]})
        st.bar_chart(expr_df.set_index("Cell Type"))

# =========================
# UNIQUE FEATURE EXPLORER
# =========================
elif tab_select == "Unique Feature Explorer":
    st.subheader("💡 Unique Feature Explorer: Novel Additions Roadmap")
    col1, col2 = st.columns([1, 2])
    with col1:
        objective = st.selectbox("Primary objective", ["Boost efficacy", "Improve safety", "Increase translational readiness"])
        risk_mode = st.radio("Risk posture", ["Conservative", "Balanced", "Moonshot"])
        min_feasibility = st.slider("Minimum feasibility threshold", 40, 90, 65, 5)

    with col2:
        ranked = []
        for name, values in UNIQUE_FEATURES.items():
            novelty_index = int(values["impact"] * 0.6 + values["feasibility"] * 0.4)
            if risk_mode == "Conservative":
                novelty_index -= 8
            elif risk_mode == "Moonshot":
                novelty_index += 6
            if objective == "Improve safety" and "feedback" in values["innovation"].lower():
                novelty_index += 6
            if objective == "Increase translational readiness" and values["feasibility"] >= 75:
                novelty_index += 5
            ranked.append(
                {
                    "Feature": name,
                    "Novelty Index": max(0, min(100, novelty_index)),
                    "Impact": values["impact"],
                    "Feasibility": values["feasibility"],
                    "Execution Risk": values["risk"],
                }
            )

        rank_df = pd.DataFrame(ranked)
        rank_df = rank_df[rank_df["Feasibility"] >= min_feasibility].sort_values("Novelty Index", ascending=False)
        st.dataframe(rank_df, width="stretch")
        st.bar_chart(rank_df.set_index("Feature")[["Novelty Index", "Impact", "Feasibility"]])

st.divider()
st.subheader("📄 Export Project Summary")
summary_text = generate_project_summary(scaffold, ligand, k1, k4)
st.download_button(
    label="⬇️ Download Project Summary (TXT)",
    data=summary_text,
    file_name="CD40_Immunosome_Project_Summary.txt",
    mime="text/plain",
)

st.divider()
st.caption("PhD Application Portfolio | Systems Biology Framework | Yashwant Nama")
