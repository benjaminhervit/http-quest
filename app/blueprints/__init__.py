from .api import bp as api_bp
from .dashboard import bp as dashboard_bp
from .main import bp as main_bp
from .quest_render import bp as quest_renderer_bp
from .quests import bp as quests_bp
from .quests.auth import bp as auth_bp
from .css_demo import bp as css_demo_bp
from .leaderboard import bp as leaderboard_bp


def get_all_blueprints():
    return [api_bp, dashboard_bp, main_bp, quest_renderer_bp, quests_bp, auth_bp, css_demo_bp, leaderboard_bp]
