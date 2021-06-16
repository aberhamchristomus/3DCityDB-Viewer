
import os, time
from PyQt5 import uic, Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import psycopg2
import psycopg2.extras
import json
import sys
from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsProject

pluginPath = os.path.dirname(__file__)
WIDGET, BASE = uic.loadUiType(os.path.join(pluginPath, 'ui', 'maske.ui'))

class dbviewer(BASE, WIDGET):

# DEFAULT SETTING
    def __init__(self, iface, parent=None):
        super().__init__(parent)

        self.iface = iface
        self.setupUi(self)

        self.cancel.clicked.connect(self.closePlugin)
        
        self.ok.clicked.connect(self.closePlugin)
        
        self.connectdb.clicked.connect(self.connected)
        
        self.btnrefresh.clicked.connect(self.filllist)
        self.filllist()
        
        self.btnremove.clicked.connect(self.DBdelete)
        self.listWidget.setSortingEnabled(True)
        self.btn_Tab_in_ListWidget.clicked.connect(self.viewtable)
        
        self.pb_addvector.clicked.connect(self.addgeom)
        
        self.pb_addtable.clicked.connect(self.addtable)
        
        self.listWidget_DS.setSortingEnabled(True)
        
        self.pb_building_lod1.clicked.connect(self.building_lod1)
        self.pb_solid_lod1.clicked.connect(self.solid_lod1)
        
        self.pb_configure_lod2.clicked.connect(self.configurelod2)
        self.pb_wall_lod2.clicked.connect(self.wall_lod2)
        self.pb_roof_lod2.clicked.connect(self.roof_lod2)
        self.pb_ground_lod2.clicked.connect(self.ground_lod2)
        self.pb_reset_lod2.clicked.connect(self.resetconfig_lod2)
        self.pb_solid_lod2.clicked.connect(self.solid_lod2)
        
        self.pb_configure_lod3.clicked.connect(self.configurelod3)
        self.pb_wall_lod3.clicked.connect(self.wall_lod3)
        self.pb_roof_lod3.clicked.connect(self.roof_lod3)
        self.pb_ground_lod3.clicked.connect(self.ground_lod3)
        self.pb_reset_lod3.clicked.connect(self.resetconfig_lod3)
        self.pb_solid_lod3.clicked.connect(self.solid_lod3)
        
        self.pb_opening_config_lod3.clicked.connect(self.configure_opening_lod3)
        self.pb_window_lod3.clicked.connect(self.window_lod3)
        self.pb_door_lod3.clicked.connect(self.door_lod3)
        self.pb_reset_opening_lod3.clicked.connect(self.resetconfig_opening_lod3)
        
        self.pb_configure_lod4.clicked.connect(self.configurelod4)
        self.pb_wall_lod4.clicked.connect(self.wall_lod4)
        self.pb_roof_lod4.clicked.connect(self.roof_lod4)
        self.pb_ground_lod4.clicked.connect(self.ground_lod4)
        self.pb_interior_wall_lod4.clicked.connect(self.interiorwall_lod4)
        self.pb_floor_lod4.clicked.connect(self.floor_lod4)
        self.pb_ceiling_lod4.clicked.connect(self.ceiling_lod4)
        self.pb_closure_lod4.clicked.connect(self.closure_lod4)
        self.pb_reset_lod4.clicked.connect(self.resetconfig_lod4)
        self.pb_solid_lod4.clicked.connect(self.solid_lod4)
        self.pb_solid_room_lod4.clicked.connect(self.solid_room_lod4)
                
        self.pb_opening_config_lod4.clicked.connect(self.configure_opening_lod4)
        self.pb_window_lod4.clicked.connect(self.window_lod4)
        self.pb_door_lod4.clicked.connect(self.door_lod4)
        self.pb_reset_opening_lod4.clicked.connect(self.resetconfig_opening_lod4)
        
        self.pb_room_config_lod4.clicked.connect(self.configure_room_lod4)
        self.pb_room_lod4.clicked.connect(self.room_lod4)
        self.pb_room_reset_lod4.clicked.connect(self.resetconfig_room_lod4)

        self.pb_furniture_config_lod4.clicked.connect(self.configure_furniture_lod4)
        self.pb_furniture_lod4.clicked.connect(self.furniture_lod4)
        self.pb_furniture_reset_lod4_2.clicked.connect(self.resetconfig_furniture_lod4)
        
        self.pb_installation_config_lod4.clicked.connect(self.configure_installation_lod4)
        self.pb_installation_lod4.clicked.connect(self.installation_lod4)
        self.pb_installation_reset_lod4_2.clicked.connect(self.resetconfig_installation_lod4)
        
    # ClosePlugins
    def closePlugin(self):
        self.close()

