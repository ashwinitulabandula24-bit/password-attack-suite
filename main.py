import hashlib
from modules.generator import build_wordlist
from modules.analyzer import calculate_entropy
from modules.simulator import run_dictionary_attack

def main():
    print("==========================================")
    print(" PASSWORD AUDIT & ATTACK SUITE SIMULATOR ")
    print("==========================================\n")
    
    # 1. Dictionary Generation
    seeds = ["Admin", "Security", "Project"]
    print(f"[1] Generating custom dictionary from seeds: {seeds}")
    wordlist = build_wordlist(seeds)
    print(f"    -> Generated {len(wordlist)} candidate words.\n")
    
    # 2. Strength & Entropy Analysis
    sample_password = "Admin2024!"
    entropy, rating = calculate_entropy(sample_password)
    print(f"[2] Password Strength Analysis for: '{sample_password}'")
    print(f"    -> Entropy: {entropy} bits")
    print(f"    -> Strength Rating: {rating}\n")
    
    # 3. Hash Cracking Simulation
    target_plaintext = "Admin123"
    target_hash = hashlib.sha256(target_plaintext.encode()).hexdigest()
    
    print(f"[3] Simulating Dictionary Attack against target hash:")
    print(f"    -> SHA-256 Hash: {target_hash}")
    
    result = run_dictionary_attack(target_hash, wordlist, algo="sha256")
    
    if result["success"]:
        print(f"    [MATCH FOUND]: Plaintext is '{result['match']}'")
        print(f"    -> Attempts: {result['attempts']}")
        print(f"    -> Time Elapsed: {result['time_seconds']}s")
    else:
        print("    [FAILED]: Password not found in wordlist.")

if __name__ == "__main__":
    main()