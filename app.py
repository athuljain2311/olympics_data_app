import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessor,helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    years,countries = helper.country_year_list(df)

    st.sidebar.header('Medal Tally')
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",countries)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in the {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"Medal Tally of {selected_country}")
    else:
        st.title(f"Medal Tally of {selected_country} in the {selected_year} Olympics")
    st.table(medal_tally)

elif user_menu == 'Overall Analysis':
    editions  = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)
    
    nations_over_time = helper.data_over_time(df,'region','Countries')
    st.title('Participating Nations Over Time')
    fig = px.line(nations_over_time,x='Edition',y='Countries')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event','Events')
    st.title('Events Over Time')
    fig = px.line(events_over_time,x='Edition',y='Events')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df,'Name','Athletes')
    st.title('Athletes Over Time')
    fig = px.line(athletes_over_time,x='Edition',y='Athletes')
    st.plotly_chart(fig)

    st.title('Number of Events over time (Every Sport)')
    fig,ax = plt.subplots(figsize=(16,16))
    x = df.drop_duplicates(['Year','Sport','Event'])
    events_pivot = x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int')
    ax = sns.heatmap(events_pivot,annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

elif user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(f"{selected_country}'s Medal Tally Over the Years")
    st.plotly_chart(fig)

    st.title(f"{selected_country} excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(18,18))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title(f"Top 10 Athletes of {selected_country}")
    top_ten_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top_ten_df)

else:
    
    athlete_df = df.drop_duplicates(['Name','region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    sports = df['Sport'].value_counts().head(30).index.tolist()
    x = []
    name = []

    for sport in sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    st.title('Distribution of Age wrt Sports (Gold Medalists)')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)

    st.title('Height vs Weight')
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=30)
    st.pyplot(fig)

    st.title('Men v/s Women Participation Over the Years')
    final = helper.men_v_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)