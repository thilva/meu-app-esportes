import streamlit as st
import requests

st.set_page_config(page_title="Resultados Desportivos Ao Vivo", page_icon="⚽", layout="wide")

st.title("⚽ Busca de Informações Desportivas em Tempo Real")
st.write("Obtenha os resultados e notícias desportivas mais recentes.")

# Campo de captura da chave de API
api_key = st.text_input("Insira a sua Chave de API:", type="password")
query = st.text_input("O que deseja procurar?", placeholder="Ex: Resultados do Vasco de hoje")

if st.button("Buscar Informações"):
    if not api_key or not query:
        st.warning("Preencha a chave de API e a pesquisa.")
    else:
        with st.spinner("A processar informações do Gemini..."):
            try:
                # 1. TRATAMENTO DA CHAVE
                texto_bruto = api_key.strip()
                
                # Se o texto contiver o domínio antigo por erro, removemos aqui
                if "googleapis.com" in texto_bruto:
                    chave_limpa = texto_bruto.replace("googleapis.com", "")
                else:
                    chave_limpa = texto_bruto
                
                # 2. A CORREÇÃO EXATA DA URL (Com todas as barras e parâmetros obrigatórios)
                url = f"https://googleapis.com{chave_limpa}"
                
                # 3. PAYLOAD ESTRUTURADO DE ACORDO COM A DOCUMENTAÇÃO
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Você é um assistente esportivo focado em dados em tempo real. Traga informações recentes e notícias atualizadas sobre: {query}"
                        }]
                    }]
                }
                
                # 4. ENVIO DA REQUISIÇÃO
                response = requests.post(url, json=payload)
                
                if response.status_code != 200:
                    st.error(f"Erro da API do Google (Código {response.status_code})")
                    st.text(f"Detalhes: {response.text}")
                else:
                    data = response.json()
                    
                    # 5. EXTRAÇÃO ROBUSTA PROTEGIDA CONTRA ERROS DE ÍNDICE
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
                        st.json(data) # Mostra o JSON recebido para análise caso venha vazio
                        
            except Exception as e:
                st.error(f"Erro no processamento da requisição: {e}")
