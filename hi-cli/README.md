# HÍ CLI
Uppkast að CLI tóli fyrir `notendur.hi.is`. Með því má fá lista yfir skrár, eyða skrám og ferja skrár á notendasvæðið. Tólið ætti að eiga heima í sér pakka en skoðum það síðar.

CLI tólið notar [Poetry](https://python-poetry.org/) sem package manager sem einfaldar uppsetningu og auðveldara verður að uppfæra pakka, þá sérstaklega þar sem [dependabot](https://dependabot.com/) lætur eiganda að Github repo-inu vita þegar uppfærslur eru aðgengilegar.



## Skipanir
**Setja upp pakka á localhost**
```sh
poetry install
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
poetry run hicli server list --remote-dir .public_html
```