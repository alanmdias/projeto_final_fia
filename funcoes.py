# Função para gerar a URL do path
def gerar_path(base, 
               categoria: Optional[str] = "",
               metodo: Optional[str] = "", 
               sufix: Optional[str] = "", 
               parametro: Optional[str] = "",
               auth: Optional[str] = "",
               token: Optional[str] = ""):
    
    if token != "":
        path = base + "/" + auth + "?token=" + token # Corrigindo como gerar URL de autenticação
    elif metodo == "":
        path = base + "/" + categoria
    elif sufix == "":
        path = base + "/" + categoria + "/" + metodo    
    else:
        path = base + "/" + categoria + "/" + metodo + "?" + sufix + "=" + parametro
    return path


# Função para obter dados, agora reutilizando a sessão
def get_dados(session, 
         base, 
         categoria,
         token: Optional[str] = "",
         metodo: Optional[str] = "", 
         sufix: Optional[str] = "",
         auth: Optional[str] = "", 
         parametro: Optional[str] = ""):

    # Corrigindo o path para autenticação
    path_auth = gerar_path(base, auth="Login/Autenticar", token=token)
    
    auth_response = session.post(path_auth)
    
    # Verifica se a autenticação foi bem-sucedida
    if auth_response.text == "true":
        print("Autenticacao realizada com sucesso!")
        
        # Gerar o path para buscar os dados
        path_get = gerar_path(base, categoria, metodo, sufix, parametro, token="")
        response_get = session.get(path_get)
        
        if response_get.status_code == 200:
            dados = response_get.json()
            return dados
        else:
            print(f"Erro na requisicao de dados: {response_get.status_code}")
            return None
    else:
        print("Falha na autenticacao:", auth_response.text)
        return None
    
# Função para salvar o arquivo json
def salvar_json(dados, path, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    return "Arquivo salvo com sucesso!"

# Função para renomear as chaves do dicionário
def renomear_chaves(dado, mapa):
    if isinstance(dado, dict):
        return {mapa.get(k, k): renomear_chaves(v, mapa) for k, v in dado.items()}
    elif isinstance(dado, list):
        return [renomear_chaves(item, mapa) for item in dado]
    else:
        return dado