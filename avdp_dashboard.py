import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="AVDP Climate-Smart Agriculture Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E8B57, #228B22);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2E8B57;
    }
    .testimonial {
        background: #f0f8e7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        font-style: italic;
        margin: 1rem 0;
    }
    .value-chain-header {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sample data generation functions
@st.cache_data
def generate_sample_data():
    """Generate comprehensive sample data for the dashboard"""
    
    # Districts in Sierra Leone
    districts = ['Western Area', 'Bo', 'Kenema', 'Kailahun', 'Kono', 'Bombali', 'Tonkolili', 'Port Loko']
    
    # IVS Rice Data
    ivs_data = []
    for district in districts:
        for year in range(2020, 2025):
            ivs_data.append({
                'District': district,
                'Year': year,
                'Hectares_Developed': np.random.randint(50, 200),
                'Farmers_Count': np.random.randint(100, 500),
                'Women_Farmers': np.random.randint(40, 200),
                'Youth_Farmers': np.random.randint(20, 100),
                'CSA_Adoption_Rate': np.random.uniform(0.3, 0.9),
                'Yield_Traditional': np.random.uniform(2.0, 3.5),
                'Yield_CSA': np.random.uniform(3.5, 6.0),
                'Income_Before': np.random.uniform(500, 1200),
                'Income_After': np.random.uniform(800, 2000)
            })
    
    # Tree Crops Data
    tree_data = []
    for district in districts:
        for year in range(2020, 2025):
            tree_data.append({
                'District': district,
                'Year': year,
                'Cocoa_Seedlings': np.random.randint(1000, 5000),
                'Oil_Palm_Seedlings': np.random.randint(500, 3000),
                'Survival_Rate_Year2': np.random.uniform(0.7, 0.95),
                'Farmers_Trained': np.random.randint(50, 300),
                'Income_Change': np.random.uniform(200, 800)
            })
    
    # Vegetable Data
    veg_data = []
    csa_techniques = ['Raised Beds', 'Mulching', 'Drip Irrigation', 'Composting', 'Intercropping']
    for district in districts:
        for technique in csa_techniques:
            veg_data.append({
                'District': district,
                'CSA_Technique': technique,
                'Farmers_Supported': np.random.randint(20, 150),
                'Onion_Yield_Increase': np.random.uniform(0.2, 0.8),
                'Pepper_Yield_Increase': np.random.uniform(0.15, 0.6),
                'Price_Premium': np.random.uniform(0.1, 0.4),
                'Women_Participation': np.random.uniform(0.6, 0.9)
            })
    
    return pd.DataFrame(ivs_data), pd.DataFrame(tree_data), pd.DataFrame(veg_data)

@st.cache_data
def create_sustainability_scores():
    """Create sustainability scores for different CSA practices"""
    practices = [
        'Raised Beds', 'Water Retention', 'Composting', 'Improved Seeds',
        'Mulching', 'Agroforestry', 'Drip Irrigation', 'Intercropping'
    ]
    
    scores_data = []
    for practice in practices:
        scores_data.append({
            'Practice': practice,
            'Climate_Resilience': np.random.uniform(3.5, 5.0),
            'Scalability': np.random.uniform(3.0, 5.0),
            'Cost_Effectiveness': np.random.uniform(3.2, 4.8),
            'Farmer_Adoption': np.random.uniform(3.0, 4.5)
        })
    
    return pd.DataFrame(scores_data)

# Data loading
ivs_df, tree_df, veg_df = generate_sample_data()
sustainability_df = create_sustainability_scores()

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; text-align: center; margin: 0;">
        🌱 AVDP Climate-Smart Agriculture Dashboard
    </h1>
    <p style="color: white; text-align: center; margin: 0.5rem 0 0 0;">
        Agricultural Value Development Program - Impact Monitoring & Evaluation
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🎛️ Dashboard Filters")
selected_districts = st.sidebar.multiselect(
    "Select Districts",
    options=ivs_df['District'].unique(),
    default=ivs_df['District'].unique()[:3]
)

selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=2020,
    max_value=2024,
    value=(2022, 2024)
)

