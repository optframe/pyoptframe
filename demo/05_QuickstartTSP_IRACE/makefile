all:

run:
	Rscript run_irace.r 

vendor:
	sudo apt-get install -y r-base
	Rscript -e "install.packages(c('irace'), repos='https://cran.rstudio.com')"
	cp /usr/local/lib/R/site-library/irace/templates/*.tmpl .

# templates must be on: /usr/local/lib/R/site-library/irace/templates
	