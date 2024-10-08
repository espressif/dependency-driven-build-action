# Contributing to Dependency Driven Build Action

## Running Python Tests

```bash
python -m unittest discover -p '*.py'
```

## GitHub Actions Tips

### Set a Multiline String as Output

Don't use `::set-output`, it's been deprecated. Use the following trick instead to set an environment variable with a multiline string:

```bash
echo "ENV_VAR<<EOF"$'\n'"$(your cammand here to generate the multi-line string)"$'\n'"EOF" >> $GITHUB_ENV
```

or set a multiline string as an output:

```bash
echo "output<<EOF"$'\n'"$(your cammand here to generate the multi-line string)"$'\n'"EOF" >> $GITHUB_OUTPUT
```
