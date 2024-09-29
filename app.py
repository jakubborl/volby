
import streamlit as st
import pandas as pd 
import plotly.express as px
# Funkce pro zadání názvů stran
def strana(x):
    
    strany = []
    with st.form(key='my_form'):  # Vytvoříme formulář
        for i in range(1, x+1):
            strana = st.text_input(f"Zadejte název {i}. strany:", key=f"strana_{i}")
            strany.append(strana)
        # Tlačítko pro odeslání formuláře
        submit_button = st.form_submit_button(label='Odeslat')
    
    if submit_button:
        # Uložení hodnot do session_state
        
        st.session_state.first_form_submitted = True  # Označíme, že první formulář byl odeslán
        st.success(f", ".join(strany))  # Zobrazení zprávy po odeslání
    
    return strany, submit_button



def volici():        
    pocet_volicu = []
    with st.form(key=f"my_form2"):
        for i in enumerate(nazvy_stran, 1):
            pocet_lidi = st.number_input(f"Zadej kolik lidí volilo stranu {i}", key=f"pocetlidi{i}", step=1)
            pocet_volicu.append(pocet_lidi)
        submit_button2 = st.form_submit_button(label=f'Odeslat')

    if submit_button2:
        st.session_state.feedback_submitted = True  # Označíme, že zpětná vazba byla odeslána
        st.success(f"Celkem volilo {pocet_volicu[1] + pocet_volicu[0]} lidí. ")
        
        
    return pocet_volicu, submit_button2


# Hlavní část aplikace
st.title("Výpočet volebního průzkumu")



# Uživatelský vstup pro počet stran
pocet_stran = st.number_input("Zadejte počet stran (2-5):", min_value=2, max_value=5, step=1)

if 'first_form_submitted' not in st.session_state:
    st.session_state.first_form_submitted = False
if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False




nazvy_stran, submitted = strana(pocet_stran)
if st.session_state.first_form_submitted:
    pocet_volicu, tlacitko = volici()
    if tlacitko:
        data = {
        'X': nazvy_stran,
        'Y': pocet_volicu
        }
        df = pd.DataFrame(data)

        # Vytvoření sloupcového grafu a změna barvy sloupců
        fig = px.bar(df, x='X', y='Y', title='Graf volebních výsledků')  # Změna barvy sloupců

        # Změna velikosti a stylu písma pomocí update_layout
        fig.update_layout(
            xaxis_title_font_size=25,
            yaxis_title_font_size=25,
            xaxis=dict(
            title="Politické strany",
            tickfont=dict(size=18),  # Velikost textu na ose X
            ),
            yaxis=dict(
                title="Počet voličů",
                tickfont=dict(size=20),  # Velikost textu na ose Y
            ),
            title_font_size=24,  # Velikost písma titulku
            )

        # Zobrazení grafu ve Streamlit
        st.plotly_chart(fig)
