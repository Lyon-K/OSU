source ./.bash_profile; source /etc/profile.d/modules.sh; date > log.txt; module load slurm; srun >> log.txt 2>> log.txt; module list >> log.txt 2>> log.txt
