
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
    procenta = []
    with st.form(key=f"my_form2"):
        for i in enumerate(nazvy_stran, 1):
            pocet_lidi = st.number_input(f"Zadej kolik lidí volilo stranu {i}", key=f"pocetlidi{i}", step=1)
            
            pocet_volicu.append(pocet_lidi)
        submit_button2 = st.form_submit_button(label=f'Odeslat')

    if submit_button2:
        st.session_state.feedback_submitted = True  # Označíme, že zpětná vazba byla odeslána
        st.success(f"Celkem volilo {sum(pocet_volicu)} lidí. ")
        
        
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
    seznam_procent = []
    
    
    
    if tlacitko:
        for i in range(len(nazvy_stran)):
            vypocet = pocet_volicu[i] / sum(pocet_volicu) * 100
            zvypocet = round(vypocet, 1)
            seznam_procent.append(zvypocet)
        data = {
            'X': nazvy_stran,
            'Y': [p / 100 for p in seznam_procent],  # Převod hodnot na desetiny pro osu Y
            'Text': seznam_procent  # Hodnoty v procentech pro text nad sloupci
        }
        df = pd.DataFrame(data)
        
        # Vytvoření sloupcového grafu
        fig = px.bar(df, x='X', y='Y', title='Graf volebních výsledků')

        # Zobrazení hodnot nad sloupci s procenty
        fig.update_traces(texttemplate='%{customdata}%', textposition='outside', customdata=df['Text'])

        # Upravení osy Y a vzhledu grafu
        fig.update_layout(
            xaxis_title_font_size=25,
            yaxis_title_font_size=25,
            xaxis=dict(
                title="Politické strany",
                tickfont=dict(size=18),
            ),
            yaxis=dict(
                title="Procenta voličů",
                tickfont=dict(size=20),
                range=[0, 0.5],  # Rozsah od 0 do 1 (100 %)
                tickformat=".0%"  # Osa Y zobrazuje procenta
            ),
            title_font_size=24,
        )
        
        # Zobrazení grafu ve Streamlit
        st.plotly_chart(fig)