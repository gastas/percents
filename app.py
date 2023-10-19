import streamlit as st
import pandas as pd
import numpy as np
import extra_streamlit_components as stx
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from unidecode import unidecode


def get_manager():
    return stx.CookieManager()

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    processed_data = output.getvalue()
    return processed_data






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

st.set_page_config(page_icon="📈", page_title="Table", layout="wide")


cookie_manager = get_manager()

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

#Нормативы


#Нормативы фикс

norm_pik = 4840
norm_npo = 4180


with st.sidebar:

    uploaded_files = st.file_uploader(
        "Загрузить файл",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
        accept_multiple_files=True,
    )

    my_vars = dict()
    i = 0;
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            #file_details = {"FileName":image_file.name,"FileType":image_file.type}
            #st.write(file_details)
            #img = load_image(image_file)
            #st.image(img,height=250,width=250)
            saved_file_name = unidecode(uploaded_file.name)
            with open(saved_file_name,'wb') as f:
                f.write(uploaded_file.getbuffer())     
            #st.success("Saved File")
            #bytes_data = uploaded_file.read()
            st.write( i, ":", uploaded_file.name)
            #st.write(bytes_data)
            data = pd.read_excel(uploaded_file, skiprows=8, header=1,index_col=0)
            my_vars['r'+str(i)] = pd.read_excel(uploaded_file)
            cookie = 'saved_file'
            val = saved_file_name
            if i==0:
                cookie_manager.set(cookie, val)

            file_not_upload = 0
        else:

            st.info(
                f"""
                    👆 Загрузите .xlsx файл.
                    """
            )

            #st.stop()
            #shows = pd.read_excel("./table.xlsx")
            #my_vars['r'+str(i)] = pd.read_excel("./table.xlsx")
        i = i + 1;
    files_count = i
    st.text(" \n")
    if len(uploaded_files) == 0: 
        st.info('Загрузите .xlsx файл')
        saved_file_name = cookie_manager.get(cookie='saved_file')
        i = 0 
        data = pd.read_excel(saved_file_name, skiprows=8, header=1,index_col=0)
        files_count = 1
        file_not_upload = 1
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
with st.expander(saved_file_name): 
    st.write(data)

with st.expander("Операции %"):
    data = data.drop(columns=['Площадка', 'WMS login'])
    data['Процент'] = data['Сумма']/7150*100
    data.loc[data['Ед. изм.'] == 'час', ['Процент']] = data['Сумма']/4840*100
    data['Процент'] = data['Процент'].round(1)
    st.write(data)
    df_xlsx = to_excel(data)
    st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='table.xlsx', key='data')


with st.expander("Все %"):
    days = data.groupby(['Операционный день', 'ФИО']).agg(sum).reset_index() #Все и часы и штуки
    days = days.pivot_table(index="ФИО", columns="Операционный день", values="Процент", fill_value=0)
    days.loc['Среднее']= days[days != 0].mean(numeric_only=True, axis=0)
    days.loc[:,'Все дни']= days.sum(numeric_only=True, axis=1)
    st.write(days)
    df_xlsx = to_excel(days)
    st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='table.xlsx', key='days')


with st.expander("Ед. изм – Час", True):
    npo = data.loc[data['Ед. изм.'] == 'час']
    npo = npo.groupby(['Операционный день', 'ФИО']).agg(sum).reset_index()
    npo = npo.pivot_table(index="ФИО", columns="Операционный день", values="Процент", fill_value=0)
    npo.loc['Среднее']= npo[npo != 0].mean(numeric_only=True, axis=0)
    npo.loc[:,'Все дни']= npo.sum(numeric_only=True, axis=1)
    st.write(npo)
    df_xlsx = to_excel(npo)
    st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='часы.xlsx', key='npo')

with st.expander("Ед. изм – Штуки", True):
    exc = data.loc[(data['Ед. изм.'] >= 'час') & (data['Процент'] > 90)]
    
    sht = (data[~data.set_index(['ФИО','Операционный день']).index.isin(exc.set_index(['ФИО','Операционный день']).index)].reset_index(drop=True))
    sht = sht.loc[sht['Ед. изм.'].isin(['шт','НЗН'])]
    sht = sht.groupby(['Операционный день', 'ФИО']).agg(sum).reset_index()
    sht = sht.pivot_table(index="ФИО", columns="Операционный день", values="Процент", fill_value=0)
    sht.loc['Среднее']= sht[sht != 0].mean(numeric_only=True, axis=0)
    sht.loc[:,'Все дни']= sht.sum(numeric_only=True, axis=1)
    st.write(sht)
    df_xlsx = to_excel(sht)
    st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='штуки.xlsx', key='sht')

# with st.expander("Деньги", True):
#     m_npo = npo.astype(int)/100*4840
#     st.write(m_npo)
#     df_xlsx = to_excel(m_npo)
#     st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='часы.xlsx', key='m_npo')
#     st.markdown("""---""")
#     m_sht = sht.astype(int)/100*7150
#     st.write(m_sht)
#     df_xlsx = to_excel(m_sht)
#     st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='часы.xlsx', key='m_sht')

with st.expander("Деньги (для человека)", True):
    pay_npo = npo.astype(int)/100*3000
    st.write(pay_npo)
    df_xlsx = to_excel(pay_npo)
    st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='часы.xlsx', key='pay_npo')
    st.markdown("""---""")
    pay_sht = sht.astype(int)/100*4000
    st.write(pay_sht)
    df_xlsx = to_excel(pay_sht)
    st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='часы.xlsx', key='pay_sht')


st.write('Количество операций')

quantity = data.loc[data['Ед. изм.'].isin(['шт','НЗН'])]
quantity = quantity.groupby(['Операционный день', 'ФИО', 'Операция']).agg(sum).reset_index()
quantity = quantity.pivot_table(index=['ФИО', 'Операция'], columns=['Операционный день'], values="Количество", fill_value=0)
st.write(quantity)
df_xlsx = to_excel(quantity)
st.download_button(label='📥 Загрузить',data=df_xlsx,file_name='операции.xlsx', key='ops')
