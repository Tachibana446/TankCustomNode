# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import math
import sys

# Use Api 2.0


def maya_useNewAPI():
    pass


class distanceTerrainNode(om.MPxNode):
    id = om.MTypeId(0x7f002)
    name = 'distanceTerrainNode'
    terrain = om.MObject()
    jointPos = om.MObject()
    distance = om.MObject()

    def __init__(self):
        om.MPxNode.__init__(self)

    @staticmethod
    def creator():
        return distanceTerrainNode()

    @staticmethod
    def initialize():
        nAttr = om.MFnTypedAttribute()
        distanceTerrainNode.terrain = nAttr.create(
            'terrain', 'terrain', om.MFnData.kMesh)
        nAttr.storable = True
        nAttr.writable = True
        nAttr = om.MFnNumericAttribute()
        distanceTerrainNode.jointPos = nAttr.create(
            'jointPosition', 'jointPos', om.MFnNumericData.k3Float, 0
        )
        nAttr.storable = True
        nAttr.writable = True
        nAttr = om.MFnNumericAttribute()
        distanceTerrainNode.distance = nAttr.create(
            'distance', 'distance', om.MFnNumericData.kFloat, 0
        )

        distanceTerrainNode.addAttribute(distanceTerrainNode.terrain)
        distanceTerrainNode.addAttribute(distanceTerrainNode.jointPos)
        distanceTerrainNode.addAttribute(distanceTerrainNode.distance)
        distanceTerrainNode.attributeAffects(
            distanceTerrainNode.terrain, distanceTerrainNode.distance)
        distanceTerrainNode.attributeAffects(
            distanceTerrainNode.jointPos, distanceTerrainNode.distance)

    def compute(self, plug, dataBlock):
        if(plug == distanceTerrainNode.distance):

            dataHandle = dataBlock.inputValue(distanceTerrainNode.terrain)
            _mesh = dataHandle.asMesh()
            if(not _mesh.hasFn(om.MFn.kMesh)):
                print(_mesh)
                print(_mesh.hasFn(om.MFn.kMesh))
                print(_mesh.isNull)
                print('mesh is null')
            else:
                polyIter = om.MItMeshPolygon(_mesh)
                while not polyIter.isDone():
                    print('\t vtx : {}'.format(polyIter.getPoints()))
                    polyIter.next(0)
            dataBlock.setClean(plug)

# ノード名、ID, creater関数, Initialize関数, ノードの種類を登録


def initializePlugin(obj):
    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.registerNode(distanceTerrainNode.name, distanceTerrainNode.id,
                             distanceTerrainNode.creator, distanceTerrainNode.initialize, om.MPxNode.kDependNode)
    except:
        sys.stderr.write('Failed to register node: %s' %
                         distanceTerrainNode.name)
        raise


def uninitializePlugin(obj):
    mplugin = om.MFnPlugin(obj)
    try:
        mplugin.deregisterNode(distanceTerrainNode.id)
    except:
        sys.stderr.write('Failed to uninitialize node: %s' %
                         distanceTerrainNode.name)
        pass
