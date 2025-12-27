"""
Demo Client for AI Website
===========================
Lightweight client to showcase real agent capabilities
without running the full minerva stack.

Calls MCPs directly:
- FRED MCP for US economic data
- IMF MCP for international data
"""

import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# MCP Endpoints
FRED_MCP_URL = "https://fred-mcp.urbancanary.workers.dev"
IMF_MCP_URL = "https://imf-mcp.urbancanary.workers.dev"

# Country name to ISO code mapping
COUNTRY_CODES = {
    "france": "FRA", "germany": "DEU", "uk": "GBR", "britain": "GBR",
    "japan": "JPN", "china": "CHN", "india": "IND", "brazil": "BRA",
    "mexico": "MEX", "canada": "CAN", "australia": "AUS", "italy": "ITA",
    "spain": "ESP", "argentina": "ARG", "russia": "RUS", "korea": "KOR",
    "indonesia": "IDN", "turkey": "TUR", "saudi": "SAU", "south africa": "ZAF",
    "nigeria": "NGA", "egypt": "EGY", "poland": "POL", "netherlands": "NLD",
    "belgium": "BEL", "sweden": "SWE", "norway": "NOR", "switzerland": "CHE",
    "austria": "AUT", "greece": "GRC", "portugal": "PRT", "ireland": "IRL",
    "denmark": "DNK", "finland": "FIN", "czech": "CZE", "hungary": "HUN",
    "romania": "ROU", "ukraine": "UKR", "vietnam": "VNM", "thailand": "THA",
    "malaysia": "MYS", "singapore": "SGP", "philippines": "PHL", "pakistan": "PAK",
    "bangladesh": "BGD", "chile": "CHL", "colombia": "COL", "peru": "PER",
    "venezuela": "VEN", "israel": "ISR", "uae": "ARE", "qatar": "QAT",
    "kuwait": "KWT", "kazakhstan": "KAZ", "united states": "USA", "us": "USA",
    "usa": "USA", "america": "USA"
}


def get_imf_data(country_code: str, tool_name: str = "imf_gdp") -> Tuple[Optional[Dict], Dict[str, str]]:
    """Fetch data from IMF MCP.

    Available tools:
    - imf_gdp: Real GDP growth (%)
    - imf_inflation: Inflation rate (%)
    - imf_unemployment: Unemployment rate (%)
    - imf_current_account: Current account balance (% of GDP)

    Returns summary data (not timeseries).
    """
    try:
        response = requests.post(
            f"{IMF_MCP_URL}/mcp/tools/call",
            json={
                "name": tool_name,
                "arguments": {
                    "country": country_code
                }
            },
            timeout=30
        )

        if response.status_code == 200:
            mcp_data = response.json()

            if "error" in mcp_data:
                print(f"IMF MCP error: {mcp_data['error']}")
                return None, {}

            if "content" in mcp_data and len(mcp_data["content"]) > 0:
                import json
                content_text = mcp_data["content"][0]["text"]
                result = json.loads(content_text)

                # IMF returns summary data
                return result, {
                    "title": result.get("title", ""),
                    "country": result.get("country", "")
                }

    except Exception as e:
        print(f"IMF MCP error: {e}")

    return None, {}


def get_fred_data(series_id: str, years: int = 10) -> Tuple[Optional[pd.DataFrame], Dict[str, str]]:
    """Fetch data from FRED MCP."""
    try:
        start_date = f"{datetime.now().year - years}-01-01"

        response = requests.post(
            f"{FRED_MCP_URL}/mcp/tools/call",
            json={
                "name": "fred_series_timeseries",
                "arguments": {
                    "series_id": series_id,
                    "start_date": start_date
                }
            },
            timeout=30
        )

        if response.status_code == 200:
            mcp_data = response.json()

            # Check for error
            if "error" in mcp_data:
                print(f"FRED MCP error: {mcp_data['error']}")
                return None, {}

            # Extract content
            if "content" in mcp_data and len(mcp_data["content"]) > 0:
                import json
                content_text = mcp_data["content"][0]["text"]
                result = json.loads(content_text)

                chart_data = result.get("chart_data", [])
                series_info = {
                    "title": result.get("title", ""),
                    "units": result.get("units", ""),
                    "frequency": result.get("frequency", "")
                }

                if chart_data:
                    df = pd.DataFrame(chart_data)
                    df["date"] = pd.to_datetime(df["date"])
                    df["value"] = pd.to_numeric(df["value"], errors="coerce")
                    df = df.dropna()
                    return df, series_info

    except Exception as e:
        print(f"FRED MCP error: {e}")

    return None, {}


