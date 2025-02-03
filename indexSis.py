import os
import xml.etree.ElementTree as ET
from datetime import datetime

def ler_nfces_da_pasta(pasta):
    nfces = []
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.xml'):
            caminho_completo = os.path.join(pasta, arquivo)
            try:
                tree = ET.parse(caminho_completo)
                root = tree.getroot()

                numero = root.find('.//nfe:infNFe/nfe:ide/nfe:nNF', ns)
                data_completa = root.find('.//nfe:infNFe/nfe:ide/nfe:dhEmi', ns)
                preco = root.find('.//nfe:total/nfe:ICMSTot/nfe:vNF', ns)
                status_code = root.find('.//nfe:protNFe/nfe:infProt/nfe:cStat', ns)

                if None in (numero, data_completa, preco, status_code):
                    print(f"Elemento(s) não encontrado(s) no arquivo: {arquivo}")
                    continue

                numero = numero.text
                data = data_completa.text.split('T')[0]  # Extrai apenas a data
                preco = float(preco.text)
                status_code = status_code.text

                if status_code == '100':
                    status = 'APROVADA'
                elif status_code == '110':
                    status = 'INUTILIZADA'
                elif status_code == '101':
                    status = 'CANCELADA'
                else:
                    status = 'OUTRO'

                nfces.append({
                    'numero': numero,
                    'data': data,
                    'preco': preco,
                    'status': status
                })

            except ET.ParseError:
                print(f"Erro ao analisar o arquivo XML: {arquivo}")
            except Exception as e:
                print(f"Ocorreu um erro ao processar o arquivo {arquivo}: {e}")

    return nfces

def gerar_relatorio(nfces):
    aprovadas = [nfce for nfce in nfces if nfce['status'] == 'APROVADA']
    inutilizadas = [nfce for nfce in nfces if nfce['status'] == 'INUTILIZADA']
    canceladas = [nfce for nfce in nfces if nfce['status'] == 'CANCELADA']

    total_final = sum(nfce['preco'] for nfce in aprovadas)

    with open('relatorio_nfces.txt', mode='w') as file:
        file.write("NFC-es Aprovadas:\n")
        for nfce in aprovadas:
            file.write(f"Numero: {nfce['numero']}, Data: {nfce['data']}, Preco: {nfce['preco']}\n")

        file.write("\nNFC-es Inutilizadas:\n")
        for nfce in inutilizadas:
            file.write(f"Numero: {nfce['numero']}, Data: {nfce['data']}, Preco: {nfce['preco']}\n")

        file.write("\nNFC-es Canceladas:\n")
        for nfce in canceladas:
            file.write(f"Numero: {nfce['numero']}, Data: {nfce['data']}, Preco: {nfce['preco']}\n")

        file.write(f"\nValor Total das NFC-es Aprovadas: {total_final}\n")

def main():
    pasta_nfces = 'xmls'  # Diretório onde os arquivos XML estão armazenados
    nfces = ler_nfces_da_pasta(pasta_nfces)
    if nfces:
        gerar_relatorio(nfces)
        print("Relatório gerado com sucesso!")
    else:
        print("Nenhuma NFC-e processada.")

if __name__ == "__main__":
    main()
