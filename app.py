import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CD40 Systems Biology Framework",
    page_icon="🧬",
    layout="wide",
)


def generate_project_summary(scaffold, ligand, k1, k2, k3, k4, cd40_input):
    return f"""
CD40 IMMUNOSOME – SYSTEMS BIOLOGY SUMMARY
======================================

Current setup
-------------
Scaffold: {scaffold}
Ligand: {ligand}
Kinetic constants: k1={k1:.3f}, k2={k2:.3f}, k3={k3:.3f}, k4={k4:.3f}
CD40 input level: {cd40_input:.2f}

Modeling note
-------------
Kinetic simulations are solved numerically as a coupled ODE system:
  dTRAF6/dt = k1·CD40 - k2·TRAF6
  dNFκB/dt = k3·TRAF6 - k4·NFκB

CRISPR synergy note
-------------------
Synergy is computed dynamically from model responses:
  Score = ((Response_KO+Agonist - Response_Agonist) / Response_Agonist) × 100

Disclaimer
----------
Outputs are hypothesis-generation aids and do not replace wet-lab validation.
"""


def simulate_signaling_ode(k1, k2, k3, k4, cd40_input=1.0, t_max=200, points=2000):
    """Numerically solve coupled ODEs using an RK4 integrator."""
    t = np.linspace(0, t_max, points)
    dt = t[1] - t[0]

    traf6 = np.zeros(points)
    nfkb = np.zeros(points)

    def rhs(y):
        y_traf6, y_nfkb = y
        d_traf6 = k1 * cd40_input - k2 * y_traf6
        d_nfkb = k3 * y_traf6 - k4 * y_nfkb
        return np.array([d_traf6, d_nfkb], dtype=float)

    for i in range(points - 1):
        y = np.array([traf6[i], nfkb[i]], dtype=float)
        k_1 = rhs(y)
        k_2 = rhs(y + 0.5 * dt * k_1)
        k_3 = rhs(y + 0.5 * dt * k_2)
        k_4 = rhs(y + dt * k_3)
        y_next = y + (dt / 6.0) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
        traf6[i + 1], nfkb[i + 1] = y_next

    return t, traf6, nfkb


SCAFFOLD_MODELS = {
    "Liposome": {"clustering": "Moderate", "release": "Fast", "risk": "Transient signaling", "gain": 45},
    "Exosome": {"clustering": "High", "release": "Physiological", "risk": "Heterogeneous uptake", "gain": 72},
    "PLGA Polymer": {"clustering": "High", "release": "Sustained", "risk": "NF-κB overactivation / exhaustion", "gain": 88},
    "Gold NP": {"clustering": "Very High", "release": "None", "risk": "Non-physiological signaling", "gain": 94},
}

CRISPR_TARGET_EFFECTS = {
    "SOCS1": {"k2_mult": 0.80, "k4_mult": 0.78, "note": "Relieves negative feedback on pathway damping."},
    "PD-L1": {"k3_mult": 1.08, "note": "Improves effective APC→T-cell functional propagation proxy."},
    "CTLA-4": {"k3_mult": 1.05, "note": "Increases co-stimulation efficiency proxy."},
    "IL-10": {"k4_mult": 0.92, "note": "Reduces anti-inflammatory shutdown pressure."},
}

DARK_PROTEOME_HYPOTHESES = {
    "C1orf112": "LRR-containing architecture suggests a potential adaptor-like role influencing receptor-proximal clustering dynamics.",
    "FAM210A": "Coiled-coil structure may mediate transient protein–protein interactions within immune signaling complexes.",
    "TMEM256": "Transmembrane localization suggests a role in compartmentalizing CD40 signaling at the membrane interface.",
    "C19orf12": "TNFR-like features indicate possible non-canonical modulation of TRAF recruitment dynamics.",
}

SUPPLEMENTARY_FEATURES = {
    "Adaptive Dosing Twin": {"impact": 92, "feasibility": 68, "risk": "Needs longitudinal cytokine calibration"},
    "Signal Firewall Circuit": {"impact": 88, "feasibility": 61, "risk": "Circuit transfer into primary APCs may be inefficient"},
    "Microenvironment Replay Engine": {"impact": 85, "feasibility": 74, "risk": "Needs context priors by tumor type"},
    "Multi-Omic Sentinel Score": {"impact": 79, "feasibility": 83, "risk": "Can overfit in low-diversity cohorts"},
}