# -------------------------------------------------------------------------------------------------------------------------
# Tab 2 - Database Connection and Adding Layer 
    # Connect New DB
    def connected(self):

        # Connect to db s
        try:
            dbname = self.dbname.text()
            user = self.user.text()
            pw = self.pw.text()
            host = self.host.text()
            port = self.port.value()
            self.conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
            self.cur = self.conn.cursor()
            self.conn.autocommit = True
            print ( self.conn.get_dsn_parameters(),"\n")

            # Read The File
            with open(self.file_path, "r", encoding = 'utf-8') as file:
                self.db_liste = json.load(file)

            # fuegt DB der DB_Liste hinzu
            self.db_liste["items"].update({dbname:{"user": user,"pw": pw, "host":host,"port":port}})

            # speichert die DB_Liste ab
            with open(self.file_path, "w", encoding = 'utf-8') as file:
                self.db_liste = json.dump(self.db_liste, file, indent=2)

            self.filllist()
            self.label_19.setText("Connect Succesfully \nConnection to "+dbname+" completed")

        except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)

            showMessage("Failed", "Connection to '" + dbname + "' Failed. Please check all the parameters")

    # Fill DB List
    def filllist(self):
        self.listWidget.clear()
        self.listWidget.setSortingEnabled(True)

        self.file_path = os.path.join(pluginPath, 'db_liste.json')
        with open(self.file_path, "r", encoding = 'utf-8') as file:
            self.db_liste = json.load(file)

        for item in self.db_liste["items"]:
            self.listWidget.addItem(item)
            
    # Delete in DB List
    def DBdelete (self):
        if self.listWidget.currentItem() is None:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", "No Database select yet")
        else:
            self.curennt = self.listWidget.currentItem().text()

            with open(self.file_path, "r+", encoding = 'utf-8') as file:
                self.db_liste = json.load(file)

            del self.db_liste['items'][self.curennt]

            for self.curennt in self.file_path:
               self.curennt=None
            with open(self.file_path, "w+", encoding = 'utf-8') as file:
                self.db_liste = json.dump(self.db_liste, file, indent=2)


        self.listWidget.clear()

        with open(self.file_path, "r", encoding = 'utf-8') as file:
            self.db_liste = json.load(file)

        for item in self.db_liste["items"]:
            self.listWidget.addItem(item)

    # View Table in List Widget
    def viewtable (self):

        if self.listWidget.currentItem() is None:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Warning", "No DB Selected")

        else:
            try:
                curennt = self.listWidget.currentItem().text()
                with open(self.file_path, "r", encoding = 'utf-8') as file:
                    db_liste = json.load(file)

                dbInfo = db_liste['items'][curennt]
                dbname = curennt
                user = dbInfo['user']
                pw = dbInfo['pw']
                host = dbInfo['host']
                port = dbInfo['port']
                conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)

            except:
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Warning", "Database not Found")

            try:
                self.label_8.setText(curennt)
                conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur.execute("""SELECT
                                    table_name
                                FROM
                                    information_schema.tables
                                WHERE
                                    table_type = 'BASE TABLE'
                                AND
                                    table_schema NOT IN ('pg_catalog', 'information_schema');
                            """)

                rows = cur.fetchall()

                for row in rows:
                    self.listWidget_DS.addItems(row)
            except:
                pass
    
    # Load Table in QGIS
    def tabInQGIS (self):

        if self.listWidget.currentItem() is None:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", "No database select yet")

        else:
            curennt = self.listWidget.currentItem().text()
            with open(self.file_path, "r", encoding = 'utf-8') as file:
                db_liste = json.load(file)
            dbInfo = db_liste['items'][curennt]
            dbname = curennt
            user = dbInfo['user']
            pw = dbInfo['pw']
            host = dbInfo['host']
            port = dbInfo['port']
            self.conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)

            if self.listWidget_DS.currentItem() is None :
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Failed", "No database select yet")
                
            else:
                curennt_ds = self.listWidget_DS.currentItem().text()
                uri = QgsDataSourceUri()

                # set host name, port, database name, username and password
                uri.setConnection(host, str(port), dbname, user, pw)

                # set database schema, table name, geometry column and optionally
                # subset (WHERE clause)

                self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                filter = self.sql.toPlainText()
                try:
                    self.cur.execute("""SELECT geom FROM""" + ' ' + curennt_ds +""";""" )
                    uri.setDataSource( "public", curennt_ds, 'geom', filter)
                    addgeom = QgsVectorLayer(uri.uri(False), curennt_ds, "postgres")
                    QgsProject.instance().addMapLayer(addgeom)
                except:
                    uri.setDataSource( "public", curennt_ds, None, filter)
                    addgeom = QgsVectorLayer(uri.uri(False), curennt_ds, "postgres")
                    QgsProject.instance().addMapLayer(addgeom)

    def tabInQGIS (self):

        if self.listWidget.currentItem() is None:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Warning", "No DB Selected")

        else:
            curennt = self.listWidget.currentItem().text()
            with open(self.file_path, "r", encoding = 'utf-8') as file:
                db_liste = json.load(file)
            dbInfo = db_liste['items'][curennt]
            dbname = curennt
            user = dbInfo['user']
            pw = dbInfo['pw']
            host = dbInfo['host']
            port = dbInfo['port']
            self.conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)

            if self.listWidget_DS.currentItem() is None :
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Warning", "Not yet Selected")
                
            else:
                curennt_ds = self.listWidget_DS.currentItem().text()
                uri = QgsDataSourceUri()

                # set host name, port, database name, username and password
                uri.setConnection(host, str(port), dbname, user, pw)

                # set database schema, table name, geometry column and optionally
                # subset (WHERE clause)

                self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                
                try:
                    self.cur.execute("""SELECT geom FROM""" + ' ' + curennt_ds +""";""" )
                    uri.setDataSource( "public", curennt_ds, 'geom', filter)
                    addgeom = QgsVectorLayer(uri.uri(False), curennt_ds, "postgres")
                    QgsProject.instance().addMapLayer(addgeom)
                except:
                    uri.setDataSource( "public", curennt_ds, None, filter)
                    addgeom = QgsVectorLayer(uri.uri(False), curennt_ds, "postgres")
                    QgsProject.instance().addMapLayer(addgeom)
    
    # Add Geometry to QGIS
    def addgeom (self) :
        tablename = self.le_tablename.text()
        geometrycol = "geom"
        
        dbname = self.dbname.text()
        user = self.user.text()
        pw = self.pw.text()
        host = self.host.text()
        port = self.port.value()
            
        uri = QgsDataSourceUri()
        uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
        uri.setDataSource ("citydb", tablename,"geometry")
        addgeom=QgsVectorLayer (uri .uri(False), tablename, "postgres")
        QgsProject.instance().addMapLayer(addgeom)
                
    # Add Table to QGIS
    def addtable(self) :
        tablename = self.le_tablename.text()
        
        dbname = self.dbname.text()
        user = self.user.text()
        pw = self.pw.text()
        host = self.host.text()
        port = self.port.value()
        
        uri = QgsDataSourceUri()
        uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
        uri.setDataSource("citydb", tablename, None, "")
        table = QgsVectorLayer(uri.uri(), tablename, "postgres")
        QgsProject.instance().addMapLayers([table])

