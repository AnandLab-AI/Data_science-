import pandas as pd   ## When we calling calss on another ipynb file it will load import pandas feature as well
import numpy as np
class Univariate:
    def QuanQual(self,dataset): 
        quan=[]
        qual=[]
        for col in dataset.columns:
            if dataset[col].dtypes == "O":
                qual.append(col)
            else:
                quan.append(col)
        return qual,quan  

    def freqtab(self,colname,dataset):
        freqTable=pd.DataFrame(columns=["Unique","Frequency","Relative","Cumsum"])
        freqTable["Unique"]=dataset[colname].value_counts().index
        freqTable["Frequency"]=dataset[colname].value_counts().values
        freqTable["Relative"]=freqTable["Frequency"]/103
        freqTable["Cumsum"]=freqTable["Relative"].cumsum()
        return freqTable

    def descriptive(self,quan,dataset):  ## Here we given 2 inputs dataset and quan , so we need to mention in parameter argumnets 
        descriptive=pd.DataFrame(index=("Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%","IQR","1.5Rule","Lesser","Greater","Min","Max"),columns=quan)
        for colname in quan:
            descriptive.loc["Mean",colname]=dataset[colname].mean()
            descriptive.loc["Median",colname]=dataset[colname].median()
            descriptive.loc["Mode",colname]=dataset[colname].mode()[0]
            descriptive.loc["Q1:25%",colname]=dataset.describe()[colname]["25%"]
            descriptive.loc["Q2:50%",colname]=dataset.describe()[colname]["50%"]
            descriptive.loc["Q3:75%",colname]=dataset.describe()[colname]["75%"]
            descriptive.loc["99%",colname]=np.percentile(dataset[colname],99)
            descriptive.loc["Q4:100%",colname]=dataset.describe()[colname]["max"]
            descriptive.loc["IQR",colname]=descriptive.loc["Q3:75%",colname] - descriptive.loc["Q1:25%",colname]
            descriptive.loc["1.5Rule",colname]= 1.5 * descriptive.loc["IQR",colname]
            descriptive.loc["Lesser",colname] = descriptive.loc["Q1:25%",colname] - descriptive.loc["1.5Rule",colname]
            descriptive.loc["Greater",colname] = descriptive.loc["Q3:75%",colname] + descriptive.loc["1.5Rule",colname]
            descriptive.loc["Min",colname] = dataset[colname].min()
            descriptive.loc["Max",colname] = dataset[colname].max()
        return descriptive

    def chkoutlier(self,descriptive):
        lesser=[]
        greater=[]
        for colName in descriptive:
            if descriptive.loc["Min",colName] < descriptive.loc["Lesser",colName]:  ## min value is less than lesser value it will be lesser - outlier
                lesser.append(colName)
            if descriptive.loc["Max",colName] > descriptive.loc["Greater",colName]: ## Max value is greater than greater value it will be greater - outlier
                greater.append(colName)
        return lesser , greater 
