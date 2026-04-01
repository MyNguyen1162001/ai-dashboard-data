"""
Schema detection module for analyzing input data structure.
"""
import pandas as pd
import json
from typing import Dict, List, Any


class SchemaDetector:
    """Analyzes data structure and generates schema summary for LLM."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.schema = None

    def detect(self) -> Dict[str, Any]:
        """Detect and return complete schema information."""
        self.schema = {
            "rows": len(self.df),
            "columns": self._analyze_columns(),
            "dimensions": self._identify_dimensions(),
            "metrics": self._identify_metrics(),
            "sample_values": self._get_samples()
        }
        return self.schema

    def _analyze_columns(self) -> List[Dict[str, Any]]:
        """Analyze each column and return metadata."""
        columns = []
        for col in self.df.columns:
            col_data = {
                "name": col,
                "dtype": str(self.df[col].dtype),
                "null_count": int(self.df[col].isna().sum()),
                "null_pct": round(self.df[col].isna().sum() / len(self.df) * 100, 1),
                "unique_count": int(self.df[col].nunique()),
                "cardinality": "high" if self.df[col].nunique() > len(self.df) * 0.5 else (
                    "medium" if self.df[col].nunique() > 10 else "low"
                )
            }

            # Add dtype-specific stats
            if pd.api.types.is_numeric_dtype(self.df[col]):
                col_data["min"] = float(self.df[col].min()) if not self.df[col].isna().all() else None
                col_data["max"] = float(self.df[col].max()) if not self.df[col].isna().all() else None
                col_data["mean"] = float(self.df[col].mean()) if not self.df[col].isna().all() else None
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                col_data["min"] = str(self.df[col].min()) if not self.df[col].isna().all() else None
                col_data["max"] = str(self.df[col].max()) if not self.df[col].isna().all() else None

            columns.append(col_data)
        return columns

    def _identify_dimensions(self) -> List[str]:
        """Identify categorical/dimensional columns."""
        dimensions = []
        threshold = len(self.df) * 0.5

        for col in self.df.columns:
            dtype = self.df[col].dtype
            is_object = pd.api.types.is_object_dtype(self.df[col])
            is_categorical = pd.api.types.is_categorical_dtype(self.df[col])
            is_datetime = pd.api.types.is_datetime64_any_dtype(self.df[col])
            is_string = pd.api.types.is_string_dtype(self.df[col])
            unique_count = self.df[col].nunique()
            passes_cardinality = unique_count < threshold

            is_cat_type = is_object or is_categorical or is_datetime or is_string
            if is_cat_type and passes_cardinality:
                dimensions.append(col)

        return dimensions

    def _identify_metrics(self) -> List[str]:
        """Identify numeric metric columns."""
        return [col for col in self.df.columns if pd.api.types.is_numeric_dtype(self.df[col])]

    def _get_samples(self) -> Dict[str, List[Any]]:
        """Get sample values from each column."""
        samples = {}
        for col in self.df.columns:
            non_null = self.df[col].dropna().unique()[:5]
            samples[col] = [str(v) for v in non_null]
        return samples

    def get_summary_for_llm(self) -> str:
        """Generate a text summary suitable for LLM prompt."""
        if not self.schema:
            self.detect()

        summary = f"Dataset: {self.schema['rows']} rows\n\n"
        summary += "Columns:\n"

        for col_info in self.schema['columns']:
            summary += f"- {col_info['name']} ({col_info['dtype']})\n"
            summary += f"  Cardinality: {col_info['cardinality']}, "
            summary += f"Nulls: {col_info['null_count']}/{self.schema['rows']}\n"

            if 'min' in col_info and col_info['min'] is not None:
                summary += f"  Range: {col_info['min']} to {col_info['max']}\n"

            if col_info['unique_count'] <= 10:
                samples = self.schema['sample_values'].get(col_info['name'], [])
                summary += f"  Values: {', '.join(samples)}\n"

        summary += f"\nDimensions (grouping columns): {', '.join(self.schema['dimensions'])}\n"
        summary += f"Metrics (numeric columns): {', '.join(self.schema['metrics'])}\n"

        return summary
