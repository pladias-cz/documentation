 R -e "install.packages('bookdown')"
# R -e "install.packages('devtools')"
# R -e  "devtools::install_github('rstudio/rmarkdown')"
R -e "rmarkdown::render('index.Rmd',output_format='all')"
#Pokud chceme jen jednu kapitolu, lze
# R -e "rmarkdown::render('chapters/120_introR.Rmd',output_format='all')"