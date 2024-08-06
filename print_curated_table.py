from softwareTable import create_curated_table

df = create_curated_table()

print(df)
print(df.columns)

print(type(df.to_dict('records')))

with open ('records.txt', 'w') as f:
    for item in df.to_dict('records'):
        f.write(str(item) + "\n")