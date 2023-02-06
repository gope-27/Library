import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
# from IPython.display import Markdown, display
# import seaborn as sns

st.set_page_config(page_title="Library", page_icon=":book:",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("")
st.markdown("")

selected = option_menu("Library Dashboard", ["Student Analysis", "Membership Analysis", "Delivery Analysis"],  # , ,"Customer Analysis" ],
                       # , 'truck', "shop", 'people', 'door-open-fill'],
                       icons=['graph-up-arrow'],
                       menu_icon="book-half",  # for menu icon
                       default_index=1,  # optional
                       orientation="horizontal",

                       styles={
    "container": {"padding": "0!important", "background-color": "#01b8aa"},
    "icon": {"color": "blue", "font-size": "14px"},
    "nav-link": {"font-size": "16px", "text-align": "center", "margin": "1px", "--hover-color": "#D3D3D3"},
    "nav-link-selected": {"background-color": "black"},
})

with open('style1.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Read Data


@st.cache(suppress_st_warning=True)
def get_data_from_csv():
    Student_Table = pd.read_csv("Student Table.csv", encoding="latin")
    Student_Table.drop(["Unnamed: 23", "Unnamed: 24",
                       "Unnamed: 25", "Unnamed: 26"], axis=1, inplace=True)
    Student_Table.rename(columns={
                         'Graduation Type': 'Graduation_Type', 'Stream Type': 'Stream_Type'}, inplace=True)
    Library_Fact = pd.read_csv("Library Fact Dataset.csv", encoding="latin")
    HR_Analytics = pd.read_csv("HR Analytics.csv")
    HR_Analytics.rename(columns={'Department ': 'Department',
                        'Qualification': 'Graduation_Type', 'Stream': 'Stream_Type'}, inplace=True)
    return Student_Table, Library_Fact, HR_Analytics


Student_Table, Library_Fact, HR_Analytics = get_data_from_csv()

if selected == "Membership Analysis":
    st.markdown("")

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")
    Dep = st.sidebar.multiselect(
        "Select the Gender:",
        options=Student_Table["Gender"].unique(),
        default=Student_Table["Gender"].unique(),
    )

    SubDep = st.sidebar.multiselect(
        "Select the Department:",
        options=Student_Table["Department"].unique(),
        default=Student_Table["Department"].unique()
    )

    Mon = st.sidebar.multiselect(
        "Select the Graduation Type:",
        options=Student_Table["Graduation_Type"].unique(),
        default=Student_Table["Graduation_Type"].unique()
    )

    stream = st.sidebar.multiselect(
        "Select the Stream Type:",
        options=Student_Table["Stream_Type"].unique(),
        default=Student_Table["Stream_Type"].unique()
    )

    df_student = Student_Table[
        (Student_Table["Gender"].isin(Dep)) &
        (Student_Table["Department"].isin(SubDep)) &
        (Student_Table["Graduation_Type"].isin(Mon)) &
        (Student_Table["Stream_Type"].isin(stream))
    ]

    # KPI's For Student_table
    # TOTAL STUDENT COUNT
    student_count = df_student['Enrollement ID'].count()

    # TOTAL MEMBERSHIP COUNT
    membership_count = df_student["Membership"].dropna().count()

    # RATIO
    ratio = student_count / membership_count
    rounded_ratio = f"1:{round(ratio)}"

    conversion = membership_count/student_count * 100
    conversion_per = round(conversion)
    conversion_percentage = str(int(conversion_per)) + "%"

    first_column, second_column, third_column, fourth_column = st.columns(4)

    with first_column:
        st.markdown(
            "<h4 style='text-align: center; color: black;'>👨‍🎓👩‍🎓Total Student </h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #01b8aa;'>" +
                    str(round(student_count))+"</h4>", unsafe_allow_html=True)

    with second_column:
        st.markdown(
            "<h4 style='text-align: center; color: black;'>🎓Membership Student</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #01b8aa;'>" +
                    str(round(membership_count))+"</h4>", unsafe_allow_html=True)

    with third_column:
        st.markdown(
            "<h4 style='text-align: center; color: black;'>📉Ratio</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #01b8aa;'>" +
                    rounded_ratio+"</h4>", unsafe_allow_html=True)
    with fourth_column:
        st.markdown(
            "<h4 style='text-align: center; color: black;'> % Conversion Percentage</h4>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #01b8aa;'>" +
                    conversion_percentage+"</h4>", unsafe_allow_html=True)

# Chart - 1
student_count = df_student.groupby(['Department'])[
    "Enrollement ID"].count().reset_index(name='Enrollement ID')
df_se = df_student.groupby(['Department']).agg(
    {'Membership': 'count'}).reset_index()
membership_count = df_se["Membership"]
conversion = membership_count/student_count['Enrollement ID'] * 100
conversion_per = conversion.round()
conversion_df = pd.DataFrame(
    {'Department': student_count['Department'], 'Conversion Percentage': conversion_per})

fig = px.bar(
    data_frame=df_se,
    x="Department",
    y="Membership",
    orientation="v",
    title='<b>Each Department Membership<b>',
    text=student_count['Enrollement ID'],
    color_discrete_sequence=["#01b8aa"]
)

line = px.line(
    data_frame=conversion_df,
    x="Department",
    y="Conversion Percentage",
    title='<b>Each Department Conversion Percentage<b>',
    text=["{}%".format(int(val * 1))
          for val in conversion_df["Conversion Percentage"]],
    # text=["{}%".format(val) for val in conversion_df["Conversion Percentage"]],

    color_discrete_sequence=["#ffd700"]
)

# Add line trace to fig and update the y axis
fig.add_trace(line.data[0])

fig.update_layout(xaxis_title="Department",
                  yaxis1=dict(title="Membership Count"),
                  yaxis2=dict(title="Conversion Percentage (%)",
                              overlaying='y',
                              side='right')
                  )

# Set line trace y axis to yaxis2
fig.data[1].yaxis = 'y2'

# Set fig background color
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")

# Hide grid lines
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)

fig.update_traces(marker_color="#3EC1CD")
# Display plot
st.plotly_chart(fig, use_container_width=True)

# ***********************************************************************************************************************************************************************
# Chart 2
df_se = df_student.groupby(['Graduation_Type', 'Stream_Type']).agg({
    'Membership': 'count'}).reset_index()
fig_hourly_sales = px.bar(
    data_frame=df_se,
    x="Stream_Type",
    y=["Membership"],
    color="Graduation_Type",
    barmode='group',
    color_discrete_sequence=["#01b8aa", "#FFC107"],
    # text = 'Membership',
    title='<b>Performance of Members through Graduation Type<b>'
)

fig_hourly_sales.update_layout(xaxis_title="Branch",
                               yaxis_title="Order Count", plot_bgcolor="rgba(0,0,0,0)")
fig_hourly_sales.update_xaxes(showgrid=False)
fig_hourly_sales.update_yaxes(showgrid=False)

# ***************************************************************************************************************************************************************************
# Chart 3
# st.markdown("<h4 style='text-align: left; ;'>Membership by Gender</h4>", unsafe_allow_html=True)
df_avg_bu = df_student.groupby(["Gender"], as_index=False)[
    'Membership'].count()
fig = go.Figure(data=[go.Pie(labels=df_avg_bu['Gender'],
                             values=df_avg_bu['Membership'],
                             hole=.5,
                             marker=dict(colors=['#01b8aa', '#FFC107']))])
fig.update_layout(title={'text': "<b>Membership by Gender<b>",
                         'x': 0.5, 'xanchor': 'center'})

# fig.update_layout(height=500, width=600)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig, use_container_width=True)

# **************************************************************************************************************************************************************************
# Chart - 4

# Create bins for CGPA categories
bins = [3, 4, 5, 6, 7, 7.5, 8, 8.5, 9, 9.5, 10]
labels = ['3-4', '4-5', '5-6', '6-7', '7-7.5',
          '7.6-8', '8-8.5', '8.6-9', '9-6.5', '9.6-10']
df_student['CGPA_bin'] = pd.cut(
    df_student['CGPA'], bins=bins, labels=labels, right=False)

# Group by CGPA_bin and count the number of memberships
df_cgpa_group = df_student.groupby(df_student['CGPA_bin']).agg({
    "Membership": "count"}).reset_index()

# Create the line chart
fig = px.line(df_cgpa_group, x='CGPA_bin', y='Membership',
              title="<b>Membership by CGPA Group</b>",
              text=(df_cgpa_group['Membership']),
              color_discrete_sequence=["#01b8aa"])

fig.update_layout(xaxis_title="CGPA Group",
                  yaxis_title="Membership",
                  plot_bgcolor="rgba(0,0,0,0)",
                  yaxis=(dict(showgrid=False)),
                  xaxis=(dict(showgrid=False))
                  )
fig.update_traces(marker_color="#FFC107")

st.plotly_chart(fig, use_container_width=True)


# ************************************************************************************************************************************************************************
#  Chart - 5
df_avg_bu = df_student.groupby(["Stream_Type"], as_index=False)[
    'Membership'].count()
fig = go.Figure(data=[go.Pie(labels=df_avg_bu['Stream_Type'],
                             values=df_avg_bu['Membership'],
                             hole=.5,
                             marker=dict(colors=['#01b8aa', '#FFC107']))])
fig.update_layout(title={'text': "<b>Membership by Stream<b>",
                         'x': 0.5, 'xanchor': 'center'})


# ************************************************************************************************************************************************************************
# #chart6
df_avg_bu = df_student.groupby(["Graduation_Type"], as_index=False)[
    'Membership'].count()

fig1 = go.Figure(data=[go.Pie(labels=df_avg_bu['Graduation_Type'],
                              values=df_avg_bu['Membership'],
                              hole=.5,
                              marker=dict(colors=['#01b8aa', '#FFC107']))])
fig1.update_layout(title={'text': "<b>Membership by convocation<b>",
                          'x': 0.5, 'xanchor': 'center'})

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig1, use_container_width=True)

