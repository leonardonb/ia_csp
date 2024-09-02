# :octocat: Problema de Satisfação (CSP) para disciplina de Inteligência Artificial

## 📃 Problema de alocação de serviços para bombeiros. 

Cada entrada tem quantos serviços cada bombeiro vai trabalhar na semana por cada tipo de posto (Incêncio, Socorro, Telefone).


### 1. Função parse_input

```python
def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    servicos = {"Incêndio": [], "Socorro": [], "Telefone": []}
    bombeiros = {}

    for line in lines[1:]:
        line = line.strip()
        if line:
            partes = line.split(',')
            nome = partes[0].strip('_')
            incendios = int(partes[1])
            socorros = int(partes[2])
            telefones = int(partes[3])

            bombeiros[nome] = {"Incêndio": incendios, "Socorro": socorros, "Telefone": telefones}

            if incendios > 0:
                servicos["Incêndio"].extend([nome] * incendios)
            if socorros > 0:
                servicos["Socorro"].extend([nome] * socorros)
            if telefones > 0:
                servicos["Telefone"].extend([nome] * telefones)

    return servicos, bombeiros
```

- Objetivo: Ler os dados de um arquivo e organizar as informações sobre os bombeiros e os serviços que eles podem realizar.

Como funciona:
- Lê o arquivo linha por linha, ignorando a primeira linha (cabeçalho).
- Para cada linha, extrai o nome do bombeiro e a quantidade de serviços que ele pode realizar (Incêndio, Socorro, Telefone).
- Armazena essas informações em um dicionário bombeiros e em uma lista servicos, que contém a lista de bombeiros para cada tipo de serviço.


### 2.Função is_valid_assignment

```python
def is_valid_assignment(assignment, bombeiros):
    dias = [set() for _ in range(7)]
    contagem_servicos = defaultdict(lambda: defaultdict(int))

    for service, escala in assignment.items():
        for dia in range(7):
            for bombeiro in escala[dia]:
                if bombeiro != "vazio":
                    if bombeiro in dias[dia]:
                        return False
                    dias[dia].add(bombeiro)
                    contagem_servicos[bombeiro][service] += 1

    for bombeiro, servicos_realizados in contagem_servicos.items():
        for servico, count in servicos_realizados.items():
            if count > bombeiros[bombeiro][servico]:
                return False

    return True
```
- Objetivo: Verificar se a alocação de bombeiros atende às restrições.
Como funciona:
- Cria uma lista de conjuntos para rastrear quais bombeiros estão alocados em cada dia da semana.
- Conta quantas vezes cada bombeiro foi alocado para cada serviço.
- Se um bombeiro for alocado mais de uma vez no mesmo dia ou exceder o número de serviços que pode realizar, a função retorna False. Caso contrário, retorna True.

### 3. Função solve_csp

```python
 def solve_csp(servicos, bombeiros):
    def generate_initial_solution():
        solution = {service: [[] for _ in range(7)] for service in servicos.keys()}
        
        for service, bombeiros_list in servicos.items():
            random.shuffle(bombeiros_list)
            index = 0
            for bombeiro in bombeiros_list:
                solution[service][index % 7].append(bombeiro)
                index += 1
            for dia in range(7):
                while len(solution[service][dia]) < 2:
                    solution[service][dia].append("vazio")
                    
        return solution

    def improve_solution(solution):
        for _ in range(1000):  # Número de tentativas de melhoria
            service = random.choice(list(servicos.keys()))
            day = random.randint(0, 6)
            bombeiro1 = random.choice(servicos[service])
            bombeiro2 = random.choice(servicos[service])

            old_assignment = solution[service][day]
            solution[service][day] = [bombeiro1, bombeiro2]

            if is_valid_assignment(solution, bombeiros):
                return solution
            else:
                solution[service][day] = old_assignment

        return None

    for _ in range(100):  # Número de tentativas para encontrar uma solução válida
        initial_solution = generate_initial_solution()
        if is_valid_assignment(initial_solution, bombeiros):
            improved_solution = improve_solution(initial_solution)
            if improved_solution:
                return improved_solution

    return None   
```

- Objetivo: Encontrar uma alocação válida de bombeiros para os serviços.
Como funciona:
- generate_initial_solution: Gera uma solução inicial aleatória, distribuindo bombeiros entre os dias da semana. Cada serviço é alocado a um dia, e se um dia tiver menos de 2 bombeiros, preenche com "vazio".
- improve_solution: Tenta melhorar a solução inicial, fazendo alterações aleatórias e verificando se a nova alocação ainda é válida.
- O loop principal tenta gerar uma solução inicial e, se válida, tenta melhorá-la.

### 4. Função format_solution

```python
    def format_solution(solution):
    dias_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"]
    formatted_output = []

    for service, escala in solution.items():
        formatted_output.append(service)
        formatted_output.append("______".join(dias_semana) + "______")
        for i in range(2):
            linha = [escala[dia][i] if len(escala[dia]) > i else "vazio" for dia in range(7)]
            linha_formatada = "_".join([nome.ljust(8, '_') for nome in linha])
            formatted_output.append(linha_formatada)
        formatted_output.append("")

    return "\n".join(formatted_output)
```
- Objetivo: Formatar a solução encontrada para exibição ou gravação em arquivo.
Como funciona:
- Cria uma representação textual da alocação de bombeiros por serviço e dia da semana, formatando os nomes para que fiquem alinhados.

### 5. Função save_solution
```python
def save_solution(solution, output_file_path):
    formatted_output = format_solution(solution)
    with open(output_file_path, 'w') as file:
        file.write(formatted_output)
```
- Objetivo: Salvar a solução formatada em um arquivo.
Como funciona: Chama a função format_solution para obter a representação textual e grava em um arquivo especificado.

### 6. Função main
```python
def main():
    entrada_path = 'entrada_1.txt'
    saida_path = 'saida_gerada.txt'
    
    servicos, bombeiros = parse_input(entrada_path)
    solution = solve_csp(servicos, bombeiros)
    
    if solution:
        print("Solução encontrada e salva em", saida_path)
        print(format_solution(solution))
        save_solution(solution, saida_path)
    else:
        print("Nenhuma solução válida encontrada.")

if __name__ == "__main__":
    main()
```
- Objetivo: Controlar o fluxo do programa.
Como funciona:
- Define os caminhos dos arquivos de entrada e saída.
- Chama as funções para ler os dados, resolver o problema e salvar a solução. Se uma solução válida for encontrada, ela é exibida e salva; caso contrário, uma mensagem de erro é exibida.

## 📍  Conclusão

Esse código implementa um algoritmo de satisfação de restrições para alocar bombeiros em diferentes serviços, garantindo que todas as restrições sejam respeitadas. Cada parte do código tem um papel específico na leitura dos dados, validação das alocações e formatação da saída.

## :octocat: Autores

- [Izabel Nascimento](https://github.com/izabelnascimento)

- [Leonardo Nunes](https://github.com/leonardonb)

- [Tayane Cibely](https://github.com/tayanecibely)
