Sys.setlocale("LC_ALL", "korean")
library(KoNLP)
library(ggplot2)
library(data.table)

useNIADic()

df <- read.csv('data/processed/동아일보-relevant_sentences.csv')

txt <- df$relevant_sentences[1]
niadic_res <- MorphAnalyzer(txt)