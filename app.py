
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px


st.set_page_config(
    page_title="Flight Data Analysis",
    page_icon="✈️",
    layout="wide"
)


def get_flight_data():
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
    airlines = ["Qantas", "Virgin Australia", "Jetstar", "Rex Airlines"]

    flight_data = []

    for i in range(200):  # Generate 200 random flight records
        origin = random.choice(cities)
        destination = random.choice([c for c in cities if c != origin])
        departure_date = datetime.now() + timedelta(days=random.randint(1, 60))
        price = random.randint(100, 500)

        flight_data.append({
            "Flight ID": f"FL{i+1:03d}",
            "Origin": origin,
            "Destination": destination,
            "Departure Date": departure_date.strftime("%Y-%m-%d"),
            "Price": price,
            "Airline": random.choice(airlines)
        })

    return pd.DataFrame(flight_data)

@st.cache_data
def load_data():
    return get_flight_data()


def main():
    st.title("✈️ Flight Booking Market Data Analysis")
    st.markdown("Internship Task by Sandip Prajapati")

    # Load the data
    df = load_data()

    # Sidebar filters
    st.sidebar.header("📊 Filter Flights")

    cities = ['All'] + sorted(df['Origin'].unique().tolist())
    selected_origin = st.sidebar.selectbox("Select Origin City", cities)
    selected_destination = st.sidebar.selectbox("Select Destination City", cities)

    filtered_df = df.copy()

    if selected_origin != 'All':
        filtered_df = filtered_df[filtered_df['Origin'] == selected_origin]

    if selected_destination != 'All':
        filtered_df = filtered_df[filtered_df['Destination'] == selected_destination]


    st.sidebar.write(f"Total Flights: {len(filtered_df)}")

    st.markdown("### 📑 Available Flight Data")
    st.dataframe(filtered_df)

    
    st.subheader("📈 Popular Routes")
    route_counts = filtered_df.groupby(['Origin', 'Destination']).size().reset_index(name='Count')

    if not route_counts.empty:
        fig = px.bar(route_counts, x='Count', y='Destination', color='Origin',
                     orientation='h', title="Most Booked Routes")
        st.plotly_chart(fig)

    st.subheader("💰 Average Price by Airline")
    price_by_airline = filtered_df.groupby('Airline')['Price'].mean().reset_index()

    if not price_by_airline.empty:
        fig2 = px.bar(price_by_airline, x='Airline', y='Price', title="Average Flight Price by Airline")
        st.plotly_chart(fig2)

    st.markdown("---")
    st.markdown("Built by Sandip Prajapati")

if __name__ == "__main__":
    main()
