# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CensoSegmento
                                 A QGIS plugin
 Censo Segmento
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-09-15
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Maximiliano Monti
        email                : renzomiguelmonti@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QVersionNumber, QCoreApplication, Qt, QObject, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QDialog, QFormLayout, QInputDialog , QLineEdit , QMessageBox
from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
from qgis.core import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .censo_segmento_dialog import CensoSegmentoDialog
import os
import sys


class CensoSegmento:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CensoSegmento_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&INDEC - CNPHyV')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CensoSegmento', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip='Por aca puede ir la cosa',
        whats_this='Que es esto',
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/censo_segmento/icon.png'
        current_dir = os.path.dirname(os.path.realpath(__file__))
        poll_icon_path = os.path.join(current_dir,'icons/poll.png')
        self.add_action(
            poll_icon_path,
            text=self.tr(u'Menu Principal'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.add_action(
            poll_icon_path,
            add_to_toolbar=False,
            text=self.tr(u'Plano de Radio'),
            callback=self.runRadio,
            parent=self.iface.mainWindow())

        self.add_action(
            poll_icon_path,
            add_to_toolbar=False,
            text=self.tr(u'Plano de Segmentación'),
            callback=self.runSegmentacion,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Censo Segmento'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = CensoSegmentoDialog()
            # Events
            self.dlg.buttonRadio.clicked.connect(self.runRadio)
            self.dlg.buttonSegmentacion.clicked.connect(self.runSegmentacion)   

        # show the dialog
        self.dlg.show()




    def runRadio(self, iface):
        from qgis.utils import iface
        #####################################Conexion existente en el admnistrador de BD##############################################
        ##########Conexion desde BD a Postgis
        QgsProject.instance().clear()
        qs = QSettings()
        dbHost = qs.value("PostgreSQL/connections/informatica/host",'10.70.80.62')
        dbPort = qs.value("PostgreSQL/connections/informatica/port",'5432')
        dbName = qs.value("PostgreSQL/connections/informatica/database",'DEVSEG')
        
        ############Pedir al usuario cargar los campos de  usuario y contraseña
        dbUsr = QInputDialog.getText(None, 'usuario', 'Introduce el nombre de usuario de la base de datos')
        dbPwd = QInputDialog.getText(None, 'contraseña', 'Introduce la contraseña', QLineEdit.Password)
        
        #####################################Conexion PostGIS##############################################

        # introducimos nombre del servidor, puerto, nombre de la base de datos, usuario y contraseña
        uri = QgsDataSourceUri()
        uri.setConnection(dbHost,dbPort,dbName,dbUsr[0],dbPwd[0])

        ##############################Verificar Usuuario y Contraseña##########################################
#        origen = QInputDialog.getText(None, 'origen', 'Introduce la ruta de acceso')
        aglomerado = QInputDialog.getText(None, 'aglomerado', 'Introduce el nombre completo del aglomerado', text = 'e0359')
        origen = os.path.dirname(__file__)
#       print(sys.path[0])
#       print (origen)


        ####################### Agrego las tablas .CSV de datos geograficos############################
        ####### Agrego tabla provincia
        capa = origen + '\datos_prov\provincia.csv'
        nomcapa = 'provincia'  
        layer = QgsVectorLayer(capa,nomcapa,'ogr')
        if not layer.isValid():
            print ("la capa no es correcta")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        ####### Agrego tabla departamento##################################
        capa = (origen + '\datos_prov\departamentos.csv')
        nomcapa = 'departamento'  
        layer = QgsVectorLayer(capa,nomcapa,'ogr')
        if not layer.isValid():
            print ("la capa no es correcta")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        #######  Agrego tabla localidad######################
        capa = (origen + '\datos_prov\localidad.csv')
        nomcapa = 'localidad'  
        layer = QgsVectorLayer(capa,nomcapa,'ogr')
        if not layer.isValid():
            print ("la capa no es correcta")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        
        


        ########################## Agrego todas las capas al proyecto###################################
        ####### Agrego la capa  Segmento
        uri.setDataSource(aglomerado[0], "arc" , "wkb_geometry" )
        layer = QgsVectorLayer(uri.uri(), "Segmentacion", "postgres")
        if not layer.isValid():
            print ("No se cargo capa Segmento")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        layer.loadNamedStyle(origen + '\estilo_radio\segmentos.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        layer.triggerRepaint()
        ########Agrego la capa  Mascara 
        sql = aglomerado[0] + ".v_radios"
        uri.setDataSource("", "( select * from " + sql + ")","wkb_geometry","","gid")
        vlayer = QgsVectorLayer(uri.uri(),"Mascara","postgres")
        if not vlayer.isValid():
            print ("No se cargola capa Mascara ")
        QgsProject.instance().addMapLayer(vlayer)
        renderer = vlayer.renderer()
        vlayer.loadNamedStyle(origen +'\estilo_radio\mascara.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        vlayer.triggerRepaint() 
        #######Agrego la capa  Especiales
        uri.setDataSource(aglomerado[0], "arc" , "wkb_geometry" )
        layer = QgsVectorLayer(uri.uri(), "CodEspeciales", "postgres")
        if not layer.isValid():
            print ("No se cargo capa Codigos Especiales")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        layer.loadNamedStyle(origen + '\estilo_radio\especiales.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        layer.triggerRepaint()
        ####### Agrego la capa  Radios desde BD
        sql = aglomerado[0] + ".v_radios"
        uri.setDataSource("", "( select * from " + sql + ")","wkb_geometry","","gid")
        vlayer = QgsVectorLayer(uri.uri(),"Radio","postgres")
        if not vlayer.isValid():
            print ("No se cargo la  capa Radio ")
        QgsProject.instance().addMapLayer(vlayer)
        renderer = vlayer.renderer()
        vlayer.loadNamedStyle(origen +'\estilo_radio\pradio.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        vlayer.triggerRepaint() 
        ####### Agrego la capa Etiquetas Manzanas  
        uri.setDataSource(aglomerado[0] , "lab" , "wkb_geometry" )
        layer = QgsVectorLayer(uri.uri(), "Etiqueta_manzana", "postgres")
        if not layer.isValid():
            print ("No se cargo capa Etiquetas manzanas")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        layer.loadNamedStyle(origen +'\estilo_radio\manzanas.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        layer.triggerRepaint() 

        ############################# Agrego la capa Descripcion ########################### 
        sql = aglomerado[0]
        uri.setDataSource("", "( select * , concat(prov,depto,codloc,lpad(frac::text,2,'0'),lpad(radio::text,2,'0'),seg) link , st_point(0,0) geom from indec.describe_segmentos_con_direcciones('" + sql + "'))","geom","", "segmento_id")
        layer = QgsVectorLayer(uri.uri(), "descripcion", "postgres")
        if not layer.isValid():
            print ("No se cargo capa Descripcion")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        layer.loadNamedStyle(origen +'\estilo_radio\descripcion.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        layer.triggerRepaint() 
        
        
        ########################### Agregar plantillas de salida##############
        #### Plantilla tamaño A4 ###############  
        pry= QgsProject.instance()
        #Añadi una verificación de la ruta del archivo qtp
###        
#
##
        ruta= origen + r'\plantillas\radio_a4.qpt'
        if os.path.exists(ruta):
            with open(ruta, 'r') as templateFile:
                myTemplateContent = templateFile.read()
            layout=QgsPrintLayout(pry)
            lmg = QgsProject.instance().layoutManager()
            layout.setName("A4")
            layout.initializeDefaults()
            myDocument = QDomDocument()
            myDocument.setContent(myTemplateContent)
            ms = QgsMapSettings()
            layout.loadFromTemplate(myDocument,QgsReadWriteContext(),True)
            lmg.addLayout(layout)
        else:
            print("error en la ruta del archivo" )
    
        #### Plantilla tamaño A3 ###############  
        ruta2= ruta= origen + r'\plantillas\radio_a3.qpt'
        if os.path.exists(ruta2):
            with open(ruta2, 'r') as templateFile:
                myTemplateContent = templateFile.read()
            layout=QgsPrintLayout(pry)
            lmg = QgsProject.instance().layoutManager()
            layout.setName("A3")
            layout.initializeDefaults()
            myDocument = QDomDocument()
            myDocument.setContent(myTemplateContent)
            ms = QgsMapSettings()
            layout.loadFromTemplate(myDocument,QgsReadWriteContext(),True)
            lmg.addLayout(layout)
        else:
            print("error en la ruta del archivo A3")



    def runSegmentacion(self , iface):
        from qgis.utils import iface
        #####################################Conexion existente en el admnistrador de BD##############################################
        ##########Conexion desde BD a Postgis
        QgsProject.instance().clear()
        qs = QSettings()
        dbHost = qs.value("PostgreSQL/connections/informatica/host",'10.70.80.62')
        dbPort = qs.value("PostgreSQL/connections/informatica/port",'5432')
        dbName = qs.value("PostgreSQL/connections/informatica/database",'DEVSEG')
        ############Pedir al usuario cargar los campos de  usuario y contraseña
        dbUsr = QInputDialog.getText(None, 'usuario', 'Introduce el nombre de usuario de la base de datos')
        dbPwd = QInputDialog.getText(None, 'contraseña', 'Introduce la contraseña', QLineEdit.Password)
        #####################################Conexion PostGIS##############################################
        # introducimos nombre del servidor, puerto, nombre de la base de datos, usuario y contraseña
        uri = QgsDataSourceUri()
        uri.setConnection(dbHost,dbPort,dbName,dbUsr[0],dbPwd[0])
        ##############################Verificar Usuuario y Contraseña##########################################
#       origen = QInputDialog.getText(None, 'origen', 'Introduce la ruta de acceso')
        aglomerado = QInputDialog.getText(None, 'aglomerado', 'Introduce el nombre completo del aglomerado', text = 'e0359')
        origen = os.path.dirname(__file__)



        ####################### Agrego las tablas .CSV de datos geograficos############################
        # Agrego tabla provincia
        capa = origen + '\datos_prov\provincia.csv'
        nomcapa = 'provincia'  
        layer = QgsVectorLayer(capa,nomcapa,'ogr')
        if not layer.isValid():
            print ("la capa no es correcta")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        ################## Agrego tabla departamento##################################
        capa = (origen + '\datos_prov\departamentos.csv')
        nomcapa = 'departamento'  
        layer = QgsVectorLayer(capa,nomcapa,'ogr')
        if not layer.isValid():
            print ("la capa no es correcta")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        ################## Agrego tabla localidad######################
        capa = (origen + '\datos_prov\localidad.csv')
        nomcapa = 'localidad'  
        layer = QgsVectorLayer(capa,nomcapa,'ogr')
        if not layer.isValid():
            print ("la capa no es correcta")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()

        ########################## Agrego todas las capas al proyecto###################################
        #Agrego la capa  SEGMENTOS 
        uri.setDataSource(aglomerado[0], "arc" , "wkb_geometry" )
        layer = QgsVectorLayer(uri.uri(), "segmentos", "postgres")
        if not layer.isValid():
            print ("No se cargo capa segmento")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        layer.loadNamedStyle(origen + '\estilo_segmento\segmento.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        layer.triggerRepaint()
        ########Agrego la capa  Mascara 
        sql = aglomerado[0] + ".v_radios"
        uri.setDataSource("", "( select * from " + sql + ")","wkb_geometry","","gid")
        vlayer = QgsVectorLayer(uri.uri(),"Mascara","postgres")
        if not vlayer.isValid():
            print ("No se cargola capa Mascara ")
        QgsProject.instance().addMapLayer(vlayer)
        renderer = vlayer.renderer()
        vlayer.loadNamedStyle(origen +'\estilo_segmento\mascara.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        vlayer.triggerRepaint() 
        # Agrego la capa  ESPECIALES
        uri.setDataSource(aglomerado[0], "arc" , "wkb_geometry" )
        layer = QgsVectorLayer(uri.uri(), "especiales", "postgres")
        if not layer.isValid():
            print ("No se cargo la capa de codigos especiales")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        layer.loadNamedStyle(origen + '\estilo_segmento\especiales.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        layer.triggerRepaint()
        ####### Agrego la capa  Radios desde BD
        sql = aglomerado[0] + ".v_radios"
        uri.setDataSource("", "( select * from " + sql + ")","wkb_geometry","","gid")
        vlayer = QgsVectorLayer(uri.uri(),"Radio","postgres")
        if not vlayer.isValid():
            print ("No se cargo la  capa Radio ")
        QgsProject.instance().addMapLayer(vlayer)
        renderer = vlayer.renderer()
        vlayer.loadNamedStyle(origen +'\estilo_segmento\pradio.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        vlayer.triggerRepaint() 
        #Agrego la capa  ETIQUETAS  MANZANA  
        sql = aglomerado[0] + ".v_manzanas"
        uri.setDataSource("", "( select * from " + sql + ")","wkb_geometry","","gid")
        layer = QgsVectorLayer(uri.uri(), "etiqueta_manzana", "postgres")
        if not layer.isValid():
            print ("el numero de aglomerado no es correcto")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        layer.loadNamedStyle(origen +'\estilo_segmento\manzana.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        layer.triggerRepaint()


        ############################# Agrego la capa  atlas segmento########################### 
        sql = "((((SELECT row_number() over () AS _uid_,* , concat(prov,lpad(dpto::text,3,'0',codloc,rac,radio,lpad(seg::text,2,'0')linkcapa FROM (SELECT row_number () over () id, prov,depto,loc,frac,radio,seg, geom  FROM (SELECT prov,depto,loc,frac,radio,seg,(st_union(geom )) geom  FROM (SELECT  substring(mza,1,2) prov, substring(mza, 3,3)  depto, substring(mza,6,3) loc, substring(mza,9,2) frac, substring(mza,11,2) radio,  seg,  geom   FROM (SELECT   mzai mza, ladoi lado, segi seg , wkb_geometry geom FROM " +  aglomerado[0] + ".arc" + " where segi is not null UNION  SELECT mzad mza, ladod lado, segd seg, wkb_geometry geom  FROM " +   aglomerado[0] + ".arc" + " where segd is not null ) foo ) foo2  group by prov,depto,loc,frac,radio,seg  ) foo3 ) AS _subq_1_ ) ) ) )"
        uri.setDataSource("", sql ,"geom","","_uid_")
        vlayer = QgsVectorLayer(uri.uri(),"capaseg","postgres")
        if not vlayer.isValid():
            print ("No se cargo la capa ")
        QgsProject.instance().addMapLayer(vlayer)
        renderer = vlayer.renderer()
        vlayer.loadNamedStyle(origen +'\estilo_segmento\capaconsulta.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        vlayer.triggerRepaint() 
        ############################# Agrego la capa Descripcion ########################### 
        sql = aglomerado[0] 
        uri.setDataSource("", "( select * ,concat(prov,dpto,codloc,lpad(frac::text,2,'0'),lpad(radio::text,2,'0'),seg) link,  st_point(0,0) geom from indec.describe_segmentos_con_direcciones('" + sql + "'))","geom","", "segmento_id")
        layer = QgsVectorLayer(uri.uri(), "descripcion_seg", "postgres")
        if not layer.isValid():
            print ("No se cargo capa Descripcion")
        QgsProject.instance().addMapLayer(layer)
        renderer = layer.renderer()
        layer.loadNamedStyle(origen +'\estilo_segmento\capaconsulta.qml')
        iface.mapCanvas().refresh() 
        QgsProject.instance().mapLayers().values()
        layer.triggerRepaint() 

        
        ########################### Agregar plantillas de salida##############
        ########################### Agregar plantillas de salida##############
        #### Plantilla tamaño A4 ###############  
        pry= QgsProject.instance()
        #Añadi una verificación de la ruta del archivo qtp
        ruta5= origen+ r'\plantillas\segmento_a4.qpt'
        if os.path.exists(ruta5):
            with open(ruta5, 'r') as templateFile:
                myTemplateContent = templateFile.read()
            layout=QgsPrintLayout(pry)
            lmg = QgsProject.instance().layoutManager()
            layout.setName("A4")
            layout.initializeDefaults()
            myDocument = QDomDocument()
            myDocument.setContent(myTemplateContent)
            ms = QgsMapSettings()
            layout.loadFromTemplate(myDocument,QgsReadWriteContext(),True)
            lmg.addLayout(layout)
        else:
            print("error en la ruta del archivo" )
    
        #### Plantilla tamaño A3 ###############  
        ruta4= ruta= origen + r'\plantillas\segmento_a3.qpt'
        if os.path.exists(ruta4):
            with open(ruta4, 'r') as templateFile:
                myTemplateContent = templateFile.read()
            layout=QgsPrintLayout(pry)
            lmg = QgsProject.instance().layoutManager()
            layout.setName("A3")
            layout.initializeDefaults()
            myDocument = QDomDocument()
            myDocument.setContent(myTemplateContent)
            ms = QgsMapSettings()
            layout.loadFromTemplate(myDocument,QgsReadWriteContext(),True)
            lmg.addLayout(layout)
        else:
            print("error en la ruta del archivo A3")
