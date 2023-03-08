# line = "SN2020adow"
# years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

# for year in years:
#     line.strip([" ", "\n", "    "])

#     if str(year) in line:
#         print(f"{line} contains year {year}")
#         continue

dumb = [1, 2, 3, 4, 5, 6, 6, 6, 7, 7, 7, 8, 9, 10, 10]

newdumb = [*set(dumb)]
print(newdumb)