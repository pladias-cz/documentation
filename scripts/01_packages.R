requiredPackages = c(
  'tidyverse' # must have
  ,'bookdown' # generates the report
  ,'DBI' # db connection
  ,'RPostgres' # db connection
  ,'knitr' # kable() and other markdown layout
  ,'kableExtra' # more formating for kable
  ,'scales' # format numbers
  ,'gridExtra' # composition of objects on the page
)

for (p in requiredPackages) {
  if (!require(p, character.only = TRUE)) {
    install.packages(p)
  }
  library(p, character.only = TRUE)
}

rm(requiredPackages, p)
select <- dplyr::select
