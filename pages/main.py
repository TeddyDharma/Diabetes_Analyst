import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
import pickle
import numpy as np
#  
conn = st.experimental_connection(
    "local_db",
    type="sql",
    url="mysql://root:@localhost:3306/diabetes"
)
text_style = '''
    <style>
        p {
            text-align: justify;
        }
        h2 {
            text-align: justify;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    '''
st.markdown(text_style, unsafe_allow_html=True)
data = conn.query("SELECT * FROM diabetes LIMIT 10")

menu_app = st.sidebar.radio(
        "Pilih menu aplikasi",
        ("Home", "Visualisasi", "Prediksi"))
if menu_app == "Home":
    st.title("Aplikasi prediksi dan visualisasi data diabetes")
    st.caption("dibuat oleh teddy dharma")
    st.header("Deskripsi Singkat")
    st.write("Diabetes adalah penyakit kronis yang ditandai dengan tingginya kadar gula darah. Glukosa merupakan sumber energi utama bagi sel tubuh manusia. Akan tetapi, pada penderita diabetes, glukosa tersebut tidak dapat digunakan oleh tubuh.")
    # need to import from PIL import Image to avoid from error
    image = Image.open("../assets/images/image1.jpg")
    st.image(image, caption="ilustrasi diabetes")
    st.write("Gula yang berada di dalam darah seharusnya diserap oleh sel-sel tubuh untuk kemudian diubah menjadi energi. Insulin adalah hormon yang bertugas untuk membantu penyerapan glukosa dalam sel-sel tubuh untuk diolah menjadi energi, sekaligus menyimpan sebagian glukosa sebagai cadangan energi")
    st.write("Apabila terjadi gangguan pada insulin, seseorang berisiko tinggi mengalami diabetes. Diabetes dapat disebabkan oleh beberapa kondisi, seperti:") 
    st.write("1.Kurangnya produksi insulin oleh pankreas")
    st.write("2.Gangguan respons tubuh terhadap insulin")
    st.write("3.Adanya pengaruh hormon lain yang menghambat kinerja insulin")
    st.write("3.Adanya pengaruh hormon lain yang menghambat kinerja insulin")
    st.write("Apabila kondisi ini diabaikan dan kadar gula darah dibiarkan tinggi tanpa dikendalikan, diabetes bisa melahirkan berbagai komplikasi membahayakan.")
if menu_app == "Visualisasi":
    st.title("Menu Visualisasi 📊")
    head_data = conn.query("SELECT * FROM diabetes LIMIT 10")
    st.header("Gambaran Data")
    st.table(head_data)
    st.write("Terlihat pada data terdapat 8 features column yang akan menentukan orang terkena diabetes atau tidak")
    diabetes_patient = pd.DataFrame(conn.query("SELECT COUNT(Outcome) AS jumlah FROM  diabetes WHERE Outcome = 1"))
    non_diabetes_patient = conn.query("SELECT COUNT(Outcome) AS jumlah FROM  diabetes WHERE Outcome = 0")
    all_data = pd.DataFrame(
        {
            "label" : ["non diabetes", "diabetes"],
            "jumlah" : [non_diabetes_patient.iloc[0]['jumlah'], diabetes_patient.iloc[0]['jumlah']]
        }  
    )    
    st.bar_chart(data=all_data, x="label", y="jumlah")
    st.write("pada plot terlihat bahwa data non diabetes lebih banyak 2 kali lipat dibandingkan dengan data pasien diabates")
    # cari berdasarkan usia
    cari_usia = st.text_input("Ketik umur")
    search_button = st.button("Cari")
    if search_button: 
        query_usia_true_count = conn.query(f"SELECT COUNT(Outcome) AS jumlah FROM diabetes WHERE Outcome = 1 AND Age <= {int(cari_usia)}") 
        query_usia_false_count = conn.query(f"SELECT COUNT(Outcome) AS jumlah FROM diabetes WHERE Outcome = 1 AND Age >  {int(cari_usia)}") 
        query_usia_true = conn.query(f"SELECT Age AS sebaran FROM  diabetes WHERE Outcome = 1 AND Age <= {int(cari_usia)}") 
        query_usia_false = conn.query(f"SELECT Age AS sebaran FROM  diabetes WHERE Outcome = 1 AND Age >  {int(cari_usia)}") 
        all_data = pd.DataFrame(
            {
                "label" : [f"usia <= {cari_usia}", f"usia > {cari_usia}"],
                "jumlah" : [query_usia_true_count.iloc[0]['jumlah'], query_usia_false_count.iloc[0]['jumlah']], 
                "sebaran" : [[query_usia_true.iloc[0]['sebaran']], [query_usia_false.iloc[0]['sebaran']]],
     
            }  
        ) 
        # st.write(data)
        st.bar_chart(data=all_data, x="label", y="jumlah")
        st.write(f"terdapat {query_usia_true_count.iloc[0]['jumlah']} orang yang terkena diabetes pada usia kurang dari {cari_usia} dan terdapat {query_usia_false_count.iloc[0]['jumlah']} orang yang terkena diabetes pada usia diatas {cari_usia}")
if menu_app == "Prediksi":
    st.title("Selamat datang di menu prediksi", )
    preg  =  st.number_input("Ketik jumlah pragnencies", step=1, format='%d', min_value=0)
    glucose = st.text_input("Ketik jumlah glukosa", value="100")
    blood_pres = st.text_input("Ketik jumlah tekanan darah", value="100")
    skin_thickeness = st.text_input("Ketik skin thickness", value="1")
    insulin = st.text_input("ketik jumlah insulin", value="100")
    BMI = st.text_input("ketik jumlah insulin", value="10")
    DiabetesPedigreeFunction = st.text_input("ketik Diabetes Pedigree Function", value="1") 
    age = st.text_input("ketik usia", value="10")
    check_button = st.button("Check")
    # model = pickle.load(open("../model/SVM.sav","rb"))
    if check_button: 
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
            append_data = []
            data = [(preg),(glucose), (blood_pres),(skin_thickeness), (insulin), (BMI),(DiabetesPedigreeFunction), (age)]
            append_data = np.array(data).reshape(1, -1)
            hasil_prediksi = model.predict(append_data)
            if hasil_prediksi == "1":
                st.error("anda terkena diabetes")
            else: 
                st.success("anda tidak terkena diabetes")