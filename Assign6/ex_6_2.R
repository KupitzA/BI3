library(samr)
library(preprocessCore)

# Read in data table
DFrame <- read.table(file = "ms_data.txt", sep = "\t", header = TRUE)
DTable <- as.matrix(as.data.frame(lapply(DFrame[,1:9], as.numeric)))
rownames(DTable) <- DFrame[,11]

# Log2 transform the data (apply log2 on every cell)
DTable <- log2(DTable)

# Apply quantil normalization of library preprocessCore
DTable <- normalize.quantiles(DTable, FALSE)

# Apply SAM function of samr library
SAM(x = DTable,
    y=NULL,
    censoring.status=NULL,
 #   resp.type="Two class paired",
    geneid = NULL,
    genenames = NULL,
    s0=NULL,
    s0.perc=NULL,
    # number of permutations
    nperms=100,
    center.arrays=FALSE,
    testStatistic="standard",
    time.summary.type="slope",
    regression.method="standard",
    return.x=TRUE,
    knn.neighbors=10,
    random.seed=NULL,
    # we performed log2 transformation
    logged2 = TRUE,
    # q-value threshold
    fdr.output = 0.20,
    eigengene.number = 1)
  