csa_filter = st.sidebar.selectbox(
    "Filter by CSA Practice",
    options=['All'] + list(veg_df['CSA_Technique'].unique())
)

gender_focus = st.sidebar.selectbox(
    "Gender/Youth Analysis",
    options=['All', 'Women Focus', 'Youth Focus']
)

# Filter data based on selections
filtered_ivs = ivs_df[
    (ivs_df['District'].isin(selected_districts)) &
    (ivs_df['Year'].between(selected_years[0], selected_years[1]))
]

filtered_tree = tree_df[
    (tree_df['District'].isin(selected_districts)) &
    (tree_df['Year'].between(selected_years[0], selected_years[1]))
]

filtered_veg = veg_df[veg_df['District'].isin(selected_districts)]
if csa_filter != 'All':
    filtered_veg = filtered_veg[filtered_veg['CSA_Technique'] == csa_filter]

# Key Performance Indicators
st.header("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_hectares = filtered_ivs['Hectares_Developed'].sum()
    st.metric(
        label="Total Hectares Developed (IVS)",
        value=f"{total_hectares:,}",
        delta=f"+{int(total_hectares * 0.15)} from last period"
    )

with col2:
    total_farmers = filtered_ivs['Farmers_Count'].sum()
    st.metric(
        label="Farmers Reached",
        value=f"{total_farmers:,}",
        delta=f"+{int(total_farmers * 0.12)} new farmers"
    )

with col3:
    avg_csa_adoption = filtered_ivs['CSA_Adoption_Rate'].mean()
    st.metric(
        label="CSA Adoption Rate",
        value=f"{avg_csa_adoption:.1%}",
        delta=f"+{avg_csa_adoption*0.1:.1%} improvement"
    )

with col4:
    total_seedlings = filtered_tree['Cocoa_Seedlings'].sum() + filtered_tree['Oil_Palm_Seedlings'].sum()
    st.metric(
        label="Tree Seedlings Distributed",
        value=f"{total_seedlings:,}",
        delta=f"+{int(total_seedlings * 0.08)} this period"
    )

# Value Chain Analysis
st.header("🌾 Value Chain Impact Analysis")

# IVS Rice Section
st.markdown('<div class="value-chain-header"><h3>🌊 Inland Valley Swamps (IVS) - Rice Cultivation with CSA</h3></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # CSA Adoption by District
    district_csa = filtered_ivs.groupby('District')['CSA_Adoption_Rate'].mean().reset_index()
    fig_csa = px.bar(
        district_csa,
        x='District',
        y='CSA_Adoption_Rate',
        title="CSA Adoption Rate by District",
        color='CSA_Adoption_Rate',
        color_continuous_scale='Greens'
    )
    fig_csa.update_layout(showlegend=False)
    st.plotly_chart(fig_csa, use_container_width=True)

with col2:
    # Yield Comparison
    yield_comparison = filtered_ivs.groupby('Year')[['Yield_Traditional', 'Yield_CSA']].mean().reset_index()
    fig_yield = go.Figure()
    fig_yield.add_trace(go.Scatter(
        x=yield_comparison['Year'],
        y=yield_comparison['Yield_Traditional'],
        mode='lines+markers',
        name='Traditional Farming',
        line=dict(color='red', dash='dash')
    ))
    fig_yield.add_trace(go.Scatter(
        x=yield_comparison['Year'],
        y=yield_comparison['Yield_CSA'],
        mode='lines+markers',
        name='CSA Farming',
        line=dict(color='green')
    ))
    fig_yield.update_layout(
        title="Rice Yield Progression: CSA vs Traditional",
        xaxis_title="Year",
        yaxis_title="Yield (tons/hectare)"
    )
    st.plotly_chart(fig_yield, use_container_width=True)

# Testimonial for IVS
st.markdown("""
<div class="testimonial">
    💬 <strong>Farmer Testimonial:</strong> "Now we grow rice even during short rains. The raised beds and improved water management have transformed our farming. My family's income has doubled!" - Aminata Kamara, Bo District
</div>
""", unsafe_allow_html=True)

# Tree Crops Section
st.markdown('<div class="value-chain-header"><h3>🌴 Tree Crops (Oil Palm & Cocoa) - Improved Varieties + CSA</h3></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Seedling Distribution
    total_cocoa = filtered_tree['Cocoa_Seedlings'].sum()
    total_palm = filtered_tree['Oil_Palm_Seedlings'].sum()
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Cocoa', 'Oil Palm'],
        values=[total_cocoa, total_palm],
        hole=.3
    )])
    fig_donut.update_layout(
        title="Seedling Distribution by Crop Type",
        annotations=[dict(text=f'Total<br>{total_cocoa + total_palm:,}', x=0.5, y=0.5, font_size=12, showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col2:
    # Survival Rate and Income Change
    survival_income = filtered_tree.groupby('District')[['Survival_Rate_Year2', 'Income_Change']].mean().reset_index()
    
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
    fig_dual.add_trace(
        go.Bar(x=survival_income['District'], y=survival_income['Survival_Rate_Year2'], name="Survival Rate"),
        secondary_y=False,
    )
    fig_dual.add_trace(
        go.Scatter(x=survival_income['District'], y=survival_income['Income_Change'], 
                  mode='lines+markers', name="Income Change ($)", line=dict(color='orange')),
        secondary_y=True,
    )
    fig_dual.update_xaxes(title_text="District")
    fig_dual.update_yaxes(title_text="Survival Rate (%)", secondary_y=False)
    fig_dual.update_yaxes(title_text="Income Change ($)", secondary_y=True)
    fig_dual.update_layout(title="Tree Survival vs Income Impact")
    st.plotly_chart(fig_dual, use_container_width=True)

# Tree Crops Testimonial
st.markdown("""
<div class="testimonial">
    💬 <strong>Farmer Testimonial:</strong> "My new cocoa trees bear faster and survive the dry season better. The improved varieties have given me hope for the future." - Mohamed Bangura, Kenema District
</div>
""", unsafe_allow_html=True)

# Vegetables Section
st.markdown('<div class="value-chain-header"><h3>🥕 Vegetables (Onions & Bulb Pepper) - CSA for Perishable Crops</h3></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Yield Increase by CSA Technique
    technique_yield = filtered_veg.groupby('CSA_Technique')[['Onion_Yield_Increase', 'Pepper_Yield_Increase']].mean().reset_index()
    
    fig_yield_tech = go.Figure()
    fig_yield_tech.add_trace(go.Bar(
        name='Onion Yield Increase',
        x=technique_yield['CSA_Technique'],
        y=technique_yield['Onion_Yield_Increase'],
        yaxis='y',
        offsetgroup=1
    ))
    fig_yield_tech.add_trace(go.Bar(
        name='Pepper Yield Increase',
        x=technique_yield['CSA_Technique'],
        y=technique_yield['Pepper_Yield_Increase'],
        yaxis='y',
        offsetgroup=2
    ))
    fig_yield_tech.update_layout(
        title="Yield Increase by CSA Technique",
        xaxis_title="CSA Technique",
        yaxis_title="Yield Increase (%)",
        barmode='group'
    )
    st.plotly_chart(fig_yield_tech, use_container_width=True)

with col2:
    # Gender Participation in Vegetable Farming
    gender_participation = filtered_veg.groupby('District')['Women_Participation'].mean().reset_index()
    
    fig_gender = px.pie(
        values=[gender_participation['Women_Participation'].mean(), 
                1 - gender_participation['Women_Participation'].mean()],
        names=['Women', 'Men'],
        title="Gender Participation in Vegetable Value Chain"
    )
    fig_gender.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_gender, use_container_width=True)

# Interactive Map
st.header("🗺️ Geographic Distribution of AVDP Activities")

# Create a map centered on Sierra Leone
map_center = [8.4606, -11.7799]  # Sierra Leone coordinates
m = folium.Map(location=map_center, zoom_start=8)

# Add markers for each district
district_coords = {
    'Western Area': [8.4606, -11.7799],
    'Bo': [7.9644, -11.7383],
    'Kenema': [7.8767, -11.1896],
    'Kailahun': [8.2814, -10.7307],
    'Kono': [8.8786, -10.9719],
    'Bombali': [9.2364, -12.1344],
    'Tonkolili': [8.7336, -11.6924],
    'Port Loko': [8.7658, -12.7876]
}

for district in selected_districts:
    if district in district_coords:
        district_data = filtered_ivs[filtered_ivs['District'] == district]
        total_farmers = district_data['Farmers_Count'].sum()
        total_hectares = district_data['Hectares_Developed'].sum()
        
        folium.Marker(
            district_coords[district],
            popup=f"""
            <b>{district}</b><br>
            Farmers: {total_farmers:,}<br>
            Hectares: {total_hectares:,}<br>
            CSA Adoption: {district_data['CSA_Adoption_Rate'].mean():.1%}
            """,
            icon=folium.Icon(color='green', icon='leaf')
        ).add_to(m)

map_data = st_folium(m, width=700, height=500)

# Sustainability Scorecard
st.header("🌱 CSA Practice Sustainability Scorecard")

# Create radar chart for sustainability scores
fig_radar = go.Figure()

categories = ['Climate Resilience', 'Scalability', 'Cost Effectiveness', 'Farmer Adoption']

for practice in sustainability_df['Practice'].head(5):  # Show top 5 practices
    practice_data = sustainability_df[sustainability_df['Practice'] == practice]
    values = [
        practice_data['Climate_Resilience'].iloc[0],
        practice_data['Scalability'].iloc[0],
        practice_data['Cost_Effectiveness'].iloc[0],
        practice_data['Farmer_Adoption'].iloc[0]
    ]
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=practice
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        )),
    showlegend=True,
    title="CSA Practice Sustainability Assessment"
)

