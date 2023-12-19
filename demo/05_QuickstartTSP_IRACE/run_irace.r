library("irace")
# Go to the directory containing the scenario files
# setwd("./tuning")
scenario <- readScenario(filename = "scenario.txt",
scenario = defaultScenario())
irace.main(scenario = scenario)