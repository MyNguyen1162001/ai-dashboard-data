"""
Chart builder module for generating plotly charts.
"""
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Any


class ChartBuilder:
    """Generates interactive plotly charts and exports as JSON specs."""

    @staticmethod
    def build_chart(data: pd.DataFrame, config: Dict[str, Any]) -> str:
        """Build a single chart and return as JSON spec."""
        if data.empty:
            return ChartBuilder._empty_chart_json()

        chart_type = config.get("type", "bar")
        x_col = config.get("x_label") or (data.columns[0] if len(data.columns) > 0 else None)
        y_col = config.get("y_label") or (data.columns[1] if len(data.columns) > 1 else data.columns[0] if len(data.columns) > 0 else None)

        if x_col not in data.columns or y_col not in data.columns:
            x_col = data.columns[0] if len(data.columns) > 0 else None
            y_col = data.columns[1] if len(data.columns) > 1 else data.columns[0] if len(data.columns) > 0 else None

        if chart_type == "bar":
            fig = ChartBuilder._build_bar(data, x_col, y_col)
        elif chart_type == "line":
            fig = ChartBuilder._build_line(data, x_col, y_col)
        elif chart_type == "area":
            fig = ChartBuilder._build_area(data, x_col, y_col)
        elif chart_type == "pie":
            fig = ChartBuilder._build_pie(data, x_col, y_col)
        elif chart_type == "scatter":
            fig = ChartBuilder._build_scatter(data, x_col, y_col)
        elif chart_type == "box":
            fig = ChartBuilder._build_box(data, x_col, y_col)
        elif chart_type == "waterfall":
            fig = ChartBuilder._build_waterfall(data, x_col, y_col)
        else:
            fig = ChartBuilder._build_bar(data, x_col, y_col)

        return fig.to_json()

    @staticmethod
    def _build_bar(data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """Build vertical bar chart (x=categories/dates, y=values)."""
        fig = go.Figure(
            data=[go.Bar(x=data[x_col], y=data[y_col], marker=dict(color="#8B0000"), orientation="v")]
        )
        fig.update_layout(
            title="",
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode="x unified",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_waterfall(data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """Build waterfall chart showing sequential changes between periods."""
        values = data[y_col].tolist()
        measures = ["absolute"] + ["relative"] * (len(values) - 1)
        deltas = [values[0]] + [values[i] - values[i - 1] for i in range(1, len(values))]

        fig = go.Figure(
            data=[go.Waterfall(
                x=data[x_col].tolist(),
                y=deltas,
                measure=measures,
                textposition="outside",
                text=[f"{v:+.0f}" if m == "relative" else f"{v:.0f}" for v, m in zip(deltas, measures)],
                connector=dict(line=dict(color="rgb(63, 63, 63)")),
                increasing=dict(marker=dict(color="#2ca02c")),
                decreasing=dict(marker=dict(color="#d62728")),
                totals=dict(marker=dict(color="#1f77b4")),
            )]
        )
        fig.update_layout(
            title="",
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_line(data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """Build line chart."""
        fig = go.Figure(
            data=[go.Scatter(x=data[x_col], y=data[y_col], mode="lines+markers",
                            line=dict(color="#ff7f0e", width=2), marker=dict(size=6))]
        )
        fig.update_layout(
            title="",
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode="x unified",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_area(data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """Build area chart."""
        fig = go.Figure(
            data=[go.Scatter(x=data[x_col], y=data[y_col], mode="lines+markers",
                            fill="tozeroy", line=dict(color="#2ca02c", width=2),
                            marker=dict(size=6))]
        )
        fig.update_layout(
            title="",
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode="x unified",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_pie(data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """Build pie chart."""
        fig = go.Figure(
            data=[go.Pie(labels=data[x_col], values=data[y_col])]
        )
        fig.update_layout(
            title="",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_scatter(data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """Build scatter plot."""
        fig = go.Figure(
            data=[go.Scatter(x=data[x_col], y=data[y_col], mode="markers",
                            marker=dict(size=8, color="#2ca02c"))]
        )
        fig.update_layout(
            title="",
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode="closest",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_box(data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
        """Build box plot."""
        fig = go.Figure(
            data=[go.Box(x=data[x_col], y=data[y_col], marker=dict(color="#d62728"))]
        )
        fig.update_layout(
            title="",
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _empty_chart_json() -> str:
        """Return empty chart JSON."""
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        fig.update_layout(title="", template="plotly_white", height=400)
        return fig.to_json()
