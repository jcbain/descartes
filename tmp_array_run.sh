#!/bin/bash
#SBATCH --account=def-yeaman
#SBATCH --mem=1G
#SBATCH --time=01:00:00
#SBATCH --array=1-4
#SBATCH --mail-user=james.bain@ucalgary.ca
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END

CMD=$(sed -n "${SLURM_ARRAY_TASK_ID}p" m_tmp)

/cvmfs/soft.computecanada.ca/easybuild/software/2017/Core/python/3.5.4/bin/python3 tmp_script.py $CMD