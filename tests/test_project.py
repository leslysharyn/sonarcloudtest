import unittest
from application import application as app
import time
from faker import Faker
import json
from application import application as app, db
from flask_jwt_extended import create_access_token

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.data_factory = Faker()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.token = create_access_token("test@test.com")
        self.usuario_username = "test@test.com"
        db.session.begin_nested()

    def tearDown(self):
        db.session.rollback()
        pass

    def test_health(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_crear_proyecto(self):
        nueva_proyecto = {
                "project": {
                    "project_name": "Nombre_del_proyecto",
                    "description": "Descripción_del_proyecto",
                    "creation_date": "2023-10-25T10:00:00", 
                    "end_date": "2023-11-25T10:00:00"
                },
                "personal_projects": [
                    {
                        "fullName": "Nombre_Completo_1",
                        "project_role": "Rol_del_Proyecto_1"
                    },
                    {
                        "fullName": "Nombre_Completo_2",
                        "project_role": "Rol_del_Proyecto_2"
                    }
                ]
            }

        endpoint_proyecto="/project?username="+str(self.usuario_username)
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_proyecto = self.client.post(endpoint_proyecto,
                                                   data=json.dumps(nueva_proyecto),
                                                   headers=headers)

        print(solicitud_nuevo_proyecto.get_data())

        self.assertEqual(solicitud_nuevo_proyecto.status_code, 201)   


    def test_obtener_proyecto(self):
        nueva_proyecto = {
                "project": {
                    "project_name": "Nombre_del_proyecto",
                    "description": "Descripción_del_proyecto",
                    "creation_date": "2023-10-25T10:00:00", 
                    "end_date": "2023-11-25T10:00:00"
                },
                "personal_projects": [
                    {
                        "fullName": "Nombre_Completo_1",
                        "project_role": "Rol_del_Proyecto_1"
                    },
                    {
                        "fullName": "Nombre_Completo_2",
                        "project_role": "Rol_del_Proyecto_2"
                    }
                ]
            }

        endpoint_proyecto="/project?username="+str(self.usuario_username)
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_proyecto = self.client.post(endpoint_proyecto,
                                                   data=json.dumps(nueva_proyecto),
                                                   headers=headers)
        respuesta_al_crear_proyecto = json.loads(solicitud_nuevo_proyecto.get_data())

        solicitud_proyectos= self.client.get(endpoint_proyecto,
                                                   headers=headers)
        respuesta_solicitud_proyectos=json.loads(solicitud_proyectos.get_data())
        
        self.assertEqual(solicitud_nuevo_proyecto.status_code, 201)  
        self.assertEqual(solicitud_proyectos.status_code, 200)


if __name__ == '__main__':
    unittest.main()


