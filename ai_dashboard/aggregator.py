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
        VALID_AGGS = {"sum", "mean", "count", "max", "min", "median"}
        agg_func = chart_config.get("agg", "sum")
        if not agg_func or agg_func not in VALID_AGGS:
            agg_func = "mean"
        title = chart_config.get("title", "")

        # Guard: non-numeric y columns can only use "count"
        if y_col and y_col in self.df.columns and not pd.api.types.is_numeric_dtype(self.df[y_col]):
            agg_func = "count"

        # --- table: return aggregated, sorted data ---
        if chart_type == "table":
            columns = chart_config.get("columns")
            group_by = chart_config.get("group_by")
            sort_by = chart_config.get("sort_by")

            if columns:
                valid_cols = [c for c in columns if c in self.df.columns]
            else:
                valid_cols = self.df.columns.tolist()[:8]
            if not valid_cols:
                return pd.DataFrame(), {}

            subset = self.df[valid_cols]

            # Aggregate if group_by is specified
            if group_by:
                valid_group = [c for c in group_by if c in subset.columns]
                if valid_group:
                    # Separate categorical (group) cols from numeric cols
                    numeric_cols = [c for c in valid_cols if c not in valid_group and pd.api.types.is_numeric_dtype(subset[c])]
                    if numeric_cols:
                        safe_agg = agg_func if agg_func == "count" else agg_func
                        agg_dict = {c: safe_agg for c in numeric_cols}
                        try:
                            subset = subset.groupby(valid_group, as_index=False).agg(agg_dict)
                        except TypeError:
                            subset = subset.groupby(valid_group, as_index=False).agg({c: "count" for c in numeric_cols})
                    else:
                        subset = subset.drop_duplicates(subset=valid_group)

            # Sort by sort_by column descending, or by first numeric column
            if sort_by and sort_by in subset.columns:
                subset = subset.sort_values(by=sort_by, ascending=False)
            else:
                # Fallback: sort by first numeric column descending
                num_cols = subset.select_dtypes(include="number").columns
                if len(num_cols) > 0:
                    subset = subset.sort_values(by=num_cols[0], ascending=False)

            return subset.head(25).reset_index(drop=True), {
                "type": "table",
                "title": title
            }

        # --- box: pass raw data (no aggregation) so plotly can compute quartiles ---
        if chart_type == "box":
            if x_col not in self.df.columns or y_col not in self.df.columns:
                return pd.DataFrame(), {}
            data = self.df[[x_col, y_col]].dropna()
            return data, {
                "type": "box",
                "x_label": x_col,
                "y_label": y_col,
                "title": title
            }

        # --- heatmap: group by two dimensions, aggregate z ---
        if chart_type == "heatmap":
            z_col = chart_config.get("z")
            if x_col not in self.df.columns or y_col not in self.df.columns or z_col not in self.df.columns:
                return pd.DataFrame(), {}
            is_numeric_z = pd.api.types.is_numeric_dtype(self.df[z_col])
            if is_numeric_z and agg_func == "count":
                z_agg = "sum"
            elif is_numeric_z:
                z_agg = agg_func
            else:
                z_agg = "count"
            data = self.df.groupby([x_col, y_col])[z_col].agg(z_agg).reset_index()
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
                agg_map = {}
                for c in [y_col, y2_col]:
                    agg_map[c] = agg_func if pd.api.types.is_numeric_dtype(self.df[c]) else "count"
                data = self.df.groupby(x_col).agg(agg_map).reset_index()
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

        # Guard against x and y being the same column (causes reset_index conflict)
        if x_col == y_col:
            data = self.df[[x_col]].copy()
            data["count"] = 1
            aggregated = data.groupby(x_col)["count"].sum().reset_index()
            aggregated.columns = [x_col, f"{x_col}_count"]
            return aggregated, {
                "type": chart_type,
                "x_label": x_col,
                "y_label": f"{x_col}_count",
                "title": title
            }

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
        try:
            aggregated = self.df.groupby(x_col)[y_col].agg(agg_func).reset_index()
        except TypeError:
            aggregated = self.df.groupby(x_col)[y_col].agg("count").reset_index()

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
                chart_title = metadata.get("title", "Untitled")
                chart_type = metadata.get("type", "unknown")
                summary += f"\nChart {idx + 1} — \"{chart_title}\" ({chart_type}):\n"
                if not data.empty:
                    summary += f"  Columns: {', '.join(data.columns.tolist())}\n"
                    summary += f"  Rows: {len(data)}\n"
                    summary += f"  Sample data:\n{data.head(5).to_string()}\n"
                else:
                    summary += "  No data available.\n"

        return summary
