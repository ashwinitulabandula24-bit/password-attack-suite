import streamlit as st
import math
import hashlib
import time

# --- Helper Functions ---
def mutate_word(word):
    leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'}
    mutations = {word, word.lower(), word.upper(), word.capitalize()}
    leet_version = "".join(leet_map.get(c.lower(), c) for c in word)
    mutations.add(leet_version)
    return list(mutations)

def build_wordlist(seeds, numbers=["123", "2024", "2025", "!", "1"]):
    wordlist = set()
    for seed in seeds:
        for var in mutate_word(seed):
            wordlist.add(var)
            for num in numbers:
                wordlist.add(f"{var}{num}")
                wordlist.add(f"{num}{var}")
    return sorted(list(wordlist))

def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if any(not c.isalnum() for c in password): charset_size += 32
    if charset_size == 0 or len(password) == 0: return 0, "Invalid"
    
    entropy = len(password) * math.log2(charset_size)
    if entropy < 28: rating = "Very Weak"
    elif entropy < 36: rating = "Weak"
    elif entropy < 60: rating = "Moderate"
    elif entropy < 128: rating = "Strong"
    else: rating = "Very Strong"
    return round(entropy, 2), rating

def run_dictionary_attack(target_hash, wordlist):
    start_time = time.time()
    for attempts, word in enumerate(wordlist, 1):
        if hashlib.sha256(word.encode('utf-8')).hexdigest() == target_hash:
            return {"success": True, "match": word, "attempts": attempts, "time_seconds": round(time.time() - start_time, 4)}
    return {"success": False, "attempts": len(wordlist), "time_seconds": round(time.time() - start_time, 4)}

# --- Streamlit UI ---
st.set_page_config(page_title="Password Audit Suite", page_icon="🔒", layout="wide")
st.title("🔒 Password Audit & Attack Suite")
st.markdown("An ethical cybersecurity tool for testing password strength, entropy, dictionary generation, and offline hash cracking resilience.")

tab1, tab2, tab3 = st.tabs(["🔑 Dictionary Generator", "📊 Password Analyzer", "💥 Hash Attack Simulator"])

with tab1:
    st.header("Custom Wordlist Generator")
    seed_input = st.text_input("Enter target seeds (comma-separated):", "Admin, Security, Project")
    if st.button("Generate Wordlist"):
        seeds = [s.strip() for s in seed_input.split(",") if s.strip()]
        wordlist = build_wordlist(seeds)
        st.success(f"Generated {len(wordlist)} total mutations!")
        st.text_area("Generated Words Preview", value="\n".join(wordlist[:30]), height=200)

with tab2:
    st.header("Password Entropy & Strength Analyzer")
    password = st.text_input("Enter a password to evaluate:", "Admin2024!", type="password")
    if password:
        entropy, rating = calculate_entropy(password)
        st.metric(label="Calculated Entropy", value=f"{entropy} bits")
        st.subheader(f"Strength Rating: {rating}")

with tab3:
    st.header("Offline Hash Attack Simulator")
    target_plain = st.text_input("Target Plaintext Password for Simulation:", "Admin123")
    target_hash = hashlib.sha256(target_plain.encode()).hexdigest()
    st.code(f"Target SHA-256 Hash: {target_hash}", language="text")
    if st.button("Run Dictionary Attack"):
        seeds = ["Admin", "Security", "Project"]
        wordlist = build_wordlist(seeds)
        result = run_dictionary_attack(target_hash, wordlist)
        if result["success"]:
            st.balloons()
            st.success(f"🎉 Password Cracked! Plaintext: **{result['match']}**")
            st.json(result)
        else:
            st.error("Target hash not found in generated dictionary.")
