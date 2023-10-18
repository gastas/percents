import streamlit as st
import pandas as pd
import numpy as np


###################################
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode


###################################

from functionforDownloadButtons import download_button

###################################



def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="📈", page_title="Table")

# st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/balloon_1f388.png", width=100)
#st.image(
#    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/scissors_2702-fe0f.png",
#    width=100,
#)

#    st.title("Table Tool")

# st.caption(
#     "PRD : TBC | Streamlit Ag-Grid from Pablo Fonseca: https://pypi.org/project/streamlit-aggrid/"
# )


# ModelType = st.radio(
#     "Choose your model",
#     ["Flair", "DistilBERT (Default)"],
#     help="At present, you can choose between 2 models (Flair or DistilBERT) to embed your text. More to come!",
# )

# with st.expander("ToDo's", expanded=False):
#     st.markdown(
#         """
# -   Add pandas.json_normalize() - https://streamlit.slack.com/archives/D02CQ5Z5GHG/p1633102204005500
# -   **Remove 200 MB limit and test with larger CSVs**. Currently, the content is embedded in base64 format, so we may end up with a large HTML file for the browser to render
# -   **Add an encoding selector** (to cater for a wider array of encoding types)
# -   **Expand accepted file types** (currently only .csv can be imported. Could expand to .xlsx, .txt & more)
# -   Add the ability to convert to pivot → filter → export wrangled output (Pablo is due to change AgGrid to allow export of pivoted/grouped data)
# 	    """
#     )
# 
#     st.text("")




with st.sidebar:

    uploaded_files = st.file_uploader(
        "",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
        accept_multiple_files=True,
    )

    my_vars = dict()
    i = 0;
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            #bytes_data = uploaded_file.read()
            st.write( i, ":", uploaded_file.name)
            #st.write(bytes_data)
            shows = pd.read_excel(uploaded_file)
            my_vars['r'+str(i)] = pd.read_excel(uploaded_file)
        else:
            st.info(
                f"""
                    👆 Загрузите .xlsx фил.
                    """
            )

            st.stop()
        i = i + 1;
    files_count = i
    st.text(" \n")
#start
    
    # if uploaded_file is not None:
    #     file_container = st.expander("Check your uploaded .xlsx")
    #     shows = pd.read_excel(uploaded_file)
    #     uploaded_file.seek(0)
    #     file_container.write(shows)

    # else:
    #     st.info(
    #         f"""
    #             👆 Upload a .xlsx file first.
    #             """
    #     )

    #     st.stop()

#sss

#aggrid
# from st_aggrid import GridUpdateMode, DataReturnMode


# gb = GridOptionsBuilder.from_dataframe(shows)
# # enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
# gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
# gb.configure_selection(selection_mode="multiple", use_checkbox=True)
# gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
# gridOptions = gb.build()
#end_aggrid

#Datefilter 

with st.sidebar:
    if files_count > 0:
        dates = pd.DataFrame()

        st.text(" \n \n \n")
        i = 0;
        for i in range(files_count):
            dates = my_vars['r'+str(i)]
            i = i + 1;
        dates = dates['Операционные сутки']
        dates['Операционные сутки'] = pd.to_datetime(shows['Операционные сутки'], format="%d.%m.%Y")


        min_date = min(dates['Операционные сутки'])
        max_date = max(dates['Операционные сутки'])
        calendar = st.date_input("", [min_date, max_date])
        #st.write(calendar)


with st.sidebar:
    # Фильтр по ФИО
    #workers = pd.DataFrame(["Все"], columns=['ФИО сотрудника'])
    if files_count > 0:
        #workers = workers.append(shows[['ФИО сотрудника']],ignore_index=True)
        workers = shows[['ФИО сотрудника']].copy()
        workers = workers['ФИО сотрудника'].unique()

        workers_names = st.multiselect(
        'ФИО сотрудника',workers)
       
        #st.write(workers_names)

st.text("")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Тарный", "Дзержинский КГТ", "Складочная", "Строгино", "Общий"])


