library(samr)
library(preprocessCore)

play <- function(rna_sample){
  # store number of up and down regulated genes
  # per fdr - nperm combination
  low_count = matrix(0, ncol = 10, nrow = 10)
  up_count = matrix(0, ncol = 10, nrow = 10)
  for(fdr in seq(from = 0.1, to = 1.0, by = 0.1)){
    for(nperms in seq(from = 10,to = 100,by = 10)){
      sink("/dev/null")
      sam <- SAM(x = rna1,
                  y = c(1,1,1,2,2,2),
                  resp.type="Two class unpaired",
                  nperms=nperms,
                  logged2 = TRUE,
                  fdr.output = fdr)
      sink()
      low_count[fdr*10,nperms*0.1] = nrow(sam$siggenes.table$genes.lo)
      up_count[fdr*10,nperms*0.1] = nrow(sam$siggenes.table$genes.up)
    }
  }
  print(low_count)
  print(up_count)
}

# Read in data table
DFrame <- read.table(file = "ms_data.txt", sep = "\t", header = TRUE)
DTable <- as.matrix(as.data.frame(lapply(DFrame[,1:9], as.numeric)))
rownames(DTable) <- DFrame[,11]

# Log2 transform the data (apply log2 on every cell)
DTable <- log2(DTable)

# Apply quantil normalization of library preprocessCore
# split the two siRNA-induced samples
rna1 <- normalize.quantiles(DTable[,1:6], FALSE)
rna2 <- normalize.quantiles(DTable[,c(1:3,7:9)], FALSE)

# Apply SAM function of samr library on sample 1
sink("/dev/null")
sam <- SAM(x = rna1,
           y = c(1,1,1,2,2,2),
           resp.type="Two class unpaired",
           nperms=100,
           genenames = rownames(DTable),
           logged2 = TRUE,
           fdr.output = 0.05)
sink()
cat("10 up-regulated genes for sample 1:\n")
print(sam$siggenes.table$genes.up[1:10,c(1,2,6)])
cat("10 down-regulated genes for sample 1:\n")
print(sam$siggenes.table$genes.lo[1:10,c(1,2,6)])

# Apply SAM function of samr library on sample 2
sink("/dev/null")
sam <- SAM(x = rna2,
           y = c(1,1,1,2,2,2),
           resp.type="Two class unpaired",
           nperms=100,
           genenames = rownames(DTable),
           logged2 = TRUE,
           fdr.output = 0.05)
sink()
cat("10 up-regulated genes for sample 2:\n")
print(sam$siggenes.table$genes.up[1:10,c(1,2,6)])
cat("10 down-regulated genes for sample 2:\n")
print(sam$siggenes.table$genes.lo[1:10,c(1,2,6)])

#play(rna1)
#play(rna2)