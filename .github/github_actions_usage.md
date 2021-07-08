# Github Actions

In the `workflows` folder you will find the YAML files describing the possible 
different workflows. 

`build_for_deployment.yaml` uses the latest Ubuntu to build the application 
with various python versions. 
In case it is successful and the pushed commit is also tagged, the current 
version will be built with python 3.7 and deployed.

## Secrets

Github allows for saving secret environmental variables such as tokens for 
PyPi deployment.
Such secrets are encrypted.
For more information you can read [this guide](https://docs.github.com/en/actions/reference/encrypted-secrets).

## Development and testing of Github Actions

With the help of application called [Act](https://github.com/nektos/act) it is 
possible to run Github Actions locally. 
After the installation you can run it with the latest Ubuntu as followed:

```bash
act -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

The deployment will not work with the secrets saved in Github. 
You will need to provide it eather with `-s TOKEN={value}` or withing the
`.secrets` file and `--secret-file FILE_PATH`.


```bash
act -P ubuntu-latest=catthehacker/ubuntu:act-latest --secret-file FILE_PATH
```
