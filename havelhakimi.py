def is_valid_degree_sequence_havel_hakimi(deg_sequence):
    step = 0

    while deg_sequence:
        step += 1
        sorted_degree_sequence = sorted(deg_sequence, reverse=True)

        print(f"Step {step}: Degree sequence: {deg_sequence}")
        print(f"     Sorted degree sequence: {sorted_degree_sequence}")

        if deg_sequence[0] < 0:
            return False  

        if deg_sequence[0] == 0:
            deg_sequence.pop(0)  
        else:
            k = deg_sequence[0]
            if len(deg_sequence) < k + 1:
                return False 
            for i in range(1, k + 1):
                deg_sequence[i] -= 1
            deg_sequence.pop(0)  

    return True 


user_input = input("Enter the degree sequence separated by spaces (e.g., 4 3 2 2 1 1 1 1 1): ")
degree_sequence = [int(deg) for deg in user_input.split()]

if is_valid_degree_sequence_havel_hakimi(degree_sequence):
    print("The degree sequence is valid for a simple graph.")
else:
    print("The degree sequence is not valid for a simple graph.")
