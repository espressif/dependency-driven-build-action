# GitHub Action - Dependency-driven Build

This action builds a ESP-IDF project with [idf-build-apps](https://github.com/espressif/idf-build-apps).

## Pre-requisites

To run this action, you need to run it inside a docker container wit

- python installed
- ESP-IDF installed
- `IDF_PATH` environment variable set to the path of the ESP-IDF installation

We recommend you to use [espressif/idf](https://hub.docker.com/r/espressif/idf) docker image.

## Inputs

TODO

## PR Labels

``build-and-test-all-apps``

builds and tests all apps in the repository. No matter what the PR contains, all apps will be built and tested.

---

``build-only``

Skip testing and only build the apps.
