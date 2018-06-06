# Read in data table
DFrame <- read.table(file = "ms_toy.txt", sep = "\t", header = TRUE)
DTable0 <- t(as.matrix(as.data.frame(lapply(DFrame[,1:1], as.numeric))))

# create new dataset without missing data
newdata <- na.omit(DFrame) 
DTable <- t(as.matrix(as.data.frame(lapply(newdata[,1:1], as.numeric))))
colnames(DTable) <- colnames(DFrame)[1]

# Calculate the mean and standard deviation of the current data
mean <- mean(DTable)
sd <- sd(DTable)

# Derive the new mean and standard deviation for the missing data based on the current
# distribution
nansize <- dim(DTable0)[1]-dim(DTable)[1]
lowquan <- qnorm(0.25, mean, sd)
lowdata <- subset(DTable, DTable[,1] <= lowquan)
newmean <- mean(lowdata)
newsd <- sd(lowdata)

# Generate the new data based on the new mean and standard deviation from the previous step
imputdata <- rnorm(nansize, newmean, newsd)

hist1 <- hist(DTable, col="blue")
hist2 <- hist(imputdata, add=T, col="red")
#plot()
for(mean in seq(from = 20, to = lowquan, by = 2)){
  for(sd in seq(from = 1, to = sd, by = 0.2)){
    imputdata1 <- rnorm(nansize, mean, sd)
    hist3 <- hist(DTable, col="blue")
    hist4 <- hist(imputdata1, add=T, col="red")
  }
}