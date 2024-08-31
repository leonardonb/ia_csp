import itertools

# Ler e parsear arquivo de entrada
def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    servicos = {"Incêndio": [], "Socorro": [], "Telefone": []}

    # Ignorar o cabeçalho
    for line in lines[1:]:
        line = line.strip()
        if line:
            partes = line.split(',')
            nome = partes[0].strip('_')  # Retira os underscores
            incendios = int(partes[1])
            socorros = int(partes[2])
            telefones = int(partes[3])

            # Adiciona o bombeiro ao serviço respectivo pelo número de vezes que ele pode ser escalado
            servicos["Incêndio"].extend([nome] * incendios)
            servicos["Socorro"].extend([nome] * socorros)
            servicos["Telefone"].extend([nome] * telefones)

    # Organiza as listas de bombeiros em grupos de 7 para representar os dias da semana
    for service in servicos:
        # Preenche com "vazio" se não houver 7 entradas para um serviço
        while len(servicos[service]) % 7 != 0:
            servicos[service].append("vazio")
        servicos[service] = [servicos[service][i:i + 7] for i in range(0, len(servicos[service]), 7)]

    return servicos

# Função para validar as restrições
def is_valid_assignment(servicos, assignment):
    dias = [set() for _ in range(7)]  # Um set para cada dia da semana
    
    for service, escala in assignment.items():
        for dia, bombeiro in enumerate(escala):
            if bombeiro in dias[dia] and bombeiro != "vazio":
                return False  # O mesmo bombeiro foi escalado para dois serviços no mesmo dia
            dias[dia].add(bombeiro)
    
    return True

# Selecionar o próximo serviço não atribuído
def select_unassigned_service(servicos, assignment):
    for service in servicos:
        if service not in assignment:
            return service
    return None

# Gerar todas as combinações possíveis de bombeiros para um serviço
def get_domain_values(service, servicos):
    return itertools.product(*servicos[service])

# Função de backtracking para resolver o CSP
def solve_csp(servicos):
    def backtrack(assignment):
        if len(assignment) == len(servicos):
            return assignment
        
        service = select_unassigned_service(servicos, assignment)
        for value in get_domain_values(service, servicos):
            assignment[service] = value
            if is_valid_assignment(servicos, assignment):
                result = backtrack(assignment)
                if result:
                    return result
            assignment.pop(service)
        return None
    
    return backtrack({})

# Formatar a solução para saída no formato desejado
def format_solution(solution):
    dias_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"]
    formatted_output = []

    for service, escala in solution.items():
        formatted_output.append(service)
        formatted_output.append("______".join(dias_semana) + "______")
        for linha in escala:
            linha_formatada = "_".join([nome.ljust(8, '_') for nome in linha])
            formatted_output.append(linha_formatada)
        formatted_output.append("")  # Linha em branco para separar serviços
    
    return "\n".join(formatted_output)

# Função para salvar a solução em um arquivo
def save_solution(solution, output_file_path):
    formatted_output = format_solution(solution)
    with open(output_file_path, 'w') as file:
        file.write(formatted_output)

# Função principal
def main():
    entrada_path = 'entrada_1.txt'
    saida_path = 'saida_gerada.txt'  # Nome do arquivo onde a saída será salva
    
    servicos = parse_input(entrada_path)
    solution = solve_csp(servicos)
    
    if solution:
        print("Solução encontrada e salva em", saida_path)
        save_solution(solution, saida_path)
    else:
        print("Nenhuma solução válida encontrada.")

if __name__ == "__main__":
    main()