st.plotly_chart(fig_radar, use_container_width=True)

# Success Stories Gallery
st.header("📸 Success Stories Gallery")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🌾 Rice Transformation in Bo District**
    
    Before: Traditional farming yielded 2.5 tons/hectare
    After: CSA practices increased yield to 5.2 tons/hectare
    
    *"The raised beds saved my crops during the flooding season"*
    """)

with col2:
    st.markdown("""
    **🌴 Cocoa Revival in Kenema**
    
    Improved seedlings showed 87% survival rate
    Farmers report 45% income increase in Year 2
    
    *"My children can now go to school thanks to better cocoa yields"*
    """)

with col3:
    st.markdown("""
    **🥕 Women's Vegetable Cooperative**
    
    25 women farmers using drip irrigation
    300% increase in off-season production
    
    *"We now supply vegetables year-round to the local market"*
    """)

# Data Download Section
st.header("📥 Data Export")

col1, col2, col3 = st.columns(3)

with col1:
    csv_ivs = filtered_ivs.to_csv(index=False)
    st.download_button(
        label="Download IVS Rice Data",
        data=csv_ivs,
        file_name=f"ivs_rice_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    csv_tree = filtered_tree.to_csv(index=False)
    st.download_button(
        label="Download Tree Crops Data",
        data=csv_tree,
        file_name=f"tree_crops_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col3:
    csv_veg = filtered_veg.to_csv(index=False)
    st.download_button(
        label="Download Vegetable Data",
        data=csv_veg,
        file_name=f"vegetable_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>AVDP Climate-Smart Agriculture Dashboard | Last Updated: {}</p>
    <p>For technical support, contact the AVDP Data Team</p>
</div>
""".format(datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)
