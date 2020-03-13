# Hunt The Wumpus

	No jogo, o jogador se encontra em uma caverna escura carregando sua arma e uma única bala afim de matar o mostro chamado Wumpus.
	Entretanto, ele terá que passar por diversos buracos sem fim seguindo apenas os seus sentidos para saber a direção que se encontra o monstro e efetuar seu único disparo.
	
---

## Ambiente wumpus

  ### Criando o ambiente virtual
  Execute o seguinte comando na raiz do projeto:
        
        pip3 install virtualenv
        
        virtualenv wumpus

  ### Ativando o ambiente virtual
  **Nas distribuições do linux / Mac**

        source wumpus/bin/activate

  **No Windows**

        wumpus\Scripts\activate.bat

  ### Instalação de dependências
  Com o ambiente virtual já ativado, execute o seguinte comando na raiz do projeto:
        
         pip3 install -r requirements.txt
---

## Execução

        python3 run.py
