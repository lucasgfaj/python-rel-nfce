import os
import xml.etree.ElementTree as ET
from datetime import datetime

def ler_nfces_da_pasta(pasta):
    nfces = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.xml'):
            caminho_completo = os.path.join(pasta, arquivo)
            tree = ET.parse(caminho_completo)
            root = tree.getroot()
            
            # Namespaces necessários para acessar os elementos
            ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

            numero = root.find('.//nfe:infNFe/nfe:ide/nfe:nNF', ns).text
            data_completa = root.find('.//nfe:infNFe/nfe:ide/nfe:dhEmi', ns).text
            data = data_completa.split('T')[0]  # Extrai apenas a data
            
            preco = float(root.find('.//nfe:total/nfe:ICMSTot/nfe:vNF', ns).text)
            status_code = root.find('.//nfe:protNFe/nfe:infProt/nfe:cStat', ns).text
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
    gerar_relatorio(nfces)
    print("Relatório gerado com sucesso!")

if __name__ == "__main__":
    main()
