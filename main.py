"""
this is a project related to used cars. In this project, I will analyze the top ten cars that maintain their
values.
"""

import pandas as pd
import numpy as np

dataframe_original = pd.read_csv("C:/used car project/vehicles.csv")


"""
we only need the price, year, manufacturer, model of the cars, and to clean up the dataset, we are going to
drop all the na values.
"""

df = dataframe_original[['price','year','manufacturer','model','condition']].dropna()
print(df.size)
print(df.head(10))
new_model_name = df["manufacturer"] + df["model"]
df["model"] = new_model_name

"""
now we can take a look at our dataset. We have 1198390 rows of data, and we have the price, year, manufacturer, model
and condition of the cars for our columns. The next step is to exclude cars that are in bad conditions. As a consumer, 
we do not want to buy cars in bad condition because that will cost us a lot of extra money to fix it. 
"""

print(df.groupby('condition').size())
# as we can see, there are 532 cars in our dataframe that has the "salvage" title, meaning that it has been
# damaged before and the is declared a total loss by the insurance company. we definitely want to exclude that
# from our dataset. And we want to exclude "fair" from our dataset, too, because most sellers have a tendency to
# prettify their car's condition so that they could sell it in a higher price. A car that has fair condition usually
# indicates that the condition is bad.

# Besides, we are only choosing cars that are newer than 2015 and more than 10000 dollars and less than 50000
# because I do not want to buy a car before 2015 and my budget is between 10000 to 50000


df = df[df.condition != "salvage"]
df = df[df.condition != "fair"]
df = df[df.year >= 2015.0]
df = df[df["price"].between(10000, 50000)]
print(df.head(10))
print(df.size)

"""
the mean of the price of different models
"""
man_model_df = df.groupby(["manufacturer", "model","year"]).mean()
print(man_model_df)

"""
lets look at the years
"""
print(df.sort_values(by = ["year"], ascending=False))
# we could see that the latest year is 2022

"""
We now want to only keep the models that have more than 1 data because we cannot calculate the depreciation rate
based on one data
"""
df = df[df.duplicated(subset=["model"], keep=False)]
print(df.head(10))
group_by_data = df.groupby(["model","year"], as_index=False).mean()

print(group_by_data)

# delete all the rows that only has car from a single year.
df_clean = group_by_data[group_by_data.duplicated(subset=["model"], keep=False)]
print(df_clean)

# Now we complete all the data cleaning and selection
# process. We have 7145 data. And because we used the group by statement, the year is already in ascending order.
df_clean.reset_index()


row_num = df_clean.shape[0]  # number of rows in the clean dataframe
depreciation_ratio_lst = [];
i = 0
model_new_price = 0
newer_year = 0
temp_lst_model_year = []
temp_lst_model_price = []

while i < row_num:
    model_name = df_clean.iat[i, 0]
    try:
        if df_clean.iat[i + 1, 0] == model_name:
            temp_lst_model_year.append(df_clean.iat[i, 1])
            temp_lst_model_price.append(df_clean.iat[i, 2])
            i += 1
            if df_clean.iat[i + 1, 0] != model_name:
                newer_year = df_clean.iat[i, 1]
                model_new_price = df_clean.iat[i, 2]
                depreciation_rate = (model_new_price - temp_lst_model_price[0]) / temp_lst_model_price[0] / \
                                    (newer_year - temp_lst_model_year[0])
                depreciation_ratio_lst.append([model_name, depreciation_rate])
                temp_lst_model_year = []
                temp_lst_model_price = []
                i += 1
                continue
            else:
                newer_year = df_clean.iat[i, 1]
                model_new_price = df_clean.iat[i, 2]
                i += 1
                continue
        else:
            # we use the straight line formula depreciation formula here to calculate the depreciation rate,
            newer_year = df_clean.iat[i, 1]
            model_new_price = df_clean.iat[i, 2]
            depreciation_rate = (model_new_price - temp_lst_model_price[0]) / temp_lst_model_price[0] / \
                                (newer_year - temp_lst_model_year[0])
            depreciation_ratio_lst.append([model_name, depreciation_rate])
            temp_lst_model_year = []
            temp_lst_model_price = []
            i += 1
            continue
    # this is used to handle the last element that could be out of index bound because we should i + 1 before
    except IndexError as error:
        break

depreciation_ratio_lst.sort(key=lambda x: x[1])
for i in range(50):
    print(depreciation_ratio_lst[i])

top_value_model_name = []
for i in range(50):
    top_value_model_name.append(depreciation_ratio_lst[i])

result = df[np.isin(df, top_value_model_name).any(axis=1)]
print(result)
group_by_result = result.groupby(["model"]).count()
group_by_result.reset_index()
top_ten_group_by = group_by_result[(group_by_result > 10).any(axis=1)]

print(top_ten_group_by)


top_ten_list = list(top_ten_group_by.index)

final_df = df_clean[np.isin(df_clean, top_ten_list).any(axis=1)]
print(final_df)
print(final_df.groupby(["model", "year"]).mean())
# we found out there are some duplicated values. So we decide to just delete all duplicate values
# because it is highly unlikely that two cars have the exactly same depreciation rate






