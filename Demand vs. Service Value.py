"""
Model exported as python.
Name : Demand vs. Service Value
Group : aCar Healthcare Ethiopia
With QGIS : 31608
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterMapLayer
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterExpression
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsExpression
import processing


class DemandVsServiceValue(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('Areaofeachhexagoninthegrid', 'Area of each hexagon in the grid (in m2)', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('HealthCareCentersLayerpoints', 'Health Care Centers Layer (points)', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterMapLayer('MapofLemuBilbiloAreaofInterestpolygon', 'Map of Lemu Bilbilo (Region of Interest ROI, polygon)', defaultValue=None, types=[QgsProcessing.TypeVectorPolygon]))
        self.addParameter(QgsProcessingParameterVectorLayer('PopulationLayerpoints', 'Population Layer (points)', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterString('hublayerameattribute', 'hub layer ame attribute', multiLine=False, defaultValue='name 1'))
        self.addParameter(QgsProcessingParameterExpression('weightedvaluepopulationlayer', 'weighted value population layer', parentLayerParameterName='', defaultValue=''))
        self.addParameter(QgsProcessingParameterFeatureSink('Km2Hexagons', '1 km2 hexagons', type=QgsProcessing.TypeVectorPolygon, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('MiddleHexangonPointsWithDistanceNearestHubAndPopulationCount', 'Middle hexangon points with distance, nearest hub and population count', type=QgsProcessing.TypeVectorPoint, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        results = {}
        outputs = {}

        # Create hexagon Grid on ROI
        alg_params = {
            'CRS': 'ProjectCrs',
            'EXTENT': parameters['MapofLemuBilbiloAreaofInterestpolygon'],
            'HOVERLAY': 0,
            'HSPACING': parameters['Areaofeachhexagoninthegrid'],
            'TYPE': 4,
            'VOVERLAY': 0,
            'VSPACING': parameters['Areaofeachhexagoninthegrid'],
            'OUTPUT': parameters['Km2Hexagons']
        }
        outputs['CreateHexagonGridOnRoi'] = processing.run('native:creategrid', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Km2Hexagons'] = outputs['CreateHexagonGridOnRoi']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Count points in polygon
        alg_params = {
            'CLASSFIELD': '',
            'FIELD': 'population',
            'POINTS': parameters['PopulationLayerpoints'],
            'POLYGONS': outputs['CreateHexagonGridOnRoi']['OUTPUT'],
            'WEIGHT': QgsExpression(' @weightedvaluepopulationlayer ').evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CountPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Distance to nearest hub (points)
        alg_params = {
            'FIELD': QgsExpression(' @hublayerameattribute ').evaluate(),
            'HUBS': parameters['HealthCareCentersLayerpoints'],
            'INPUT': outputs['CountPointsInPolygon']['OUTPUT'],
            'UNIT': 3,
            'OUTPUT': parameters['MiddleHexangonPointsWithDistanceNearestHubAndPopulationCount']
        }
        outputs['DistanceToNearestHubPoints'] = processing.run('qgis:distancetonearesthubpoints', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['MiddleHexangonPointsWithDistanceNearestHubAndPopulationCount'] = outputs['DistanceToNearestHubPoints']['OUTPUT']
        return results

    def name(self):
        return 'Demand vs. Service Value'

    def displayName(self):
        return 'Demand vs. Service Value'

    def group(self):
        return 'aCar Healthcare Ethiopia'

    def groupId(self):
        return 'aCar Healthcare Ethiopia'

    def createInstance(self):
        return DemandVsServiceValue()
