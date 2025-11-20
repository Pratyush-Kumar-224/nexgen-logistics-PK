import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest 
from io import BytesIO

st.set_page_config(layout="wide", page_title="NexGen Cost-Efficiency Imbalance Predictor")

st.title("NexGen Cost-Efficiency Imbalance Predictor (V-IP)")
st.markdown("Leveraging ML for Proactive Asset Management & Cost Leakage Reduction.")

@st.cache_data
def load_and_process_data():
    try:
        df_vehicles = pd.read_csv('vehicle_fleet.csv')
        df_routes = pd.read_csv('routes_distance.csv')
        df_costs = pd.read_csv('cost_breakdown.csv')
        max_orders = len(df_vehicles)
        order_ids = [f'ORD{i:06d}' for i in range(1, max_orders + 1)]
        vehicle_ids = df_vehicles['Vehicle_ID'].tolist()
        df_mapping = pd.DataFrame({'Order_ID': order_ids, 'Vehicle_ID': vehicle_ids})
        
        df_routes_mapped = df_routes.merge(df_mapping, on='Order_ID', how='inner')
        total_distance = df_routes_mapped.groupby('Vehicle_ID')['Distance_KM'].sum().reset_index()
        total_distance.rename(columns={'Distance_KM': 'Total_Distance_KM'}, inplace=True)

        df_costs_mapped = df_costs.merge(df_mapping, on='Order_ID', how='inner')
        total_maintenance = df_costs_mapped.groupby('Vehicle_ID')['Vehicle_Maintenance'].sum().reset_index()
        total_maintenance.rename(columns={'Vehicle_Maintenance': 'Total_Maintenance_Costs'}, inplace=True)
        
        df_master = df_vehicles.merge(total_distance, on='Vehicle_ID', how='left')
        df_master = df_master.merge(total_maintenance, on='Vehicle_ID', how='left')

        df_master[['Total_Distance_KM', 'Total_Maintenance_Costs']] = df_master[['Total_Distance_KM', 'Total_Maintenance_Costs']].fillna(0)

        MAX_DISTANCE_REF = df_master['Total_Distance_KM'].max() * 1.5 
        df_master['Utilization_Rate'] = df_master['Total_Distance_KM'] / MAX_DISTANCE_REF

        maintenance_min = df_master['Total_Maintenance_Costs'].min()
        maintenance_max = df_master['Total_Maintenance_Costs'].max()
        if maintenance_max == maintenance_min:
             df_master['Normalized_Maintenance'] = 0 
        else:
            df_master['Normalized_Maintenance'] = (df_master['Total_Maintenance_Costs'] - maintenance_min) / (maintenance_max - maintenance_min)

        epsilon = 0.01 
        df_master['Cost_Leakage_Index'] = df_master['Normalized_Maintenance'] / (df_master['Utilization_Rate'] + epsilon)

        X_ml = df_master[['Cost_Leakage_Index', 'Age_Years', 'Utilization_Rate']].copy()
        X_ml = X_ml.fillna(X_ml.mean()) 

        model = IsolationForest(contamination=0.1, random_state=42) 
        df_master['Anomaly_Flag'] = model.fit_predict(X_ml)
        df_master['Risk_Flag'] = df_master['Anomaly_Flag'].apply(lambda x: 'HIGH_RISK_ANOMALY' if x == -1 else 'Normal')
        
        df_final_report = df_master[['Vehicle_ID', 'Vehicle_Type', 'Age_Years', 'Status',
                                     'Total_Distance_KM', 'Total_Maintenance_Costs',
                                     'Utilization_Rate', 'Cost_Leakage_Index', 'Risk_Flag']]
        
        return df_final_report
    
    except FileNotFoundError:
        st.error("Error: Ensure all data files (vehicle_fleet.csv, routes_distance.csv, cost_breakdown.csv) are in the project directory.")
        return pd.DataFrame()

df_data = load_and_process_data()

if not df_data.empty:
    
    st.sidebar.header("Filter Options")
    type_filter = st.sidebar.multiselect(
        "Filter by Vehicle Type:",
        options=df_data['Vehicle_Type'].unique(),
        default=df_data['Vehicle_Type'].unique()
    )
    risk_filter = st.sidebar.selectbox(
        "Filter by Risk Flag:",
        options=['All', 'HIGH_RISK_ANOMALY', 'Normal'],
        index=0
    )

    filtered_data = df_data[df_data['Vehicle_Type'].isin(type_filter)]
    if risk_filter != 'All':
         filtered_data = filtered_data[filtered_data['Risk_Flag'] == risk_filter]

    col1, col2, col3, col4 = st.columns(4)
    total_vehicles = len(df_data)
    anomalies = len(df_data[df_data['Risk_Flag'] == 'HIGH_RISK_ANOMALY'])
    
    col1.metric("Total Fleet Assets", total_vehicles)
    col2.metric("High-Risk Anomalies", anomalies, f"{anomalies/total_vehicles:.1%}")
    col3.metric("Max Cost Leakage Index", f"{df_data['Cost_Leakage_Index'].max():.2f}")
    col4.metric("Avg. Maintenance Cost", f"₹ {df_data['Total_Maintenance_Costs'].mean():,.0f}")
    

    st.header("Risk Profile: Utilization, Age, and Cost Leakage")
    st.markdown("**Bubble size** and **color** indicate the **Cost Leakage Index (CLI)**. High CLI vehicles are candidates for early review.")
    
    fig = px.scatter(
        filtered_data,
        x='Utilization_Rate',
        y='Age_Years',
        size='Cost_Leakage_Index',
        color='Cost_Leakage_Index', 
        hover_name='Vehicle_ID',
        size_max=40,
        color_continuous_scale=px.colors.sequential.Inferno,
        labels={'Utilization_Rate': 'Utilization Rate (vs Max Ref)', 'Age_Years': 'Vehicle Age (Years)'}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.header("Detailed Vehicle Report")
    st.dataframe(filtered_data.sort_values('Cost_Leakage_Index', ascending=False), use_container_width=True)
    
    def to_csv(df):
        output = BytesIO()
        df.to_csv(output, index=False)
        return output.getvalue()

    st.download_button(
        label="Download Filtered Data as CSV",
        data=to_csv(filtered_data),
        file_name='nexgen_cost_report.csv',
        mime='text/csv',
    )