def create_chart(df: pd.DataFrame, title: str, y_label: str = "Value") -> str:
    """Create a plotly chart and return HTML."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["value"],
        mode="lines",
        line=dict(color="#667eea", width=2),
        fill="tozeroy",
        fillcolor="rgba(102, 126, 234, 0.1)"
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#fff")),
        xaxis=dict(
            title="",
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="#888")
        ),
        yaxis=dict(
            title=y_label,
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="#888"),
            titlefont=dict(color="#888")
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=20, t=50, b=30),
        height=350
    )

    return fig.to_html(include_plotlyjs="cdn", full_html=False)


# Common queries and their FRED series
# Format: keyword -> (series_id, title, y_label, transform)
# transform: "level" = raw data, "yoy" = year-over-year % change
QUERY_MAPPINGS = {
    "inflation": ("CPIAUCSL", "US Inflation Rate (YoY)", "Percent", "yoy"),
    "us inflation": ("CPIAUCSL", "US Inflation Rate (YoY)", "Percent", "yoy"),
    "cpi": ("CPIAUCSL", "US Consumer Price Index", "Index", "level"),
    "unemployment": ("UNRATE", "US Unemployment Rate", "Percent", "level"),
    "gdp": ("GDP", "US Gross Domestic Product", "Billions of Dollars", "level"),
    "us gdp": ("GDP", "US Gross Domestic Product", "Billions of Dollars", "level"),
    "fed funds": ("FEDFUNDS", "Federal Funds Rate", "Percent", "level"),
    "interest rate": ("FEDFUNDS", "Federal Funds Rate", "Percent", "level"),
    "10 year": ("DGS10", "10-Year Treasury Rate", "Percent", "level"),
    "treasury": ("DGS10", "10-Year Treasury Rate", "Percent", "level"),
}


def transform_to_yoy(df: pd.DataFrame) -> pd.DataFrame:
    """Transform data to year-over-year percentage change."""
    df = df.copy()
    df = df.sort_values("date")
    df["value"] = df["value"].pct_change(periods=12) * 100  # 12 months for YoY
    df = df.dropna()
    return df


def detect_country(query: str) -> Optional[Tuple[str, str]]:
    """Detect country from query. Returns (country_name, country_code) or None."""
    query_lower = query.lower()
    for name, code in COUNTRY_CODES.items():
        if name in query_lower:
            return (name.title(), code)
    return None


def detect_indicator(query: str) -> Tuple[str, str, str]:
    """Detect what indicator user wants. Returns (tool_name, title, y_label)."""
    query_lower = query.lower()

    if "inflation" in query_lower or "cpi" in query_lower or "price" in query_lower:
        return ("imf_inflation", "Inflation Rate", "Percent")
    elif "unemployment" in query_lower or "jobless" in query_lower:
        return ("imf_unemployment", "Unemployment Rate", "Percent")
    elif "current account" in query_lower or "trade balance" in query_lower:
        return ("imf_current_account", "Current Account Balance", "% of GDP")
    else:
        # Default to GDP growth
        return ("imf_gdp", "Real GDP Growth", "Percent")


def get_demo_response(query: str) -> Tuple[str, Optional[str], str]:
    """
    Get a demo response for a query.

    Returns:
        (text_response, chart_html, agent_name)
    """
    query_lower = query.lower().strip()

    # Detect if query is about a specific country
    country_info = detect_country(query)

    # If non-US country detected, use IMF data
    if country_info and country_info[1] != "USA":
        country_name, country_code = country_info
        tool_name, indicator_title, y_label = detect_indicator(query)

        imf_data, series_info = get_imf_data(country_code, tool_name)

        if imf_data is not None:
            latest_value = imf_data.get("latest_value", 0)
            latest_year = imf_data.get("latest_year", "")
            previous_value = imf_data.get("previous_value", 0)
            previous_year = imf_data.get("previous_year", "")
            change = imf_data.get("change", "0")

            # Determine direction
            try:
                change_val = float(change)
                direction = "up" if change_val > 0 else "down" if change_val < 0 else "unchanged"
                direction_emoji = "📈" if change_val > 0 else "📉" if change_val < 0 else "➡️"
            except:
                direction = "changed"
                direction_emoji = ""

            text = f"""Here's **{country_name}'s {indicator_title}** from IMF:

