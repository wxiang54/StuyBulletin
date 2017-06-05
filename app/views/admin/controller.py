from app.blueprints import admin_mod
from flask import url_for, request, session, current_app, redirect, g, render_template

from datetime import datetime

from app.models.opportunities import Opportunity

from app.core.authentication import require_login, require_role

from app.extensions import db

import logging

LOG = logging.getLogger(__name__)

@admin_mod.route('/')
@require_login
@require_role('admin')
def index():
    """ Admin dashboard """

    return 'admin_index'

# DONE
@admin_mod.route('/opportunities')
@admin_mod.route('/opportunities/<int:page>')
@require_login
#@require_role('admin')
def opportunities(page = 1):
    """ Returns all opportunities for a admin (paginated) seperated by either tag, but sorted in the recommendation order (see neural net fun times)

    :param page: Page to return
    :type page: int
    """

    # Implement the whole suggestion thing
    opportunities = Opportunity.query.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    return render_template("admin/admin_opportunities.html", opportunities = opportunities)

# DON'T NEED
@admin_mod.route('/my_opportunities/<int:page>')
@require_login
@require_role('admin')
def my_opportunities(page = 1):
    """ Returns all opportunities that a admin has created or approved

    :param page: Page to return
    :type page: int
    """

    # Implement this in the database first

    return 'admin.controller.my_opportunities'

# DONE
@admin_mod.route('/opportunity/<int:op_id>')
@require_login
#@require_role('admin')
def opportunity(op_id = 0):
    """ Returns a single opportunity to display information
        **EDITING AND REMOVING FXN**
    :param op_id: ID of the opportunity to display information of
    :type op_id: int
    """

    opportunity = Opportunity.query.filter_by(id = op_id).first()
    return render_template("admin/admin_opportunity.html", opportunity = opportunity)

# IN PROG
@admin_mod.route('/search/<int:page>')
@require_login
@require_role('admin')
def search(page = 1):
    """ Returns a paginated list of opportunities as pursuant to the search parameters given by the GET parameters

    The paramaters should be:
     - search (str) the string to search for
     - tags (str) the tags (as a comma seperated list) to search for

    :param page: Page to return
    :type page: int
    """

    return 'admin.controller.search'

# DONE
@admin_mod.route('/add-opportunity/', methods=['GET', 'POST'])
@require_login
#@require_role('admin')
def add_opportunity(op_id = 0): # init param?
    """ Returns a interface for admins to create opportunities

    Everything is a string
    """
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        organization = request.form['organization']

        start_time = datetime(year = 2017, month = 1, day = 20) # Figure this out
        end_time = datetime(year = 2017, month = 1, day = 20) # Figure this out

        hours = int(request.form['hours'])

        deadline = datetime(year = 2017, month = 1, day = 20) # Figure this out

        required_materials_raw = request.form['required_materials']
        tags_raw = request.form['tags']

        required_materials = required_materials_raw.split(',')
        tags = tags_raw.split(',')

        link = request.form['link']

        o = Opportunity(name = name,
                        description = description,
                        organization = organization,
                        start_time = start_time,
                        end_time = end_time,
                        hours = hours,
                        deadline = deadline,
                        link = link)

        for r in required_materials:
            o.add_required_material(r)

        for t in tags:
            o.add_tag(t)

        db.session.add(o)
        db.session.commit()

        # how to get op_id of newest entry?
        opportunity = Opportunity.query.filter_by(id = op_id).first()
        return redirect(url_for("admin.controller.opportunity", op_id = op_id))
    return render_template("admin/admin_add.html")

# DONE
@admin_mod.route('/edit-opportunity-form/<int:op_id>')
@require_login
#@require_role('admin')
def edit_opportunity_form(op_id = 0):
    """ Returns a interface for admins to edit opportunities

    :param op_id: ID of the opportunity to edit information of
    :type op_id: int
    """

    opportunity = Opportunity.query.filter_by(id = op_id).first()
    return render_template("admin/admin_edit.html", opportunity = opportunity)

# DONE
@admin_mod.route('/edit-opportunity/<int:op_id>', methods = ["POST"])
@require_login
#@require_role('admin')
def edit_opportunity(op_id = 0):
    """ edits the opportunity in the DB
    :param op_id: ID of the opportunity to edit information of
    :type op_id: int
    """

    # NEW VALUES
    name = request.form["name"]
    description = request.form["description"]
    organization = request.form["organization"]

    # CHANGE DB ENTRY
    opportunity = Opportunity.query.filter_by(id = op_id).first()
    opportunity.name = name
    opportunity.description = description
    opportunity.organization = organization
    db.session.commit()

    return redirect(url_for("admin.controller.opportunity", op_id = op_id))

# IN PROG
@admin_mod.route('/remove-opportunity/<int:op_id>')
@require_login
#@require_role('admin')
def remove_opportunity(op_id = 0):
    """ Returns a interface for admins to remove opportunities
        :param op_id: ID of the opportunity to remove information of
        :type op_id: int
    """

    return redirect(url_for("admin.controller.opportunities", page = 1))
