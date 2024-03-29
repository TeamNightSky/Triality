"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import json
import re
import typing as t
from dataclasses import Field, fields
from datetime import datetime

from ..const import DATETIME_FORMAT


class BaseModel:
    def __post_init__(self):
        for field in fields(self):
            if not field.init:
                continue

            value = getattr(self, field.name)
            if value is None:
                continue
            elif isinstance(value, Model):
                continue

            if isinstance(field.type, type):
                if issubclass(field.type, BaseModel):
                    if isinstance(value, dict):
                        setattr(
                            self, field.name, self._convert_to_model(field.type, value)
                        )
                    else:
                        raise ValueError(
                            f"Json data {value!r} could not be converted to model type {field.type!r}"
                        )
            elif origin := t.get_origin(field.type):
                if origin is list or origin is tuple:
                    self._convert_sequence(field, value)
                elif origin is dict:
                    self._convert_dict(field, value)
                elif origin is t.Union:
                    self._convert_optional(field, value)

    def _convert_to_model(self, model_class: type, value: dict) -> "Model":
        return model_class(**value)

    def _convert_sequence(self, field: Field, value: t.Any) -> None:
        model_class, *_ = t.get_args(field.type)
        if issubclass(model_class, Model):
            setattr(
                self,
                field.name,
                [self._convert_to_model(model_class, item) for item in value],
            )

    def _convert_dict(self, field: Field, value: t.Any) -> None:
        _, model_class, *_ = t.get_args(field.type)
        if issubclass(model_class, Model):
            setattr(
                self,
                field.name,
                {
                    key: self._convert_to_model(model_class, sub_value)
                    for key, sub_value in value.items()
                },
            )

    def _convert_optional(self, field: Field, value: t.Any) -> None:
        model_class, *_ = t.get_args(field.type)
        if isinstance(model_class, type):
            if issubclass(model_class, Model):
                setattr(self, field.name, self._convert_to_model(field.type, value))

    def to_json_string(self) -> str:
        return json.dumps(self, cls=DataclassEncoder)

    def from_json_string(self, data: str) -> "Model":
        return json.loads(data, cls=DataclassDecoder)

    def to_json(self) -> dict:
        return DataclassEncoder().default(self)


class Model(BaseModel):
    pass


class DataclassEncoder(json.JSONEncoder):
    def default(self, model: BaseModel) -> t.Dict[str, t.Any]:
        data = {}
        for field in fields(model):  # type: ignore[attr-defined]
            if field.name.startswith("_"):
                continue
            elif not field.init:
                continue
            try:
                value = self.convert(getattr(model, field.name))
                data[field.name] = value
            except AttributeError:
                pass
        return data

    def convert(self, value: t.Any) -> t.Any:
        if isinstance(value, Model):
            return value.to_json()
        elif isinstance(value, list) or isinstance(value, tuple):
            return [self.convert(item) for item in value]
        elif isinstance(value, dict):
            return {key: self.convert(sub_value) for key, sub_value in value.items()}
        elif isinstance(value, datetime):
            return value.strftime(DATETIME_FORMAT)
        else:
            return value


class DataclassDecoder(json.JSONDecoder):
    decode_hooks: t.Dict[str, t.Callable] = {}

    def decode(self, s):
        result = super().decode(s)
        return self.convert(result)

    @staticmethod
    def decode_hook(pattern: str) -> t.Callable:
        def hook(f: t.Callable) -> t.Callable:
            DataclassDecoder.decode_hooks[pattern] = f
            return f

        return hook

    def convert(self, data: t.Any) -> t.Any:
        if isinstance(data, dict):
            return {key: self.convert(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert(item) for item in data]
        elif isinstance(data, str):
            for pattern, hook in self.decode_hooks.items():
                if re.match(pattern, data):
                    return hook(data)
        return data


@DataclassDecoder.decode_hook(r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d\d\d\d\d\d")
def decode_datetime(value: str):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
