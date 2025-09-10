from alex_red_teaming.config import Config
from alex_red_teaming.agents import RedTeamingAgent
from alex_red_teaming.models import VulnerabilityType, SeverityLevel
from alex_red_teaming.utils import setup_logging

__version__ = "1.0.0"
__author__ = "Red-Teaming Agent"

# Export main classes and functions
__all__ = [
    "Config",
    "RedTeamingAgent",
    "VulnerabilityType",
    "SeverityLevel",
    "setup_logging",
]