# ************************************************************************************************************************************************************************


# Group data by Department, Graduation_Type, Stream_Type, and Gender
df_student_grouped = df_student.groupby(['Department', 'Graduation_Type', 'Stream_Type', 'Gender']).agg({
    'Membership': 'count'}).reset_index()

# Pivot data to create a pivot table
df_student_pivot = df_student_grouped.pivot_table(index='Department', columns=[
                                                  'Graduation_Type', 'Stream_Type', 'Gender'], values='Membership', aggfunc='sum', fill_value=0)

# Plot pivot table as a heatmap
# sns.heatmap(df_student_pivot, annot=True, cmap='Blues')
plt.title("Membership by Department, Graduation_Type, Stream_Type, and Gender")

# Display pivot table in Streamlit
st.table(df_student_pivot)

# *******************************************************************************************************************************************************************************

pivot_table = pd.pivot_table(df_student, values='Membership', index=['Department'],
                             columns=['Stream_Type',
                                      'Graduation_Type', 'Gender'],
                             aggfunc='count')

# Fill NaN values with 0
pivot_table = pivot_table.fillna(0)

# Convert the pivot table to integers
pivot_table = pivot_table.astype(int)

# Reset the index and columns names
pivot_table = pivot_table.reset_index()
pivot_table.columns = pivot_table.columns.map('_'.join)

# Rename the columns for better readability
pivot_table = pivot_table.rename(columns={'Department': 'Department',
                                          'Membership_Correspondence_BA_F': 'BA_Correspondence_Female',
                                          'Membership_Correspondence_BA_M': 'BA_Correspondence_Male',
                                          'Membership_Correspondence_MA_F': 'MA_Correspondence_Female',
                                          'Membership_Correspondence_MA_M': 'MA_Correspondence_Male',
                                          'Membership_FullTime_BA_F': 'BA_FullTime_Female',
                                          'Membership_FullTime_BA_M': 'BA_FullTime_Male',
                                          'Membership_FullTime_MA_F': 'MA_FullTime_Female',
                                          'Membership_FullTime_MA_M': 'MA_FullTime_Male',
                                          })

# Display the pivot table
st.dataframe(pivot_table)
