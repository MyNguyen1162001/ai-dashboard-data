"""
HTML builder module for assembling the final dashboard using jinja2.
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader


def format_human_readable(value: float) -> str:
    """Format large numbers with K/M/B/T suffixes."""
    abs_val = abs(value)
    sign = "-" if value < 0 else ""
    if abs_val >= 1_000_000_000_000:
        return f"{sign}{abs_val / 1_000_000_000_000:.1f}T"
    elif abs_val >= 1_000_000_000:
        return f"{sign}{abs_val / 1_000_000_000:.1f}B"
    elif abs_val >= 1_000_000:
        return f"{sign}{abs_val / 1_000_000:.1f}M"
    elif abs_val >= 10_000:
        return f"{sign}{abs_val / 1_000:.1f}K"
    elif isinstance(value, float):
        return f"{sign}{abs_val:,.2f}"
    else:
        return f"{sign}{abs_val:,}"


class HTMLBuilder:
    """Assembles HTML dashboard using jinja2 templates."""

    def __init__(self, template_dir: str = "templates"):
        """Initialize jinja2 environment."""
        base_dir = Path(__file__).parent
        self.env = Environment(loader=FileSystemLoader(base_dir / template_dir))

    def build(self,
              title: str,
              kpis: Dict[str, float],
              charts_json: List[str],
              chart_insights: List[str],
              overall_summary: str) -> str:
        """Assemble complete HTML dashboard."""
        template = self.env.get_template("dashboard.html")

        # Format KPIs for display
        kpi_cards = self._format_kpis(kpis)

        # Ensure we have insights for all charts
        while len(chart_insights) < len(charts_json):
            chart_insights.append("Chart analysis in progress.")

        context = {
            "title": title,
            "kpi_cards": kpi_cards,
            "charts": [json.loads(chart_json) for chart_json in charts_json],
            "chart_insights": chart_insights[:len(charts_json)],
            "overall_summary": overall_summary
        }

        return template.render(context)

    @staticmethod
    def _format_kpis(kpis: Dict[str, float]) -> List[Dict[str, Any]]:
        """Format KPI data for display cards."""
        kpi_cards = []

        for key, value in list(kpis.items())[:4]:  # Limit to 4 KPI cards
            if isinstance(value, (int, float)):
                formatted_value = format_human_readable(value)
            else:
                formatted_value = str(value)

            # Extract column name and metric type from key
            parts = key.rsplit("_", 1)
            col_name = parts[0] if len(parts) > 1 else key
            metric_type = parts[1].upper() if len(parts) > 1 else "VALUE"

            kpi_cards.append({
                "label": f"{col_name} ({metric_type})",
                "value": formatted_value
            })

        return kpi_cards
