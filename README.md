# Lab Week 11: Sequence Similarity Networks with Biopython

[Slides](https://docs.google.com/presentation/d/1PgdqqCLnB3RUA7krQhsLdLNJWBmzOEiYOjfxrf9jNf0/edit?slide=id.g3f9c62c1b5f_0_0#slide=id.g3f9c62c1b5f_0_0)

In this lab you will build a **sequence similarity network (SSN)**, a graph that groups proteins by how similar
their sequences are, entirely in Python. Web tools like the
[EFI Enzyme Similarity Tool](https://efi.igb.illinois.edu/efi-est/) do this for you. Today you'll do each step yourself:

1. Read protein sequences from a FASTA file with **[Biopython](https://biopython.org)**.
2. Compare sequences with Biopython's **`PairwiseAligner`** and the BLOSUM62 substitution matrix.
3. Score every pair, build the network with **NetworkX**, and use it to identify three mystery proteins.
4. Compare 3D structures with **TM-align** to investigate the protein that sequence alone can't place.
5. *(Bonus)* Repeat the search with **MMseqs2** and **Foldseek**, two fast tools used in current research.

The dataset is 74 globins (hemoglobins, myoglobins, neuroglobins, cytoglobins and plant leghemoglobins) from
[UniProt](https://www.uniprot.org).

## Starting the Lab

Start the lab by cloning this repository and moving into its folder. Then create the lab environment:

```bash
make environment
```

If you don't have `make`, run the command it uses instead: `conda env create -f environment.yml -n chem274A_ssn`.

After the environment is created, activate it and start Jupyter **from this folder** (the one containing this README),
so the notebooks can find `data/` and `ssn_plot.py`:

```bash
conda activate chem274A_ssn
jupyter lab
```

Complete notebooks 1–3 in order, since they build on each other. **Make sure you get to Notebook 3**: it's where
everything comes together.

| Notebook | Topic | Time |
|---|---|---|
| `01_sequences_biopython.ipynb` | Reading FASTA files, the `SeqRecord` and `Seq` classes | ~12 min |
| `02_pairwise_alignment.ipynb` | Alignment, BLOSUM62, normalizing scores | ~20 min |
| `03_building_an_ssn.ipynb` | All-vs-all scoring, building and thresholding the network, mystery proteins, 3D structure | ~35 min |
| `04_bonus_mmseqs_foldseek.ipynb` | *(Bonus)* Running MMseqs2 and Foldseek from Python with `subprocess` | if time allows |

### Bonus notebook setup

Notebook 4 needs MMseqs2 and Foldseek, which come from the `bioconda` channel. They work on Linux, macOS (Intel and
Apple Silicon) and WSL, but **not native Windows**. Create the separate bonus environment with:

```bash
make environment-bonus
conda activate chem274A_ssn_bonus
jupyter lab
```

Without `make`, the first line is `conda env create -f environment-bonus.yml -n chem274A_ssn_bonus`.

## Files

| File | What it is |
|---|---|
| `data/globins.fasta` | the 74 protein sequences |
| `data/globins_metadata.csv` | protein type and organism for each sequence |
| `data/structures/` | crystal structures from the Protein Data Bank, used in Notebook 3 |
| `ssn_plot.py` | a helper that draws the network (you don't need to edit it) |

## Report Out

1. Look at the [Biopython GitHub repository](https://github.com/biopython/biopython). What programming languages is it
   written in? Why might the alignment code in particular be written in a faster language than Python?

2. As a group, discuss the `SeqRecord` and `PairwiseAligner` classes. What are some of their attributes and methods?
   Do they feel "Pythonic"? How do they compare to the RDKit molecule objects from Lab 5?

3. Why did we normalize the alignment scores before building the network? What would go wrong if we had used raw scores?

4. What similarity cutoff did your group choose, and how did you decide? At that cutoff, did the clusters match the
   known protein types?

5. What do you think each mystery protein is? Which one didn't fit anywhere, and what did its structure show?
   What can you conclude when a protein has no neighbors in an SSN, and what can't you conclude?
