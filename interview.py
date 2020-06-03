import os

import matplotlib.pyplot as plt
import pandas as pd

"""
part 1
"""
tour_cap_nat_file_name = 'tour_cap_nat.tsv'
path = os.path.join(os.getcwd(), tour_cap_nat_file_name)
tour_cap_df = pd.read_csv(path, sep='\t')

col = tour_cap_df.columns[0]
cols = col.split(',')
tour_cap_df[cols] = tour_cap_df[col].str.split(",", expand=True)
tour_cap_df = tour_cap_df.drop(col, axis=1)


def filter_tour_cap():
    return (tour_cap_df['accommod'] == 'BEDPL') & (tour_cap_df['unit'] == 'NR') & (tour_cap_df['nace_r2'] == 'I551')


tour_cap_df = tour_cap_df[filter_tour_cap()]
cols.extend(['2016 '])

tour_cap_df = tour_cap_df[cols]
convert_names = {'geo\\time': 'code', '2016 ': 'bed'}

tour_cap_df = tour_cap_df.rename(columns=convert_names)

tin_file_name = 'tin00083.tsv'

file_path = os.path.join(os.getcwd(), tin_file_name)
tin_df = pd.read_csv(file_path, sep='\t')

col = tin_df.columns[0]
cols = col.split(',')

tin_df[cols] = tin_df[col].str.split(",", expand=True)
tin_df = tin_df.drop(col, axis=1)


def filter_tin():
    return tin_df['ind_type'] == 'IND_TOTAL'


tin_df = tin_df[filter_tin()]
cols.extend(['2016 '])
tin_df = tin_df[cols]


def filter_wrong_values():
    return (tin_df['geo\\time'].isin(['EA', 'EU27_2007', 'EU27_2020', 'EU28'])) | \
           (tin_df['2016 '].str.endswith(': ')) | \
           (tin_df['2016 '].str.endswith(' u')) | \
           (tin_df['2016 '].str.endswith(' bu'))


tin_df = tin_df[~filter_wrong_values()]
tin_df['2016 '] = tin_df['2016 '].str.rstrip(' b')
convert_names = {'2016 ': 'percent', 'geo\\time': 'code'}
tin_df = tin_df.rename(columns=convert_names)

# merge
df = tour_cap_df.merge(tin_df, left_on='code', right_on='code')
df = df[['code', 'bed', 'percent']]
df.to_csv('result.csv')

"""
part 2
"""
# visualize
df = df.astype({'bed': int, 'percent': int, 'code': str})

# bar 1
plt.figure(figsize=(12, 9), dpi=120)
plt.bar(df['code'], df['bed'])
plt.title('Number by code')
plt.xlabel('Country Code')
plt.ylabel('Number of Bed-places')

# bar 2
plt.figure(figsize=(12, 9), dpi=120)
plt.bar(df['code'], df['percent'])
plt.title('Percentage by code')
plt.xlabel('Country Code')
plt.ylabel('Percentage of individuals online')

# scatter 1
plt.figure(figsize=(12, 9))
for i in df.index:
    plt.scatter(x=df.iloc[i]['bed'], y=df.iloc[i]['percent'], label=df.iloc[i]['code'])
plt.legend(loc='upper right')
plt.title('Scatter of Country')
plt.xlabel('Number of Bed-places')
plt.ylabel('Percentage of individuals online')

plt.show()
