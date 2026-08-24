# API reference

This guide is itself the "collection of standalone scripts and training docs" that
[21_packaging.md](disseminating/21_packaging.md) says doesn't need a `src/` package — so there is no
`pyproject.toml` to install and no library-wide reference to generate. What autodoc can still document
are the two worked-example scripts the onboarding and reference docs point readers at: the same
technique this page demonstrates is exactly what a `src/<pkg>/` package would use once a project grows
one.

## `scripts.show_h5_keys`

```{eval-rst}
.. automodule:: scripts.show_h5_keys
   :members:
   :private-members:
```

## `sample_data.make_example`

```{eval-rst}
.. automodule:: sample_data.make_example
   :members:
```