**{latest_year}:** {latest_value:.1f}%  {direction_emoji}
**{previous_year}:** {previous_value:.1f}%

Year-over-year change: **{change}%**

*Source: IMF World Economic Outlook*"""

            # Create a simple bar chart comparing years
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[str(previous_year), str(latest_year)],
                y=[previous_value, latest_value],
                marker_color=["#667eea", "#764ba2"],
                text=[f"{previous_value:.1f}%", f"{latest_value:.1f}%"],
                textposition="outside"
            ))
            fig.update_layout(
                title=dict(text=f"{country_name} {indicator_title}", font=dict(size=16, color="#fff")),
                xaxis=dict(title="", tickfont=dict(color="#888")),
                yaxis=dict(title=y_label, gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#888")),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=50, r=20, t=50, b=30),
                height=300
            )
            chart_html = fig.to_html(include_plotlyjs="cdn", full_html=False)

            return text, chart_html, "Isla"

        return f"I couldn't retrieve {indicator_title} data for {country_name}. Please try the full Minerva app.", None, "Isla"

    # US data - use FRED
    series_id = None
    default_title = ""
    default_y_label = ""
    transform = "level"

    for keyword, (sid, ttl, ylabel, xform) in QUERY_MAPPINGS.items():
        if keyword in query_lower:
            series_id = sid
            default_title = ttl
            default_y_label = ylabel
            transform = xform
            break

    if series_id:
        # Fetch real data
        df, series_info = get_fred_data(series_id)

        if df is not None and len(df) > 0:
            # Apply transformation if needed
            if transform == "yoy":
                df = transform_to_yoy(df)
                title = default_title  # Use our title for YoY
                y_label = default_y_label
            else:
                title = series_info.get("title") or default_title
                y_label = series_info.get("units") or default_y_label

            if len(df) > 0:
                latest = df.iloc[-1]
                latest_date = latest["date"].strftime("%B %Y")
                latest_value = latest["value"]

                # Format the response based on transform type
                if transform == "yoy":
                    direction = "up" if latest_value > 0 else "down"
                    text = f"""Here's the latest **{title}** data from FRED:

**Current Inflation ({latest_date}):** {latest_value:.1f}%

US inflation is currently running at **{abs(latest_value):.1f}%** year-over-year, based on the Consumer Price Index.

The chart below shows the inflation trend over the past 10 years."""
                else:
                    text = f"""Here's the latest **{title}** data from FRED:

**Latest Reading ({latest_date}):** {latest_value:,.2f} {y_label}

The chart below shows the historical trend over the past 10 years."""

                chart_html = create_chart(df, title, y_label)
                return text, chart_html, "Fred"

        return f"I tried to fetch {default_title} data but couldn't retrieve it. Please try again.", None, "Fred"

    # Default response for unmatched queries
    return """I can help you with US economic data from FRED! Try asking about:

• **Inflation** - Consumer Price Index (CPI)
• **Unemployment** - US unemployment rate
• **GDP** - Gross Domestic Product
• **Fed Funds Rate** - Federal Reserve interest rate
• **Treasury Rates** - 10-year yields

Just ask something like "Show me US inflation" or "What's the unemployment rate?"
""", None, "Grace"


if __name__ == "__main__":
    # Test
    text, chart, agent = get_demo_response("show me us inflation")
    print(f"Agent: {agent}")
    print(f"Text: {text[:200]}...")
    print(f"Chart: {'Yes' if chart else 'No'}")
