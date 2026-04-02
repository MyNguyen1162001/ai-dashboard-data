"""
HTML builder module for assembling the storytelling dashboard using jinja2.
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
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
              overall_summary: str,
              subtitle: str = "",
              headline_kpi: Optional[Dict[str, Any]] = None,
              insight_bullets: Optional[List[Dict[str, str]]] = None,
              kpi_configs: Optional[List[Dict[str, Any]]] = None,
              chart_badges: Optional[List[str]] = None,
              chart_titles: Optional[List[str]] = None) -> str:
        """Assemble complete HTML dashboard with storytelling elements."""
        template = self.env.get_template("dashboard.html")

        # Format KPIs for display with context
        kpi_cards = self._format_kpis(kpis, kpi_configs)

        # Ensure we have insights for all charts
        while len(chart_insights) < len(charts_json):
            chart_insights.append("Chart analysis in progress.")

        context = {
            "title": title,
            "subtitle": subtitle,
            "headline_kpi": headline_kpi,
            "kpi_cards": kpi_cards,
            "insight_bullets": insight_bullets or [],
            "charts": [json.loads(chart_json) for chart_json in charts_json],
            "chart_insights": chart_insights[:len(charts_json)],
            "chart_badges": chart_badges or [],
            "chart_titles": chart_titles or [],
            "overall_summary": overall_summary
        }

        return template.render(context)

    @staticmethod
    def _format_kpis(kpis: Dict[str, float],
                     kpi_configs: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """Format KPI data for display cards with context."""
        kpi_cards = []
        kpi_items = list(kpis.items())[:5]  # Up to 5 KPI cards

        for i, (key, value) in enumerate(kpi_items):
            if isinstance(value, (int, float)):
                formatted_value = format_human_readable(value)
            else:
                formatted_value = str(value)

            # Try to get label and context from kpi_configs
            label = None
            context = None
            unit = None

            if kpi_configs and i < len(kpi_configs):
                cfg = kpi_configs[i]
                label = cfg.get("label")
                context = cfg.get("context")
                # Extract unit suffix from label or context
                suffix = cfg.get("suffix", "")
                if suffix:
                    unit = suffix

            # Fallback label from key
            if not label:
                parts = key.rsplit("_", 1)
                col_name = parts[0] if len(parts) > 1 else key
                metric_type = parts[1].upper() if len(parts) > 1 else ""
                label = f"{col_name}" + (f" ({metric_type})" if metric_type else "")

            kpi_cards.append({
                "label": label,
                "value": formatted_value,
                "context": context,
                "unit": unit
            })

        return kpi_cards
