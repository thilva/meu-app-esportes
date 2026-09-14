import streamlit as st
import requests

st.set_page_config(page_title="Resultados Desportivos Ao Vivo", page_icon="⚽", layout="wide")

st.title("⚽ Busca de Informações Desportivas em Tempo Real")
st.write("Obtenha os resultados e notícias desportivas mais recentes.")

# Campo para digitar a chave
api_key = st.text_input("Insira a sua Chave de API:", type="password")
query = st.text_input("O que deseja procurar?", placeholder="Ex: Resultados dos jogos de hoje")

if st.button("Buscar Informações"):
    if not api_key or not query:
        st.warning("Preencha a chave de API e a pesquisa.")
    else:
        with st.spinner("A processar..."):
            try:
                # 1. TRATAMENTO RADICAL DA CHAVE
                texto_bruto = api_key.strip()
                
                # Procuramos apenas onde começa o prefixo real 'aq.' ou 'AIza'
                if "aq." in texto_bruto.lower():
                    posicao = texto_bruto.lower().find("aq.")
                    chave_limpa = texto_bruto[posicao:]
                elif "aiza" in texto_bruto.lower():
                    posicao = texto_bruto.lower().find("aiza")
                    chave_limpa = texto_bruto[posicao:]
                else:
                    chave_limpa = texto_bruto
                
                # 2. URL BASE PROTEGIDA (Sem variáveis misturadas no domínio)
                url_base = "https://googleapis.com"
                url_final = f"{url_base}?key={chave_limpa}"
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Você é um assistente desportivo em tempo real. Forneça as informações desportivas mais recentes e resultados ao vivo de hoje sobre: {query}"
                        }]
                    }]
                }
                
                # 3. Envio da requisição utilizando a URL corrigida à força
                response = requests.post(url_final, json=payload)
                
                if response.status_code != 200:
                    st.error(f"Erro da API do Google (Código {response.status_code})")
                    st.text(f"Detalhes: {response.text}")
                else:
                    data = response.json()
                    
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                            texto = candidate['content']['parts'][0]['text']
                            st.subheader("📊 Resultados Encontrados:")
                            st.markdown(texto)
                        else:
                            st.warning("Estrutura de conteúdo não encontrada na resposta.")
                    else:
                        st.warning("Nenhum resultado retornado.")
                        
            except Exception as e:
                st.error(f"Erro no processamento: {e}")