with tab1:

    tarnyi_total = pd.DataFrame()

    tarnyi_operations2 = pd.DataFrame()
    tarnyi_operations3 = pd.DataFrame()
  
    

    for i in range(files_count):


        #st.write(min_date)
       # st.write(max_date)
        shows = my_vars['r'+str(i)]
        shows['Операционные сутки'] = pd.to_datetime(shows['Операционные сутки'], format="%d.%m.%Y").dt.date
        shows = shows[(shows['Операционные сутки'] >= calendar[0]) & (shows['Операционные сутки']<= calendar[1])]
        if workers_names:
            shows = shows[(shows['ФИО сотрудника'] == workers_names[0])]



        tarnyi = shows[shows['СЦ'] == 'СЦ Яндекс Маркет Тарный Дропофф']

        # response = AgGrid(
        #     tarnyi,
        #     gridOptions=gridOptions,
        #     enable_enterprise_modules=True,
        #     height=400,
        #     update_mode=GridUpdateMode.MODEL_CHANGED,
        #     data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        #     fit_columns_on_grid_load=False,
        # )

        

      #  st.write(workersday)

        tarnyi2 = tarnyi[['Кол-во сканов', 'Кол-во оплачиваемых сканов', 'Часы в операциях', 'Часы в НПО', 'Оплата за НПО', 'Всего оплата']].copy()

        # tarnyi2["Сотрудники"] = [22]

        #Количество операций

        operations = tarnyi.groupby(by=["Имя операции новое"])["Кол-во сканов"].sum()
        operations2 = tarnyi.groupby(by=["Имя операции новое"])["Кол-во оплачиваемых сканов"].sum()
        operations3 = tarnyi.groupby(by=["Имя операции новое"])["Всего оплата"].sum()

        # st.write(operations)
        # st.write(operations2)
       # tarnyi2.insert(6, "Сотрудники", workersday)

        #Человеко-дни сотрудники
        workersday = tarnyi.groupby(["Операционные сутки", "ФИО сотрудника"]).size().reset_index(name="count").shape[0]
        tarnyi2 = tarnyi2.sum(axis=0).to_frame().T
        tarnyi2['Сотрудники'] = workersday



        
        #st.write(operations)

        tarnyi_total = tarnyi_total.append(tarnyi2,ignore_index=True)

        tarnyi_operations = pd.DataFrame()

        tarnyi_operations = tarnyi_operations.append(operations,ignore_index=False)
        tarnyi_operations = tarnyi_operations.append(operations2,ignore_index=False)
        tarnyi_operations = tarnyi_operations.append(operations3,ignore_index=False)
        #st.table(tarnyi2)

        filename = uploaded_files[i].name
        with st.expander(filename):
            #st.header("Количество операций")
            #st.table(tarnyi_operations.style.format("{:.0f}").highlight_null(props="color: transparent;"))
            tarnyi_operations = tarnyi_operations.transpose()
            st.table(tarnyi_operations.style.format("{:.0f}").highlight_null(props="color: transparent;"))

       # st.table(tarnyi_total)
        #tarnyi = pd.concat([tarnyi2, tarnyi2_1], axis=1)

    tarnyi_total = tarnyi_total.transpose()    
    #tarnyi_operations = tarnyi_operations.transpose() 
    # tarnyi_operations2 = tarnyi_operations2.transpose() 
    # tarnyi_operations3 = tarnyi_operations3.transpose() 

   # st.dataframe(tarnyi_total.style.format({'Сотрудники': '{:.1f}', 'Кол-во сканов': '{:.2f}', 'Кол-во оплачиваемых сканов': '{:.1f}'}))
    st.table(tarnyi_total)

    # with st.expander("Кол-во оплачиваемых сканов"):
    #     #st.header("Количество операций")
    #     st.table(tarnyi_operations2.style.format("{:.0f}").highlight_null(props="color: transparent;"))
    # with st.expander("Всего оплата"):
    #     #st.header("Количество операций")
    #     st.table(tarnyi_operations3.style.format("{:.0f}").highlight_null(props="color: transparent;"))
    #st.table(my_vars['r1'])
    #st.table(tarnyi[r1])


    # shows['Операционные сутки'] = pd.to_datetime(shows['Операционные сутки'], format="%d.%m.%Y")
    # min_date = min(shows['Операционные сутки'])
    # max_date = max(shows['Операционные сутки'])
    # st.write(min_date)
    # d3 = st.date_input("", [min_date, max_date])
    # st.write(d3)

with tab2:

    dzerzh_total = pd.DataFrame()

    for i in range(files_count):

        shows = my_vars['r'+str(i)]

        dzerzh = shows[shows['СЦ'] == 'СЦ МК Дзержинский КГТ']

        dzerzh2 = dzerzh[['Кол-во сканов', 'Кол-во оплачиваемых сканов', 'Часы в операциях', 'Часы в НПО', 'Оплата за НПО', 'Всего оплата']].copy()
        #Человеко-дни сотрудники
        workersday = dzerzh.groupby(["Операционные сутки", "ФИО сотрудника"]).size().reset_index(name="count").shape[0]
        dzerzh2 = dzerzh2.sum(axis=0).to_frame().T
        dzerzh2['Сотрудники'] = workersday

        dzerzh_total = dzerzh_total.append(dzerzh2,ignore_index=True)

        #st.table(dzerzh2)

    dzerzh_total = dzerzh_total.transpose()    
    st.table(dzerzh_total)