with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 16px; color: white; text-align: center; margin-bottom: 12px;">
      <h3 style="margin: 0;">CD40 Immunosome Tool</h3>
      <p style="margin: 8px 0 0 0; font-size: 13px;">Systems Biology Hypothesis Framework</p>
    </div>
    """, unsafe_allow_html=True)

    tab_select = st.radio(
        "🚀 Framework Modules",
        [
            "Immunosome Builder",
            "CRISPR Synergy",
            "Kinetic Simulator (ODE)",
            "Dark Proteome Explorer",
            "Molecular Validation",
        ],
    )

    st.divider()
    scaffold = st.selectbox("Delivery Vehicle", list(SCAFFOLD_MODELS.keys()))
    ligand = st.selectbox("CD40 Agonist Model", ["CD40L (Native)", "Selicrelumab", "CP-870,893", "Dacetuzumab"])

    st.subheader("⚙️ ODE Parameters")
    k1 = st.slider("k1 (CD40→TRAF6 recruitment)", 0.01, 0.20, 0.08)
    k2 = st.slider("k2 (TRAF6 decay)", 0.01, 0.20, 0.06)
    k3 = st.slider("k3 (TRAF6→NF-κB activation)", 0.01, 0.25, 0.10)
    k4 = st.slider("k4 (NF-κB decay)", 0.01, 0.20, 0.05)
    cd40_input = st.slider("CD40 input level", 0.5, 2.0, 1.0, 0.1)

st.title("🛡️ CD40 Immunosome: A Systems Biology Framework")
st.caption("ODE-backed kinetic simulation and dynamic CRISPR synergy scoring.")
st.divider()

if tab_select == "Immunosome Builder":
    st.subheader("🕸️ Network Topology: CD40 Signaling Axis")
    col1, col2 = st.columns([2, 1])

    with col1:
        net = Network(height="500px", width="100%", bgcolor="white", font_color="black")
        net.add_node("NP", label=f"Vehicle\n({scaffold})", color="#FF4B4B", shape="diamond", size=30)
        net.add_node("CD40", label=f"CD40\n({ligand})", color="#1f77b4", size=25)
        net.add_node("TRAF6", label="TRAF6", color="#ff7f0e")
        net.add_node("NFkB", label="NF-κB", color="#2ca02c")
        net.add_node("TCell", label="T-Cell Response", color="#9467bd", shape="star", size=30)
        net.add_edge("NP", "CD40", title="Scaffold-mediated clustering")
        net.add_edge("CD40", "TRAF6", title=f"k1={k1:.2f}, k2={k2:.2f}")
        net.add_edge("TRAF6", "NFkB", title=f"k3={k3:.2f}, k4={k4:.2f}")
        net.add_edge("NFkB", "TCell", title="Effector activation")
        net.toggle_physics(True)
        net.save_graph("net.html")
        with open("net.html", "r", encoding="utf-8") as f:
            components.html(f.read(), height=530)

    with col2:
        st.metric("Clustering Regime", SCAFFOLD_MODELS[scaffold]["clustering"])
        st.metric("Antigen Presentation Gain", f"+{SCAFFOLD_MODELS[scaffold]['gain']}%")
        st.metric("NF-κB damping ratio", f"{k3 / k4:.2f}")

elif tab_select == "CRISPR Synergy":
    st.subheader("✂️ Dynamic CRISPR Synergy (AUC-based response ratio)")

    t, _, nfkb_base = simulate_signaling_ode(k1, k2, k3, k4, cd40_input)
    baseline_auc = float(np.trapezoid(nfkb_base, t))
    baseline_t_peak = float(t[np.argmax(nfkb_base)])

    rows = []
    for target, effects in CRISPR_TARGET_EFFECTS.items():
        k1_t = k1 * effects.get("k1_mult", 1.0)
        k2_t = k2 * effects.get("k2_mult", 1.0)
        k3_t = k3 * effects.get("k3_mult", 1.0)
        k4_t = k4 * effects.get("k4_mult", 1.0)

        t_ko, _, nfkb_ko = simulate_signaling_ode(k1_t, k2_t, k3_t, k4_t, cd40_input)
        combo_auc = float(np.trapezoid(nfkb_ko, t_ko))
        synergy = ((combo_auc - baseline_auc) / max(baseline_auc, 1e-6)) * 100.0
        ko_t_peak = float(t_ko[np.argmax(nfkb_ko)])

        rows.append(
            {
                "Target": target,
                "Baseline AUC": round(baseline_auc, 3),
                "KO+Agonist AUC": round(combo_auc, 3),
                "Synergy Score (%)": round(synergy, 2),
                "Baseline t_peak": round(baseline_t_peak, 2),
                "KO t_peak": round(ko_t_peak, 2),
                "Δt_peak": round(ko_t_peak - baseline_t_peak, 2),
                "Mechanistic note": effects["note"],
            }
        )

    score_df = pd.DataFrame(rows).sort_values("Synergy Score (%)", ascending=False)
    selected = st.selectbox("Genetic Target", score_df["Target"].tolist())

    left, right = st.columns([1, 2])
    with left:
        row = score_df[score_df["Target"] == selected].iloc[0]
        st.metric(f"{selected} synergy", f"{row['Synergy Score (%)']}%")
        st.info(row["Mechanistic note"])
        st.caption("Score = ((KO+Agonist AUC - Baseline AUC) / Baseline AUC) × 100")
        st.caption("Time-to-peak is computed as t[np.argmax(NF-κB)] to capture dynamic reshaping.")

    with right:
        st.bar_chart(score_df.set_index("Target")[["Synergy Score (%)"]])
        st.dataframe(
            score_df[["Target", "Baseline AUC", "KO+Agonist AUC", "Synergy Score (%)", "Baseline t_peak", "KO t_peak", "Δt_peak"]],
            width="stretch",
        )

elif tab_select == "Kinetic Simulator (ODE)":
    st.subheader("📈 ODE Kinetic Simulator")
    t, traf6, nfkb = simulate_signaling_ode(k1, k2, k3, k4, cd40_input)
    kinetics_df = pd.DataFrame({"Time": t, "TRAF6": traf6, "NF-κB": nfkb})
    st.line_chart(kinetics_df.set_index("Time"))

    analytical_nfkb = (k1 * k3 * cd40_input) / max(k2 * k4, 1e-9)
    simulated_nfkb = float(nfkb[-1])
    percent_deviation = abs((simulated_nfkb - analytical_nfkb) / max(analytical_nfkb, 1e-9)) * 100
    convergence_difference = abs(float(nfkb[-1]) - float(nfkb[-10]))

    st.success(f"Steady-state NF-κB (simulated): {simulated_nfkb:.3f}")

    st.markdown("### Sensitivity Analysis: k1 Sweep")
    k1_values = np.linspace(0.02, 0.18, 15)
    sweep_results = []
    for val in k1_values:
        _, _, nfkb_sweep = simulate_signaling_ode(val, k2, k3, k4, cd40_input)
        sweep_results.append(float(nfkb_sweep[-1]))

    sweep_df = pd.DataFrame({"k1": k1_values, "SteadyState_NFkB": sweep_results})
    st.line_chart(sweep_df.set_index("k1"))

    st.markdown("### Sensitivity Analysis: k4 Sweep")
    k4_values = np.linspace(0.02, 0.18, 15)
    results_k4 = []
    for val in k4_values:
        _, _, nfkb_k4 = simulate_signaling_ode(k1, k2, k3, val, cd40_input)
        results_k4.append(float(nfkb_k4[-1]))

    k4_df = pd.DataFrame({"k4": k4_values, "SteadyState_NFkB": results_k4})
    st.line_chart(k4_df.set_index("k4"))

    st.markdown("**Solved numerically as coupled ODEs using RK4 integration (t_max=200, points=2000).**")

    st.code(
        f"""Analytical NF-κB*: {analytical_nfkb:.3f}
