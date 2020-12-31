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
### Setja upp pakka á localhost
```sh
poetry install
```


### Skoða dependency tré
```sh
poetry show --tree
```


### Uppfæra pakka á localhost
```sh
poetry update
```


## Keyra build
```sh
hicli build --help
```

**Dæmi**

```sh
hicli build
hicli build --clean # eyðir build möppu fyrst
```

### Lista upp möppur og skrár á notandasvæði
```sh
hicli server list --help
```


**Dæmi**

```sh
hicli server list --remote-dir .public-html/<heiti-á-undirmöppu> # default .public_html
```

![tree view](https://www.dropbox.com/s/yplhpvltuetizi9/2020-12-26_15-19.png?raw=1)


### Eyða öllum möppum og skrám frá rótarmöppu
> **⚠ Aðvörun: Mjög hæg aðgerð og má endurskrifa með því að senda ssh skipun á server**
>
> Eyðir öllum skrám á server


```sh
hicli server delete --remote-dir .public_html/staging/edbook
```


## Afrita build möppu á notandasvæði
> **⚠ Aðvörun: Mjög hæg aðgerð og má endurskrifa með því að zip-a build fyrst og unzippa á server**
>
> Afritar allar skrár á server


```sh
# Ef <einhver-mappa> er ekki til á server þá er hún búin til
hicli server copy --local-dir _build --remote-dir .public_html/<einhver-mappa>
```
