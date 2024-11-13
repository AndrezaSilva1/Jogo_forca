import os
import random
import time
from typing import List

class JogoDaForca:
    def __init__(self, vidas:int=3,pontos:int=0):
        """Inicializa jogo da forca com numero de vida e ponto

        Args:
            vidas (int):numero de vidas do jogador
            pontos (int):pontos acumulados do jogador
        """
        self.vidas=vidas #vidas restantes do jogador
        self.pontos=pontos #pontos jogador
        self.palavra_certa=[] #palavra que vai ser advinhada
        self.palavra_exibida=[]  #representacao atual da palavra
        self.tentativas_restantes=0 #tentativas para advinhar
        self.letras_erradas=0 #contador letras erradas
        self.total_letras_certas=0 #contador letras certas

    def limpar_tela(self)->None:
        """Limpa terminal

        utilizando comandos para sistema Windows e Unix
        """
        if os.name=='nt':
            os.system('cls') #comando limpar Windows
        else:
            os.system('clear') #comando limpar Linux/Mac

    def cabecalho(self)->None:
        """mostra o cabecalho do jogo"""
        print("***** JOGO DA FORCA COM PYTHON *****")

    def placar(self)->None:
        """mostrar o placar atual do jogo"""
        self.cabecalho() #chama função para exibir cabeçalho
        print(f"Vidas: {self.vidas} | Letras certas: {self.total_letras_certas} | Letras erradas: {self.letras_erradas}")
        print(f"Tentativas restantes: {self.tentativas_restantes} | Pontos: {self.pontos}")
        print("ACERTE A PALAVRA ABAIXO")
        print("".join(self.palavra_exibida)) #mostra a palavra com letras advinhadas

    def game_over(self)->bool:
        """mostrar Game Over perguntar se o jogador que jogar novamente

        Returns:
            bool:retorna True se o jogador jogar de novo e False ao contrario
        """
        print("========")
        print("GAME OVER")
        print("========")
        return self.pergunta("Deseja jogar novamente? [S/N]: ")

    def pergunta(self,alternativa:str,erro:str="Digite S para sim e N para não")->bool:
        """perguntas com opção 'sim' e 'não'.

        Args:
            alternativa(str):pergunta a ser feita pelo jogador 
            erro(str):mensagem de erro ser a entrada for invalida

        Returns:
            bool:retorna True resposta for 'S' e false se for 'N'
        """
        resultado = ''
        while resultado not in ['S', 'N']:
            resultado = input(alternativa).upper()
            if resultado=='S':
                return True
            elif resultado=='N':
                return False
            else:
                print(erro)

    def jogada(self,alternativa:str)->str:
        """entrada usuário e volta o primeiro caractere digitado

        Args:
            alternativa (str):mensagem a ser exibida ao jogador

        Returns:
            str:caractere digitado pelo jogador
        """
        while True:
            digitou=input(alternativa) #ler entrada do jogar
            if len(digitou)>0: #verifica o jogador digitou algo
                return digitou[0].lower() #inicia primeira letra em minúscula
            else:
                print("Certifique-se de digitar um valor.") #mensagem erro tiver entrada for vazia

    def carregar_palavras(self, nome_arquivo: str) -> List[str]:
        """carrega palavras de arquivo e voltar lista de palavras

        Args:
            nome_arquivo (str): Nome arquivo das palavras serão carregadas

        Returns:
            List[str]: Lista de palavras  completa
        """
        palavras=[]
        try:
            with open(nome_arquivo, 'r') as arquivo:
                palavras = [linha.strip().lower() for linha in arquivo] #ler palavra e adcionar maisculas
        except FileNotFoundError:
            print(f"Arquivo {nome_arquivo} não encontrado.") #mensagem de erro,arquivo nao for achado
        return palavras

    def salvar_palavras(self,nome_arquivo:str,palavras:List[str])->None:
        """salva palavra arquivo por linha

        Args:
            nome_arquivo (str):nome do arquivo palavras salvas
            palavras (List[str]):lista de palavra serem salvas
        """
        with open(nome_arquivo,'w') as arquivo:
            for palavra in palavras:
                arquivo.write(palavra + '\n') #escreve palavra uma nova linha

    def gerenciador_palavra(self)->List[str]:
        """gerenciador adição de palavras, permitindo usuário insira novas palavras.

        Returns:
            List[str]:lista palavra adcionada ao usuario
        """
        self.cabecalho()
        palavras_recebidas = []
        while True:
            palavras=input("Digite uma palavra:").lower() #le nova palavra ao jogador
            if "_" in palavras: #verifica se a palavra contém underlines
                print("Underlines não são permitidos em palavras para o jogo!")
            else:
                palavras_recebidas.append(palavras) #adicionar a palavra lista
                if not self.pergunta("Deseja adicionar outra palavra? [S/N]: "):
                    break #sai do loop se o jogador não quiser adicionar mais palavras
        self.salvar_palavras('palavras.txt', palavras_recebidas) #salvar palavras no arquivo
        return palavras_recebidas

    def selecionar_palavra(self, palavras: List[str]) -> str:
        """selecionar palavra aleatoria a lista de palavra

        Args:
            palavras (List[str]):lista de palavra restante

        Returns:
            str:palavra selecionada aleatoriamente
        """
        return random.choice(palavras) #voltar a palavra aleatoria a lista

    def quantidade_tentativas(self, palavra_jogo: str) -> int:
        """quantidade de tentativas baseadas no tamanho da palavra

        Args:
            palavra_jogo (str):palavra que vai ser jogadar

        Returns:
            int:numero tentativas do jogador
        """
        return max(2, len(palavra_jogo) // 3) #retorna o número mínimo de 2 ou 1/3 tamanho palavra

    def letras_certas(self, palavra_jogo: str) -> str:
        """quantidade de letras certas palavra

        Args:
            palavra_jogo (str):palavra correta mostrada

        Returns:
            str:representação da palavra letras importantes
        """
        self.palavra_exibida = ['_'] * len(palavra_jogo) #palavra exibida com underscores
        quantidade_letra = len(palavra_jogo) // 2 #calcula quantas letras expor 
        for i in range(quantidade_letra):
            self.palavra_exibida[i] = palavra_jogo[i] #mostrar primeira letra palavra
        return self.palavra_exibida

    def jogo(self) -> None:
        """ logica  jogo

        função controla fluxo do jogo, gerenciando tentativas e verificar o jogador ganhou ou perdeu
        """
        self.total_letras_certas = 0  #resetar letras certas para novo jogo
        self.letras_erradas = 0       #resetar letras erradas para novo jogo
        self.palavra_certa = self.selecionar_palavra(self.carregar_palavras('palavras.txt')) #determinar palavra aleatoria
        self.letras_certas(self.palavra_certa) #prepara palavra exibida
        self.tentativas_restantes = self.quantidade_tentativas(self.palavra_certa) #estabelece numero tentativas
        
        while self.tentativas_restantes >- 0:
            self.placar() #placar atual
            letra=self.jogada("Digite uma letra: ") #reivindicar letra jogador
            acertou = letra in self.palavra_certa #validam letra palavra correta
            if acertou:
                for i in range(len(self.palavra_certa)):
                    if letra == self.palavra_certa[i] and self.palavra_exibida[i] == '_': 
                        self.palavra_exibida[i] = letra  #alterar palavra
                        self.total_letras_certas += 1 #acrescentar contador letras 
                if '_' not in self.palavra_exibida:
                    self.pontos += 10 #acrescentar pontos jogador                   
                    self.placar()
                    print(f"Você ganhou! A palavra era: {self.palavra_certa}")
                    break  #loop se o jogador advinhou a palavra
            else:
                self.letras_erradas += 1
                self.tentativas_restantes -= 1
                print(f"A letra '{letra}' não está na palavra.")

        if self.tentativas_restantes == 0:
            self.vidas -= 1
            self.placar()
            print(f"Você perdeu! A palavra era: {self.palavra_certa}")
            if self.vidas == 0:
                print("Fim de todas as vidas. Game Over!")
            return

def main()->None:
    """Função principal para executar o jogo da forca"""
    jogo=JogoDaForca() #cria uma instância jogo
    while True:
        jogo.jogo() #executa jogo
        if not jogo.game_over(): #pergunta jogador deseja jogar novamente
            break #loop se o jogador não quiser jogar

if __name__ == '__main__':
    main() #chama função principal do jogo