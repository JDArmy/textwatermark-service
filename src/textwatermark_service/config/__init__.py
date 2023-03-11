"""
Configuration center.
Use https://www.dynaconf.com/
""" ""
import sys
from functools import lru_cache
from pathlib import Path

from dynaconf import Dynaconf  # type: ignore


@lru_cache()
def get_settings():
    """get settings"""
    _base_dir = Path(__file__).parent.parent

    _settings_files = [
        # All config file will merge.
        Path(__file__).parent
        / "settings.yml",  # Load default config.
    ]

    # User configuration. It will be created automatically by the pip installer .
    _external_files = [Path(sys.prefix, "etc", "textwatermarkserv", "settings.yml")]

    return Dynaconf(
        # Set env `TEXTWATERMARK_FOO='bar'`，use `settings.FOO` .
        envvar_prefix="TEXTWATERMARKSERV",
        settings_files=_settings_files,  # load user configuration.
        # environments=True,  # Enable multi-level configuration，
        # eg: default, development, production
        load_dotenv=True,  # Enable load .env
        # env_switcher='TEXTWATERMARK_ENV',
        # If true, can't use `settings.foo`, but can only use `settings.FOO`
        lowercase_read=False,
        includes=_external_files,  # Customs settings.
        base_dir=_base_dir,  # `settings.BASE_DIR`
    )


settings = get_settings()
