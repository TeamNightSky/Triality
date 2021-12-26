import json
import typing as t

# import logging

# logger = logging.getLogger('triality')


class Model:
    def __post_init__(self):
        for name, field in self.__dataclass_fields__.items():
            value = getattr(self, name)
            if issubclass(field.type, Model):
                if isinstance(value, dict):
                    setattr(self, name, self._convert_to_model(field.type, value))
                else:
                    raise ValueError(
                        f"Json data {value!r} could not be converted to model type {field.type!r}"
                    )
            else:
                origin = t.get_origin(field.type)
                if origin is list or origin is tuple:
                    model_class, *_ = t.get_args(field.type)
                    if issubclass(model_class, Model):
                        setattr(
                            self,
                            name,
                            [
                                self._convert_to_model(model_class, item)
                                for item in value
                            ],
                        )
                elif origin is dict:
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

    def _convert_to_model(self, model_class: type, value: dict) -> "Model":
        return model_class(**value)

    def to_json(self) -> str:
        return json.dumps(self, cls=DataclassEncoder)


class DataclassEncoder(json.JSONEncoder):
    def default(self, model: Model) -> t.Dict[str, t.Any]:
        data = {}
        for name in model.__dataclass_fields__():  # type: ignore[attr-defined]
            if not name.startswith("_"):
                if value := self.convert(getattr(model, name, None)):
                    data[name] = value
        return data

    def convert(self, value: t.Any) -> t.Any:
        if isinstance(value, Model):
            return value.to_json()
        elif isinstance(value, list) or isinstance(value, tuple):
            return [self.convert(item) for item in value]
        elif isinstance(value, dict):
            return {key: self.convert(sub_value) for key, sub_value in value.items()}
        else:
            return value
