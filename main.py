import streamlit as st
import ekgdata
import person
from PIL import Image 
persons = person.get_person_data()
Personenliste = [person.get_full_name() for person in persons]

st.write("# EKG APP")

st.write("## Versuchsperson auswählen")



if 'current_user' not in st.session_state:
    st.session_state.current_user = Personenliste[0] if Personenliste else "None"  # Setze den Standardwert auf die erste Person in der Liste

current_user = st.selectbox(
    'Versuchsperson',
    options=Personenliste,
    key="sbVersuchsperson",
)

st.session_state.current_user = current_user
current_person = person.get_person_object_by_full_name(st.session_state.current_user)

if current_person:
    col1, col2 = st.columns(2)

    with col2:
        st.image(
            Image.open(current_person.picture_path),
            caption=current_person.get_full_name()
        )

    with col1:
        st.write(f"Geburtsjahr: {current_person.date_of_birth}")
        st.write(f"Alter: {current_person.age}")
        st.write(f"Geschlecht: {current_person.gender}")
        st.write(f"Maximale Herzfrequenz: "f"{current_person.max_hr:.0f} BPM")

if not current_person:
    st.image("data/pictures/none.jpg", caption="Keine Person ausgewählt")

elif not current_person.ekg_tests:
    st.write("Keine EKG-Daten für diese Person vorhanden.")

else:
    ekg = ekgdata.EKGdata(current_person.ekg_tests[0])

    st.plotly_chart(ekg.plot_time_series_with_peaks())
    st.write(f"EKG Testdatum: {current_person.ekg_tests[0]['date']}")

    col2, col1 = st.columns(2)
    col2.metric("Maximale Herzfrequenz EKG", f"{ekg.max_hr():.0f} BPM")
    col1.metric("Durchschnittliche Herzfrequenz EKG", f"{ekg.estimate_hr():.1f} BPM")





 


