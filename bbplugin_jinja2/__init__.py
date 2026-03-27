import json

from jinja2 import Environment, StrictUndefined


class Jinja2Transformer:
    """Renders a Jinja2 template (the transform ``code``) against JSON input data.

    The JSON input is parsed and exposed to the template as ``data``.
    If the input is a JSON object, its top-level keys are also available
    directly as template variables (so ``{{ name }}`` and ``{{ data.name }}``
    are equivalent).

    On success, returns the rendered string.
    On failure, raises an exception (message becomes the transform stderr output).
    """

    transform_types = ['jinja2']
    default_inputs = ['application/json']
    default_outputs = ['text/plain']

    def transform(self, metadata):
        input_text = (metadata.input_data
                      if isinstance(metadata.input_data, str)
                      else metadata.input_data.decode('utf-8'))
        data = json.loads(input_text)
        env = Environment(undefined=StrictUndefined)
        template = env.from_string(metadata.transform_content)
        context = {'data': data}
        if isinstance(data, dict):
            context.update(data)
        return template.render(**context)