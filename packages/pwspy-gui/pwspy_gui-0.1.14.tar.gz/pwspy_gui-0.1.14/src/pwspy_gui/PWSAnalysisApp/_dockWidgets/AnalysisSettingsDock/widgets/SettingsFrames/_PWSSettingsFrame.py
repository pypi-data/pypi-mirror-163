# Copyright 2018-2020 Nick Anthony, Backman Biophotonics Lab, Northwestern University
#
# This file is part of PWSpy.
#
# PWSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PWSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PWSpy.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
import os
from glob import glob
import typing

from pwspy_gui.PWSAnalysisApp._dockWidgets.AnalysisSettingsDock.widgets.SettingsFrames._AbstractSettingsFrame import AbstractSettingsFrame
from pwspy_gui.PWSAnalysisApp._dockWidgets.AnalysisSettingsDock.widgets.SettingsFrames._sharedWidgets import ExtraReflectanceSelector, HardwareCorrections, \
    QHSpinBox, QHDoubleSpinBox, VerticallyCompressedWidget
from pwspy_gui.PWSAnalysisApp.componentInterfaces import CellSelector
from pwspy_gui.PWSAnalysisApp._dockWidgets.AnalysisSettingsDock.runtimeSettings import PWSRuntimeAnalysisSettings
if typing.TYPE_CHECKING:
    from pwspy_gui.sharedWidgets.extraReflectionManager import ERManager

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QScrollArea, QGridLayout, QLineEdit, QLabel, QGroupBox, QHBoxLayout, QWidget, QRadioButton, \
    QFrame, QCheckBox, QDoubleSpinBox

from pwspy.analysis.pws import PWSAnalysisSettings
from pwspy_gui.PWSAnalysisApp import applicationVars
from pwspy_gui.PWSAnalysisApp.sharedWidgets.collapsibleSection import CollapsibleSection


