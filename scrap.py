import pandas as pd

df = pd.read_csv("meds.txt", delimiter="\t")
df = df[['DrugName',
       'ActiveIngredient']].drop_duplicates()

df.to_csv("med_name_princ.csv")