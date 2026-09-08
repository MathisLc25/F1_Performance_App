import streamlit as st
import fastf1
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np

st.set_page_config(page_title="Pitwall F1 - Groupe 2", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #0E1117;}
    h1 {color: #FF1801; font-family: 'Arial', sans-serif; text-transform: uppercase; text-align: center; font-weight: 900;}
    h3 {color: #E0E0E0;}
    [data-testid="metric-container"] {background-color: #1E2329; padding: 15px; border-radius: 10px; border-left: 5px solid #FF1801;}
    .stTabs [data-baseweb="tab-list"] {gap: 24px;}
    .phase-box {border-radius:5px; padding:15px; color:white; text-align:center; font-weight:bold; margin-bottom:10px;}
    .stTabs [data-baseweb="tab"] {height: 50px; white-space: pre-wrap; background-color: #1E2329; border-radius: 5px 5px 0px 0px; padding: 10px 20px; color: white;}
    .stTabs [aria-selected="true"] {background-color: #FF1801 !important; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title(" Pitwall Télémétrie & IA")
st.markdown("<p style='text-align: center; color: #888;'>Interface d'Ingénierie de Piste - ECE Groupe 2</p>", unsafe_allow_html=True)
st.markdown("---")

fastf1.Cache.enable_cache('cache')

@st.cache_data
def load_data(year, gp, driver1, driver2):
    session = fastf1.get_session(year, gp, 'Q')
    session.load(telemetry=True, weather=False, messages=False)
    lap1 = session.laps.pick_driver(driver1).pick_fastest()
    lap2 = session.laps.pick_driver(driver2).pick_fastest()
    return lap1, lap2

with st.sidebar:
    st.image("https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png", width=130)
    st.header(" Paramètres")
    annee = st.selectbox("Année", [2024, 2023], index=0)
    grand_prix = st.selectbox("Grand Prix", ["Bahrain", "Monaco", "Monza", "Silverstone", "Barcelone"], index=0)
    st.divider()
    pilote_1 = st.selectbox("Pilote 1 (Référence)", ["VER", "LEC", "HAM", "ALO", "NOR", "SAI", "RUS", "PER"], index=0)
    pilote_2 = st.selectbox("Pilote 2 (Analyse IA)", ["VER", "LEC", "HAM", "ALO", "NOR", "SAI", "RUS", "PER"], index=1)

if pilote_1 == pilote_2:
    st.error(" Les pilotes doivent être différents pour effectuer une comparaison.")
else:
    try:
        with st.spinner(' Téléchargement de la télémétrie...'):
            lap1, lap2 = load_data(annee, grand_prix, pilote_1, pilote_2)
            tel1 = lap1.get_telemetry()
            tel2 = lap2.get_telemetry()
        
        st.write(f"###  {grand_prix} {annee} - Qualifications")
        col1, col2, col3 = st.columns(3)
        col1.metric(label=f"🏎️ Chrono {pilote_1}", value=str(lap1['LapTime'])[-12:-3])
        col2.metric(label=f"🏎️ Chrono {pilote_2}", value=str(lap2['LapTime'])[-12:-3], delta="Analyse IA active")
        
        tel2['Acceleration'] = tel2['Speed'].diff().fillna(0)
        X = tel2[['Speed', 'Acceleration']].values
        
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        tel2['Cluster_Raw'] = kmeans.fit_predict(X) 

        idx_sorted_by_speed = tel2.groupby('Cluster_Raw')['Speed'].mean().sort_values().index
        mapping = {idx_sorted_by_speed[0]: 0, idx_sorted_by_speed[1]: 1, idx_sorted_by_speed[2]: 2}
        tel2['Phase_Pilotage'] = tel2['Cluster_Raw'].map(mapping)
        
        col3.metric(label=" Statut Modèle", value="KMeans Opérationnel", delta="3 Clusters", delta_color="normal")
        st.markdown("<br>", unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([" Comparaison Vitesse", " Tracé & Zones IA", " Rapport Stratégique"])
        
        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=tel1['Distance'], y=tel1['Speed'], mode='lines', name=f"{pilote_1}", line=dict(color='#00d2be', width=2.5)))
            fig.add_trace(go.Scatter(x=tel2['Distance'], y=tel2['Speed'], mode='lines', name=f"{pilote_2}", line=dict(color='#FF1801', width=2.5)))
            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Distance (m)",
                yaxis_title="Vitesse (km/h)",
                hovermode="x unified",
                margin=dict(l=20, r=20, t=50, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            custom_colors = ["#FF1801", "#FFD700", "#00FF00"] 
            
            fig_map = px.scatter(
                tel2, x="X", y="Y", color="Phase_Pilotage", 
                color_continuous_scale=custom_colors, 
                title=f"Zones de pilotage identifiées par l'IA ({pilote_2})"
            )
            fig_map.update_layout(
                template="plotly_dark",
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, visible=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=50, b=0),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_map, use_container_width=True)
            
        with tab3:
            st.info(f"**Diagnostic Machine Learning actif sur la monoplace de {pilote_2}**")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.error("🔴 Phase 1 : Freinage")
            with c2:
                st.warning("🟡 Phase 2 : Virage")
            with c3:
                st.success("🟢 Phase 3 : Accélération")
            st.markdown("---")
            st.write(" *Coaching :* Localisez les points rouges sur le tracé pour identifier les zones de freinage fort.")


    except Exception as e:
        st.error(f"Erreur technique : {e}")
