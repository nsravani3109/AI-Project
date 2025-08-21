"""
Dashboard application for monitoring call metrics and load status
"""
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
from config.settings import settings

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Inbound Sales AI Agent Dashboard"

# API base URL
API_BASE_URL = f"http://localhost:{settings.port}/api"
API_HEADERS = {"X-API-Key": settings.api_key}


def fetch_call_metrics():
    """Fetch call metrics from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/metrics/calls", headers=API_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching call metrics: {e}")
        return None


def fetch_load_metrics():
    """Fetch load metrics from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/metrics/loads", headers=API_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching load metrics: {e}")
        return None


def fetch_recent_calls():
    """Fetch recent calls data"""
    # This would typically fetch from a calls endpoint
    # For now, we'll return mock data
    return [
        {
            "id": 1,
            "carrier": "MC-123456",
            "load_id": "LOAD001",
            "outcome": "accepted",
            "rate": 2500.00,
            "timestamp": "2024-01-15 10:30:00"
        },
        {
            "id": 2,
            "carrier": "MC-789012",
            "load_id": "LOAD002",
            "outcome": "negotiating",
            "rate": 2200.00,
            "timestamp": "2024-01-15 11:15:00"
        }
    ]


# Dashboard layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Inbound Sales AI Agent Dashboard", className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    
    # Metrics Cards Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Calls", className="card-title"),
                    html.H2(id="total-calls", className="text-primary")
                ])
            ])
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Conversion Rate", className="card-title"),
                    html.H2(id="conversion-rate", className="text-success")
                ])
            ])
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Available Loads", className="card-title"),
                    html.H2(id="available-loads", className="text-info")
                ])
            ])
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg. Rate", className="card-title"),
                    html.H2(id="avg-rate", className="text-warning")
                ])
            ])
        ], width=3)
    ], className="mb-4"),
    
    # Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Call Outcomes"),
                dbc.CardBody([
                    dcc.Graph(id="outcome-chart")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sentiment Analysis"),
                dbc.CardBody([
                    dcc.Graph(id="sentiment-chart")
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Load Status Chart
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Load Status Distribution"),
                dbc.CardBody([
                    dcc.Graph(id="load-status-chart")
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # Recent Calls Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Recent Calls"),
                dbc.CardBody([
                    html.Div(id="recent-calls-table")
                ])
            ])
        ], width=12)
    ]),
    
    # Auto-refresh interval
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0
    )
], fluid=True)


# Callbacks for updating dashboard
@app.callback(
    [Output('total-calls', 'children'),
     Output('conversion-rate', 'children'),
     Output('available-loads', 'children'),
     Output('avg-rate', 'children'),
     Output('outcome-chart', 'figure'),
     Output('sentiment-chart', 'figure'),
     Output('load-status-chart', 'figure'),
     Output('recent-calls-table', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    """Update all dashboard components"""
    
    # Fetch metrics
    call_metrics = fetch_call_metrics()
    load_metrics = fetch_load_metrics()
    recent_calls = fetch_recent_calls()
    
    # Default values if API is not available
    if not call_metrics:
        call_metrics = {
            "total_calls": 0,
            "conversion_rate": 0,
            "outcome_distribution": {},
            "sentiment_distribution": {}
        }
    
    if not load_metrics:
        load_metrics = {
            "available_loads": 0,
            "average_rate": 0,
            "total_loads": 0,
            "booked_loads": 0,
            "completed_loads": 0
        }
    
    # Update metric cards
    total_calls = call_metrics["total_calls"]
    conversion_rate = f"{call_metrics['conversion_rate']:.1f}%"
    available_loads = load_metrics["available_loads"]
    avg_rate = f"${load_metrics['average_rate']:,.0f}"
    
    # Create outcome chart
    outcome_data = call_metrics.get("outcome_distribution", {})
    if outcome_data:
        outcome_fig = px.pie(
            values=list(outcome_data.values()),
            names=list(outcome_data.keys()),
            title="Call Outcomes"
        )
    else:
        outcome_fig = go.Figure().add_annotation(text="No data available", showarrow=False)
    
    # Create sentiment chart
    sentiment_data = call_metrics.get("sentiment_distribution", {})
    if sentiment_data:
        sentiment_fig = px.bar(
            x=list(sentiment_data.keys()),
            y=list(sentiment_data.values()),
            title="Carrier Sentiment"
        )
        sentiment_fig.update_layout(showlegend=False)
    else:
        sentiment_fig = go.Figure().add_annotation(text="No data available", showarrow=False)
    
    # Create load status chart
    load_status_data = {
        "Available": load_metrics["available_loads"],
        "Booked": load_metrics["booked_loads"],
        "Completed": load_metrics["completed_loads"]
    }
    
    load_fig = px.bar(
        x=list(load_status_data.keys()),
        y=list(load_status_data.values()),
        title="Load Status Distribution",
        color=list(load_status_data.keys()),
        color_discrete_map={
            "Available": "#17a2b8",
            "Booked": "#ffc107",
            "Completed": "#28a745"
        }
    )
    load_fig.update_layout(showlegend=False)
    
    # Create recent calls table
    if recent_calls:
        calls_df = pd.DataFrame(recent_calls)
        calls_table = dash_table.DataTable(
            data=calls_df.to_dict('records'),
            columns=[
                {"name": "Call ID", "id": "id"},
                {"name": "Carrier", "id": "carrier"},
                {"name": "Load ID", "id": "load_id"},
                {"name": "Outcome", "id": "outcome"},
                {"name": "Rate ($)", "id": "rate", "type": "numeric", "format": {"specifier": ",.0f"}},
                {"name": "Timestamp", "id": "timestamp"}
            ],
            style_cell={'textAlign': 'left'},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{outcome} = accepted'},
                    'backgroundColor': '#d4edda',
                    'color': 'black',
                },
                {
                    'if': {'filter_query': '{outcome} = rejected'},
                    'backgroundColor': '#f8d7da',
                    'color': 'black',
                }
            ]
        )
    else:
        calls_table = html.P("No recent calls available")
    
    return (
        total_calls, conversion_rate, available_loads, avg_rate,
        outcome_fig, sentiment_fig, load_fig, calls_table
    )


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