# ------------------------------------------------------------------------------------------------------------------------ 
    # Add Building LOD1 layer
    def building_lod1(self):
      try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT geometry FROM surface_geometry WHERE geometry IS NOT NULL")
       
       tablename = "surface_geometry"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "geometry IS NOT NULL")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Building_lod1", "postgres")
       QgsProject.instance().addMapLayer(addgeom)  
      
      except:
         def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
         showMessage("Failed", "Fill The Parameter first!")

    def solid_lod1(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM surface_geometry WHERE is_solid = 1")
       
       tablename = "surface_geometry"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "solid_geometry", "is_solid = 1")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Solid_Building_lod1", "postgres")
       QgsProject.instance().addMapLayer(addgeom)
        
     except:
         def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
         showMessage("Failed", "Fill The Parameter first!")
# ------------------------------------------------------------------------------------------------------------------------
# Tab 4 - LOD 2 Viewer
    # Configuration LOD 2
    def configurelod2(self):
     try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       conn.autocommit = True
       
       curr = conn.cursor()
       
       curr.execute("CREATE TABLE them_surface_lod2 AS (SELECT geometry, objectclass_id FROM surface_geometry INNER JOIN thematic_surface ON root_id = lod2_multi_surface_id)")
     
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Succes", "Table Created")
       
     except:
      def showMessage(title, mesage):
         QMessageBox.information(None, title, mesage)
      showMessage("Failed", dbname + " Already Configured or Check the parameter")        

    # Add Wall Layer - LOD 2
    def wall_lod2(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod2 WHERE objectclass_id = '34'")
       
       tablename = "them_surface_lod2"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 34")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Wall_lod2", "postgres")
       QgsProject.instance().addMapLayer(addgeom)          

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
    
    # Add Roof Layer - LOD 2
    def roof_lod2(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod2 WHERE objectclass_id = '33'")
       
       tablename = "them_surface_lod2"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 33")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Roof_lod2", "postgres")
       QgsProject.instance().addMapLayer(addgeom)
     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Ground Layer - LOD 2
    def ground_lod2(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod2 WHERE objectclass_id = '35'")
       
       tablename = "them_surface_lod2"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 35")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Ground_lod2", "postgres")
       QgsProject.instance().addMapLayer(addgeom)
       
     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")

    def solid_lod2(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM surface_geometry WHERE is_solid = 1")
       
       tablename = "surface_geometry"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "solid_geometry", "is_solid = 1")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Solid_Model_lod2", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Reset Your Configuration - LOD 2
    def resetconfig_lod2(self):       
        try:  
           dbname = self.dbname.text()
           user = self.user.text()
           pw = self.pw.text()
           host = self.host.text()
           port = self.port.value()
           
           conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
           conn.autocommit = True
           
           curr = conn.cursor()
           
           curr.execute("DROP TABLE them_surface_lod2")
         
           def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
           showMessage("Succes", "Table Deleted")
                          
        except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", dbname + " Already Reset or Check the parameter")      

