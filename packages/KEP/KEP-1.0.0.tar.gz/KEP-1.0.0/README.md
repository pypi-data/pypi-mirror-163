# Knowledge Extraction for COVID-19 Publications (KEP)

## Content
This package provides the functionality of extracting and displaying key knowledge to enable a rapid understanding of COVID-19 publications. Current focuses include key topics and top disease and location mentions of the input COVID-19 publication. More functions are on the way.

## Prerequisites

Install packages before use (with tested versions):

* Python >=3.8  
* spacy (3.0.8)
* scispacy (0.4.0)
* gensim (4.1.2)
* nltk (3.7)
* en-core-web-sm (https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz)
* en-ner-bc5cdr-md (https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bc5cdr_md-0.4.0.tar.gz)
* bs4 (BeautifulSoup4)
* wordcloud
* pandas
* matplotlib

Default:
* re
* string
* os
* urllib
* xml

Local package:
* nltk_data (https://github.com/nltk/nltk_data/tree/gh-pages/packages) (rename the "packages" folder as "nltk_data" and put it in your own python project)


## Instruction

### Load the KEP package

pip install KEP


### Sample code

```
from KEP import To_Generate_Disease,To_Generate_Key_Word,To_Generate_Location,To_Generate_All 

To_Generate_All(7824075)



# If multiple publications at a time, uncomment the following lines and replace the PMC ID:
# To_Generate_All(7824075)
# To_Generate_All(7824470)
# To_Generate_All(6988269)
# ...
```


### Input

Input the PMC ID of a publication (or a set of PMC IDs)

(For example: input "7824075" representing the publication https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7824075/)

### Output
1. The bar graph and word cloud of the key topics
2. The bar graph of the top disease mentions
3. The bar graph of the top location mentions



## References

1. Chen, Q., Allot, A., & Lu, Z. (2020). Keep up with the latest coronavirus research. Nature, 579(7798), 193-194.
2. Comeau, D. C., Wei, C. H., Islamaj Doğan, R., & Lu, Z. (2019). PMC text mining subset in BioC: about three million full-text articles and growing. Bioinformatics, 35(18), 3533-3535.
3. BioC API for PMC: https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PMC/
4. Part of the functionality is based on the en-ner-bc5cdr-md, en-core-web-sm, and gensim packages.

## Citation
TBA.

## Report an issue
Should you have any questions or comments, please feel free to contact the author.