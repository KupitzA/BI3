# Read in null-mutants.tsv as numeric matrix
df_null_mutants = read.table(
  file = "null-mutants.tsv",
  header = TRUE,
  stringsAsFactors = TRUE,
  sep = "\t"
)
rownames(df_null_mutants) = df_null_mutants$strain
mtrx = data.matrix(df_null_mutants[2:ncol(df_null_mutants)])

# global container storing the variances per genes
variance <- rep(0, ncol(mtrx))
# global container storing the probabilities
mtrx_prob <- mtrx[2:nrow(mtrx), ]

# initialize genes varances for mutants from wildtype
initializeVariance <- function() {
  for (j in 1:ncol(mtrx)) {
    temp <- 0
    for (i in 2:nrow(mtrx)) {
      temp <- temp + abs(mtrx[i, j] - mtrx[1, j])
    }
    # use variance vector as global accessible variable
    variance[j] <<- temp / (nrow(mtrx_prob))
  }
}

# update the variances for each gene based on the
# equation of noise modle step 2
# since we previousely used variances for each gene
# we interpret the equation in the same way
updateVariance <- function(p_from, p_to) {
  curr_variance <- rep(0, ncol(mtrx))
  counter <- rep(0, ncol(mtrx))
  for (i in 1:length(p_from)) {
    square_dist <- mtrx[p_from[i], p_to[i]] - mtrx[1, p_to[i]]
    square_dist <- square_dist**2
    curr_variance[p_to[i]] <- square_dist
    counter[p_to[i]] <- counter[p_to[i]] + 1
  }
  for(i in 1:length(curr_variance)){
    if(counter[i] != 0){
      variance[i] <<- curr_variance[i]/(1+counter[i])
    }
  }
}

# compute the probabilities that the deviation is due
# to a real regulation event
probabilities <- function() {
  for (b in 1:nrow(mtrx_prob)) {
    for (a in 1:ncol(mtrx_prob)) {
      deviation <- abs(mtrx[b + 1, a] - mtrx[1, a])
      phi <- pnorm(deviation / sqrt(variance[a]))
      mtrx_prob[b, a] <<- 2 * phi - 1
    }
  }
}

# re-estimate wilde-type expression level
# accounts to step 3 of the noise modle
updateWildType <- function(p_from, p_to){
  for(i in 1:ncol(mtrx)){
    temp <- mtrx[1,i]
    counter <- 0
    for(j in 1:length(p_from)){
      if(p_to[j] == i){
        temp <- temp + mtrx[p_from[j]+1,i]
        counter <- counter + 1
      }
    }
    mtrx[1,i] <<- temp/(counter+1)
  }
}


refine <- function() {
  # Noise model iterative step (1)
  # search gene pairs for refining the error modle
  p_from <<- c()
  p_to <<- c()
  for (b in 1:nrow(mtrx_prob)) {
    for (a in 1:ncol(mtrx_prob)) {
      if (mtrx_prob[b, a] < 0.05) {
        p_from <- c(p_from, b)
        p_to <- c(p_to, a)
      }
    }
  }
  # Noise model iterative step (2)
  updateVariance(p_from, p_to)
  # Noise model iterative step (3)
  updateWildType(p_from, p_to)
}

output <- function(){
  for (b in 1:nrow(mtrx_prob)) {
    for (a in 1:ncol(mtrx_prob)) {
      if (mtrx_prob[b, a] < 0.05) {
        cat(colnames(mtrx)[b], "\t",
            colnames(mtrx)[a], "\t",
            mtrx_prob[b,a], "\n")
      }
    }
  }
}

# Main
iterations <- 1
initializeVariance()

for (i in 1:iterations) {
  # First part of Noise model step (1)
  # calculate probabilities for each pair of genes
  probabilities()
  refine()
}
output()