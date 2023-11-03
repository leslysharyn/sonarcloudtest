from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import db, User, Project, PersonalProjects, PersonalProjectsSchema, ProjectSchemaPost, ProjectSchemaGet
from hashlib import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from datetime import timedelta
import os
import json
import random
import string
import requests
import hashlib


class CreateProyect(Resource):
    @jwt_required()
    def post(self):
        try:
           
            token = request.headers.get('Authorization')
            token = True
            #username = request.args.get('username')
            user_name = get_jwt_identity()

            #if token and username:
            if user_name and token:

                data = request.json
                request_user = User.query.filter(User.username == user_name).first()
                if not request_user:
                    return {"message": "Usuario no encontrado"}, 404
                else:
                    new_project = Project(
                        company_id = request_user.id,
                        project_name = data["project"]["project_name"],
                        description = data["project"]["description"],
                        creation_date = data["project"]["creation_date"],
                        end_date = data["project"]["end_date"]
                    )
                    db.session.add(new_project)
                    db.session.commit()

                    if new_project.id:
                        project_info_data = data.get("personal_projects")
                        if project_info_data:
                            for project_info in project_info_data:
                                new_project_info = PersonalProjects(
                                    company_id = request_user.id,
                                    project_id = new_project.id,
                                    fullName = project_info["fullName"],
                                    project_role = project_info["project_role"]
                                )
                                db.session.add(new_project_info)
                    
                        db.session.commit()
                        return {"message": "Proyecto creado correctamente"}, 201            
            else:
                return jsonify({"message": "Falta el token en el encabezado de la solicitud"}), 400

        except KeyError as e:
            return {'message': f'Key error: {str(e)}'}, 400

    @jwt_required()    
    def get(self):
        try:
            token = request.headers.get('Authorization')
            token = True
            user_name = get_jwt_identity()

            #if token and username:
            if user_name and token:
                request_user = User.query.filter(User.username == user_name).first()
                if request_user:
                    projects = Project.query.filter(Project.company_id == request_user.id).all()
                    if projects:
                        for project in projects:
                            
                            personal_projects = PersonalProjects.query.filter(PersonalProjects.project_id == project.id).all()
                            
                            if personal_projects:
                                project.personal_projects = personal_projects
                            else:
                                project.personal_projects = []
                        project_schema = ProjectSchemaGet(many=True)
                        return project_schema.dump(projects), 200
                    else:
                        return {"message": "No hay proyectos"}, 404
                else:
                    return {"message": "Usuario no encontrado"}, 404
            else:
                return jsonify({"message": "Falta el token en el encabezado de la solicitud"}), 400

        except KeyError as e:
            return {'message': f'Key error: {str(e)}'}, 400


class Ping(Resource):
    def get(self):
        return "pong", 200
    

class Health(Resource):
    def get(self):
        return "pong", 200    




   
