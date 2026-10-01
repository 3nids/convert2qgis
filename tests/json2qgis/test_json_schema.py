import subprocess
import sys

import pytest

from convert2qgis.json2qgis.utils import get_schema_json


def test_bundled_schema_matches_type_defs() -> None:
    pytest.importorskip("pydantic")

    from convert2qgis.json2qgis.json_schema import build_json_schema  # noqa: PLC0415

    assert get_schema_json() == build_json_schema(), (
        "The bundled JSON schema is outdated, regenerate it with `uv run python -m convert2qgis.json2qgis.json_schema`."
    )


def test_runtime_does_not_import_pydantic() -> None:
    subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys;"
            "import convert2qgis.json2qgis.json2qgis, convert2qgis.xlsform2qgis.xlsform2qgis;"
            "assert 'pydantic' not in sys.modules",
        ],
        check=True,
    )
