# coding: latin-1
# **************************************************************************
# *
# * Authors:     Carlos Oscar Sorzano
# *
# * [1] uam, madrid, Spain
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

SCHRODINGER_HOME = 'SCHRODINGER_HOME' #Acceso by Plugin.getHome()

ATTRIBUTES_MAPPING = {'SiteScore': 'score', 'Dscore': 'druggability', 'size': 'nPoints',
                      'volume': 'volume', 'exposure': 'exposure', 'enclosure': 'enclosure',
                      'contact': 'contact', 'phobic': 'hidrophobic', 'philic': 'hidrophilic',
                      'balance': 'balance', 'don/acc': 'don/acc', 'class': 'class',
                      'contactAtoms': 'contactAtoms', 'contactResidues': 'contactResidues'}

#################################### SYSTEM PREPARATION ############

MSJ_SYSPREP = '''task {
  task = "desmond:auto"
}

build_geometry {
  #add counterion
  %s  
  box = {
     shape = %s
     size = %s
     size_type = %s
  }
  override_forcefield = %s
  rezero_system = %s
  #add salt
  %s  
  #add solvent
  %s
}

assign_forcefield {
  forcefield = %s
}

# command example:
# $SCHRODINGER/utilities/multisim -HOST <hostname> -JOBNAME desmond_trial -m desmond_trial.msj \
desmond_trial.mae -o desmond_trial.cms
'''

ADD_COUNTERION = '''add_counterion = {
     ion = %s
     number = %s
  }'''

ADD_SALT = '''salt = {
     concentration = %s
     negative_ion = %s
     positive_ion = %s
  }'''

SOLVENT = 'solvent = %s'

SIZE_SINGLE = '%s'
SIZE_LIST = '[%s %s %s]'
ANGLES = '[%s %s %s %s %s %s]'

################################ SYSTEM RELAXATION ##################

MSJ_SYSRELAX_INIT = '''task {
  task = "desmond:auto"
  set_family = {
    desmond = {
      checkpt.write_last_step = no
    }
  }
}
'''

MSJ_SYSRELAX_SIM = '''
simulate {
  annealing   = %s
  dir         = %s
  glue        = %s
  time        = %s
  timestep    = %s
  temperature = %s
  #Pressure
  %s
  #Tension
  %s
  ensemble = {
    class  = %s
    method = %s
    thermostat.tau = %s
    #barostat tau
    %s 
    #Browian delta max
    %s
  }
  
  #restrains
  %s   
  
  randomize_velocity.interval = %s
  eneseq.interval             = 0.3

  trajectory {
  center = solute
  first = 0.0
  format = dtr
  interval = %s
  periodicfix = true
  }
}
'''

TIMESTEP = '''[%s %s %s]'''
PRESSURE = '''pressure = [%s %s]'''
TENSION = '''surface_tension = %s'''
BAROSTAT = '''barostat.tau = %s'''

BROWNIAN = '''brownie.delta_max = %s'''

RESTRAINS = '''restrain    = { atom = %s force_constant = %s }'''

# Desmond standard NPT relaxation protocol
# All times are in the unit of ps.
# Energy is in the unit of kcal/mol.
# 1) "Brownian Dynamics NVT, T = 10 K, small timesteps, and restraints on solute heavy atoms, 100ps"
# 2) "NVT, T = 10 K, small timesteps, and restraints on solute heavy atoms, 12ps"
# 3) "NPT, T = 10 K, and restraints on solute heavy atoms, 12ps"
# 4) "NPT, T = 300 K and restraints on solute heavy atoms, 12ps"
# 5) "NPT, T = 300 K and no restraints, 24ps"
DESMOND_NPT_RELAX = '''\
{'simTime': 100.0, "bondedT": 0.001, "nearT": 0.001, "farT": 0.003, 'temperature': 10.0, 'deltaMax': 0.1,\
'ensemType': 'Minimization (Brownian)', 'restrains': 'Solute_heavy_atom'}
{'simTime': 12.0, "bondedT": 0.001, "nearT": 0.001, "farT": 0.003, 'temperature': 10.0,\
'ensemType': 'NVT', 'thermostat': 'Langevin', 'restrains': 'Solute_heavy_atom'}
{'simTime': 12.0, 'temperature': 10.0, 'ensemType': 'NPT', 'thermostat': 'Langevin', 'barostat': 'Langevin', \
'presRelaxCons': 50.0, 'restrains': 'Solute_heavy_atom'}
{'simTime': 12.0, 'temperature': 300.0, 'ensemType': 'NPT', 'thermostat': 'Langevin', 'barostat': 'Langevin', \
'presRelaxCons': 50.0, 'restrains': 'Solute_heavy_atom'}
{'simTime': 24.0, 'temperature': 300.0, 'ensemType': 'NPT', 'thermostat': 'Langevin', 'barostat': 'Langevin', \
'presRelaxCons': 2.0}
'''