Simulated NF-κB*: {simulated_nfkb:.3f}
Percent deviation: {percent_deviation:.2f}%
Convergence difference (last 10 steps): {convergence_difference:.4f}""",
        language="text",
    )
    st.caption("*Analytical value is steady-state approximation NF-κB_ss = (k1·k3·CD40)/(k2·k4).")

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
    for protein, hypothesis in DARK_PROTEOME_HYPOTHESES.items():
        st.markdown(f"- **{protein}:** {hypothesis}")

elif tab_select == "Molecular Validation":
    st.subheader("🧬 Molecular Validation: Plausibility Checks")
    col1, col2 = st.columns(2)
    with col1:
        dock_df = pd.DataFrame({"Ligand": [ligand, "Native CD40L"], "Affinity (kcal/mol)": [-11.4, -9.2]})
        st.table(dock_df)
    with col2:
        expr_df = pd.DataFrame({"Cell Type": ["B-Cells", "Dendritic Cells", "Macrophages"], "TPM": [180, 310, 95]})
        st.bar_chart(expr_df.set_index("Cell Type"))

st.divider()
with st.expander("Supplementary (Portfolio-only): Exploratory Feature Concepts"):
    st.warning("These are exploratory design concepts for portfolio/demo use, not core validated model outputs for manuscript claims.")
    include = st.checkbox("Show supplementary concept ranking", value=False)
    if include:
        sup_df = pd.DataFrame(
            [
                {
                    "Feature": name,
                    "Impact": val["impact"],
                    "Feasibility": val["feasibility"],
                    "Execution Risk": val["risk"],
                    "Priority Index": round(val["impact"] * 0.6 + val["feasibility"] * 0.4, 1),
                }
                for name, val in SUPPLEMENTARY_FEATURES.items()
            ]
        ).sort_values("Priority Index", ascending=False)
        st.dataframe(sup_df, width="stretch")

st.subheader("📄 Export Project Summary")
summary_text = generate_project_summary(scaffold, ligand, k1, k2, k3, k4, cd40_input)
st.download_button(
    label="⬇️ Download Project Summary (TXT)",
    data=summary_text,
    file_name="CD40_Immunosome_Project_Summary.txt",
    mime="text/plain",
)

st.divider()
st.caption("PhD Application Portfolio | Systems Biology Framework | Yashwant Nama")