class PWSSettingsFrame(AbstractSettingsFrame, QScrollArea):
    def __init__(self, erManager: ERManager, cellSelector: CellSelector):
        super().__init__()
        self.cellSelector = cellSelector

        self._frame = VerticallyCompressedWidget(self)
        self._layout = QGridLayout()
        self._frame.setLayout(self._layout)
        self._frame.setFixedWidth(350)
        self.setMinimumWidth(self._frame.width()+5)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidget(self._frame)

        """Set up Frame"""
        """Presets"""
        row = 0
        self._analysisNameEdit = QLineEdit()
        self._layout.addWidget(QLabel("Analysis Name: "), row, 0, 1, 1)
        self._layout.addWidget(self._analysisNameEdit, row, 1, 1, 1)
        row += 1
        self.presets = QGroupBox("Presets")
        self.presets.setLayout(QHBoxLayout())
        self.presets.layout().setContentsMargins(0, 0, 0, 5)
        _2 = QWidget()
        _2.setLayout(QHBoxLayout())
        _2.layout().setContentsMargins(5, 0, 5, 0)
        for f in glob(os.path.join(applicationVars.analysisSettingsDirectory, '*_analysis.json')):
            name = os.path.split(f)[-1][:-14]
            b = QRadioButton(name)
            b.released.connect(
                lambda n=name: self.loadFromSettings(
                    PWSAnalysisSettings.fromJson(applicationVars.analysisSettingsDirectory, n)))
            _2.layout().addWidget(b)
        _ = QScrollArea()
        _.setWidget(_2)
        _.setFrameShape(QFrame.NoFrame)
        _.setContentsMargins(0, 0, 0, 0)
        _.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        _.horizontalScrollBar().setStyleSheet("QScrollBar:horizontal { height: 10px; }")
        self.presets.setFixedHeight(45)
        self.presets.layout().addWidget(_)
        self._layout.addWidget(self.presets, row, 0, 1, 4)
        row += 1

        '''Hardwarecorrections'''
        self.hardwareCorrections = HardwareCorrections(self)
        self.hardwareCorrections.stateChanged.connect(self._updateSize)
        self._layout.addWidget(self.hardwareCorrections, row, 0, 1, 4)
        row += 1

        '''Extra Reflection'''
        self.extraReflection = ExtraReflectanceSelector(self, erManager)
        self._layout.addWidget(self.extraReflection, row, 0, 1, 4)
        row += 1

        '''Use relative or absolute units of reflectance'''
        self.scaling = QGroupBox("Scaling")
        self.scaling.setLayout(QHBoxLayout())
        self.scaling.layout().setContentsMargins(2, 2, 2, 5)
        self.relativeUnits = QCheckBox("Use Relative Units", self)
        self.relativeUnits.setToolTip("If checked then reflectance (and therefore all other parameters) will be scaled such that any reflectance matching that\n"
                                      "of the reference image will be 1. If left unchecked then the `Reference Material` will be used to scale reflectance to\n"
                                      "match the actual physical reflectance of the sample.")
        self.scaling.layout().addWidget(self.relativeUnits)
        self._layout.addWidget(self.scaling, row, 0, 1, 4)
        row += 1

        '''SignalPreparations'''
        self.signalPrep = QGroupBox("Signal Prep")
        self.signalPrep.setFixedSize(175, 75)
        self.signalPrep.setToolTip("In order to reduce the effects of measurement noise we filter out the high frequencies from our signal. We do this using a\n"
                                   "Buttersworth low-pass filter. Best to stick with the defaults on this one.")
        layout = QGridLayout()
        layout.setContentsMargins(5, 1, 5, 5)
        _ = layout.addWidget

        orderLabel = QLabel("Filter Order")
        self.filterOrder = QHSpinBox()
        self.filterOrder.setRange(0, 6)
        self.filterOrder.setToolTip("A low-pass filter is applied to the spectral signal to reduce noise. This determines the `order` of the digital filter.")
        orderLabel.setToolTip(self.filterOrder.toolTip())
        cutoffLabel = QLabel("Cutoff Freq.")
        self.filterCutoff: QDoubleSpinBox = QHDoubleSpinBox()
        self.filterCutoff.setToolTip("The frequency in units of 1/wavelength for the filter cutoff.")
        self.filterCutoff.setDecimals(3)  # Greater precision than default
        cutoffLabel.setToolTip(self.filterCutoff.toolTip())
        self.filterCheckbox = QCheckBox("Low-pass Filtering", self)
        def stateChange(state: bool):
            self.filterOrder.setEnabled(state)
            self.filterCutoff.setEnabled(state)
        self.filterCheckbox.stateChanged.connect(stateChange)
        self.filterCheckbox.setChecked(True)  # This is just to initialize the proper state
        _(self.filterCheckbox, 0, 0, 1, 2)
        _(orderLabel, 1, 0, 1, 1)
        _(self.filterOrder, 1, 1, 1, 1)
        _(cutoffLabel, 2, 0, 1, 1)
        _(self.filterCutoff, 2, 1, 1, 1)
        _(QLabel("nm<sup>-1</sup>"), 2, 2, 1, 1)
        self.signalPrep.setLayout(layout)
        self._layout.addWidget(self.signalPrep, row, 0, 1, 2)

        '''Cropping'''
        self.cropping = QGroupBox("Wavelength Cropping")
        self.cropping.setFixedSize(125, 75)
        self.cropping.setToolTip("In the past it was found that there was exceptionally high noise at the very beginning and end of an acquisition. For this reason we would exclude the first and last wavelengths of the image cube. While it is likely that the noise issue has now been fixed we still do this for consistency's sake.")
        layout = QGridLayout()
        layout.setContentsMargins(5, 1, 5, 5)
        _ = layout.addWidget
        self.wavelengthStart = QHSpinBox()
        self.wavelengthStop = QHSpinBox()
        self.wavelengthStart.setToolTip("Sometimes the beginning and end of the spectrum can have very high noise. For this reason we crop the data before analysis.")
        self.wavelengthStop.setToolTip("Sometimes the beginning and end of the spectrum can have very high noise. For this reason we crop the data before analysis.")
        self.wavelengthStart.setRange(300, 800)
        self.wavelengthStop.setRange(300, 800)
        self.croppingCheckbox = QCheckBox("Enable Cropping", self)
        def cropStateChanged(state: bool):
            self.wavelengthStop.setEnabled(state)
            self.wavelengthStart.setEnabled(state)
        self.croppingCheckbox.stateChanged.connect(cropStateChanged)
        self.croppingCheckbox.setChecked(True)  # This is just to initialze the propert state.
        _(self.croppingCheckbox, 0, 0, 1, 2)
        _(QLabel("Start"), 1, 0)
        _(QLabel("Stop"), 1, 1)
        _(self.wavelengthStart, 2, 0)
        _(self.wavelengthStop, 2, 1)
        self.cropping.setLayout(layout)
        self._layout.addWidget(self.cropping, row, 2, 1, 2)
        row += 1

        '''Polynomial subtraction'''
        self.polySub = QGroupBox("Polynomial Subtraction")
        self.polySub.setFixedSize(150, 50)
        self.polySub.setToolTip("A polynomial is fit to each spectrum and then it is subtracted from the spectrum."
                                "This is so that we remove effects of absorbtion and our final signal is only due to interference"
                                "For liquid covered samples this is always set to 0. For samples in air a 2nd order polynomial is used.")
        layout = QGridLayout()
        layout.setContentsMargins(5, 1, 5, 5)
        _ = layout.addWidget
        self.polynomialOrder = QHSpinBox()
        _(QLabel("Order"), 0, 0, 1, 1)
        _(self.polynomialOrder, 0, 1, 1, 1)
        self.polySub.setLayout(layout)
        self._layout.addWidget(self.polySub, row, 0, 1, 2)

        # WaveNumber Filtering
        self.waveNumberCutoff = QHDoubleSpinBox()
        self.waveNumberCutoff.setValue(4.3)  # OPD = estimated depth * 2(roundtrip) * 1.37 (RI of cell). DOF=1.1um -> OPD = 2.95. To achieve 5% attenuation at 2.95um a 3dB cutoff of 4.3 is selected (4th-order butterworth)
        self.cutoffWaveNumber = QCheckBox("Perform Filtering")
        self.cutoffWaveNumber.stateChanged.connect(lambda state: self.waveNumberCutoff.setEnabled(state != QtCore.Qt.Unchecked))
        self.cutoffWaveNumber.setCheckState(QtCore.Qt.Checked)
        self.cutoffWaveNumber.setCheckState(QtCore.Qt.Unchecked)  # Default to off

        layout = QGridLayout()
        layout.setContentsMargins(5, 1, 5, 5)

        layout.addWidget(self.cutoffWaveNumber, 0, 0, 1, 2)
        layout.addWidget(QLabel("OPD Cutoff (um)"), 1, 0, 1, 1)
        layout.addWidget(self.waveNumberCutoff, 1, 1, 1, 1)
        wnFilter = QGroupBox("OPD Filtering")
        wnFilter.setLayout(layout)
        wnFilter.setToolTip("A 4th order buttersworth filter will be applied to the spectra (x axis: wavenumber) at the specified cutoff frequency."
                            "The cutoff is the frequency at which the attenuation will be -3dB. After the cutoff the attenuation slope will be 80dB per decade.")
        self._layout.addWidget(wnFilter, row, 2, 1, 2)

        row += 1


        '''Advanced Calculations'''
        self.advanced = CollapsibleSection('Skip Advanced Analysis', 200, self)
        self.advanced.stateChanged.connect(self._updateSize)
        self.advanced.setToolTip("If this box is ticked then some of the less common analyses will be skipped. This saves time and harddrive space.")
        self.autoCorrStopIndex = QHSpinBox()
        self.autoCorrStopIndex.setToolTip("Autocorrelation slope is determined by fitting a line to the first values of the autocorrelation function. This value determines how many values to include in this linear fit.")
        self.minSubCheckBox = QCheckBox("MinSub")
        self.minSubCheckBox.setToolTip("The calculation of autocorrelation decay slope involves taking the natural logarithm of of the autocorrelation. However noise often causes the autocorrelation to have negative values which causes problems for the logarithm. Checking this box adds an offset to the autocorrelation so that no values are negative.")
        layout = QGridLayout()
        _ = layout.addWidget
        _(QLabel("AutoCorr Stop Index"), 0, 0, 1, 1)
        _(self.autoCorrStopIndex, 0, 1, 1, 1)
        _(self.minSubCheckBox, 1, 0, 1, 1)
        self.advanced.setLayout(layout)
        self._layout.addWidget(self.advanced, row, 0, 1, 4)
        row += 1

        self._updateSize()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self._updateSize() #For some reason this must be done here and in the __init__ for it to start up properly.

    def _updateSize(self):
        height = 100  # give this much excess room.
        height += self.presets.height()
        height += self.hardwareCorrections.height()
        height += self.extraReflection.height()
        height += self.scaling.height()
        height += self.signalPrep.height()
        height += self.polySub.height()
        height += self.advanced.height()
        self._frame.setFixedHeight(height)

    def loadFromSettings(self, settings: PWSAnalysisSettings):
        if settings.filterCutoff is None:
            self.filterCheckbox.setChecked(False)
        else:
            self.filterCheckbox.setChecked(True)
            self.filterCutoff.setValue(settings.filterCutoff)
        self.filterOrder.setValue(settings.filterOrder)
        self.polynomialOrder.setValue(settings.polynomialOrder)
        self.extraReflection.loadFromSettings(settings.numericalAperture, settings.referenceMaterial, settings.extraReflectanceId)
        if settings.wavelengthStop is None:
            self.croppingCheckbox.setChecked(False)
        else:
            self.croppingCheckbox.setChecked(True)
            self.wavelengthStop.setValue(settings.wavelengthStop)
            self.wavelengthStart.setValue(settings.wavelengthStart)
        self.advanced.setCheckState(2 if settings.skipAdvanced else 0)
        self.autoCorrStopIndex.setValue(settings.autoCorrStopIndex)
        self.minSubCheckBox.setCheckState(2 if settings.autoCorrMinSub else 0)
        self.relativeUnits.setCheckState(2 if settings.relativeUnits else 0)
        self.hardwareCorrections.loadCameraCorrection(settings.cameraCorrection)
        if settings.waveNumberCutoff is None:
            self.cutoffWaveNumber.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.cutoffWaveNumber.setCheckState(QtCore.Qt.Checked)
            self.waveNumberCutoff.setValue(settings.waveNumberCutoff)

    def getSettings(self) -> PWSRuntimeAnalysisSettings:
        erMetadata, refMaterial, numericalAperture = self.extraReflection.getSettings()
        refMeta = self.cellSelector.getSelectedReferenceMeta()
        cellMeta = self.cellSelector.getSelectedCellMetas()
        name = self._analysisNameEdit.text()
        if refMeta is None:
            raise ValueError('Please select a reference Cell.')
        if name == '':
            raise ValueError("Please give your analysis a name.")
        if len(cellMeta) == 0:
            raise ValueError('Please select cells to analyse.')
        refMeta = refMeta.pws
        cellMeta = [i.pws for i in cellMeta if i.pws is not None]  # If we select some acquisitions that don't have dynamics then they'll get stripped out here
        if refMeta is None:
            raise ValueError("The selected reference acquisition has no valid PWS data.")
        if len(cellMeta) == 0:
            raise ValueError("No valid PWS acquisitions were selected.")
        cutoff = self.filterCutoff.value() if self.filterCheckbox.checkState() else None
        wvStart = self.wavelengthStart.value() if self.croppingCheckbox.checkState() else None
        wvStop = self.wavelengthStop.value() if self.croppingCheckbox.checkState() else None
        return PWSRuntimeAnalysisSettings(settings=PWSAnalysisSettings(filterOrder=self.filterOrder.value(),
                                                                       filterCutoff=cutoff,
                                                                       polynomialOrder=self.polynomialOrder.value(),
                                                                       referenceMaterial=refMaterial,
                                                                       wavelengthStart=wvStart,
                                                                       wavelengthStop=wvStop,
                                                                       skipAdvanced=self.advanced.checkState() != 0,
                                                                       autoCorrMinSub=self.minSubCheckBox.checkState() != 0,
                                                                       autoCorrStopIndex=self.autoCorrStopIndex.value(),
                                                                       numericalAperture=numericalAperture,
                                                                       relativeUnits=self.relativeUnits.checkState() != 0,
                                                                       cameraCorrection=self.hardwareCorrections.getCameraCorrection(),
                                                                       extraReflectanceId=erMetadata.idTag if erMetadata is not None else None,
                                                                       waveNumberCutoff=self.waveNumberCutoff.value() if self.cutoffWaveNumber.checkState != QtCore.Qt.Unchecked else None),
                                          extraReflectanceMetadata=erMetadata,
                                          referenceMetadata=refMeta,
                                          cellMetadata=cellMeta,
                                          analysisName=name)



