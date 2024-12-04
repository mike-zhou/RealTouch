import FreeCAD
from abc import ABC, abstractmethod
import time

class Axis:
    def __init__(self, docName: str, startPos: float, endPos: float):
        self._document = FreeCAD.getDocument(docName)
        self._startPos = startPos
        self._endPos = endPos
        self._currentPos = startPos

    def _recompute(self):
        FreeCAD.getDocument(self._docName).recompute()


    def curAbsPos(self):
        return self._currentPos
    

    def absStartPos(self):
        return self._startPos
    

    def absEndPos(self):
        return self._endPos


    def curLogPos(self):
        if self._startPos < self._endPos:
            return self._currentPos - self._startPos
        else:
            return self._startPos - self._currentPos
    
    def logStartPos(self):
        return 0
    

    def logEndPos(self):
        return abs(self._endPos - self._startPos)


    def stepUp(self, steps: float = 1):
        """ Advance to the end of the axis """
        if steps < 0:
            steps = 0

        if self._startPos < self._endPos:
            self._currentPos += steps
            if self._currentPos > self._endPos:
                self._currentPos = self._endPos
        else:
            self._currentPos -= steps
            if self._currentPos < self._endPos:
                self._currentPos = self._endPos
        

    def stepDown(self, steps: float = 1):
        """ Return to the start of the axis """
        if steps < 0:
            steps = 0

        if self._startPos < self._endPos:
            self._currentPos -= steps
            if self._currentPos < self._startPos:
                self._currentPos = self._startPos
        else:
            self._currentPos += steps
            if self._currentPos > self._startPos:
                self._currentPos = self._startPos


    def setAbsPos(self, position: float):
        self._currentPos = position
        if self._startPos < self._endPos:
            if self._currentPos < self._startPos:
                self._currentPos = self._startPos
            elif self._currentPos > self._endPos:
                self._currentPos = self._endPos
        else:
            if self._currentPos < self._endPos:
                self._currentPos = self._endPos
            elif self._currentPos > self._startPos:
                self._currentPos = self._startPos


    def setLogPos(self, offset:float):
        if offset < 0:
            offset = 0
        
        if self._startPos < self._endPos:
            self._currentPos = self._startPos + offset
            if self._currentPos > self._endPos:
                self._currentPos = self._endPos
        else:
            self._currentPos = self._startPos - offset
            if self._currentPos < self._endPos:
                self._currentPos = self._endPos


    @abstractmethod
    def refresh(self):
        """ Recompute the object """
        pass

class Axis_A(Axis):
    def __init__(self):
        super().__init__(docName='subAsm_Axis_A', 
                         startPos=10, 
                         endPos=850)

    def refresh(self):
        self._document.getObject('Variables').Apos = self._currentPos
        self._document.recompute()


class Axis_B(Axis):
    def __init__(self):
        super().__init__(docName='subAsm_Axis_B', 
                         startPos=-490, 
                         endPos=-80)

    def refresh(self):
        self._document.getObject('Variables').B = self._currentPos
        self._document.recompute()


class Axis_U(Axis):
    def __init__(self):
        super().__init__(docName='Assembly', 
                         startPos=0, 
                         endPos=180)

    def refresh(self):
        self._document.getObject('Variables').U = self._currentPos
        self._document.recompute()


class Axis_V(Axis):
    def __init__(self):
        super().__init__(docName='Assembly', 
                         startPos=0, 
                         endPos=90)

    def refresh(self):
        self._document.getObject('Variables').Vpos = self._currentPos
        self._document.recompute()


class Axis_W(Axis):
    def __init__(self):
        super().__init__(docName='subAsm_Axis_W', 
                         startPos=-20, 
                         endPos=0)

    def refresh(self):
        self._document.getObject('Variables').Wpos = self._currentPos
        self._document.recompute()


class Axis_X(Axis):
    def __init__(self):
        super().__init__(docName='Assembly', 
                         startPos=50, 
                         endPos=780)

    def refresh(self):
        self._document.getObject('Variables').X = self._currentPos
        self._document.recompute()


class Axis_Y(Axis):
    def __init__(self):
        super().__init__(docName='Assembly', 
                         startPos=-130, 
                         endPos=-500)

    def refresh(self):
        self._document.getObject('Variables').Y = self._currentPos
        self._document.recompute()


class Axis_Z(Axis):
    def __init__(self):
        super().__init__(docName='Assembly', 
                         startPos=150, 
                         endPos=430)

    def refresh(self):
        self._document.getObject('Variables').Z = self._currentPos
        self._document.recompute()


def test_axis(axis: Axis):
    """ Move Axis from beginning to the end, then back to beginning """
    axis.setLogPos(0)
    axis.refresh()
    time.sleep(2)

    counter = 0
    while counter < axis.logEndPos():
        axis.stepUp()
        axis.refresh()
        counter += 1
    
    time.sleep(2)
    
    while counter > axis.logStartPos():
        axis.stepDown()
        axis.refresh()
        counter -= 1


# open all documents in Freecad, then
# run the following command in python console:
#     exec(open("d:/freecad/realtouch/scripts/axis.py").read())
if __name__ == "__main__":
    test_axis(Axis_A())
    time.sleep(2)
    test_axis(Axis_B())
    time.sleep(2)
    test_axis(Axis_X())
    time.sleep(2)
    test_axis(Axis_Y())
    time.sleep(2)
    test_axis(Axis_Z())
    time.sleep(2)
    test_axis(Axis_U())
    time.sleep(2)
    test_axis(Axis_V())
    time.sleep(2)
    test_axis(Axis_W())
    time.sleep(2)
    