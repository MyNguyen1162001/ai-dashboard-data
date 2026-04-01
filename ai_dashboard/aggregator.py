"""
Data aggregation module for preparing chart and KPI data.
"""
import pandas as pd
from typing import Dict, List, Any, Tuple


class DataAggregator:
    """Aggregates data based on LLM schema analysis decisions."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.aggregated_results = {}

    def process_kpis(self, kpi_columns: List[str]) -> Dict[str, float]:
        """Calculate KPI values (sum, mean, count for each metric)."""
        kpi_data = {}

        for col in kpi_columns:
            if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col]):
                kpi_data[f"{col}_sum"] = float(self.df[col].sum())
                kpi_data[f"{col}_mean"] = float(self.df[col].mean())
                kpi_data[f"{col}_count"] = int(self.df[col].count())

        self.aggregated_results["kpis"] = kpi_data
        return kpi_data

    def prepare_chart_data(self, chart_config: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Prepare aggregated data for a specific chart."""
        x_col = chart_config.get("x")
        y_col = chart_config.get("y")
        agg_func = chart_config.get("agg", "sum")

        if x_col not in self.df.columns or y_col not in self.df.columns:
            return pd.DataFrame(), {}

        # For line and scatter charts, try to preserve temporal/sequential order
        if chart_config.get("type") in ["scatter", "line"]:
            # Try to convert to datetime if not already
            x_data = self.df[x_col]
            if not pd.api.types.is_datetime64_any_dtype(x_data):
                try:
                    x_data = pd.to_datetime(x_data, errors="coerce")
                except:
                    pass
            
            # If we have datetime data, preserve chronological order without aggregation
            if pd.api.types.is_datetime64_any_dtype(x_data):
                data = self.df[[x_col, y_col]].copy()
                data[x_col] = x_data
                data = data.sort_values(by=x_col).dropna()
                return data, {"type": chart_config.get("type")}

        # Aggregate for other chart types and non-temporal x columns
        aggregated = self.df.groupby(x_col)[y_col].agg(agg_func).reset_index()
        
        # For line/scatter charts, sort by x-value; for others, sort by y-value descending
        if chart_config.get("type") in ["scatter", "line"]:
            aggregated = aggregated.sort_values(by=x_col)
        else:
            aggregated = aggregated.sort_values(by=y_col, ascending=False).head(20)  # Limit to top 20

        return aggregated, {
            "type": chart_config.get("type"),
            "x_label": x_col,
            "y_label": f"{y_col} ({agg_func})",
            "agg_function": agg_func
        }

    def prepare_all_charts(self, charts_config: List[Dict[str, Any]]) -> Dict[int, Tuple[pd.DataFrame, Dict]]:
        """Prepare data for all charts specified in config."""
        chart_data = {}
        for idx, chart_config in enumerate(charts_config):
            data, metadata = self.prepare_chart_data(chart_config)
            chart_data[idx] = (data, metadata)

        self.aggregated_results["charts"] = chart_data
        return chart_data

    def get_summary_string(self) -> str:
        """Generate text summary of aggregated data for LLM narrative generation."""
        summary = "Aggregated Data Summary:\n\n"

        # KPI Summary
        if "kpis" in self.aggregated_results:
            summary += "Key Performance Indicators:\n"
            for key, value in self.aggregated_results["kpis"].items():
                if isinstance(value, float):
                    summary += f"- {key}: {value:,.2f}\n"
                else:
                    summary += f"- {key}: {value}\n"
            summary += "\n"

        # Chart Summary
        if "charts" in self.aggregated_results:
            summary += "Chart Data:\n"
            for idx, (data, metadata) in self.aggregated_results["charts"].items():
                if not data.empty:
                    summary += f"\nChart {idx + 1} ({metadata.get('type', 'unknown')}):\n"
                    summary += f"  {metadata}\n"
                    summary += f"  Top rows:\n{data.head(3).to_string()}\n"

        return summary
