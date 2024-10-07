# GitHub Action - Dependency-driven Build & Test

This action build and test your ESP-IDF projects based on the changed files in the PR.

- build ESP-IDF projects with [idf-build-apps](https://github.com/espressif/idf-build-apps).
- test ESP-IDF projects with [pytest-embedded](https://github.com/espressif/pytest-embedded).

## Pre-requisites

To run this action, you need to run it inside a docker container with

- python installed
- ESP-IDF installed
- `IDF_PATH` environment variable set to the path of the ESP-IDF installation

We recommend you to use [espressif/idf](https://hub.docker.com/r/espressif/idf) docker image.

## Getting Started

TODO

## Usage

### Inputs

TODO

### Outputs

#### `outputs.modified_files`

A space separated list of files that were modified in the PR.

#### `outputs.idf_build_apps_args`

A space separated list of arguments to pass to `idf-build-apps` command.

## More Ways to Configure

Not only the inputs, but also from the PR labels, environment variables can be used to configure the action.

### Supported PR Labels

#### `build-and-test-all-apps`

builds and tests all apps in the repository. No matter what the PR contains, all apps will be built and tested.

#### `build-only`

Skip testing and only build the apps.

### Supported Environment Variables

To apply the environment variables, you need to add them to the `env` section of the github action step in your workflow file.

```yaml
steps:
  - name: Build and Test
    uses: espressif/github-action-dependency-driven-build@v1
    env:
      BUILD_AND_TEST_ALL_APPS: 1
```

#### `BUILD_AND_TEST_ALL_APPS`

set to `1` to build and test all apps in the repository. No matter what the PR contains, all apps will be built and tested.

#### `BUILD_ONLY`

set to `1` to skip testing and only build the apps.