# ------------------------------------------------------------------------------------------------------------------------
# Tab 5 - LOD 3 Viewer
    # Configuration LOD 3
    def configurelod3(self):
      try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       conn.autocommit = True
       
       curr = conn.cursor()
       
       curr.execute("CREATE TABLE them_surface_lod3 AS (SELECT geometry, objectclass_id FROM surface_geometry INNER JOIN thematic_surface ON root_id = lod3_multi_surface_id)")
     
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Succes", "Table Created")
       
      except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", dbname + " Already Configured or Check the parameter")      

    # Add Wall Layer
    def wall_lod3(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod3 WHERE objectclass_id = '34'")
       
       tablename = "them_surface_lod3"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 34")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Wall and Interior Wall_lod3", "postgres")
       QgsProject.instance().addMapLayer(addgeom) 

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Roof Layer
    def roof_lod3(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod3 WHERE objectclass_id = '33'")
       
       tablename = "them_surface_lod3"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 33")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Roof_lod3", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Ground Layer
    def ground_lod3(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod3 WHERE objectclass_id = '35'")
       
       tablename = "them_surface_lod3"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 35")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Ground_lod3", "postgres")
       QgsProject.instance().addMapLayer(addgeom)
       
     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")

    # Reset Your Configuration - LOD 3
    def resetconfig_lod3(self):       
        try:  
           dbname = self.dbname.text()
           user = self.user.text()
           pw = self.pw.text()
           host = self.host.text()
           port = self.port.value()
           
           conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
           conn.autocommit = True
           
           curr = conn.cursor()
           
           curr.execute("DROP TABLE them_surface_lod3")
                   
           def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
           showMessage("Succes", "Table Deleted")
                          
        except:
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Failed", dbname + " Database already reset or Check the parameter")

    # Configuration Opening - LOD 3
    def configure_opening_lod3(self):
      try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       conn.autocommit = True
       
       curr = conn.cursor()
       
       curr.execute("CREATE TABLE them_surface_opening_lod3 AS (SELECT geometry, objectclass_id FROM surface_geometry INNER JOIN opening ON root_id = lod3_multi_surface_id WHERE geometry IS NOT NULL)")
     
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Succes", "Table Created")
       
      except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", dbname + " Already Configured or Check the parameter")   

    # Add Window Layer
    def window_lod3(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_opening_lod3 WHERE objectclass_id = '38'")
       
       tablename = "them_surface_opening_lod3"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 38")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Window_lod3", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Door Layer
    def door_lod3(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_opening_lod3 WHERE objectclass_id = '39'")
       
       tablename = "them_surface_opening_lod3"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 39")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Door_lod3", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")

    # Reset Your Configuration - Opening LOD 3
    def resetconfig_opening_lod3(self):       
        try:  
           dbname = self.dbname.text()
           user = self.user.text()
           pw = self.pw.text()
           host = self.host.text()
           port = self.port.value()
           
           conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
           conn.autocommit = True
           
           curr = conn.cursor()
           
           curr.execute("DROP TABLE them_surface_opening_lod3")
                   
           def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
           showMessage("Succes", "Table Deleted")
                          
        except:
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Failed", dbname + " Database already reset or Check the parameter")
                    
                    
    def solid_lod3(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM surface_geometry WHERE is_solid = 1")
       
       tablename = "surface_geometry"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "solid_geometry", "is_solid = 1")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Solid_Model_lod3", "postgres")
       QgsProject.instance().addMapLayer(addgeom)
      
     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
#------------------------------------------------------------------------------------------------------------------------------- 
# Tab 6 - LOD 4 Viewer
    # Configuration LOD 4
    def configurelod4(self):
     try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       conn.autocommit = True
       
       curr = conn.cursor()
       
       curr.execute("CREATE TABLE them_surface_lod4 AS (SELECT geometry, objectclass_id,solid_geometry,room_id FROM surface_geometry INNER JOIN thematic_surface ON root_id = lod4_multi_surface_id)")
     
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Succes", "Table Created")
       
     except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", dbname + " Already Configured or Check the parameter")          

    # Add Wall Layer
    def wall_lod4(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod4 WHERE objectclass_id = '34'")
       
       tablename = "them_surface_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 34")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Wall_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom) 

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Interior Layer(self):
    def interiorwall_lod4(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod4 WHERE objectclass_id = '31'")
       
       tablename = "them_surface_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 31")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Interior Wall_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom) 

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Roof Layer
    def roof_lod4(self):
     try:
        
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod4 WHERE objectclass_id = '33'")
       
       tablename = "them_surface_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 33")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Roof_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Ground Layer
    def ground_lod4(self):
     try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod4 WHERE objectclass_id = '35'")
       
       tablename = "them_surface_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 35")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Ground_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")

    # Add Floor Surface 
    def floor_lod4(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod4 WHERE objectclass_id = '32'")
       
       tablename = "them_surface_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 32")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Floor_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")

    # Add Ceiling Surface 
    def ceiling_lod4(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod4 WHERE objectclass_id = '30'")
       
       tablename = "them_surface_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 30")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Ceiling_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)         

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Closure Surface 
    def closure_lod4(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod4 WHERE objectclass_id = '36'")
       
       tablename = "them_surface_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 36")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Closure_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)       

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Reset Your Configuration - Opening LOD 4
    def resetconfig_lod4(self):       
        try:  
           dbname = self.dbname.text()
           user = self.user.text()
           pw = self.pw.text()
           host = self.host.text()
           port = self.port.value()
           
           conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
           conn.autocommit = True
           
           curr = conn.cursor()
           
           curr.execute("DROP TABLE them_surface_lod4")
                   
           def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
           showMessage("Succes", "Table Deleted")
                          
        except:
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Failed", dbname + " Database already reset or Check the parameter") 
                    
    # Configuration Opening - LOD 4
    def configure_opening_lod4(self):
      try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       conn.autocommit = True
       
       curr = conn.cursor()
       
       curr.execute("CREATE TABLE them_surface_opening_lod4 AS (SELECT geometry, objectclass_id FROM surface_geometry INNER JOIN opening ON root_id = lod4_multi_surface_id WHERE geometry IS NOT NULL)")
     
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Succes", "Table Created")
       
      except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", dbname + " Already Configured or Check the parameter") 

    # Add Window Layer
    def window_lod4(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_opening_lod4 WHERE objectclass_id = '38'")
       
       tablename = "them_surface_opening_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 38")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Window_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Add Door Layer
    def door_lod4(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_opening_lod4 WHERE objectclass_id = '39'")
       
       tablename = "them_surface_opening_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 39")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Door_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Reset Your Configuration - Opening LOD 3
    def resetconfig_opening_lod4(self):       
        try:  
           dbname = self.dbname.text()
           user = self.user.text()
           pw = self.pw.text()
           host = self.host.text()
           port = self.port.value()
           
           conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
           conn.autocommit = True
           
           curr = conn.cursor()
           
           curr.execute("DROP TABLE them_surface_opening_lod4")
                   
           def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
           showMessage("Succes", "Table Deleted")
                          
        except:
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Failed", dbname + " Database already reset or Check the parameter")

    # Configuration Opening - LOD 4
    def configure_room_lod4(self):
      try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       conn.autocommit = True
       
       curr = conn.cursor()
       
       curr.execute("CREATE TABLE them_surface_room_lod4 AS (SELECT surface_geometry.gmlid,cityobject.id,surface_geometry.solid_geometry,cityobject.name,surface_geometry.root_id FROM surface_geometry INNER JOIN cityobject ON surface_geometry.cityobject_id = cityobject.id WHERE is_solid = 1 AND root_id != 1)")
     
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Succes", "Table Created")
       
      except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", dbname + " Already Configured or Check the parameter") 

    # Add Window Layer
    def room_lod4(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_lod4 WHERE room_id IS NOT NULL")
       
       tablename = "them_surface_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Room_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Reset Your Configuration - Opening LOD 3
    def resetconfig_room_lod4(self):       
        try:  
           dbname = self.dbname.text()
           user = self.user.text()
           pw = self.pw.text()
           host = self.host.text()
           port = self.port.value()
           
           conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
           conn.autocommit = True
           
           curr = conn.cursor()
           
           curr.execute("DROP TABLE them_surface_room_lod4")
                   
           def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
           showMessage("Succes", "Table Deleted")
                          
        except:
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Failed", dbname + " Database already reset or Check the parameter")

    def solid_lod4(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM surface_geometry WHERE is_solid = 1")
       
       tablename = "surface_geometry"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "solid_geometry", "is_solid = 1")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Solid_Model_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")

    def solid_room_lod4(self):
     try:
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM surface_geometry WHERE is_solid = 1 AND root_id != 1")
       
       tablename = "them_surface_room_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "solid_geometry")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Solid_Room_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
           
# ----------------------------------------------------------------------------------------------------------------------- 
# Tab 7 - LOD 4 - Building Furniture and Installation

    # Configuration Building Furniture - LOD 4
    def configure_furniture_lod4(self):
      try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       conn.autocommit = True
       
       curr = conn.cursor()
       
       curr.execute("CREATE TABLE them_surface_furniture_lod4 AS (SELECT geometry, objectclass_id FROM surface_geometry INNER JOIN building_furniture ON root_id = lod4_brep_id WHERE geometry IS NOT NULL)")
     
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Succes", "Table Created")
       
      except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", dbname + " Already Configured or Check the parameter") 

    # Add Building Furniture Layer
    def furniture_lod4(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_furniture_lod4 WHERE objectclass_id = '40'")
       
       tablename = "them_surface_furniture_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 40")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Building_Furniture_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Reset Your Configuration - Furniture LOD 4
    def resetconfig_furniture_lod4(self):       
        try:  
           dbname = self.dbname.text()
           user = self.user.text()
           pw = self.pw.text()
           host = self.host.text()
           port = self.port.value()
           
           conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
           conn.autocommit = True
           
           curr = conn.cursor()
           
           curr.execute("DROP TABLE them_surface_furniture_lod4")
                   
           def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
           showMessage("Succes", "Table Deleted")
                          
        except:
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Failed", dbname + " Database already reset or Check the parameter")
    
    # Configuration Building Installation - LOD 4
    def configure_installation_lod4(self):
      try:  
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       conn.autocommit = True
       
       curr = conn.cursor()
       
       curr.execute("CREATE TABLE them_surface_installation_lod4 AS (SELECT geometry, objectclass_id FROM surface_geometry INNER JOIN building_installation ON root_id = lod4_brep_id WHERE geometry IS NOT NULL)")
     
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Succes", "Table Created")
       
      except:
            def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
            showMessage("Failed", dbname + " Already Configured or Check the parameter")  

    # Add Building Buildig Installation Layer
    def installation_lod4(self):
     try:   
       dbname = self.dbname.text()
       user = self.user.text()
       pw = self.pw.text()
       host = self.host.text()
       port = self.port.value()
       
       conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
       
       curr = conn.cursor()
       
       curr.execute("SELECT* FROM them_surface_installation_lod4 WHERE objectclass_id = '28'")
       
       tablename = "them_surface_installation_lod4"
       
       uri = QgsDataSourceUri()
       uri.setConnection(str(host), "5432", str(dbname), str(user), str(pw))
       uri.setDataSource("citydb", tablename, "geometry", "objectclass_id = 28")
       addgeom=QgsVectorLayer (uri .uri(False), dbname +" Building_installation_lod4", "postgres")
       QgsProject.instance().addMapLayer(addgeom)

     except:
       def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
       showMessage("Failed", "Fill The Parameter first!")
       
    # Reset Your Configuration - Building Installation LOD 4
    def resetconfig_installation_lod4(self):       
        try:  
           dbname = self.dbname.text()
           user = self.user.text()
           pw = self.pw.text()
           host = self.host.text()
           port = self.port.value()
           
           conn = psycopg2.connect(database=dbname, user=user, password=pw, host=host, port=port)
           conn.autocommit = True
           
           curr = conn.cursor()
           
           curr.execute("DROP TABLE them_surface_installation_lod4")
                   
           def showMessage(title, mesage):
                QMessageBox.information(None, title, mesage)
           showMessage("Succes", "Table Deleted")
                          
        except:
                def showMessage(title, mesage):
                    QMessageBox.information(None, title, mesage)
                showMessage("Failed", dbname + " Database already reset or Check the parameter")
