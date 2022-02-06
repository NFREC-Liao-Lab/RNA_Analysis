#!/bin/bash -l
#SBATCH --job-name=blast2go_blast      # Job name
#SBATCH --mail-type=all            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=wanghaihua@ufl.edu       # Where to send mail	
#SBATCH --ntasks=1                      # Number of MPI ranks
#SBATCH --cpus-per-task=9               # Number of cores per MPI rank 
#SBATCH --nodes=1                       # Number of nodes
#SBATCH --ntasks-per-node=1             # How many tasks on each node
#SBATCH --ntasks-per-socket=1           # How many tasks on each CPU or socket
#SBATCH --mem-per-cpu=7G             # Memory per core
#SBATCH --time=30-00:00:00                 # Time limit hrs:min:sec
#SBATCH --output=blast2go_blast_%j.log     # Standard output and error log

pwd; hostname; date
 

#################################
#this script blast the DNA and protein sequences to nt and nr database

#load the modules
module load ncbi_blast/2.2.26
#module load ncbi_toolkit
#module load bowtie
#module load bowtie2

#set the database 
nr_DB="/data/reference/blast/201911/nr"
nt_DB="/data/reference/blast/201911/nt"


#remove * in the fasta files
for i in *.pep.fasta
do
  a=$(basename "$i" .pep.fasta)
  sed 's/*//' $a.pep.fasta > $a.pep.new.fasta
done
 
#run the blast
 for i in *.pep.new.fasta
do
  a=$(basename "$i" .pep.new.fasta)
  blastp -db $nr_DB -query $a.pep.new.fasta -out $a.nr.blast.fmt5.xml -num_threads 32 -outfmt 5 -max_target_seqs 10 -evalue 1e-5 ;
  
done 


echo "The blast progress has been done"
