# analyse simulation data

setwd("/home/mario/mm2535@cornell.edu/sfi_2017/")


# read datasets
t0.9 = read.table("trustThreshold-0.9.txt", header = TRUE)
t2.5 = read.table("trustThreshold-2.5.txt", header = TRUE)
t4 = read.table("trustThreshold-4.txt", header = TRUE)
t6 = read.table("trustThreshold-6.txt", header = TRUE)
t8 = read.table("trustThreshold-8.txt", header = TRUE)
t16 = read.table("trustThreshold-16.txt", header = TRUE)

# plots
time = t16$time + 1
n = 1:29

# trust Thresholds 
trustThresholds = c(as.character( round((1/length(n))*0.9, 2) ), as.character( round((1/length(n))*2.5,2) ), as.character( round((1/length(n))*4, 2) ), 
                    as.character( round((1/length(n))*6, 2) ), as.character( round((1/length(n))*8,2) ), as.character( round((1/length(n))*16,2) ))
trustThresholdsdata = list(t0.9, t2.5, t4, t6, t8, t16)
colors = c('chocolate3', 'brown3', 'chartreuse3', 'darkgoldenrod3', 'blue3', 'darkgreen')

tiff('information_flow.tiff', width = 720, height = 720)
for(index in 1:length(trustThresholds)){
    get.data = trustThresholdsdata[[index]][,-1]
    mean = apply(get.data, 1, mean)
    sd = apply(get.data, 1, sd)
    
    # build confidence intervals at 1.96
    ci.upper = mean + 1.96*(sd/sqrt(length(mean)))
    ci.lower = mean - 1.96*(sd/sqrt(length(mean)))
    
    # only 1 plot
    title = paste("Average Information Flow (Sample Size = 150)")
    if(index == 1){
      plot(mean, ylab = "Proportion of New Information", xlab = "Time",  main = title, ylim = c(0,0.6), type="n")  
      legend(1, 0.6, trustThresholds, cex = 1.2, col = colors, lty = c(1,1,1), title="Trust Thresholds", bty='n')
      }
    
    lines(mean, type = 'l', col = colors[index])
    #lines(ci.lower, type = 'l', lty = 2, col = colors[index])
    #lines(ci.upper, type = 'l', lty = 2, col = colors[index])
}
dev.off()
