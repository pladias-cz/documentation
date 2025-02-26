requiredPackages = c(
  'tidyverse' # must have
)

for (p in requiredPackages) {
  if (!require(p, character.only = TRUE)) {
    install.packages(p)
  }
  library(p, character.only = TRUE)
}

rm(requiredPackages, p)
select <- dplyr::select
