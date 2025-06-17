import streamlit as st
import pandas as pd
import joblib

st.title("Prediksi Dropout Mahasiswa")

model = joblib.load("PrediksiModel.pkl")

with st.sidebar:
    st.header('Jaya Jaya Institute Web App')
    st.image('Gambar/Edu.png', width=250)
    st.write('Sebagai institusi pendidikan yang bermutu, Jaya Jaya Institute melopori perubahan global secara menyeluruh serta mendidik generasi yang berkualitas')

# Inisialisasi session_state
if "input_data" not in st.session_state:
    st.session_state.input_data = None

if st.session_state.input_data is None:
    with st.form("student_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            educational_special_needs = st.radio("Educational Special Needs", ["Tidak", "Ya"])
        with col2:
            debtor = st.radio("Debtor (Punya Tunggakan)", ["Tidak", "Ya"])
        with col3:
            tuition_fees_up_to_date = st.radio("Tuition Fees Up To Date (Lunas)", ["Tidak", "Ya"])

        col1, col2 = st.columns(2)
        with col1:
            scholarship_holder = st.radio("Scholarship Holder (Penerima Beasiswa)", ["Tidak", "Ya"])
        with col2:
            international = st.radio("International Student", ["Tidak", "Ya"])

        curricular_units_1st_sem_credited = st.number_input("1st Sem: SKS Diakui", min_value=0, max_value=24)
        curricular_units_1st_sem_approved = st.number_input("1st Sem: SKS Lulus", min_value=0, max_value=24)
        curricular_units_2nd_sem_credited = st.number_input("2nd Sem: SKS Diakui", min_value=0, max_value=24)
        curricular_units_2nd_sem_enrolled = st.number_input("2nd Sem: SKS Diambil", min_value=0, max_value=24)
        curricular_units_2nd_sem_approved = st.number_input("2nd Sem: SKS Lulus", min_value=0, max_value=24)

        submitted = st.form_submit_button("Submit & Predict")

        if submitted:
            # Simpan input ke session_state
            st.session_state.input_data = {
                'Educational_special_needs': 1 if educational_special_needs == "Ya" else 0,
                'Debtor': 1 if debtor == "Ya" else 0,
                'Tuition_fees_up_to_date': 1 if tuition_fees_up_to_date == "Ya" else 0,
                'Scholarship_holder': 1 if scholarship_holder == "Ya" else 0,
                'International': 1 if international == "Ya" else 0,
                'Curricular_units_1st_sem_credited': curricular_units_1st_sem_credited,
                'Curricular_units_1st_sem_approved': curricular_units_1st_sem_approved,
                'Curricular_units_2nd_sem_credited': curricular_units_2nd_sem_credited,
                'Curricular_units_2nd_sem_enrolled': curricular_units_2nd_sem_enrolled,
                'Curricular_units_2nd_sem_approved': curricular_units_2nd_sem_approved
            }

else:
    df = pd.DataFrame([st.session_state.input_data])
    st.write("Data yang Anda input:")
    st.dataframe(df)

    prediction = model.predict(df)[0]
    proba = model.predict_proba(df)[0]

    if prediction == 0:
        st.error(f"🚨 Mahasiswa diprediksi *DROP OUT*")
        col1,col2,col3=st.columns(3)
        with col2:
            st.image('Gambar/Dropout.jpeg')
    else:
        st.success(f"✅ Mahasiswa diprediksi Lulus ")
        col1,col2,col3=st.columns(3)
        with col2:
            st.image('Gambar/graduate.jpeg')
    if st.button(" Prediksi Ulang"):
        st.session_state.input_data = None
