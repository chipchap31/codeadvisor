from flask import Blueprint, redirect, request, abort, render_template

from middlewares.user_middlewares import require_login
from mongo import database
import ast
feedback = Blueprint('feedback', __name__)


@feedback.route('/feedback/delete/<id>')
def delete_feedback(id):
    deleted = database.delete_feedback(id)

    if not deleted:
        return abort(501)
    return redirect(f'/posts/{deleted["post_name"]}')


@feedback.route("/feedback/edit/<id>", methods=["POST", "GET"])
def edit_feedback(id):
    feedback = database.feedback_single(id)
    user = require_login(request.cookies)
    if not user:
        return abort(401)

    if not feedback:
        # return false since the feedback is not found
        # or there was a server error
        return False

    if request.method == "POST":
        data = request.form
        feedback_arr = []
        labels = []
        index = 1
        for obj in feedback['feedback']:
            for key, value in obj.items():
                labels.append(key)

        for label in labels:
            feedback_arr.append({
                label: {
                    "rate": int(data['rate%s' % index]),
                    "advice": data['advice%s' % index]
                }

            })
            index += 1
        doc = {
            'feedback_arr': feedback_arr,
            'edited': True,
            '_id': feedback['_id']
        }

        database.edit_feedback(doc)
        return redirect("/posts/%s" % feedback['post_name'])
    top_advisors = database.get_top_advisor()
    return render_template('feedback/edit-feedback.html', user_auth=user, config={
        "store":  feedback,
        "top_advisors": top_advisors,
        "referrer": request.referrer
    })
