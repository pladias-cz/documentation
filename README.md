# Pladias.cz documentation
Documentation of the project Pladias for the Pladias community

## Build documentation
1) create a file /scripts/local.R with content like this:
    ```r
    dbUser <- 'pladias'
    dbPassword <- 'pladias'
    ```
2) if you need a new chapter, do not forget to register it also in the ./bookdown.yml file
3) run ```Rscript build.R```
4) check that you add also new files in the /docs directory to the commit
5) commit&push
6) in some minutes the content of https://pladias-cz.github.io/documentation/ is updated
