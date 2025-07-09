from flask import request, url_for, redirect

from app.auth import bp

from app.extensions import db
from app.models.user import User

@bp.route('/register', methods=['POST'])
def register():
    print("REGISTER NEW USER!")
    print(request.form.values)
    if request.method == 'POST':
        username = request.form['username']
        if username:
            #check for existing user
            existing_user = User.query.filter_by(username=username).first()
            if existing_user is None:
                #add new user
                new_user = User(username=username)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('main.index', new_user=True))
    
    return redirect(url_for('main.index'))