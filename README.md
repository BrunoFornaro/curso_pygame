# Integrantes do grupo:
- Bruno Pereira Fornaro - B44398
- Daniel Ambrosim Falqueto - B43618
- Gustavo Navarro Rozas - B42592
- Hugo de Araújo e Silva - B43907
- Matheus Medeiros Carvalho da Fonseca - B44252


# Objetivo
O intuito do nosso trabalho foi fazer um shooter com o tema bebê, que consiste em um bebê que não gosta de verduras e, por isso, atira brinquedos nelas.


# Alterações feitas
## Novo tema
Alteramos a imagem de fundo do código original, que era o espaço para azulejo (verde), madeira e quadrado, dando 3 fases do jogo.
Mudamos também a imagem da seringa para a de um bebê, já que foi o tema escolhido. A alteração dos inimigos, do código original, também foi feita,
mudando para verduras e legumes.


## Principais alterações 
- Foram removidos os caracteres especiais das 'variáveis'; 
-Foi corrigido o fim do jogo (adicionando o quit depois de encerrar o loop);
- Tempo de tiro limitado a um disparo a cada meio segundo;
- Foi adicionado um placar onde mostram vida, pontos e nível;
- Tela em fullscreen; 
- Manutenção de inimigos atualizada. Foram adicionados diferentes tipos de inimigos e dois inimigos não se sobrepõe quando nascem;
- Colisão e alvejado corrigidos. Era conferido se era morto antes de tirar um ponto de vida, inimigos com uma vida na prática possuíam duas;
- A velocidade no respectivo eixo zera ao soltar o botão de movimentação;
- Foi implementado velocidades aleatórias para diferentes tipos de inimigos;
- Mudamos a movimentação para as teclas w, a, s, d e espaço para atirar;
- Um limitador de velocidade foi inserido para a "nave" (que será um bebê), para se mover mais naturalmente;
- Mudança nos tamanhos dos sprites (ficaram menores, para aproveitar melhor a tela), na quantidade de inimigos (agora surgem mais inimigos) e quantidade e velocidades dos tiros (nova arma, com apenas "dois tiros") para deixar o jogo mais 'difícil';
- Velocidade alterada dos inimigos (agora são mais rápidos); 
- Os níveis agora são infinitos e a cada novo nível, a partir do 3, a quantidade de inimigos aumenta;
- Novo inimigo "imortal" e que nasce acima da posição do jogador, descendo rápido (um brócolis com 100 vidas);
- Novas imagens foram adquiridas para a nossa versão com o tema "Bebê";
- As imagens foram atualizadas;
- Imagens convertidas para png;
- Powerups adicionados, ao pegar o powerup o jogador ganha uma vida extra ou sobe um nível de arma. 
- Armas modificadas, adicionada uma arma especial que dura 5 segundos depois de pegar um powerup de arma ("arma com quatro tiros", sendo dois deles para os lados); 
- Velocidade ajustada (o jogador está se movimentando ligeiramente mais rápido), para se mover mais naturalmente;
- Tamanhos e velocidades dos tiros alterados (os tiros "se movimentam" na tela mais rápido);
- Uma música autoral foi feita para o jogo. Adicionado som para derrota e som para colisão (também autoral) do tiro com o inimigo foram implementados;
- Teclas para alterar o som foram adicionadas. M para mutar, N para diminuir e B para aumentar o som.
- Adicionado menu de iniciar, de pausa e de fim de jogo (game over). O jogador pode pausar, sair do jogo, aumentar ou diminuir o volume e jogar novamente, caso perca.

- A princípio, a modificação mais recente (e final) está na tag "a2_33_final". O jogo deve ser executado pelo "main.py" dentro da pasta "coronashooter".


# Observações
Vale ressaltar que foi tomado o devido cuidado para que o resultado final incluísse apenas imagens e áudios livres. Inclusive, alguns dos nossos áudios, como a música de fundo do jogo e o som de acertar o inimigo, são autorais do nosso grupo.