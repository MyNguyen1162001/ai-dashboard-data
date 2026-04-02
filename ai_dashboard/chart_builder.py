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
        title = config.get("title", "")

        # Table has no x/y — handle before column resolution
        if chart_type == "table":
            fig = ChartBuilder._build_table(data, title)
            return fig.to_json()

        x_col = config.get("x_label") or config.get("x") or (data.columns[0] if len(data.columns) > 0 else None)
        y_col = config.get("y_label") or config.get("y") or (data.columns[1] if len(data.columns) > 1 else data.columns[0] if len(data.columns) > 0 else None)

        if x_col not in data.columns or y_col not in data.columns:
            x_col = data.columns[0] if len(data.columns) > 0 else None
            y_col = data.columns[1] if len(data.columns) > 1 else data.columns[0] if len(data.columns) > 0 else None

        if chart_type == "bar":
            fig = ChartBuilder._build_bar(data, x_col, y_col, title)
        elif chart_type == "line":
            fig = ChartBuilder._build_line(data, x_col, y_col, title)
        elif chart_type == "area":
            fig = ChartBuilder._build_area(data, x_col, y_col, title)
        elif chart_type == "pie":
            fig = ChartBuilder._build_pie(data, x_col, y_col, title)
        elif chart_type == "scatter":
            fig = ChartBuilder._build_scatter(data, x_col, y_col, title)
        elif chart_type == "box":
            fig = ChartBuilder._build_box(data, x_col, y_col, title)
        elif chart_type == "waterfall":
            fig = ChartBuilder._build_waterfall(data, x_col, y_col, title)
        elif chart_type == "heatmap":
            z_col = config.get("z_label") or config.get("z") or (data.columns[2] if len(data.columns) > 2 else y_col)
            fig = ChartBuilder._build_heatmap(data, x_col, y_col, z_col, title)
        elif chart_type == "combo":
            y2_col = config.get("y2_label") or config.get("y2") or (data.columns[2] if len(data.columns) > 2 else y_col)
            fig = ChartBuilder._build_combo(data, x_col, y_col, y2_col, title)
        else:
            fig = ChartBuilder._build_bar(data, x_col, y_col, title)

        return fig.to_json()

    @staticmethod
    def _build_bar(data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """Build vertical bar chart (x=categories/dates, y=values)."""
        fig = go.Figure(
            data=[go.Bar(x=data[x_col], y=data[y_col], marker=dict(color="#8B0000"), orientation="v")]
        )
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode="x unified",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_waterfall(data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
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
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_line(data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """Build line chart."""
        fig = go.Figure(
            data=[go.Scatter(x=data[x_col], y=data[y_col], mode="lines+markers",
                            line=dict(color="#ff7f0e", width=2), marker=dict(size=6))]
        )
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode="x unified",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_area(data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """Build area chart."""
        fig = go.Figure(
            data=[go.Scatter(x=data[x_col], y=data[y_col], mode="lines+markers",
                            fill="tozeroy", line=dict(color="#2ca02c", width=2),
                            marker=dict(size=6))]
        )
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode="x unified",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_pie(data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """Build pie chart."""
        fig = go.Figure(
            data=[go.Pie(labels=data[x_col], values=data[y_col])]
        )
        fig.update_layout(
            title=title,
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_scatter(data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """Build scatter plot."""
        fig = go.Figure(
            data=[go.Scatter(x=data[x_col], y=data[y_col], mode="markers",
                            marker=dict(size=8, color="#2ca02c"))]
        )
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode="closest",
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_box(data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
        """Build box plot."""
        fig = go.Figure(
            data=[go.Box(x=data[x_col], y=data[y_col], marker=dict(color="#d62728"))]
        )
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_heatmap(data: pd.DataFrame, x_col: str, y_col: str, z_col: str, title: str = "") -> go.Figure:
        """Build heatmap for 2D categorical breakdown (e.g. region × month)."""
        pivot = data.pivot_table(index=y_col, columns=x_col, values=z_col, aggfunc="sum")
        fig = go.Figure(
            data=go.Heatmap(
                z=pivot.values.tolist(),  # tolist() avoids numpy bdata binary encoding in JSON
                x=pivot.columns.tolist(),
                y=pivot.index.tolist(),
                colorscale="Reds",
                hoverongaps=False,
                hovertemplate=f"{x_col}: %{{x}}<br>{y_col}: %{{y}}<br>{z_col}: %{{z}}<extra></extra>"
            )
        )
        fig.update_layout(
            title=title,
            xaxis_title=x_col,
            yaxis_title=y_col,
            template="plotly_white",
            height=400
        )
        return fig

    @staticmethod
    def _build_table(data: pd.DataFrame, title: str = "") -> go.Figure:
        """Build tabular view showing top rows of aggregated data."""
        fig = go.Figure(
            data=go.Table(
                header=dict(
                    values=list(data.columns),
                    fill_color="#8B0000",
                    font=dict(color="white", size=12),
                    align="left",
                    height=32
                ),
                cells=dict(
                    values=[data[col].tolist() for col in data.columns],
                    fill_color=[["#f9f9f9" if i % 2 == 0 else "white" for i in range(len(data))]],
                    align="left",
                    height=28
                )
            )
        )
        fig.update_layout(
            title=title,
            template="plotly_white",
            height=max(400, 60 + len(data) * 30)
        )
        return fig

    @staticmethod
    def _build_combo(data: pd.DataFrame, x_col: str, y_col: str, y2_col: str, title: str = "") -> go.Figure:
        """Build dual-axis combo chart: bar for primary metric, line for secondary."""
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=data[x_col], y=data[y_col], name=y_col, marker_color="#8B0000", opacity=0.8),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=data[x_col], y=data[y2_col], name=y2_col,
                       mode="lines+markers", line=dict(color="#1f77b4", width=2), marker=dict(size=6)),
            secondary_y=True
        )
        fig.update_layout(
            title=title,
            hovermode="x unified",
            template="plotly_white",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_yaxes(title_text=y_col, secondary_y=False)
        fig.update_yaxes(title_text=y2_col, secondary_y=True)
        fig.update_xaxes(title_text=x_col)
        return fig

    @staticmethod
    def _empty_chart_json() -> str:
        """Return empty chart JSON."""
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        fig.update_layout(title="", template="plotly_white", height=400)
        return fig.to_json()
