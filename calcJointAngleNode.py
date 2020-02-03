# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import math
import sys
# import pdb

# Use Api 2.0


def maya_useNewAPI():
    pass


class calcJointAngleNode(om.MPxNode):
    id = om.MTypeId(0x7f003)
    name = 'calcJointAngleNode'
    inputR = om.MObject()
    inputDistance = om.MObject()
    offsetTerrain = om.MObject()
    angleOffset = om.MObject()
    unit = om.MObject()
    outputAngle = om.MObject()

    def __init__(self):
        om.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return calcJointAngleNode()

    @staticmethod
    def initialize():
        # output Angle
        nAttr = om.MFnNumericAttribute()
        calcJointAngleNode.outputAngle = nAttr.create(
            'outputAngle', 'outputAngle', om.MFnNumericData.kFloat, 0.0)
        calcJointAngleNode.addAttribute(calcJointAngleNode.outputAngle)
        # input R
        nAttr = om.MFnNumericAttribute()
        calcJointAngleNode.inputR = nAttr.create(
            'inputRadius', 'inputR', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.writable = True
        calcJointAngleNode.addAttribute(calcJointAngleNode.inputR)
        calcJointAngleNode.attributeAffects(
            calcJointAngleNode.inputR, calcJointAngleNode.outputAngle)
        # input Distance
        nAttr = om.MFnNumericAttribute()
        calcJointAngleNode.inputDistance = nAttr.create(
            'inputDistance', 'inputDistance', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.writable = True
        calcJointAngleNode.addAttribute(calcJointAngleNode.inputDistance)
        calcJointAngleNode.attributeAffects(
            calcJointAngleNode.inputDistance, calcJointAngleNode.outputAngle)
        # offsetTerrain
        nAttr = om.MFnNumericAttribute()
        calcJointAngleNode.offsetTerrain = nAttr.create(
            'offsetTerrain', 'offsetTerrain', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.writable = True
        calcJointAngleNode.addAttribute(calcJointAngleNode.offsetTerrain)
        calcJointAngleNode.attributeAffects(
            calcJointAngleNode.offsetTerrain, calcJointAngleNode.outputAngle)
        # angleOffset
        nAttr = om.MFnNumericAttribute()
        calcJointAngleNode.angleOffset = nAttr.create(
            'angleOffset', 'angleOffset', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.writable = True
        calcJointAngleNode.addAttribute(calcJointAngleNode.angleOffset)
        calcJointAngleNode.attributeAffects(
            calcJointAngleNode.angleOffset, calcJointAngleNode.outputAngle)
        # unit
        nAttr = om.MFnNumericAttribute()
        calcJointAngleNode.unit = nAttr.create(
            'unit', 'unit', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.writable = True
        calcJointAngleNode.addAttribute(calcJointAngleNode.unit)
        calcJointAngleNode.attributeAffects(
            calcJointAngleNode.unit, calcJointAngleNode.outputAngle)

    # 実際の計算

    def compute(self, plug, dataBlock):
        if(plug == calcJointAngleNode.outputAngle):
            dataHandle = dataBlock.inputValue(calcJointAngleNode.inputR)
            ir = dataHandle.asFloat()
            dataHandle = dataBlock.inputValue(calcJointAngleNode.angleOffset)
            _angleOffset = dataHandle.asFloat()
            result = 90 + _angleOffset
            if(ir != 0):
                dataHandle = dataBlock.inputValue(
                    calcJointAngleNode.inputDistance)
                inpDistance = dataHandle.asFloat()
                dataHandle = dataBlock.inputValue(calcJointAngleNode.unit)
                u = dataHandle.asFloat()
                dataHandle = dataBlock.inputValue(
                    calcJointAngleNode.offsetTerrain)
                ot = dataHandle.asFloat()
                # オフセットを除いた車輪と地表との距離の半径比（sin(θ)で求まる値）
                dist = (inpDistance * u - ot) / ir
                # arcsinの範囲から超えるときはデフォルトの角度を返す
                if(dist < 1 and dist > -1):
                    rad = math.asin(dist)
                    result = math.degrees(rad) + _angleOffset

            outHandle = dataBlock.outputValue(calcJointAngleNode.outputAngle)
            outHandle.setFloat(result)
            dataBlock.setClean(plug)


# ノード名、ID, creater関数, Initialize関数, ノードの種類を登録


def initializePlugin(obj):
    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.registerNode(calcJointAngleNode.name, calcJointAngleNode.id,
                             calcJointAngleNode.creator, calcJointAngleNode.initialize, om.MPxNode.kDependNode)
    except:
        sys.stderr.write('Failed to register node: %s' %
                         calcJointAngleNode.name)
        raise


def uninitializePlugin(obj):
    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.deregisterNode(calcJointAngleNode.id)
    except:
        sys.stderr.write('Failed to uninitialize node: %s' %
                         calcJointAngleNode.name)
        pass
