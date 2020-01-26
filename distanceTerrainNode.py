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
    terrainMatrix = om.MObject()
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
        nAttr = om.MFnMatrixAttribute()
        distanceTerrainNode.terrainMatrix = nAttr.create(
            'terrainMatrix', 'terrainMtrx')
        nAttr.storable = True

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

        distanceTerrainNode.addAttribute(distanceTerrainNode.terrainMatrix)
        distanceTerrainNode.addAttribute(distanceTerrainNode.terrain)
        distanceTerrainNode.addAttribute(distanceTerrainNode.jointPos)
        distanceTerrainNode.addAttribute(distanceTerrainNode.distance)
        distanceTerrainNode.attributeAffects(
            distanceTerrainNode.terrainMatrix, distanceTerrainNode.distance)
        distanceTerrainNode.attributeAffects(
            distanceTerrainNode.terrain, distanceTerrainNode.distance)
        distanceTerrainNode.attributeAffects(
            distanceTerrainNode.jointPos, distanceTerrainNode.distance)

    # 実際の計算
    def compute(self, plug, dataBlock):
        if(plug == distanceTerrainNode.distance):
            dataHandle = dataBlock.inputValue(distanceTerrainNode.terrain)
            _mesh = dataHandle.asMesh()
            if(not _mesh.hasFn(om.MFn.kMesh)):
                dataBlock.setClean(plug)
                return
            dataHandle = dataBlock.inputValue(distanceTerrainNode.jointPos)
            x, y, z = dataHandle.asFloat3()  # 調査する点の座標
            pvec = om.MFloatVector(x, y, z)
            polyIter = om.MItMeshPolygon(_mesh)
            # ワールド行列
            dataHandle = dataBlock.inputValue(
                distanceTerrainNode.terrainMatrix)
            matrix = dataHandle.asMatrix()

            nomesh = True  # 直下に面がない場合のフラグ
            # 面を構成する点ごとに繰り返す
            while(not polyIter.isDone()):
                triangles = polyIter.getTriangles(om.MSpace.kObject)  # 頂点
                _triPoints = triangles[0]
                triPoints = [_triPoints[:3], _triPoints[3:]]
                for (_ip, points) in enumerate(triPoints):
                    length = len(points)  # 頂点数
                    count = 0  # 外積の結果
                    yAvg = 0  # y成分平均
                    for i in range(length):
                        t1vec = om.MFloatVector(points[i])
                        t2vec = om.MFloatVector(points[(i+1) % length])
                        # ワールド座標に
                        t1vec = self.vectorCalc(t1vec, matrix)
                        t2vec = self.vectorCalc(t2vec, matrix)
                        yAvg += t1vec.y
                        t1vec.y = 0
                        t2vec.y = 0
                        sub1 = (pvec - t1vec)
                        sub2 = (t1vec - t2vec)
                        # print("[t1 {}  t2 {}]: s1({}) s2({}) ({})".format(str(t1vec), str(t2vec), str(sub1), str(sub2), str(sub1 ^ sub2)))
                        if((sub1 ^ sub2).y >= 0):
                            count += 1
                        else:
                            count -= 1
                    yAvg /= length
                    if(count == length or count == -length):
                        # 直下の面であるといえる
                        outputHandle = dataBlock.outputValue(
                            distanceTerrainNode.distance)
                        outputHandle.setFloat(y - yAvg)
                        nomesh = False
                        break
                if(not nomesh):
                    break
                polyIter.next(0)

            if(nomesh):
                outputHandle = dataBlock.outputValue(
                    distanceTerrainNode.distance)
                outputHandle.setFloat(999)

            dataBlock.setClean(plug)

    # 行列とベクトルの計算
    @staticmethod
    def vectorCalc(vec, matrix):
        if(not isinstance(matrix, om.MMatrix)):
            # print('is not matrix')
            return vec
        vm = om.MMatrix([[vec.x, 0, 0, 1], [0, vec.y, 0, 1],
                         [0, 0, vec.z, 1], [0, 0, 0, 1]])
        res = vm * matrix
        # print('input vector:{}'.format(vec))
        # print('world matrix')
        # print(matrix)
        # print('result vector')
        result = om.MFloatVector(res.getElement(
            0, 0), res.getElement(1, 1), res.getElement(2, 2))
        # print(result)
        return om.MFloatVector(result)


def fmt(obj):
    if(obj is om.MPointArray):
        return "[{}, {}, {}]".format(fmt(obj[0]), fmt(obj[1]), fmt(obj[2]))
    elif(obj is om.MPoint):
        return "({}, {}, {})".format(str(obj.x), str(obj.y), str(obj.z))
    else:
        return str(obj)

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
