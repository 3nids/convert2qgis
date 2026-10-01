"""
Generate the bundled JSON Schema from the dataclasses in `type_defs.py`.

Build-time only: it needs `pydantic` from the `dev` dependency group, so runtime code must never import this module.
Regenerate the schema after changing `type_defs.py` with:

    uv run python -m convert2qgis.json2qgis.json_schema
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter
from pydantic.json_schema import GenerateJsonSchema

from convert2qgis.json2qgis.type_defs import ProjectDef

SCHEMA_PATH = Path(__file__).parent.joinpath("schema/schema_20251121.json")


class _GenerateJsonSchema(GenerateJsonSchema):
    def normalize_name(self, name: str) -> str:
        return super().normalize_name(name).removesuffix("Def")

    def field_title_should_be_set(self, schema: Any) -> bool:  # noqa: ARG002
        return False


def _finalize_object_schema(name: str, schema: dict[str, Any]) -> None:
    if "title" in schema:
        schema["title"] = name

    properties = schema.get("properties", {})
    for required_name in schema.get("required", []):
        if required_name not in properties:
            raise ValueError(
                f'"{name}" requires "{required_name}", but has no such property.'
            )

        # a default value is meaningless for a required property
        properties[required_name].pop("default", None)


def build_json_schema() -> dict[str, Any]:
    schema = TypeAdapter(ProjectDef).json_schema(schema_generator=_GenerateJsonSchema)

    _finalize_object_schema("Project", schema)
    for name, definition in schema["$defs"].items():
        _finalize_object_schema(name, definition)

        # e.g. the JSON shapes of `FormItemDef`
        for variant in definition.get("oneOf", []):
            _finalize_object_schema(variant["title"], variant)

    return {"$schema": GenerateJsonSchema.schema_dialect, **schema}


def main() -> None:
    SCHEMA_PATH.write_text(json.dumps(build_json_schema(), indent=2) + "\n")


if __name__ == "__main__":
    main()
