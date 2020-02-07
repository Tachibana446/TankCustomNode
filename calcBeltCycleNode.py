# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import math
import sys

# Use Api 2.0

def maya_useNewAPI():
    pass

class calcBeltCycleNode(om.MPxNode):
    id = om.MTypeId(0x7f004)
    name = 'calcBeltCycleNode'
    inputTrailUValue = om.MObject()
    inputTrailUMax = om.MObject()
    inputTrailLength = om.MObject()

    inputBeltUMax = om.MObject()
    inputBeltLength = om.MObject()

    outputUValue = om.MObject()

    def __init__(self):
        om.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return calcBeltCycleNode()

    @staticmethod
    def initialize():
        # output U Value
        nAttr = om.MFnNumericAttribute()
        calcBeltCycleNode.outputUValue = nAttr.create(
            'outputUValue', 'outputUValue', om.MFnNumericData.kFloat, 0.0)
        calcBeltCycleNode.addAttribute(calcBeltCycleNode.outputUValue)

        # input Trail U Value
        nAttr = om.MFnNumericAttribute()
        calcBeltCycleNode.inputTrailUValue = nAttr.create(
            'inputTrailUValue', 'inputTrailUValue', om.MFnNumericData.kFloat, 0.0
        )
        nAttr.storable = True
        nAttr.writable = True
        calcBeltCycleNode.addAttribute(calcBeltCycleNode.inputTrailUValue)
        calcBeltCycleNode.attributeAffects(
            calcBeltCycleNode.inputTrailUValue, calcBeltCycleNode.outputUValue
        )
        # input Trail U Max
        nAttr = om.MFnNumericAttribute()
        calcBeltCycleNode.inputTrailUMax = nAttr.create(
            'inputTrailUMax', 'inputTrailUMax', om.MFnNumericData.kFloat, 0.01
        )
        nAttr.storable = True
        nAttr.writable = True
        calcBeltCycleNode.addAttribute(calcBeltCycleNode.inputTrailUMax)
        calcBeltCycleNode.attributeAffects(
            calcBeltCycleNode.inputTrailUMax, calcBeltCycleNode.outputUValue
        )
        # input Trail Length
        nAttr = om.MFnNumericAttribute()
        calcBeltCycleNode.inputTrailLength = nAttr.create(
            'inputTrailLength', 'inputTrailLength', om.MFnNumericData.kFloat, 0.0
        )
        nAttr.storable = True
        nAttr.writable = True
        calcBeltCycleNode.addAttribute(calcBeltCycleNode.inputTrailLength)
        calcBeltCycleNode.attributeAffects(
            calcBeltCycleNode.inputTrailLength, calcBeltCycleNode.outputUValue
        )
        
        # input Belt U Max
        nAttr = om.MFnNumericAttribute()
        calcBeltCycleNode.inputBeltUMax = nAttr.create(
            'inputBeltUMax', 'inputBeltUMax', om.MFnNumericData.kFloat, 0.01
        )
        nAttr.storable = True
        nAttr.writable = True
        calcBeltCycleNode.addAttribute(calcBeltCycleNode.inputBeltUMax)
        calcBeltCycleNode.attributeAffects(
            calcBeltCycleNode.inputBeltUMax, calcBeltCycleNode.outputUValue
        )
        # input Belt Length
        nAttr = om.MFnNumericAttribute()
        calcBeltCycleNode.inputBeltLength = nAttr.create(
            'inputBeltLength', 'inputBeltLength', om.MFnNumericData.kFloat, 0.0
        )
        nAttr.storable = True
        nAttr.writable = True
        calcBeltCycleNode.addAttribute(calcBeltCycleNode.inputBeltLength)
        calcBeltCycleNode.attributeAffects(
            calcBeltCycleNode.inputBeltLength, calcBeltCycleNode.outputUValue
        )

    def compute(self, plug, dataBlock):
        if(plug == calcBeltCycleNode.outputUValue):
            dataHandle = dataBlock.inputValue(calcBeltCycleNode.inputTrailLength)
            tLen = dataHandle.asFloat()
            dataHandle = dataBlock.inputValue(calcBeltCycleNode.inputTrailUMax)
            tMax = dataHandle.asFloat()
            dataHandle = dataBlock.inputValue(calcBeltCycleNode.inputTrailUValue)
            tVal = dataHandle.asFloat()
            dataHandle = dataBlock.inputValue(calcBeltCycleNode.inputBeltLength)
            bLen = dataHandle.asFloat()
            dataHandle = dataBlock.inputValue(calcBeltCycleNode.inputBeltUMax)
            bMax = dataHandle.asFloat()
            
            result = 0
            if(tMax != 0 and bLen != 0):
                distance = (tVal / tMax) * tLen
                result = distance * bMax / bLen
                result %= bMax
            
            outHandle = dataBlock.outputValue(calcBeltCycleNode.outputUValue)
            outHandle.setFloat(result)
            dataBlock.setClean(plug)

def initializePlugin(obj):
    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.registerNode(calcBeltCycleNode.name, calcBeltCycleNode.id,
                             calcBeltCycleNode.creator, calcBeltCycleNode.initialize, om.MPxNode.kDependNode)
    except:
        sys.stderr.write('Failed to register node: %s' %
                         calcBeltCycleNode.name)
        raise


def uninitializePlugin(obj):
    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.deregisterNode(calcBeltCycleNode.id)
    except:
        sys.stderr.write('Failed to uninitialize node: %s' %
                         calcBeltCycleNode.name)
        pass
