import abc
import os
from PyQt5.QtCore import QObject
from cachetools import cachedmethod, LRUCache
from pwspy import dataTypes as pwsdt
from pwspy_gui.PWSAnalysisApp.componentInterfaces import ROIManager


class _DefaultROIManager(ROIManager, QObject):
    def __init__(self, parent: QObject = None):
        super().__init__(parent=parent)
        self._cache = LRUCache(maxsize=2048)  # Store this many ROIs at once

    @staticmethod
    def _getCacheKey(roiFile: pwsdt.RoiFile):
        return os.path.split(roiFile.filePath)[0], roiFile.name, roiFile.number

    def removeRoi(self, roiFile: pwsdt.RoiFile):
        self._cache.pop(self._getCacheKey(roiFile))
        roiFile.delete()
        self.roiRemoved.emit(roiFile)

    def updateRoi(self, roiFile: pwsdt.RoiFile, roi: pwsdt.Roi):
        roiFile.update(roi)
        self._cache[self._getCacheKey(roiFile)] = roiFile
        self.roiUpdated.emit(roiFile)

    def createRoi(self, acq: pwsdt.Acquisition, roi: pwsdt.Roi, roiName: str, roiNumber: int, overwrite: bool = False) -> pwsdt.RoiFile:
        """

        Args:
            acq: The acquisition to save the ROI to
            roi: The ROI to save.
            roiName: The name to save the ROI as.
            roiNumber: The number to save the ROI as.
            overwrite: Whether to overwrite existing ROIs with conflicting name/number combo.

        Returns:
            A reference to the created ROIFile

        Raises:
            OSError: If `overwrite` is false and an ROIFile for this name and number already exists.

        """
        try:
            roiFile = acq.saveRoi(roiName, roiNumber, roi, overwrite=overwrite)
        except OSError as e:
            raise e
        self._cache[self._getCacheKey(roiFile)] = roiFile
        self.roiCreated.emit(roiFile, overwrite)
        return roiFile

    @cachedmethod(lambda self: self._cache, key=lambda acq, roiName, roiNum: (acq.filePath, roiName, roiNum))  # Cache results
    def getROI(self, acq: pwsdt.Acquisition, roiName: str, roiNum: int) -> pwsdt.RoiFile:
        return acq.loadRoi(roiName, roiNum)

    def close(self):
        self._cache.clear()
