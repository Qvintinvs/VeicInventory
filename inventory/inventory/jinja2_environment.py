"""Custom Jinja2 environment factory for Django."""

from django.urls import reverse
from django.templatetags.static import static as django_static
from jinja2 import Environment


def url_for(endpoint, **kwargs):
    """Flask-compatible url_for for Jinja2 templates.
    
    Maps Flask route names to Django URL names.
    Handles 'static' endpoint specially and common Flask blueprint routes.
    """
    if endpoint == "static":
        filename = kwargs.get("filename", "")
        return django_static(filename)
    
    # Map Flask blueprint.function names to Django URL names
    endpoint_map = {
        "wrf_standard.render_inventory_page": "home",
        "wrf_standard.delete_vehicle_emission": "delete_vehicle_emission",
        "wrf_standard.visualize": "visualize",
        "emission_round.schedule_emission_round": "schedule_emission_round",
    }
    
    django_name = endpoint_map.get(endpoint, endpoint)
    
    # For named URL endpoints, try to reverse them
    try:
        return reverse(django_name, kwargs={k: v for k, v in kwargs.items()})
    except Exception:
        # Fallback: return # if URL not found
        return "#"


def create_jinja2_environment(**options):
    """Factory function to create a Jinja2 environment with custom globals."""
    env = Environment(**options)
    env.globals["url_for"] = url_for
    return env
