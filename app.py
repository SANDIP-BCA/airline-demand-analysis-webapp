"""
My First Data Analysis Web App!
==============================

Hi! I'm a fresher Python developer and this is my airline booking analysis project.
I built this for my internship applications to show what I've learned so far.

What I used to build this:
- Streamlit (for making the web app - it's so cool!)
- Pandas (for working with data - still learning but getting better!)
- Plotly (for making pretty charts)
- Python basics that I learned in college and online courses

This was challenging but fun to build! I learned a lot about:
- How to load and clean data
- Making interactive charts (plotly is amazing!)
- Building web apps with Streamlit
- Writing functions and organizing code

I'm still learning and there's probably better ways to do some things,
but I'm proud of what I built and excited to learn more!
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

@st.cache_data  # This is a cool Streamlit feature I learned about!
def load_data():
    """
    This function loads the airline data from CSV file.
    I used the @st.cache_data decorator because I read it makes the app faster.
    It prevents reloading the data every time someone uses a filter.
    """
    try:
        # Read the CSV file - I put all my data in airline_data.csv
        df = pd.read_csv('airline_data.csv')
        
        # I had to convert the dates from text to actual date format
        # This took me a while to figure out but pd.to_datetime() works great!
        df['booking_date'] = pd.to_datetime(df['booking_date'])
        df['departure_date'] = pd.to_datetime(df['departure_date'])
        
        # I created some new columns to make analysis easier
        # The route column combines origin and destination - pretty neat!
        df['route'] = df['origin'] + ' → ' + df['destination']
        df['month'] = df['departure_date'].dt.strftime('%Y-%m')  # For monthly trends
        df['day_of_week'] = df['departure_date'].dt.day_name()  # For demand patterns
        
        return df
    except FileNotFoundError:
        st.error("😅 Oops! Can't find the airline_data.csv file. Make sure it's in the same folder as this app!")
        return pd.DataFrame()  # Return empty dataframe if file not found
    except Exception as e:
        st.error(f"😔 Something went wrong loading the data: {str(e)}")
        return pd.DataFrame()

def get_popular_routes(df, top_n=10):
    """
    This function finds the most popular flight routes.
    I group the data by route and count how many bookings each route has.
    Then I sort them to get the most popular ones first.
    """
    # Group by route and count bookings - I learned this from pandas documentation!
    route_popularity = df.groupby('route').agg({
        'booking_id': 'count',        # Count total bookings
        'price': 'mean',              # Average price for the route
        'passengers': 'sum'           # Total passengers on this route
    }).reset_index()
    
    # Rename columns to make them more readable
    route_popularity.columns = ['Route', 'Total_Bookings', 'Average_Price', 'Total_Passengers']
    
    # Sort by booking count (highest first) - ascending=False means big to small
    route_popularity = route_popularity.sort_values('Total_Bookings', ascending=False)
    
    # Return only the top N routes (default is 10)
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
    This is the main function that runs my whole app!
    I put everything here so it's easy to understand.
    """
    # App title and intro
    st.title("✈️ My Airline Data Analysis Project")
    st.markdown("### Learning Data Science with Real Flight Data!")
    
    # A bit about me and this project
    st.markdown("""
    **Hi there! 👋 I'm a fresher developer looking for internships**
    
    I built this dashboard to show what I've learned about Python and data analysis so far. 
    It's my first real project using Streamlit and I'm pretty excited about how it turned out!
    
    *Please be patient with me - I'm still learning but eager to improve! 😊*
    """)
    
    # What I learned section - keeping it simple and honest
    with st.expander("📚 What I learned building this (click to expand)", expanded=False):
        st.markdown("""
        **This project taught me:**
        - How to work with CSV files and pandas (took me a while to get the hang of it!)
        - Making interactive charts with Plotly (so much cooler than static graphs!)
        - Building web apps with Streamlit (much easier than I thought it would be)
        - Organizing my code into functions (still practicing this!)
        - Handling errors when things go wrong (learned this the hard way 😅)
        
        **What I want to learn next:**
        - More advanced pandas operations
        - Better chart design and colors
        - Working with APIs and databases
        - Machine learning (seems really cool!)
        - How to make my code even cleaner
        """)
    
    st.markdown("---")
    
    # Load the data - fingers crossed it works!
    with st.spinner("Loading my airline data... 🤞"):
        df = load_data()
    
    # Check if data loaded - I had to learn about error handling
    if df.empty:
        st.error("😔 Couldn't load the data! Make sure airline_data.csv is in the right place.")
        st.info("📝 **Note:** I'm still learning about file handling, so please make sure the CSV file is uploaded!")
        return
    
    # Yay! Data loaded successfully
    st.success(f"🎉 Great! I found {len(df):,} airline booking records to analyze!")
    
    # A little note about what I learned
    st.info("💡 **Cool feature:** I used @st.cache_data to make this faster - it only loads the data once!")
    
    # Sidebar for filters - this is where users can play with the data
    st.sidebar.header("🎛️ Try These Filters!")
    st.sidebar.markdown("**Filter the data to see different results:**")
    st.sidebar.markdown("Play around with these - the charts will update automatically! 🚀")
    
    # Origin filter
    origins = ['All'] + sorted(df['origin'].unique().tolist())
    selected_origin = st.sidebar.selectbox(
        "Pick a departure city:",
        origins,
        help="Where do flights start from?"
    )
    
    # Destination filter
    destinations = ['All'] + sorted(df['destination'].unique().tolist())
    selected_destination = st.sidebar.selectbox(
        "Pick a destination city:",
        destinations,
        help="Where do flights go to?"
    )
    
    # Date range filter
    min_date = df['departure_date'].min().date()
    max_date = df['departure_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Pick dates to analyze:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="What time period should I look at?"
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
    
    # Check if we still have data after filtering
    if filtered_df.empty:
        st.warning("😅 Oops! No flights match those filters. Try different cities or dates!")
        return
    
    # Show how many records we're looking at now
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Current Results**")
    st.sidebar.metric("Records Found", f"{len(filtered_df):,}")
    if len(date_range) == 2:
        days_diff = (date_range[1] - date_range[0]).days
        st.sidebar.metric("Days Selected", f"{days_diff} days")
    
    # A little note about how the filtering works
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Pretty cool:** The charts update instantly when you change filters! That's the magic of Streamlit.")
    
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
    
    # Different ways to look at the data - I made tabs to organize everything
    st.markdown("### 📊 Let's Explore the Data!")
    st.markdown("*I organized the analysis into different tabs - click around and see what you find interesting!*")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 Popular Routes", 
        "💰 Price Trends", 
        "📅 Busy Days", 
        "📋 All the Data"
    ])
    
    with tab1:
        st.subheader("🚀 Which Routes Are Most Popular?")
        st.markdown("Let's see which flights people book the most!")
        
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
            
            # Some cool insights I discovered
            st.subheader("🔍 What I Found Interesting:")
            most_popular = popular_routes.iloc[0]
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(
                    f"**#1 Most Popular:** {most_popular['Route']}\n\n"
                    f"**Times Booked:** {most_popular['Total_Bookings']:,}\n\n"
                    f"**Average Cost:** ${most_popular['Average_Price']:.2f}"
                )
            
            with col2:
                st.info(
                    f"**Routes Found:** {len(popular_routes)}\n\n"
                    f"**Total Travelers:** {popular_routes['Total_Passengers'].sum():,}\n\n"
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
        st.markdown("Interactive data exploration demonstrating pandas DataFrame operations:")
        
        # Display filtered dataframe with technical context
        st.markdown("**Current Dataset:** Filtered airline booking records")
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download option with technical note
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"airline_analysis_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Export functionality using pandas to_csv() method"
        )
        
        # Data summary for technical showcase
        st.markdown("---")
        st.markdown("**📊 Dataset Summary Statistics**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Data Shape:** {filtered_df.shape[0]} rows × {filtered_df.shape[1]} columns
            
            **Numerical Columns:**
            - Price range: ${filtered_df['price'].min():.2f} - ${filtered_df['price'].max():.2f}
            - Passengers: {filtered_df['passengers'].sum():,} total
            - Average booking: {filtered_df['passengers'].mean():.1f} passengers
            """)
        
        with col2:
            st.markdown(f"""
            **Categorical Data:**
            - Unique origins: {filtered_df['origin'].nunique()}
            - Unique destinations: {filtered_df['destination'].nunique()}
            - Airlines: {filtered_df['airline'].nunique()}
            - Aircraft types: {filtered_df['aircraft_type'].nunique()}
            """)
    
    # A simple footer message
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 14px;'>
            <p>🛩️ Thanks for checking out my first data analysis project!</p>
            <p>Built by a fresher developer learning Python, Streamlit, and data science 📊</p>
            <p><em>Still learning and always improving! 😊</em></p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
