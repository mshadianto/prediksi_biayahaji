"""Visualization utilities"""
import plotly.graph_objects as go
from typing import Dict

def create_prediction_chart(scenarios: Dict[str, float], months_ahead: int = 24) -> go.Figure:
    """Buat chart prediksi biaya haji"""
    months = list(range(0, months_ahead + 1))
    
    fig = go.Figure()
    
    colors = {"Konservatif": "green", "Realistis": "blue", "Optimistis": "red"}
    
    for scenario, base_cost in scenarios.items():
        annual_growth = 0.08  # 8% pertumbuhan tahunan
        monthly_growth = annual_growth / 12
        
        costs = [base_cost * (1 + monthly_growth) ** month for month in months]
        
        fig.add_trace(go.Scatter(
            x=months,
            y=costs,
            mode='lines+markers',
            name=f'Skenario {scenario}',
            line=dict(color=colors[scenario], width=3),
            hovertemplate=f'<b>{scenario}</b><br>Bulan: %{{x}}<br>Biaya: Rp %{{y:,.0f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Prediksi Biaya Haji Indonesia",
        xaxis_title="Bulan Ke Depan",
        yaxis_title="Biaya (IDR)",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig
