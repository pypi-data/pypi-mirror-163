# rust_decider

Rust implementation of bucketing, targeting, overrides, and dynamic config logic.

## Usage

```sh
 source .env/bin/activate
 maturin develop
 python
```

```python
import rust_decider
d = rust_decider.init("darkmode fractional_availability value", "../cfg.json")
d.printer() # prints yooo
ctx = rust_decider.make_ctx({"user_id": "8"})
x = d.choose("exp_1", ctx)
x.decision() # prints the variant!!!!
y = d.get_map("dc_map", ctx) # fetch a map DC
y.err() # check that error is empty
y.val() # get the actual map itself
```

## Development

`cd decider-py/` and run `maturin develop` to build `reddit-decider` python wheel.

## Publishing

Package is automatically published on merge to master to https://pypi.org/project/reddit-decider/ via drone pipeline.

# Formatting / Linting

cargo fmt    --manifest-path decider-py/test/Cargo.toml
cargo clippy --manifest-path decider-py/test/Cargo.toml
