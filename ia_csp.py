import random
from collections import defaultdict


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

    for _ in range(1000):  # Número de tentativas para encontrar uma solução válida
        initial_solution = generate_initial_solution()
        if is_valid_assignment(initial_solution, bombeiros):
            improved_solution = improve_solution(initial_solution)
            if improved_solution:
                return improved_solution

    return None


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


def save_solution(solution, output_file_path):
    formatted_output = format_solution(solution)
    with open(output_file_path, 'w') as file:
        file.write(formatted_output)


def calculate_all():
    for i in range(1, 101):
        main(i, False, 'resources/out/saida_gerada_{}.txt'.format(i))


def main(num_file, print_console, saida_path):
    entrada_path = 'resources/in/entrada_{}.txt'.format(num_file)
    
    servicos, bombeiros = parse_input(entrada_path)
    solution = solve_csp(servicos, bombeiros)

    if solution:
        if print_console:
            print("\nSolução encontrada e salva em", saida_path)
            print(format_solution(solution))
        save_solution(solution, saida_path)
    else:
        print("Arquivo: ", num_file)
        print("Nenhuma solução válida encontrada.")


calculate_all()
main(49, True, 'resources/saida_gerada.txt')
