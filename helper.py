
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0,'Overall')

    return years,countries

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    else:
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]
    
    if flag == 1:
        x = temp_df[['Year','Gold','Silver','Bronze']].groupby('Year').sum().sort_values('Year',ascending=False).reset_index()
        x['Year'] = x['Year'].astype(str)
    else:
        x = temp_df[['region','Gold','Silver','Bronze']].groupby('region').sum().sort_values('Gold',ascending=False).reset_index()
    
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    
    return x