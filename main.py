import streamlit as st
import requests

# Configuração da página do Streamlit
st.set_page_config(page_title="Resultados Desportivos Ao Vivo", page_icon="⚽", layout="wide")

st.title("⚽ Busca de Informações Desportivas em Tempo Real")
st.write("Obtenha os resultados e notícias desportivas mais recentes.")

# Campo para introduzir a chave de API
api_key = st.text_input("Insira a sua Chave de API:", type="password")
query = st.text_input("O que deseja procurar?", placeholder="Ex: Resultados do Vasco de hoje")

if st.button("Buscar Informações"):
    if not api_key or not query:
        st.warning("Preencha a chave de API e a pesquisa.")
    else:
        with st.spinner("A processar informações do Gemini..."):
            try:
                # 1. LIMPEZA ABSOLUTA DA CHAVE
                # Remove espaços em branco e quebras de linha invisíveis
                chave_bruta = api_key.strip()
                
                # Se a palavra 'googleapis.com' estiver colada na chave, removemos completamente
                if "googleapis.com" in chave_bruta:
                    chave_limpa = chave_bruta.replace("googleapis.com", "")
                else:
                    chave_limpa = chave_bruta
                
                # 2. ENDPOINT ISOLADO (Sem parâmetros na string de texto)
                url_limpa = "https://googleapis.com"
                
                # 3. PASSAGEM DE PARÂMETROS PROTEGIDA
                # O Python codifica a chave nativamente e impede o redirecionamento para '/'
                parametros_url = {"key": chave_limpa}
                
                # Estrutura de dados (Payload) exigida pela API do Gemini
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Você é um assistente desportivo focado em dados em tempo real e atualizados de hoje. Traga as informações desportivas mais recentes e ao vivo sobre: {query}"
                        }]
                    }]
                }
                
                # 4. ENVIO SEGURO VIA HTTP POST
                response = requests.post(url_limpa, params=parametros_url, json=payload)
                
                # 5. TRATAMENTO DA RESPOSTA
                if response.status_code != 200:
                    st.error(f"Erro da API do Google (Código {response.status_code})")
                    st.text(f"Detalhes do erro emitido pelo servidor:\n{response.text}")
                else:
                    data = response.json()
                    
                    # Extração segura e estruturada utilizando índices numéricos de listas
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                            texto = candidate['content']['parts'][0]['text']
                            st.subheader("📊 Resultados Encontrados:")
                            st.markdown(texto)
                        else:
                            st.warning("A estrutura interna de conteúdo ('parts') não foi encontrada.")
                    else:
                        st.warning("Nenhum resultado foi retornado nos candidatos da API.")
                        st.json(data)
                        
            except Exception as e:
                st.error(f"Erro no processamento da requisição: {e}")
