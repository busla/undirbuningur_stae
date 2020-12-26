# HÍ CLI
Uppkast að CLI tóli fyrir `notendur.hi.is`. Með því má fá lista yfir skrár, eyða skrám og ferja skrár á notendasvæðið. Tólið ætti að eiga heima í sér pakka en skoðum það síðar.

CLI tólið notar [Poetry](https://python-poetry.org/) sem package manager sem einfaldar uppsetningu og auðveldara verður að uppfæra pakka, þá sérstaklega þar sem [dependabot](https://dependabot.com/) lætur eiganda að Github repo-inu vita þegar uppfærslur eru aðgengilegar.


Til að losna við username og password prompt má setja eftirfarandi `env` breytur í umhverfið.

```sh
HI_USERNAME=notandanafn án @hi.is
HI_PASSWORD=pass
```

## Install Poetry
Sjá [Poetry docs](https://python-poetry.org/docs/#installation)


## Skipanir
**Setja upp pakka á localhost**
```sh
poetry install
```


**Skoða dependency tré**
```sh
poetry show --tree
```


**Uppfæra pakka á localhost**
```sh
poetry update
```


**Keyra build**
```sh
poetry run hicli build
```

**Lista upp möppur og skrár á notandasvæði**
```sh
poetry run hicli server --host krafla.rhi.hi.is list --remote-dir .public-html
```
![tree view](https://www.dropbox.com/s/yplhpvltuetizi9/2020-12-26_15-19.png?raw=1)


**Eyða öllum möppum og skrám frá rótarmöppu**
```sh
poetry run hicli server --host krafla.rhi.hi.is delete --remote-dir .public_html/staging/edbook
```


**Afrita build möppu á notandasvæði**
```sh
poetry run hicli server --host krafla.rhi.hi.is copy --local-dir ../_build --remote-dir .public_html/staging/edbook
```
