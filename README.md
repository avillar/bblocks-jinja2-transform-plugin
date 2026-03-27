# bblocks-jinja2-transform-plugin

Adds a `jinja2` transform type to the [OGC Building Blocks postprocessor](https://github.com/opengeospatial/bblocks-postprocess-action).

The transform renders a [Jinja2](https://jinja.palletsprojects.com/) template against JSON input data, producing any text-based output (HTML, XML, plain text, etc.).

## Usage

Declare the plugin in `transform-plugins.yml` at the root of your building blocks repository:

```yaml
plugins:
  - pip: git+https://github.com/avillar/bblocks-jinja2-transform-plugin.git
    modules:
      - bbplugin_jinja2
```

Then declare a `jinja2` transform in your `transforms.yaml`:

```yaml
transforms:
  - id: html-summary
    type: jinja2
    inputs:
      mediaTypes: [application/json]
    outputs:
      mediaTypes:
        - mimeType: text/html
          defaultExtension: html
    code: |
      <dl>
      {% for key, value in data.items() %}
        <dt>{{ key }}</dt><dd>{{ value }}</dd>
      {% endfor %}
      </dl>
```

## Template context

The JSON input is parsed and made available in two ways:

- **`data`** — the full parsed value (works for objects, arrays, and primitives)
- **top-level keys** — if the input is a JSON object, its keys are also injected directly as template variables

So given input `{"name": "Alice", "role": "Engineer"}`, both `{{ data.name }}` and `{{ name }}` resolve to `"Alice"`.

Undefined variables raise an error (Jinja2 `StrictUndefined`).

## Requirements

- Python ≥ 3.10
- [Jinja2](https://pypi.org/project/Jinja2/) (installed automatically by the postprocessor)