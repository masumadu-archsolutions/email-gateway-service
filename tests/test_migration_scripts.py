import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory

from config import settings
from tests.base_test_case import BaseTestCase


class TestMigrationScript(BaseTestCase):
    @pytest.mark.model
    def test_migration_scripts_single_head(self, test_app):
        # test script
        config = Config()
        config.set_main_option("script_location", f"{settings.app_root}/migrations")
        script = ScriptDirectory.from_config(config)
        result = script.get_current_head()

        assert isinstance(result, str)
