"""
Propósito: Dividir as questões por padrão. Observa-se que ao início de cada questão tem uma faixa de alguma cor, que é o padrão de início de cada questão
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a imagem "colunas_concatenadas_verticalmente.png" do passo 6 para essa pasta do passo 7

OBS2: puxe a pasta "inteiras" do passo 5 para essa pasta do passo 7

OBS3: este código foi modificado para percorrer o penúltimo pixel da direita (largura-2) procurando por pixels azuis
OBS4: quando encontra um pixel azul (não branco), corta 35 pixels acima
OBS5: considera variações de tons de azul
"""

from PIL import Image
import os

def eh_azul(pixel_rgb, tolerancia=50):
    """
    Verifica se um pixel é azul (considerando variações)
    Retorna True se for azul, False caso contrário
    """
    r, g, b = pixel_rgb
    
    # Critérios para ser considerado azul:
    # 1. O componente azul deve ser significativamente maior que o vermelho e verde
    # 2. Não deve ser branco (componentes muito altos e equilibrados)
    
    # Verifica se não é branco (todos os componentes muito altos e próximos)
    if r > 200 and g > 200 and b > 200:
        return False
    
    # Verifica se não é preto (todos os componentes muito baixos)
    if r < 30 and g < 30 and b < 30:
        return False
    
    # Verifica se o azul é dominante
    if b > r + 30 and b > g + 30:
        return True
    
    # Verifica tons de azul mais claros (como 129, 219, 246)
    if b > 200 and g > 150 and r > 100:
        # Tons azulados claros
        if b > g and b > r:
            return True
    
    # Verifica tons de azul muito claros (como 234, 249, 254)
    if r > 200 and g > 200 and b > 200:
        # Se todos são altos mas o azul é o maior
        if b > r and b > g:
            return True
    
    return False

def encontrar_posicoes_pixels_azuis(imagem):
    """
    Encontra posições onde há pixels azuis no penúltimo pixel da direita
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # Percorre a imagem de cima para baixo
    y = 0
    while y < altura:
        # Pega o penúltimo pixel da direita (largura-2)
        pixel = pixels[largura-2, y]
        
        if len(pixel) == 4:  # RGBA
            r, g, b, a = pixel
        else:  # RGB
            r, g, b = pixel[:3]
        
        # Verifica se é azul
        if eh_azul((r, g, b)):
            # Corta 35 pixels acima do pixel azul encontrado
            posicao_corte = y - 35
            if posicao_corte < 0:  # Evitar posições negativas
                posicao_corte = 0
            
            posicoes_corte.append(posicao_corte)
            print(f"Pixel azul encontrado em y={y}, RGB({r},{g},{b}), cortando em y={posicao_corte}")
            
            # Pula para frente para evitar encontrar o mesmo pixel azul novamente
            # Pula 35 pixels para garantir que não pegamos o mesmo ponto
            y += 35
        else:
            y += 1
    
    return posicoes_corte

def dividir_imagem_por_pixels_azuis(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente cortando 35 pixels ANTES de cada pixel azul encontrado
    """
    # Abre a imagem
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    print(f"Verificando penúltimo pixel da direita (x={largura-2})")
    
    # Encontra as posições dos pixels azuis
    posicoes_corte = encontrar_posicoes_pixels_azuis(imagem)
    
    if not posicoes_corte:
        print("Nenhum pixel azul encontrado na imagem!")
        return
    
    # Remove duplicatas e ordena
    posicoes_corte = sorted(list(set(posicoes_corte)))
    print(f"Encontradas {len(posicoes_corte)} posições de corte")
    
    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Corta as seções da imagem
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        # Garantir que a posição de corte é válida
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta a seção ANTES do pixel azul
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        # Salva a imagem cortada
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # A próxima seção começa 35 pixels após o pixel azul encontrado
        posicao_anterior = posicao_corte 
    
    # Corta a seção final (após a última posição)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    # Substitua pelo caminho da sua imagem
    caminho_imagem = "colunas_concatenadas_verticalmente.png"
    
    # Substitua pelo nome da pasta de saída desejada
    pasta_saida = "colunas"
    
    # Executa a divisão
    dividir_imagem_por_pixels_azuis(caminho_imagem, pasta_saida)
    
    print("Divisão concluída!")