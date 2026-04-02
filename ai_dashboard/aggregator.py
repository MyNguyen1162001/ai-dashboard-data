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

    def process_kpis(self, kpi_columns: List[Any]) -> Dict[str, float]:
        """Calculate KPI values using LLM-specified aggregation per metric.

        Accepts either:
        - List[str]: legacy format, falls back to sum/mean/count
        - List[Dict]: new format with {column, agg} per KPI
        """
        kpi_data = {}

        for item in kpi_columns:
            if isinstance(item, dict):
                col = item.get("column")
                agg = item.get("agg", "sum")
            else:
                col = item
                agg = None  # legacy: compute all three

            if col not in self.df.columns or not pd.api.types.is_numeric_dtype(self.df[col]):
                continue

            if agg:
                if agg == "sum":
                    kpi_data[f"{col}"] = float(self.df[col].sum())
                elif agg == "mean":
                    kpi_data[f"{col}"] = float(self.df[col].mean())
                elif agg == "count":
                    kpi_data[f"{col}"] = int(self.df[col].count())
                elif agg == "max":
                    kpi_data[f"{col}"] = float(self.df[col].max())
                elif agg == "min":
                    kpi_data[f"{col}"] = float(self.df[col].min())
            else:
                # Legacy fallback: emit all three
                kpi_data[f"{col}_sum"] = float(self.df[col].sum())
                kpi_data[f"{col}_mean"] = float(self.df[col].mean())
                kpi_data[f"{col}_count"] = int(self.df[col].count())

        self.aggregated_results["kpis"] = kpi_data
        return kpi_data

    def prepare_chart_data(self, chart_config: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Prepare aggregated data for a specific chart."""
        chart_type = chart_config.get("type")
        x_col = chart_config.get("x")
        y_col = chart_config.get("y")
        agg_func = chart_config.get("agg", "sum")
        title = chart_config.get("title", "")

        # --- table: return raw rows for requested columns ---
        if chart_type == "table":
            columns = chart_config.get("columns")
            if columns:
                valid_cols = [c for c in columns if c in self.df.columns]
            else:
                valid_cols = self.df.columns.tolist()[:8]
            if not valid_cols:
                return pd.DataFrame(), {}
            return self.df[valid_cols].head(25).reset_index(drop=True), {
                "type": "table",
                "title": title
            }

        # --- heatmap: group by two dimensions, aggregate z ---
        if chart_type == "heatmap":
            z_col = chart_config.get("z")
            if x_col not in self.df.columns or y_col not in self.df.columns or z_col not in self.df.columns:
                return pd.DataFrame(), {}
            data = self.df.groupby([x_col, y_col])[z_col].agg(agg_func).reset_index()
            data.columns = [x_col, y_col, z_col]
            return data, {
                "type": "heatmap",
                "x_label": x_col,
                "y_label": y_col,
                "z_label": z_col,
                "title": title
            }

        # --- combo: group by x, aggregate both y and y2 ---
        if chart_type == "combo":
            y2_col = chart_config.get("y2")
            if x_col not in self.df.columns or y_col not in self.df.columns:
                return pd.DataFrame(), {}
            if y2_col and y2_col in self.df.columns:
                data = self.df.groupby(x_col).agg({y_col: agg_func, y2_col: agg_func}).reset_index()
                data = data.sort_values(by=x_col)
                return data, {
                    "type": "combo",
                    "x_label": x_col,
                    "y_label": y_col,
                    "y2_label": y2_col,
                    "title": title
                }
            # y2 missing — fall through to bar
            chart_type = "bar"

        if x_col not in self.df.columns or y_col not in self.df.columns:
            return pd.DataFrame(), {}

        # For line and scatter charts, try to preserve temporal/sequential order
        if chart_type in ["scatter", "line"]:
            x_data = self.df[x_col]
            # Only attempt datetime conversion for string/object columns — never numeric
            if not pd.api.types.is_datetime64_any_dtype(x_data) and \
               (pd.api.types.is_object_dtype(x_data) or pd.api.types.is_string_dtype(x_data)):
                try:
                    x_data = pd.to_datetime(x_data, errors="coerce")
                except:
                    pass

            # If we have datetime data with valid values, preserve chronological order
            if pd.api.types.is_datetime64_any_dtype(x_data) and x_data.notna().any():
                data = self.df[[x_col, y_col]].copy()
                data[x_col] = x_data
                data = data.sort_values(by=x_col).dropna()
                return data, {"type": chart_type, "title": title}

        # Aggregate for other chart types and non-temporal x columns
        aggregated = self.df.groupby(x_col)[y_col].agg(agg_func).reset_index()

        # For line/scatter charts, sort by x-value; for others, sort by y-value descending
        if chart_type in ["scatter", "line"]:
            aggregated = aggregated.sort_values(by=x_col)
        else:
            aggregated = aggregated.sort_values(by=y_col, ascending=False).head(20)  # Limit to top 20

        return aggregated, {
            "type": chart_type,
            "x_label": x_col,
            "y_label": f"{y_col} ({agg_func})",
            "agg_function": agg_func,
            "title": title
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