with tab3:

    sklado_total = pd.DataFrame()

    for i in range(files_count):

        shows = my_vars['r'+str(i)]

        sklado = shows[shows['СЦ'] == 'СЦ Яндекс.Маркет МСК Складочная']

        sklado2 = sklado[['Кол-во сканов', 'Кол-во оплачиваемых сканов', 'Часы в операциях', 'Часы в НПО', 'Оплата за НПО', 'Всего оплата']].copy()
        #Человеко-дни сотрудники
        workersday = sklado.groupby(["Операционные сутки", "ФИО сотрудника"]).size().reset_index(name="count").shape[0]
        sklado2 = sklado2.sum(axis=0).to_frame().T
        sklado2['Сотрудники'] = workersday
        sklado_total = sklado_total.append(sklado2,ignore_index=True)

        #st.table(sklado2)

    sklado_total = sklado_total.transpose()    
    st.table(sklado_total)



    # sklado = shows[shows['СЦ'] == 'СЦ Яндекс.Маркет МСК Складочная']

    # # response_d = AgGrid(
    # #     sklado,
    # #     gridOptions=gridOptions,
    # #     enable_enterprise_modules=True,
    # #     height=400,
    # #     update_mode=GridUpdateMode.MODEL_CHANGED,
    # #     data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    # #     fit_columns_on_grid_load=False,
    # # )

    # sklado2 = sklado[['Кол-во сканов', 'Кол-во оплачиваемых сканов', 'Часы в операциях', 'Часы в НПО', 'Оплата за НПО', 'Всего оплата']].copy()
    # sklado2 = sklado2.sum(axis=0)
    # sklado2.columns = ["Name", "filename"]

    # st.table(sklado2)    
with tab4:

    strogino_total = pd.DataFrame()

    for i in range(files_count):

        shows = my_vars['r'+str(i)]

        strogino = shows[shows['СЦ'] == 'СЦ Яндекс.Маркет Строгино']

        strogino2 = strogino[['Кол-во сканов', 'Кол-во оплачиваемых сканов', 'Часы в операциях', 'Часы в НПО', 'Оплата за НПО', 'Всего оплата']].copy()
        #Человеко-дни сотрудники
        workersday = strogino.groupby(["Операционные сутки", "ФИО сотрудника"]).size().reset_index(name="count").shape[0]
        strogino2 = strogino2.sum(axis=0).to_frame().T
        strogino2['Сотрудники'] = workersday
        strogino_total = strogino_total.append(strogino2,ignore_index=True)

        #st.table(strogino2)

    strogino_total = strogino_total.transpose()    
    st.table(strogino_total)


    # strogino = shows[shows['СЦ'] == 'СЦ Яндекс.Маркет Строгино']

    # # response_d = AgGrid(
    # #     strogino,
    # #     gridOptions=gridOptions,
    # #     enable_enterprise_modules=True,
    # #     height=400,
    # #     update_mode=GridUpdateMode.MODEL_CHANGED,
    # #     data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    # #     fit_columns_on_grid_load=False,
    # # ) 

    # strogino2 = strogino[['Кол-во сканов', 'Кол-во оплачиваемых сканов', 'Часы в операциях', 'Часы в НПО', 'Оплата за НПО', 'Всего оплата']].copy()
    # strogino2 = strogino2.sum(axis=0)

    # st.table(strogino2) 

with tab5:

    vsego_total = pd.DataFrame()

    for i in range(files_count):

        shows = my_vars['r'+str(i)]

        vsego = shows

        # response = AgGrid(
        #     tarnyi,
        #     gridOptions=gridOptions,
        #     enable_enterprise_modules=True,
        #     height=400,
        #     update_mode=GridUpdateMode.MODEL_CHANGED,
        #     data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        #     fit_columns_on_grid_load=False,
        # )

        vsego2 = vsego[['Кол-во сканов', 'Кол-во оплачиваемых сканов', 'Часы в операциях', 'Часы в НПО', 'Оплата за НПО', 'Всего оплата']].copy()
        #Человеко-дни сотрудники
        workersday = vsego.groupby(["Операционные сутки", "ФИО сотрудника"]).size().reset_index(name="count").shape[0]
        vsego2 = vsego2.sum(axis=0).to_frame().T
        vsego2['Сотрудники'] = workersday
        vsego_total = vsego_total.append(vsego2,ignore_index=True)


        #st.table(tarnyi2)

       # st.table(tarnyi_total)
        #tarnyi = pd.concat([tarnyi2, tarnyi2_1], axis=1)

    vsego_total = vsego_total.transpose()   

    st.table(vsego_total)
    #st.table(my_vars['r1'])
    #st.table(tarnyi[r1])


    #st.write(tarnyi_total)


st.text("")



