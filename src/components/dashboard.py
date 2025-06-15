"""Enhanced dashboard component dengan data riil"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render_dashboard(data_collector, predictor, rag_system):
    """Render enhanced dashboard dengan data riil"""
    
    st.header("📊 Dashboard Prediksi Biaya Haji")
    
    # Quick stats dari data riil
    historical_data = rag_system.knowledge_base["data_historis"]
    latest_cost = historical_data[2025]['average']
    prev_cost = historical_data[2024]['average']
    change_2025 = ((latest_cost - prev_cost) / prev_cost) * 100
    
    # Lonjakan 2023
    cost_2022 = historical_data[2022]['average']
    cost_2023 = historical_data[2023]['average']
    lonjakan_2023 = ((cost_2023 - cost_2022) / cost_2022) * 100
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Biaya Haji 2025",
            f"Rp {latest_cost/1000000:.1f}M",
            f"{change_2025:+.1f}%",
            help="Berdasarkan Keppres 6/2025"
        )
    
    with col2:
        st.metric(
            "Lonjakan 2023",
            f"+{lonjakan_2023:.0f}%",
            "Rp 39M → 90M",
            help="Anomali pasca-COVID"
        )
    
    with col3:
        # Prediksi 2026
        pred_2026 = predictor.predict_future_cost(1)
        growth_2026 = ((pred_2026 - latest_cost) / latest_cost) * 100
        st.metric(
            "Prediksi 2026",
            f"Rp {pred_2026/1000000:.1f}M",
            f"{growth_2026:+.1f}%",
            help="Berdasarkan trend analysis"
        )
    
    with col4:
        growth_rate = predictor.growth_analysis['average_normal_growth'] * 100
        st.metric(
            "Growth Normal",
            f"{growth_rate:.1f}%/tahun",
            "2016-2022",
            help="Periode sebelum anomali 2023"
        )
    
    # Main visualization
    st.subheader("📈 Trend Historis & Prediksi")
    
    # Create comprehensive chart
    fig = create_comprehensive_chart(historical_data, predictor)
    st.plotly_chart(fig, use_container_width=True)
    
    # Two column layout untuk analisis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Real-time data integration
        st.subheader("🌍 Data Real-time")
        
        with st.spinner("Mengambil data ekonomi real-time..."):
            gold_data = data_collector.get_gold_price()
            exchange_rate = data_collector.get_exchange_rate()
        
        if gold_data:
            # Display current economic indicators
            econ_col1, econ_col2 = st.columns(2)
            
            with econ_col1:
                st.metric(
                    "Harga Emas",
                    f"${gold_data['current_price']:.0f}/oz",
                    f"{gold_data['change']:+.1f}$"
                )
            
            with econ_col2:
                st.metric(
                    "USD/IDR",
                    f"Rp {exchange_rate:,.0f}",
                    help="Mempengaruhi biaya haji"
                )
            
            # Correlation analysis dengan data riil
            st.markdown("**💡 Impact Analysis:**")
            
            # Calculate correlation impact
            base_cost = predictor.calculate_base_cost()
            gold_adjusted_cost = predictor.apply_gold_correlation(base_cost, gold_data['current_price'])
            gold_impact = ((gold_adjusted_cost - base_cost) / base_cost) * 100
            
            if abs(gold_impact) > 1:
                impact_color = "🔴" if gold_impact > 0 else "🟢"
                st.markdown(f"{impact_color} Harga emas saat ini berpotensi mengubah biaya haji sebesar **{gold_impact:+.1f}%**")
            else:
                st.markdown("🟡 Harga emas saat ini dalam range normal")
    
    with col2:
        st.subheader("🎯 Prediksi Multi-Skenario")
        
        # Get prediction scenarios
        scenarios = predictor.generate_prediction_scenarios(
            gold_data['current_price'] if gold_data else 2000, 
            exchange_rate
        )
        
        # Display scenarios
        for scenario, cost in scenarios.items():
            delta_pct = ((cost - latest_cost) / latest_cost) * 100
            
            if scenario == "Konservatif":
                st.metric(scenario, f"Rp {cost/1000000:.1f}M", f"{delta_pct:+.1f}%", delta_color="inverse")
            elif scenario == "Optimistis":
                st.metric(scenario, f"Rp {cost/1000000:.1f}M", f"{delta_pct:+.1f}%", delta_color="off")
            else:
                st.metric(scenario, f"Rp {cost/1000000:.1f}M", f"{delta_pct:+.1f}%")
        
        # Confidence indicator
        st.markdown("**🎯 Confidence Level:**")
        st.progress(0.85, text="85% (1 tahun ke depan)")
    
    # Regional Analysis
    st.subheader("🗺️ Analisis Regional Terbaru")
    
    regional_data = predictor.analyze_regional_differences(2025)
    
    # Create regional comparison chart
    cities = list(regional_data.keys())
    costs = [regional_data[city]['cost']/1000000 for city in cities]  # Convert to millions
    colors = ['red' if regional_data[city]['category'] == 'Mahal' 
             else 'green' if regional_data[city]['category'] == 'Murah' 
             else 'blue' for city in cities]
    
    fig_regional = go.Figure(data=[
        go.Bar(
            x=[city.title() for city in cities],
            y=costs,
            marker_color=colors,
            text=[f"Rp {cost:.1f}M" for cost in costs],
            textposition='auto',
        )
    ])
    
    fig_regional.update_layout(
        title="Perbandingan Biaya per Embarkasi (2025)",
        xaxis_title="Embarkasi",
        yaxis_title="Biaya (Juta Rupiah)",
        showlegend=False,
        template='plotly_white',
        height=400
    )
    
    # Add average line
    avg_cost = latest_cost / 1000000
    fig_regional.add_hline(
        y=avg_cost, 
        line_dash="dash", 
        line_color="gray",
        annotation_text=f"Rata-rata: Rp {avg_cost:.1f}M"
    )
    
    st.plotly_chart(fig_regional, use_container_width=True)
    
    # Risk Factors
    st.subheader("⚠️ Faktor Risiko & Peluang")
    
    risk_factors = predictor.get_risk_factors()
    
    risk_col1, risk_col2 = st.columns(2)
    
    with risk_col1:
        st.markdown("**🔴 Risiko Kenaikan:**")
        high_risk_factors = ['inflasi_global', 'kebijakan_saudi', 'nilai_tukar', 'geopolitik']
        for factor in high_risk_factors:
            if factor in risk_factors:
                st.markdown(f"• {risk_factors[factor]}")
    
    with risk_col2:
        st.markdown("**🟢 Peluang Stabilitas:**")
        st.markdown("""
        • Normalisasi pasca-anomali 2023
        • Trend kembali ke growth rate normal
        • Perbaikan infrastruktur haji
        • Stabilitas ekonomi regional
        """)
    
    # Summary insights
    st.subheader("💡 Key Insights")
    
    summary = predictor.get_prediction_summary()
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown(f"""
        **📊 Data Summary:**
        - **Current Cost**: Rp {summary['current_cost_2025']/1000000:.1f}M
        - **Expected Growth**: {summary['expected_growth_rate']} per tahun
        - **Confidence**: {summary['confidence_level']} untuk prediksi 1 tahun
        - **Metodologi**: {summary['prediction_method']}
        """)
    
    with insights_col2:
        st.markdown(f"""
        **🎯 Recommendations:**
        - **Timeline Optimal**: Daftar 2-3 tahun ke depan untuk stabilitas biaya
        - **Embarkasi**: Aceh/Medan untuk biaya lebih rendah
        - **Monitoring**: Pantau harga emas dan nilai tukar
        - **Planning**: Siapkan buffer 10-15% dari prediksi
        """)

def create_comprehensive_chart(historical_data, predictor):
    """Create comprehensive chart dengan historical + prediksi"""
    
    # Historical data
    years = sorted(historical_data.keys())
    costs = [historical_data[year]['average']/1000000 for year in years]  # Convert to millions
    
    # Future predictions
    future_predictions = predictor.predict_multiple_years(3)
    future_years = sorted(future_predictions.keys())
    future_costs = [future_predictions[year]['realistis']/1000000 for year in future_years]
    
    fig = go.Figure()
    
    # Historical line
    fig.add_trace(go.Scatter(
        x=years,
        y=costs,
        mode='lines+markers',
        name='Data Historis (Keppres)',
        line=dict(color='blue', width=4),
        marker=dict(size=8, color='blue')
    ))
    
    # Future prediction line
    fig.add_trace(go.Scatter(
        x=future_years,
        y=future_costs,
        mode='lines+markers',
        name='Prediksi (ML)',
        line=dict(color='red', width=3, dash='dash'),
        marker=dict(size=6, color='red')
    ))
    
    # Highlight anomali 2023
    fig.add_annotation(
        x=2023, 
        y=historical_data[2023]['average']/1000000,
        text="Anomali COVID<br>+128%",
        showarrow=True,
        arrowhead=2,
        arrowcolor="orange",
        font=dict(color="orange", size=12),
        bgcolor="rgba(255,165,0,0.1)",
        bordercolor="orange"
    )
    
    # Add trend phases
    fig.add_vrect(
        x0=2016, x1=2022,
        fillcolor="green", opacity=0.1,
        annotation_text="Periode Normal", annotation_position="top left"
    )
    
    fig.add_vrect(
        x0=2023, x1=2023.9,
        fillcolor="red", opacity=0.1,
        annotation_text="Anomali", annotation_position="top"
    )
    
    fig.add_vrect(
        x0=2024, x1=max(future_years),
        fillcolor="blue", opacity=0.05,
        annotation_text="Normalisasi", annotation_position="top right"
    )
    
    fig.update_layout(
        title="Analisis Komprehensif: Biaya Haji Indonesia 2016-2028",
        xaxis_title="Tahun",
        yaxis_title="Biaya Haji (Juta Rupiah)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig