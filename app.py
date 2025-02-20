import streamlit as st
import random 
import requests

st.set_page_config(
    page_title="Pokedex", 
    page_icon="🔥",
    layout="centered")


#funcion para obtener datos de un pokemon
def get_pokemon_data(pokemon_name):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None
    

#funcion para obtener un pokemon aleatorio
def get_random_pokemon():
    random_id = random.randint(1, 898)
    return get_pokemon_data(str(random_id))

#titulo y descripcion
st.title("🔥 Explorador de Pokemon")
st.markdown("Este es un explorador de Pokemon, puedes buscar un Pokemon por su nombre o ver un Pokemon aleatorio.")

#crear dos columnas para la busqueda y el pokemon 
col1, col2 = st.columns([2, 1])
                        
#columna de busqueda 

with col1:
    pokemon_name = st.text_input("Imgresa el nombre del Pokemon", "")

with col2:
    random_pokemon = st.button("Pokemon Aleatorio 🎲")


pokemon_data = None

#manejar la busqueda o el boton de pokemon aleatorio
if pokemon_name:
    pokemon_data = get_pokemon_data(pokemon_name)
elif random_pokemon:
    pokemon_data = get_random_pokemon()


#mostrar los datos del pokemon
if pokemon_data:
    #crear dos columnas para la imagen y la informacion
    img_col, info_col = st.columns([2, 1])

    with img_col:
        #mostrar la imagen del pokemon
        st.image(
            pokemon_data["sprites"]["other"]["official-artwork"]["front_default"],
            caption=f"#{pokemon_data['id']} {pokemon_data['name'].title()}",
            use_container_width=True
        )   
    with info_col:
        #información básica
        st.subheader ("Información Básica")
        st.write(f"**Nombre:** {pokemon_data['name'].title()}")
        st.write(f"**Altura:** {pokemon_data['height']/10} m")
        st.write(f"**Peso:** {pokemon_data['weight']/10} kg")
        st.write(f"**Experiencia Base:** {pokemon_data['base_experience']}")
        st.write(f"**Orden:** {pokemon_data['order']}")

    #estadisticas
    st.subheader("Estadísticas")
    stats_cols = st.columns(3)
    stats = pokemon_data["stats"]

    for idx, stat in enumerate(stats):
        col_idx = idx % 3
        with stats_cols[col_idx]:
            st.metric(
                label=stat["stat"]["name"].replace("-", " ").title(),
                value=stat["base_stat"]
            )        
            
    #habilidades
    st.subheader("Habilidades")
    abilities = [ability["ability"]["name"].replace("-", " ").title() 
                for ability in pokemon_data["abilities"]]
    for ability in abilities:
        st.write(f"⭐ {ability}")

elif pokemon_name or random_pokemon:
    st.error("Pokemon no encontrado. Intenta de nuevo.")
else:
    st.info(" 👆 Ingresa el nombre de un Pokemon o presiona el boton para un Pokemon aleatorio.")