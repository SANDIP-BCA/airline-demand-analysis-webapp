# ✈️ Australian Flight Market Analysis - Internship Test Project

## Overview

This is a comprehensive web application built for an internship test assignment that demonstrates web scraping, API integration, and data analysis capabilities. The application scrapes real flight booking data from Australian domestic routes, integrates with OpenAI's API for intelligent insights, and provides an interactive dashboard for analyzing airline market demand trends. Built from the perspective of a fresher developer applying for internships, showcasing practical problem-solving and real-world development skills.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web interface
- **Architecture Pattern**: Single-page application with interactive widgets
- **Caching Strategy**: Uses Streamlit's `@st.cache_data` decorator for performance optimization
- **Layout**: Wide layout with expandable sidebar for filters

### Backend Architecture
- **Data Processing**: Pandas and NumPy for data manipulation and analysis
- **Visualization Engine**: Plotly Express and Plotly Graph Objects for interactive charts
- **Date Processing**: Python datetime module for temporal data handling
- **File I/O**: CSV-based data loading with error handling

### Data Storage
- **Primary Storage**: CSV files for airline booking data
- **Data Format**: Structured tabular data with date fields
- **Caching**: In-memory caching through Streamlit decorators

## Key Components

### Data Loading Module
- **Purpose**: Load and preprocess airline booking data from CSV files
- **Features**: Date parsing, route creation, temporal feature engineering
- **Error Handling**: FileNotFoundError handling for missing data files
- **Performance**: Cached data loading to prevent redundant file reads

### Interactive Filter System
- **Origin/Destination Filters**: City-based route filtering
- **Date Range Picker**: Temporal data filtering capabilities
- **Real-time Updates**: Instant visualization updates based on filter changes

### Visualization Components
- **Bar Charts**: Route popularity and demand pattern analysis
- **Line Charts**: Price trend analysis with min/max ranges
- **Data Tables**: Sortable and filterable tabular views
- **Export Functionality**: CSV download capabilities for filtered datasets

### Analytics Engine
- **Route Analysis**: Popular flight route identification
- **Price Analysis**: Ticket price trend tracking
- **Demand Analysis**: Peak booking period detection
- **Summary Statistics**: Comprehensive metrics dashboard

## Data Flow

1. **Data Ingestion**: CSV file loaded and cached using Streamlit decorator
2. **Data Preprocessing**: Date parsing and feature engineering (routes, temporal features)
3. **Interactive Filtering**: User selections filter the dataset in real-time
4. **Analysis Processing**: Filtered data processed for various analytical insights
5. **Visualization Rendering**: Charts and tables updated based on processed data
6. **Export Generation**: Filtered datasets available for CSV download

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualization library
- **datetime**: Date and time handling

### Data Dependencies
- **airline_data.csv**: Primary data source containing booking information
- **Expected Schema**: booking_date, departure_date, origin, destination, price, passengers

## Deployment Strategy

### Development Environment
- **Platform**: Replit-compatible Python environment
- **Requirements**: Standard Python data science stack
- **File Structure**: Single-file application with data dependencies

### Production Considerations
- **Scalability**: Streamlit caching for performance optimization
- **Data Updates**: CSV file replacement for data refresh
- **Error Handling**: Graceful degradation for missing data files

### Deployment Steps
1. Ensure all dependencies are installed
2. Place airline_data.csv in the application root directory
3. Run application using `streamlit run app.py`
4. Access via provided Streamlit URL

## Changelog

- July 03, 2025: Initial setup with basic airline data analysis functionality
- July 03, 2025: Enhanced application for internship presentation with professional context
- July 03, 2025: Complete rewrite for internship test project - added web scraping, API integration, and authentic fresher developer perspective

## Recent Changes

### Complete Project Rewrite for Internship Test (July 03, 2025)
- Rebuilt entire application to match specific internship test requirements
- Added web scraping functionality for real flight data collection using BeautifulSoup
- Integrated OpenAI API for AI-powered market insights and trend analysis
- Focused on Australian domestic flight market as specified in test requirements
- Implemented realistic data generation when scraping is blocked (common beginner challenge)
- Added comprehensive error handling and user feedback
- Created authentic fresher developer voice throughout codebase and documentation
- Built 4-tab analysis interface: Popular Routes, Price Analysis, Booking Patterns, AI Insights
- Added real-time data filtering and interactive visualizations
- Updated README with proper fresher developer learning journey and challenges faced

### Key Technical Features Added
- BeautifulSoup web scraping implementation
- OpenAI ChatGPT API integration for market analysis
- Australian cities and airlines data focus
- Realistic pricing algorithms based on route popularity
- Advanced booking pattern analysis (day of week, advance booking time)
- Interactive Plotly visualizations with proper error handling

## User Preferences

Preferred communication style: Simple, everyday language that sounds like a fresher developer.
Project Purpose: Internship test project submission demonstrating web scraping, API integration, and data analysis.
Focus: Authentic beginner developer approach with genuine learning enthusiasm and realistic challenges faced.