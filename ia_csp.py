import itertools

# Ler e parsear arquivo de entrada
def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Dicionário para armazenar os serviços com a lista de bombeiros para cada dia
    servicos = {}
    current_service = None

    for line in lines:
        line = line.strip()
        if line:
            if not line.startswith("DOM"):
                # Identifica o serviço (ex: Incêndio, Socorro, Telefone)
                current_service = line
                servicos[current_service] = [[] for _ in range(7)]  # 7 dias da semana
            else:
                # Adiciona os nomes dos bombeiros ao serviço atual para cada dia da semana
                bombeiros = line.split('_')
                for i, bombeiro in enumerate(bombeiros):
                    servicos[current_service][i].append(bombeiro)
    
    return servicos

# Função para validar as restrições
def is_valid_assignment(servicos, assignment):
    dias = [set() for _ in range(7)]  # Um set para cada dia da semana
    
    for service, escala in assignment.items():
        for dia, bombeiro in enumerate(escala):
            if bombeiro in dias[dia]:
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

# Formatar a solução para salvar em um arquivo de saída
def format_solution(solution):
    formatted_output = []
    for service, escala in solution.items():
        formatted_output.append(service)
        for dia in zip(*escala):
            formatted_output.append("_".join(dia))
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
