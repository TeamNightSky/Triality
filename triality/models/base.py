import json
import re
import typing as t
from dataclasses import Field
from datetime import datetime

from ..const import DATETIME_FORMAT


class Model:
    def __post_init__(self):
        for name, field in self.__dataclass_fields__.items():
            value = getattr(self, name)
            if isinstance(value, Model):
                continue
            if isinstance(field.type, type):
                if issubclass(field.type, Model):
                    if isinstance(value, dict):
                        setattr(self, name, self._convert_to_model(field.type, value))
                    else:
                        raise ValueError(
                            f"Json data {value!r} could not be converted to model type {field.type!r}"
                        )
            elif origin := t.get_origin(field.type):
                if origin is list or origin is tuple:
                    self._convert_sequence(name, field, value)
                elif origin is dict:
                    self._convert_dict(name, field, value)
                elif origin is t.Union:
                    self._convert_optional(name, field, value)

    def _convert_to_model(self, model_class: type, value: dict) -> "Model":
        return model_class(**value)

    def _convert_sequence(self, name: str, field: Field, value: t.Any) -> None:
        model_class, *_ = t.get_args(field.type)
        if issubclass(model_class, Model):
            setattr(
                self,
                name,
                [self._convert_to_model(model_class, item) for item in value],
            )

    def _convert_dict(self, name: str, field: Field, value: t.Any) -> None:
        _, model_class, *_ = t.get_args(field.type)
        if issubclass(model_class, Model):
            setattr(
                self,
                name,
                {
                    key: self._convert_to_model(model_class, sub_value)
                    for key, sub_value in value.items()
                },
            )

    def _convert_optional(self, name: str, field: Field, value: t.Any) -> None:
        model_class, *_ = t.get_args(field.type)
        if issubclass(model_class, Model):
            setattr(self, name, self._convert_to_model(field.type, value))

    def to_json_string(self) -> str:
        return json.dumps(self, cls=DataclassEncoder)

    def from_json_string(self, data: str) -> "Model":
        return json.loads(data, cls=DataclassDecoder)

    def to_json(self) -> dict:
        return DataclassEncoder().default(self)


class DataclassEncoder(json.JSONEncoder):
    def default(self, model: Model) -> t.Dict[str, t.Any]:
        data = {}
        for name in model.__dataclass_fields__:  # type: ignore[attr-defined]
            if not name.startswith("_"):
                if value := self.convert(getattr(model, name, None)):
                    data[name] = value
        return data

    def convert(self, value: t.Any) -> t.Any:
        if isinstance(value, Model):
            return value.to_json_string()
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
