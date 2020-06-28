import pandas as pd 
import seaborn as sns
import numpy as np 
from numpy import nan
from sklearn.ensemble import RandomForestRegressor
from scipy.stats.stats import pearsonr
from sklearn.metrics import roc_auc_score
#%matplotlib inline

def load():
    file_path = './Factorial_study_data.csv'
    df = pd.read_csv(file_path,delimiter=',')

    file_path = './d_modeled.csv'
    df_d_modeled = pd.read_csv(file_path,delimiter=',')
    df_d_modeled = df_d_modeled[df_d_modeled["Avg Fiber width"]!=0]
    df_d_modeled = df_d_modeled.drop([4, 14, 34, 44])
    #df_d_modeled
    #merge
    index2 = (df["Pressure (bar)"]==2)
    print(index2)
    df.loc[df["Pressure (bar)"]==2,"Pressure (bar)"] = 2.5
    x = pd.merge(df, df_d_modeled,  how='left', left_on=["wt% PPF", "Pressure (bar)", "Speed (mm/s)"], right_on = ["wt% PPF", "Pressure (bar)", "Speed (mm/s)"])
    print(len(x))
    x.loc[index2,"Pressure (bar)"] = 2
    x
    df = x

    df = df[~np.isnan(df["Mean fiber"])]
    df = df[~np.isnan(df["Mean spacing"])]
    df = df[~np.isnan(df["Spacing (mm)"])]
    df = df[~np.isnan(df["Avg Fiber width"])]

    diff = pd.DataFrame()
    df.dropna()
    diff["machine precision(%)"] = (df["Spacing (mm)"] - df["Mean spacing"])*100/df["Spacing (mm)"]
    diff["material accuracy(%)"] = (df["Mean fiber"]-df["Avg Fiber width"])*100/df["Avg Fiber width"]
    diff = diff.abs()
    diff["material"] = df["wt% PPF"]

    diff["material"] = df["wt% PPF"]
    diff["spacing"] = df["Spacing (mm)"]
    diff["speed"] = df["Speed (mm/s)"]
    diff["pressure"] = df["Pressure (bar)"]
    diff["layer"] = df["Layer #"]
    diff["scaffold"] = df["Scaffold #"]
    diff["config no."] =[i for i in range(diff.shape[0])]

    df["viscosity"] = 0
    df.at[df["wt% PPF"]==85, "viscosity"] = 45
    df.at[df["wt% PPF"]==90, "viscosity"] = 66

    df.dropna(subset = ["Spacing (mm)", "Speed (mm/s)", "Pressure (bar)", "viscosity"], inplace=True)

    dataX = df[["Spacing (mm)", "Speed (mm/s)", "Pressure (bar)", "viscosity", "Layer #"]]
    #diff["machine precision(%)"]
    dataY = diff[["machine precision(%)", "material accuracy(%)"]]

    return (df, diff, dataX, dataY)
