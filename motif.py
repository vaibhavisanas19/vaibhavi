import streamlit as st
import re
from Bio import SeqIO
from io import StringIO


# ✅ Function to Find Motifs (Fixed 'matches' Shadowing Issue)
def find_motifs(seq_records, motif):
    results = {}  # Dictionary to store results
    motif_regex = re.compile(motif, re.IGNORECASE)  # Case insensitive regex

    for record in seq_records:
        found_motifs = [(m.start() + 1, m.group()) for m in motif_regex.finditer(str(record.seq))]
        results[record.id] = found_motifs  # Store results per sequence

    return results  # Return results dict


# ✅ Streamlit UI
st.title("🧬 Motif Detection in DNA Sequences")
st.write("Upload a **FASTA file** or enter sequences manually.")

# 🔹 User Input Choice
input_method = st.radio("Choose Input Method:", ("Upload FASTA File", "Enter Sequences Manually"))

# ✅ Sequence Handling
fasta_sequences = []  # Local variable (no shadowing issue)

if input_method == "Upload FASTA File":
    uploaded_file = st.file_uploader("Upload a FASTA file", type=["fasta"])
    if uploaded_file:
        fasta_sequences = list(SeqIO.parse(uploaded_file, "fasta"))

elif input_method == "Enter Sequences Manually":
    user_sequences = st.text_area("Enter sequences in FASTA format:",
                                  ">Seq1\nATGCGTACGTTAGTAACTG\n>Seq2\nATGCGTACGTTAGTACCTG")
    if user_sequences:
        fasta_sequences = list(SeqIO.parse(StringIO(user_sequences), "fasta"))

# ✅ Motif Pattern Input
motif_pattern = st.text_input("Enter Motif Pattern (e.g., ATGCG)", "")

# ✅ Perform Motif Search
if fasta_sequences and motif_pattern:
    motif_results = find_motifs(fasta_sequences, motif_pattern)

    # ✅ Display Results
    st.write("### 🔍 Motif Search Results:")
    for seq_id, motif_matches in motif_results.items():  # Changed 'matches' to 'motif_matches'
        if motif_matches:
            st.write(f"**{seq_id}:** Found {len(motif_matches)} matches")
            match_text = ", ".join([f"Position {pos} ('{match}')" for pos, match in motif_matches])
            st.write(f"🔹 {match_text}")
        else:
            st.write(f"**{seq_id}:** ❌ No matches found")
