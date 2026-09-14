import streamlit as st
import requests

st.set_page_config(page_title="Resultados Desportivos Ao Vivo", page_icon="⚽", layout="wide")

st.title("⚽ Busca de Informações Desportivas em Tempo Real")
st.write("Obtenha os resultados e notícias desportivas mais recentes.")

# Campo para digitar a chave pura (Ex: AQ.ab8rn6...)
api_key = st.text_input("AQ.Ab8RN6LRVXTnfUKdoTqVNbE1FA1T-AFq2gPfiQzNnmUBZuSAMA", type="password")
query = st.text_input("O que deseja procurar?", placeholder="Ex: Resultados dos jogos de hoje")

if st.button("Buscar Informações"):
    if not api_key or not query:
        st.warning("Preencha a chave de API e a pesquisa.")
    else:
        with st.spinner("A processar..."):
            try:
                # Remove espaços e força o texto a ficar limpo
                texto_chave = api_key.strip()
                
                # SEgurança Máxima: Se o Streamlit injetar 'googleapis.comaq...' à força,
                # nós removemos o texto intruso e deixamos apenas a chave pura 'aq...'
                if "googleapis.com" in texto_chave:
                    chave = texto_chave.replace("googleapis.com", "")
                else:
                    chave = texto_chave

                # Montagem direta usando APENAS a chave corrigida
                url = f"https://googleapis.com{chave}"

                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Você é um assistente desportivo em tempo real. Forneça as informações desportivas mais recentes e resultados ao vivo de hoje sobre: {query}"
                        }]
                    }]
                }
                
                response = requests.post(url, json=payload)
                
                if response.status_code != 200:
                    st.error(f"Erro da API do Google (Código {response.status_code})")
                    st.text(f"Detalhes: {response.text}")
                else:
                    data = response.json()
                    
                    # Leitura segura dos índices da lista de resposta do Gemini
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
