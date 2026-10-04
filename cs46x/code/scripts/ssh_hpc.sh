script="hpc-share/ai-recycling/srun_script.sh"

#ssh submit "source ./.bash_profile; date >> ./hpc-share/log.txt; $script >> ./hpc-share/logi.txt"

# We get 'bash: module: command not found' 
#ssh submit "source ./.bash_profile; date > log.txt; module list >> log.txt 2>> log.txt"

# This fails when echoing $PATH, i see my local path as an error on my terminal
#ssh submit "source ./.bash_profile; date > log.txt; echo $PATH >> log.txt 2>> log.txt; module list >> log.txt 2>> log.txt"

# $PATH still causes script to fail 
#ssh submit "source ./.bash_profile; source /etc/profile; date > log.txt; echo $PATH >> log.txt 2>> log.txt"

# To run module, we need to source modules.sh if it is not previously sourced, 
#	this works, but path is still not loaded and recycling_module which is saved cannot be loaded
#ssh submit "source ./.bash_profile; source /etc/profile.d/modules.sh; date > log.txt; module load slurm; module restore recycling_module; module list >> log.txt 2>> log.txt"

# Attempt to `Force pseudo-terminal allocation` resulted in the same issue
#ssh -t submit "source ./.bash_profile; source /etc/profile.d/modules.sh; date > log.txt; module load slurm; module restore recycling_module; module list >> log.txt 2>> log.txt"

# Attempt to `Force tty` resulted in the same issue
ssh -t -t submit "source ./.bash_profile; source /etc/profile.d/modules.sh; date > log.txt; module load slurm; module restore recycling_module; module list >> log.txt 2>> log.txt"

# ISSUE: Unable to load $PATH environment in ssh connection

sleep 5
