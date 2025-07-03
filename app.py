"""
Airline Booking Market Demand Analysis Web App
==============================================

This Streamlit application analyzes airline booking demand data with interactive
filters and visualizations. Built for beginner Python developers.

Author: Fresher Python Developer
Purpose: Job Application Test Task
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Airline Demand Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """
    Load airline booking data from CSV file.
    Uses Streamlit's caching decorator to improve performance.
    
    Returns:
        pd.DataFrame: Loaded airline booking data
    """
    try:
        # Load the CSV file
        df = pd.read_csv('airline_data.csv')
        
        # Convert date columns to datetime
        df['booking_date'] = pd.to_datetime(df['booking_date'])
        df['departure_date'] = pd.to_datetime(df['departure_date'])
        
        # Create additional useful columns for analysis
        df['route'] = df['origin'] + ' → ' + df['destination']
        df['month'] = df['departure_date'].dt.strftime('%Y-%m')
        df['day_of_week'] = df['departure_date'].dt.day_name()
        
        return df
    except FileNotFoundError:
        st.error("❌ airline_data.csv file not found. Please ensure the data file is in the same directory as this app.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()

def get_popular_routes(df, top_n=10):
    """
    Analyze and return the most popular flight routes by booking count.
    
    Args:
        df (pd.DataFrame): Airline booking data
        top_n (int): Number of top routes to return
        
    Returns:
        pd.DataFrame: Top routes with booking counts
    """
    route_popularity = df.groupby('route').agg({
        'booking_id': 'count',
        'price': 'mean',
        'passengers': 'sum'
    }).reset_index()
    
    route_popularity.columns = ['Route', 'Total_Bookings', 'Average_Price', 'Total_Passengers']
    route_popularity = route_popularity.sort_values('Total_Bookings', ascending=False)
    
    return route_popularity.head(top_n)

def analyze_price_trends(df):
    """
    Analyze price trends over time by month.
    
    Args:
        df (pd.DataFrame): Airline booking data
        
    Returns:
        pd.DataFrame: Monthly price trends
    """
    monthly_trends = df.groupby('month').agg({
        'price': ['mean', 'min', 'max'],
        'booking_id': 'count'
    }).reset_index()
    
    # Flatten column names
    monthly_trends.columns = ['Month', 'Average_Price', 'Min_Price', 'Max_Price', 'Booking_Count']
    monthly_trends = monthly_trends.sort_values('Month')
    
    return monthly_trends

def identify_high_demand_periods(df):
    """
    Identify high-demand periods based on booking frequency and passenger count.
    
    Args:
        df (pd.DataFrame): Airline booking data
        
    Returns:
        pd.DataFrame: High-demand periods analysis
    """
    # Analyze by day of week
    dow_demand = df.groupby('day_of_week').agg({
        'booking_id': 'count',
        'passengers': 'sum',
        'price': 'mean'
    }).reset_index()
    
    dow_demand.columns = ['Day_of_Week', 'Total_Bookings', 'Total_Passengers', 'Average_Price']
    
    # Order days properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_demand['Day_of_Week'] = pd.Categorical(dow_demand['Day_of_Week'], categories=day_order, ordered=True)
    dow_demand = dow_demand.sort_values('Day_of_Week')
    
    return dow_demand

def create_route_popularity_chart(route_data):
    """
    Create an interactive bar chart for route popularity.
    
    Args:
        route_data (pd.DataFrame): Route popularity data
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    fig = px.bar(
        route_data,
        x='Total_Bookings',
        y='Route',
        orientation='h',
        title='Most Popular Flight Routes by Booking Count',
        labels={'Total_Bookings': 'Number of Bookings', 'Route': 'Flight Route'},
        color='Total_Bookings',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_price_trend_chart(trend_data):
    """
    Create an interactive line chart for price trends over time.
    
    Args:
        trend_data (pd.DataFrame): Monthly price trend data
        
    Returns:
        plotly.graph_objects.Figure: Line chart figure
    """
    fig = go.Figure()
    
    # Add average price line
    fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Average_Price'],
        mode='lines+markers',
        name='Average Price',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    # Add min/max price area
    fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Max_Price'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Min_Price'],
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(0,100,80,0.2)',
        name='Price Range',
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title='Price Trends Over Time',
        xaxis_title='Month',
        yaxis_title='Price ($)',
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_demand_heatmap(demand_data):
    """
    Create a bar chart showing demand patterns by day of week.
    
    Args:
        demand_data (pd.DataFrame): Day-of-week demand data
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    fig = px.bar(
        demand_data,
        x='Day_of_Week',
        y='Total_Bookings',
        title='Booking Demand by Day of Week',
        labels={'Total_Bookings': 'Total Bookings', 'Day_of_Week': 'Day of Week'},
        color='Total_Bookings',
        color_continuous_scale='reds'
    )
    
    fig.update_layout(height=400)
    
    return fig

def main():
    """
    Main function that runs the Streamlit application.
    """
    # App header
    st.title("✈️ Airline Booking Market Demand Analysis")
    st.markdown("### Interactive Dashboard for Flight Booking Data Analysis")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading airline booking data..."):
        df = load_data()
    
    # Check if data loaded successfully
    if df.empty:
        st.warning("⚠️ No data available. Please check your data file.")
        return
    
    # Display data overview
    st.success(f"✅ Data loaded successfully! Total records: {len(df):,}")
    
    # Sidebar filters
    st.sidebar.header("🎛️ Filter Options")
    st.sidebar.markdown("Use these filters to customize your analysis:")
    
    # Origin filter
    origins = ['All'] + sorted(df['origin'].unique().tolist())
    selected_origin = st.sidebar.selectbox(
        "Select Origin City:",
        origins,
        help="Choose departure city or 'All' for all origins"
    )
    
    # Destination filter
    destinations = ['All'] + sorted(df['destination'].unique().tolist())
    selected_destination = st.sidebar.selectbox(
        "Select Destination City:",
        destinations,
        help="Choose arrival city or 'All' for all destinations"
    )
    
    # Date range filter
    min_date = df['departure_date'].min().date()
    max_date = df['departure_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Choose the date range for analysis"
    )
    
    # Apply filters to data
    filtered_df = df.copy()
    
    if selected_origin != 'All':
        filtered_df = filtered_df[filtered_df['origin'] == selected_origin]
    
    if selected_destination != 'All':
        filtered_df = filtered_df[filtered_df['destination'] == selected_destination]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['departure_date'].dt.date >= start_date) &
            (filtered_df['departure_date'].dt.date <= end_date)
        ]
    
    # Check if filtered data is empty
    if filtered_df.empty:
        st.warning("⚠️ No data matches your filter criteria. Please adjust your filters.")
        return
    
    # Display filtered data summary
    st.sidebar.markdown("---")
    st.sidebar.metric("Filtered Records", f"{len(filtered_df):,}")
    st.sidebar.metric("Date Range", f"{len(date_range)} days" if len(date_range) == 2 else "Select range")
    
    # Main analysis sections
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Bookings",
            f"{len(filtered_df):,}",
            help="Total number of flight bookings in filtered data"
        )
    
    with col2:
        st.metric(
            "Total Passengers",
            f"{filtered_df['passengers'].sum():,}",
            help="Total number of passengers across all bookings"
        )
    
    with col3:
        st.metric(
            "Average Price",
            f"${filtered_df['price'].mean():.2f}",
            help="Average ticket price in filtered data"
        )
    
    with col4:
        st.metric(
            "Unique Routes",
            f"{filtered_df['route'].nunique():,}",
            help="Number of unique flight routes"
        )
    
    st.markdown("---")
    
    # Analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Popular Routes", 
        "📈 Price Trends", 
        "🔥 High Demand Periods", 
        "📋 Raw Data"
    ])
    
    with tab1:
        st.subheader("Most Popular Flight Routes")
        st.markdown("Analysis of the most frequently booked flight routes:")
        
        # Get popular routes
        popular_routes = get_popular_routes(filtered_df)
        
        if not popular_routes.empty:
            # Display chart
            route_chart = create_route_popularity_chart(popular_routes)
            st.plotly_chart(route_chart, use_container_width=True)
            
            # Display table
            st.subheader("📋 Popular Routes Data Table")
            st.dataframe(
                popular_routes,
                use_container_width=True,
                hide_index=True
            )
            
            # Additional insights
            st.subheader("🔍 Key Insights")
            most_popular = popular_routes.iloc[0]
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(
                    f"**Most Popular Route:** {most_popular['Route']}\n\n"
                    f"**Total Bookings:** {most_popular['Total_Bookings']:,}\n\n"
                    f"**Average Price:** ${most_popular['Average_Price']:.2f}"
                )
            
            with col2:
                st.info(
                    f"**Total Routes Analyzed:** {len(popular_routes)}\n\n"
                    f"**Total Passengers:** {popular_routes['Total_Passengers'].sum():,}\n\n"
                    f"**Price Range:** ${popular_routes['Average_Price'].min():.2f} - ${popular_routes['Average_Price'].max():.2f}"
                )
        else:
            st.warning("No route data available for the selected filters.")
    
    with tab2:
        st.subheader("Price Trends Over Time")
        st.markdown("Analysis of how ticket prices change over different time periods:")
        
        # Get price trends
        price_trends = analyze_price_trends(filtered_df)
        
        if not price_trends.empty:
            # Display chart
            price_chart = create_price_trend_chart(price_trends)
            st.plotly_chart(price_chart, use_container_width=True)
            
            # Display table
            st.subheader("📋 Monthly Price Trends Data")
            st.dataframe(
                price_trends,
                use_container_width=True,
                hide_index=True
            )
            
            # Price insights
            st.subheader("💰 Price Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                highest_month = price_trends.loc[price_trends['Average_Price'].idxmax()]
                st.success(
                    f"**Highest Average Price Month:** {highest_month['Month']}\n\n"
                    f"**Average Price:** ${highest_month['Average_Price']:.2f}\n\n"
                    f"**Bookings That Month:** {highest_month['Booking_Count']:,}"
                )
            
            with col2:
                lowest_month = price_trends.loc[price_trends['Average_Price'].idxmin()]
                st.success(
                    f"**Lowest Average Price Month:** {lowest_month['Month']}\n\n"
                    f"**Average Price:** ${lowest_month['Average_Price']:.2f}\n\n"
                    f"**Bookings That Month:** {lowest_month['Booking_Count']:,}"
                )
        else:
            st.warning("No price trend data available for the selected filters.")
    
    with tab3:
        st.subheader("High Demand Periods Analysis")
        st.markdown("Identification of peak booking periods and demand patterns:")
        
        # Get demand analysis
        demand_analysis = identify_high_demand_periods(filtered_df)
        
        if not demand_analysis.empty:
            # Display chart
            demand_chart = create_demand_heatmap(demand_analysis)
            st.plotly_chart(demand_chart, use_container_width=True)
            
            # Display table
            st.subheader("📋 Demand by Day of Week")
            st.dataframe(
                demand_analysis,
                use_container_width=True,
                hide_index=True
            )
            
            # Demand insights
            st.subheader("📅 Demand Pattern Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                peak_day = demand_analysis.loc[demand_analysis['Total_Bookings'].idxmax()]
                st.error(
                    f"**Peak Demand Day:** {peak_day['Day_of_Week']}\n\n"
                    f"**Total Bookings:** {peak_day['Total_Bookings']:,}\n\n"
                    f"**Average Price:** ${peak_day['Average_Price']:.2f}"
                )
            
            with col2:
                low_day = demand_analysis.loc[demand_analysis['Total_Bookings'].idxmin()]
                st.info(
                    f"**Lowest Demand Day:** {low_day['Day_of_Week']}\n\n"
                    f"**Total Bookings:** {low_day['Total_Bookings']:,}\n\n"
                    f"**Average Price:** ${low_day['Average_Price']:.2f}"
                )
        else:
            st.warning("No demand pattern data available for the selected filters.")
    
    with tab4:
        st.subheader("📋 Raw Data Explorer")
        st.markdown("Explore the filtered dataset in detail:")
        
        # Display filtered dataframe
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download option
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"airline_analysis_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download the current filtered dataset as a CSV file"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ using Streamlit • Data Analysis for Airline Booking Market</p>
            <p>This application demonstrates data analysis skills for job application purposes</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
