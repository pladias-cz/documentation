# Rscript build.R
setwd("~/Repositories/Pladias/documentationNew")
# getwd()
source("scripts/01_packages.R")

bookdown::render_book('index.Rmd', output_format='all')
