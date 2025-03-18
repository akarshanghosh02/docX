import pandas as pd

# Reads the ComponentName csv file and return the list
def readCSVFiles():
    df = pd.read_csv("componentName.csv")
    df.set_index("component", inplace=True)
    return df
