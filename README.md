# AGORITMOS DE BUSCA - IA

A seguir, são defindos alguns algorítmos de busca implementados usando linguagem Python. Cada algorítmo possui sua diferença quanto ao método de pesquisa, diferenciando apenas alguns pontos específicos.


### Observações válidas a todos os algoritmos
Algumas opções de ajustes podem ser feitos em todos os algorítmos. Estes ajustes servem exatamente para definir valores aleatórios, modo de expansão dos vizinhos, definição de ponto de partida e de destino de maneira mais fácil. Ou seja, para definir valores aleatórios ou os predefinidos, basta alterar apenas um valor específico para cada opção. Caso o usuário queira aprofundar mais, estas opções podem ser alteradas com mais detalhes no restante do código.

As opções são as seguintes:

    set_random_wall       
Define se um muro será gerado de maneira aleatória.

    set_random_start_cell
Define se a célula de início de busca usará as coordenadas pré-definidas ou se utilizará um valor aleatório.

    set_random_end_cell
Define se a célula de destino usará as coordenadas pré-definidas ou se utilizará um valor aleatório.

    set_diagonal_movement
Define se ao adicionar os vizinho de uma determinada célula, os vizinhos nas diagonais serão adicionadas ou não.

Por padrão, todas estas opções podem assumir valores de `True` ou `False`, para verdadeiro ou falso, respectivamente. Quando o valor estiver definido como `True`, quer dizer que a ação descriminada na opção será executada. O contrário também é válido.

## Busca em Largura - Breadth-First Search - BFS
A execução do algorítmo se dá expandido todos os nós a partir do nó inicial em busca do nó de destino. Essa expansão ocorre de maneira uniforme, de modo que ao chegar em uma célula, todas as celulas vizinhas serão adicionadas em uma lista das próximas celulas a serem expandidas. Ao final desta expansão, caso tenha uma solução, a mesma será encontrada.

## Busca em Profundidade - Deapth-First Search - DFS
Ao contrário da busca em lagura, esta ao encontrar uma célula, descerá no seu vizinho e assim segue no subsequente de modo até que encontre um ponto de parada. Caso encontre e não seja o objetivo, o mesmo volta nesta cadeia vizitando os demais nós e seguindo o mesmo raciocínio até vizitar todos os nós possíveis. Caso haja uma solução, a mesma será encontrada.

## Busca de Custo Uniforme - Uniforme Cost Search - UCS
Seguindo uma abordagem parecida com a da busca em largura, este método também expande todos de maneira uniforme, com uma excessão que adota um método de distanciamento, porém contando a partir do nó inicial. Ou seja, ao expandir, o mesmo dá prioridade ao nó que esteja mais perto do ponto de partida.

## Busca pela Melhor Escolha - Best-First Search
Neste método de busca, é adotado uma função heurística para calcular a menor distância até o nó destino. O caminho será definido expandindo pela célula que esteja mais próxima do objetivo. Caso haja uma solução, a mesma será encontrada.

## A-estrela - A-star - A*
Neste algorítmo, também será usada uma função heurística com o objetivo de encontrar o menor caminho até o nó destino. A abordagem é bem similar ao do método anterior, destinguindo apenas em alguns pontos. Caso haja uma solução, a mesma será encontrada.

### Observações finais
Os algorítmos possuem alguns blocos de códigos comentados. Estes comentários servem exatamente para definir uma opção que pode ser executada, sendo que há ainda uma outra opção, também válida, que pode ser executada, diferenciando apenas em alguns detalhes, mas chegando a uma solução caso esta exista. Os principais comentários estão em partes que definem como serão econtrados os nós fílhos, ou seja, a ordem de descoberta dos nós ou a na parte da função heurística, para definir qual método de cálculo foi usado.