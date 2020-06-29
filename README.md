
### Test Files
test/covid-like_10_seqs.fasta  
test/covid-like_test_atypical_seqs.fasta

### example usage:

> docker run -it -u $(id -u):$(id -g) -v "$(pwd)"/test:/home/appuser j81docker/gor1_batch:1.0

==========================================================

### IN CONTAINER

==========================================================

INPUT: FASTA_FILE, a multisequence fasta file
OUTPUT: GOR1
> multi_fasta_exec.py {FASTA_FILE}
