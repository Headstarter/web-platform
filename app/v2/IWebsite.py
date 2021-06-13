# Flask imports
from app import app
from app.router import my_redirect
from flask import render_template, session, request, url_for, redirect, g, request, Blueprint, flash
from app.models import User, Tag, Company, Position, Application, insert_position, \
	update_position, db, filter_offers_by_tag, filter_applications, filter_all_offers_by_tag, update_company
import os
from werkzeug.utils import secure_filename
from app.v2.target import Target_Group

# OOP imports
from abc import ABCMeta, abstractmethod

class IWebsite:
    __metaclass__ = ABCMeta

    language = 'bg'

    def change_language(self, new_language):
        self.language = new_language

    def version(self):
        return '1.0'

    @abstractmethod
    def template_folder(self): 
        raise NotImplementedError

    @abstractmethod
    def homepage(self): 
        raise NotImplementedError

    @abstractmethod
    def position_details(self, id): 
        raise NotImplementedError

    @abstractmethod
    def browse_positions(self): 
        raise NotImplementedError

    @abstractmethod
    def your_profile(self): 
        raise NotImplementedError

    @abstractmethod
    def view_cv(self, id): 
        raise NotImplementedError

    @abstractmethod
    def company_preview(self, id): 
        raise NotImplementedError

    @abstractmethod
    def edit_profile(self):
        raise NotImplementedError
    
    @abstractmethod
    def upload_picture(self):
        raise NotImplementedError

    @abstractmethod
    def cv_confirm(self):
        raise NotImplementedError
        
    @abstractmethod
    def publish_position(self):
        raise NotImplementedError
        
    @abstractmethod
    def edit_position(self, positionId):
        raise NotImplementedError

    @abstractmethod
    def list_my_positions(self):
        raise NotImplementedError

    @abstractmethod
    def list_my_candidates(self):
        raise NotImplementedError

    @abstractmethod
    def faq(self):
        raise NotImplementedError

    @abstractmethod
    def news(self):
        raise NotImplementedError

    @abstractmethod
    def media(self):
        raise NotImplementedError
        
    @abstractmethod
    def blog_posts(self):
        raise NotImplementedError

    @abstractmethod
    def about(self):
        raise NotImplementedError
