source('local.R')

manuscriptResolution <- 1200
color_cz <- "#f6c85f"
color_us <- "#0b84a5"


db <- dbConnect(
  Postgres(),
  dbname = "pladias",
  host = "localhost",
  port = 7777,
  user = dbUser,
  password = dbPassword
)