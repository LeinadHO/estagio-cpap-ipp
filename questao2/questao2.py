# Importação das bibliotecas utilizadas
import pandas as pd
from pathlib import Path

# Carregamento dos dados do arquivo
dados_carnaval_2018 = pd.read_csv('Agenda_BL_Rua_Carnaval_Rio-2018_Imprensa.csv', sep=';')

# Padronização dos dados carregados
dados_carnaval_2018 = dados_carnaval_2018.drop(columns=['Unnamed: 12'])
dados_carnaval_2018.columns = ['bloco', 'bairro', 'regiao', 'data', 'data_relativa', 'concentracao', 'desfile', 'final', 'local_da_concentracao', 'percurso', 'publico_estimado', 'ano_primeiro_desfile']
dados_carnaval_2018['bairro'] = dados_carnaval_2018['bairro'].astype(str).str.strip().str.capitalize()
dados_carnaval_2018['bloco'] = dados_carnaval_2018['bloco'].astype(str).str.strip()
dados_carnaval_2018['data'] = pd.to_datetime(dados_carnaval_2018['data'], dayfirst=True)

# Listagem dos bairros disponíveis para busca 
bairros = sorted(dados_carnaval_2018['bairro'].dropna().unique())
print("* Bairros disponíveis para busca:")
for bairro in bairros:
    print("-", bairro)

continuar = True
while continuar:
    bairro_escolhido = input("\nDigite o nome exato do bairro que deseja consultar: ").strip()

    # Filtragem e correção de erros de entrada
    df_bairro_escolhido = dados_carnaval_2018[dados_carnaval_2018['bairro'].str.lower() == bairro_escolhido.lower()].copy()

    if df_bairro_escolhido.empty:
        print(f"Nenhum bloco encontrado para o bairro '{bairro_escolhido}'")
        continue
    
    # Agrupamento dos blocos por data de realização
    resultados = df_bairro_escolhido.groupby(df_bairro_escolhido['data'].dt.date)['bloco'].apply(list).reset_index(name="blocos")

    # Exibição dos resultados de busca no terminal
    print(f"\nBlocos encontrados no bairro '{bairro_escolhido}':\n")
    for _, linha in resultados.iterrows():
        data = linha['data']
        blocos = ", ".join(linha['blocos'])
        print(f"{data}: {blocos}")
    
    # Exportação dos dados em um arquivo .csv (se desejado)
    opcao = input("\nDeseja exportar os resultados para um arquivo .csv? (s/n): ").strip().lower()
    possiveis_opcoes_afirmativas = ["s", "sim", "y", "yes"]
    for opcao_possivel in possiveis_opcoes_afirmativas:
        if opcao == opcao_possivel:
            caminho_arquivo = Path(f"blocos_{bairro_escolhido.lower().replace(' ', '_')}.csv")
            resultados.to_csv(caminho_arquivo, index=False)
            print(f"Arquivo salvo em {caminho_arquivo.resolve()}")
    
    # Definição da continuidade do loop
    opcao = input("\nDeseja continuar fazendo buscas? (s/n): ").strip().lower()
    continuar = opcao in possiveis_opcoes_afirmativas

