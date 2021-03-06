# **************************************************************************
# *
# * Authors:     Daniel Del Hoyo (ddelhoyo@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
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
import os
import pyworkflow.viewer as pwviewer
from pwchem.viewers import PyMolViewer
from ..objects import SetOfSchrodingerGrids

class BBoxViewer(pwviewer.Viewer):
  _label = 'Viewer Schrodinger grids'
  _environments = [pwviewer.DESKTOP_TKINTER]
  _targets = [SetOfSchrodingerGrids]

  def _visualize(self, obj, **kwargs):
    pmlFile = obj.getBBoxPml()
    if pmlFile == None or not os.path.exists(pmlFile):
      obj.buildBBoxesPML()
      pmlFile = obj.getBBoxPml()

    pymolV = PyMolViewer(project=self.getProject())
    return pymolV._visualize(pmlFile, cwd=os.path.dirname(pmlFile))