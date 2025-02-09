import re
import requests
from Bio.Seq import Seq
from Bio.SeqUtils import molecular_weight

# ---------------------------
# Banner and Safe Input
# ---------------------------
def display_banner():
    """Display an attractive banner for BioSeqenzer."""
    banner = r"""
   ____  _             ____                      
  | __ )| | __ _ _   _/ ___| _   _ _ __ ___  ___  
  |  _ \| |/ _` | | | \___ \| | | | '__/ _ \/ _ \ 
  | |_) | | (_| | |_| |___) | |_| | | |  __/  __/ 
  |____/|_|\__,_|\__, |____/ \__,_|_|  \___|\___| 
                 |___/  BioSeqenzer by Kirat        
    """
    print(banner)
    print("-" * 60)

def safe_input(prompt, default=None):
    """Wrap input() with a try/except to return a default value in sandboxed environments."""
    try:
        return input(prompt)
    except Exception:
        print(f"[Warning] Input not available; using default value: {default}")
        return default

# ---------------------------
# Online Sequence Fetching
# ---------------------------
def fetch_sequence_online(sequence_id):
    """Fetch a sequence from NCBI using the provided sequence ID."""
    url = f"https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?db=nuccore&id={sequence_id}&report=fasta"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.split('\n', 1)[1].replace("\n", "")
    return None

# ---------------------------
# Genomic Sequence Analysis
# ---------------------------
def find_motifs(dna_sequence):
    """Identify common motifs within the genomic sequence."""
    motifs = {
        "Start Codon (ATG)": [m.start() for m in re.finditer("ATG", dna_sequence)],
        "Stop Codons (TAA, TAG, TGA)": [m.start() for m in re.finditer("TAA|TAG|TGA", dna_sequence)],
        "TATA Box (Promoter)": [m.start() for m in re.finditer("TATAAA", dna_sequence)],
        "CAAT Box (Promoter)": [m.start() for m in re.finditer("CAAT", dna_sequence)],
        "GC Box (Promoter)": [m.start() for m in re.finditer("GGGCGG", dna_sequence)],
        "Splice Donor Site (GT)": [m.start() for m in re.finditer("GT", dna_sequence)],
        "Splice Acceptor Site (AG)": [m.start() for m in re.finditer("AG", dna_sequence)],
        "Polyadenylation Signal (AATAAA)": [m.start() for m in re.finditer("AATAAA", dna_sequence)]
    }
    return motifs

def translate_dna(dna_sequence):
    """Translate a DNA sequence into a protein sequence."""
    seq_obj = Seq(dna_sequence)
    return seq_obj.translate(to_stop=True)

def calculate_protein_weight(protein_sequence):
    """Calculate the molecular weight of the translated protein."""
    return molecular_weight(protein_sequence, seq_type='protein')

# ---------------------------
# Primer Design Functions
# ---------------------------
def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    return str(Seq(seq).reverse_complement())

def design_primers(dna_seq):
    """Design primers with restriction enzyme sites."""
    forward_primer = "CATATG" + dna_seq[:20]
    reverse_primer = "CTCGAG" + reverse_complement(dna_seq[-20:])
    return forward_primer, reverse_primer

# ---------------------------
# Main Workflow
# ---------------------------
def main():
    display_banner()
    dna_seq = safe_input("Enter genomic sequence: ", default="TATAAAATGCGTAA").strip().upper()
    motifs = find_motifs(dna_seq)
    protein_seq = translate_dna(dna_seq)
    protein_weight = calculate_protein_weight(protein_seq)
    forward_primer, reverse_primer = design_primers(dna_seq)
    
    print("\n--- Sequence Analysis Results ---")
    for motif, positions in motifs.items():
        print(f"{motif}: {positions}")
    
    print("\nTranslated Protein Sequence:", protein_seq)
    print("Molecular Weight of Protein:", protein_weight, "Da")
    print("\n--- Primer Design ---")
    print("Forward Primer:", forward_primer)
    print("Reverse Primer:", reverse_primer)
    
if __name__ == "__main__":
    main()