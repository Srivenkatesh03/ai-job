import os
import yaml
from typing import Any, Dict, Optional


class PromptManager:
    """Manages centralized loading, caching, and rendering of YAML prompt templates."""

    def __init__(self, filepath: Optional[str] = None):
        if filepath is None:
            # Resolve default filepath to app/ai/prompts.yaml
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(base_dir, "prompts.yaml")
        
        self.filepath = filepath
        self._templates: Dict[str, Dict[str, str]] = {}
        self.load_templates()

    def load_templates(self) -> None:
        """Load and parse prompt templates from the YAML file."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                f"Prompt templates registry file not found at: '{self.filepath}'"
            )
        
        with open(self.filepath, "r", encoding="utf-8") as f:
            try:
                self._templates = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise RuntimeError(
                    f"Error parsing prompt templates YAML file: {e}"
                ) from e

    def get_template(self, category: str, template_type: str = "user") -> str:
        """Retrieve a raw prompt template from cache by category and type (system/user).
        
        Raises:
            KeyError: If the category or type is missing from templates.
        """
        category_data = self._templates.get(category)
        if not category_data:
            raise KeyError(
                f"Prompt category '{category}' not found in registry. Options: {list(self._templates.keys())}"
            )
            
        template = category_data.get(template_type)
        if not template:
            raise KeyError(
                f"Template type '{template_type}' not found under category '{category}'."
            )
            
        return template.strip()

    def render_prompt(self, category: str, template_type: str = "user", **kwargs: Any) -> str:
        """Fetch the template and format it dynamically with key-value variables."""
        template = self.get_template(category, template_type)
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(
                f"Missing prompt interpolation variable: {e} required for category '{category}' type '{template_type}'."
            ) from e


# Global singleton instance
prompt_manager = PromptManager()
