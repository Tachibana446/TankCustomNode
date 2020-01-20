# -*- coding: utf-8 -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import math, sys

# Maya API 2.0を使用するために必要な関数
def maya_useNewAPI():
    pass

# 実際のクラス
class sampleNode(om.MPxNode):
    id = om.MTypeId(0x7f001) # 一意なID
    input = om.MObject()
    output = om.MObject()

    # インスタンスを返すメソッド
    @staticmethod
    def creator():
        return sampleNode()

    # 初期化時にMayaから呼ばれるメソッド
    # アトリビュートの設定を行う
    @staticmethod
    def initialize():
        # アトリビュートはMFnAttributeクラスのサブクラスのcreateメソッドを使い定義する
        nAttr = om.MFnNumericAttribute()
        sampleNode.input = nAttr.create(
            'input', 'i', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.writable = True

        nAttr = om.MFnNumericAttribute()
        sampleNode.output = nAttr.create('output', 'o', om.MFnNumericData.kFloat, 0.0)
        nAttr.storable = True
        nAttr.writable = True

        # 定義した後はMPxNodeのaddAttributeを実行する
        sampleNode.addAttribute(sampleNode.input)
        sampleNode.addAttribute(sampleNode.output)
        # また、inputが変更された際にoutputを再計算するように設定する
        sampleNode.attributeAffects( sampleNode.input, sampleNode.output)
        
    # コンストラクタは親のコンストラクタを呼ぶ
    def __init__(self):
        om.MPxNode.__init__(self)

    # アトリビュートの値が計算される際にMayaから呼び出されるメソッド
    def compute(self, plug, dataBlock):
        if(plug == sampleNode.output):
            dataHandle = dataBlock.inputValue(sampleNode.input)
            inputFloat = dataHandle.asFloat()
            result = math.sin(inputFloat) * 10.0
            outputHandle = dataBlock.outputValue(sampleNode.output)
            outputHandle.setFloat(result)
            dataBlock.setClean(plug)
            
    # http://help.autodesk.com/view/MAYAUL/2016/ENU/
    # api1.0では明示的にplugの処理を行わないことを伝えない限りMStatus.kUnknownParameterは返さないとされる
    # api2.0ではそもそもMStatusがないので無視して良さそう

# 新しいノードの登録を行うMayaから呼ばれる関数
def initializePlugin(obj):
    mplugin = om.MFnPlugin(obj)

    try:
        mplugin.registerNode('sampleNode', sampleNode.id, sampleNode.creator,
                             sampleNode.initialize, om.MPxNode.kDependNode)
    except:
        sys.stderr.write('Faled to register node: %s' % 'sampleNode')
        raise

# プラグインを終了する際にMayaから呼ばれる関数
def uninitializePlugin(mobject):
    mplugin = om.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(sampleNode.id)
    except:
        sys.stderr.write('Faled to uninitialize node: %s' % 'sampleNode')
        raise
