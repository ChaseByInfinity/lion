from lion import * 

@app.route('/')
def index():
    firstTwo = Press.query.order_by('date_posted desc').limit(2)
  
    
    return render_template('index.html', firstTwo=firstTwo)


# volunteer login
@app.route('/volunteer/login/', methods=['GET', 'POST'])
def volunteer_login():
    try:
        
            
        if request.method == 'POST':
            if request.form['username']:
                if request.form['password']:
                    username = request.form['username']
                    password = request.form['password']
                    
                    vol = Volunteer.query.filter(Volunteer.username == username).first()
                    
                    if not vol:
                        flash('This user does not exist')
                        return redirect(request.url)
                    
                    else:
                        if sha256_crypt.verify(password, vol.password):
                            session['logged_in'] = True
                            session['username'] = username
                            
                            return redirect(url_for('dashboard_home'))
                        
                        else:
                            flash('Password you entered is incorrect')
                            return redirect(request.url)
                else:
                    flash('You must enter your password')
                    return redirect(url_for('volunteer_login'))
            else:
                
                flash('You must enter your username')
                return redirect(url_for('volunteer_login'))
                
        return render_template('volunteer_login.html')
    except Exception as e:
        return str(e)
    
    
# volunteer dashboard begin
@app.route('/dashboard/')
@login_required
def dashboard_home():
    try:
        return render_template('dashboard_home.html')
    except Exception as e:
        return str(e)
    
@app.route('/volunteers/')
@login_required
def dashboard_volunteer():
    try:
        isAdmin = None
        username = session['username']
        currUser = Volunteer.query.filter(Volunteer.username == username).first()
        
        if currUser.admin == True:
            isAdmin = True
        
        
        volunteers = Volunteer.query.all()
        return render_template('dashboard_vol.html', volunteers=volunteers, isAdmin=isAdmin)
    except Exception as e:
        return str(e)
    
#edit individual volunter
@app.route('/edit/volunteer/<vol_id>', methods=['GET', 'POST'])
@login_required
def vol_edit(vol_id):
    try:
       
        username = session['username']
        currUser = Volunteer.query.filter(Volunteer.username == username).first()
        
        if not currUser.admin == True:
            flash('You must be a volunteer administrator to edit volunteers')
            return redirect(url_for('dashboard_home'))
            
            
        volunteer = Volunteer.query.get(vol_id)
        
        if request.method == 'POST':
            username = request.form['username']
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            
            
            volunteer.username = username
            volunteer.fname = fname
            volunteer.lname = lname
            volunteer.email = email
            
            db.session.commit()
            db.session.flush()
            
            session['username'] = username
            
            flash('Changes saved!')
            return redirect(url_for('dashboard_volunteer'))
        
    
        
        return render_template('dashboard_edit.html', volunteer=volunteer)
    except Exception as e:
        return str(e)
    
    
# password change
@app.route('/change/password/<vol_id>', methods=['GET', 'POST'])
@login_required
def change_password(vol_id):
    try:
        
        volunteer = Volunteer.query.get(vol_id)
        
        if request.method == 'POST':
            if request.form['oldpw']:
                if request.form['newpw']:
                    
                    oldpw = request.form['oldpw']
                    newpw = request.form['newpw']
                    
                    if sha256_crypt.verify(oldpw, volunteer.password):
                        hashedpw = sha256_crypt.encrypt(newpw)
                        volunteer.password = hashedpw
                        db.session.commit()
                        db.session.flush()
                        
                        flash('Changes saved')
                        return redirect(url_for('dashboard_volunteer'))
                else:
                    flash('You must enter a new password')
                    return redirect(request.url)
                
            else:
                flash('You must enter your old password')
                return redirect(request.url)
        
        return render_template('password_change.html', volunteer=volunteer)
        
    except Exception as e:
        return str(e)
    
    
# new volunteer
@app.route('/new/volunteer/', methods=['GET', 'POST'])
def new_volunteer():
    try:
        username = session['username']
        currUser = Volunteer.query.filter(Volunteer.username == username).first()
        
        if not currUser.admin == True:
            flash('You must be a volunteer administrator to edit volunteers')
            return redirect(url_for('dashboard_home'))
        
        if request.method == 'POST':
            if request.form['username']:
                if request.form['fname']:
                    if request.form['lname']:
                        if request.form['email']:
                            if request.form['password']:
                                username = request.form['username']
                                fname = request.form['fname']
                                lname = request.form['lname']
                                password = request.form['password']
                                email = request.form['email']

                                admin = request.form.get('admin')
                                
                                password = sha256_crypt.encrypt(password)

                                if admin == "Yes":
                                    admin = True

                                else: 
                                    admin = False

                                newVolunteer = Volunteer(fname, lname, username, email, password, admin)
                                db.session.add(newVolunteer)
                                db.session.flush()
                                db.session.commit()

                                flash('Volunteer created')
                                return redirect(url_for('dashboard_volunteer'))
                            else:
                                flash('You must enter a password')
                                return redirect(request.url)
                        else:
                            flash('You must enter an email')
                            return redirect(request.url)
                        
                    else:
                        flash('You must enter a lastname')
                        return redirect(request.url)
                
                else:
                    flash('You must enter a first name')
                    return redirect(request.url)
                
            else:
                flash('You must enter a username')
                return redirect(request.url)
        
        return render_template('new_volunteer.html')
    except Exception as e:
        return str(e)
    
    
    
# press home
@app.route('/press/home/')
@login_required
def press_home():
    try:
        press = Press.query.order_by('date_posted desc').all()
        return render_template('press_home.html', press=press)
    except Exception as e:
        return str(e)
    
    
# new press
@app.route('/new/press/', methods=['GET', 'POST'])
@login_required
def new_press():
    try:
        username = session['username']
        currVol = Volunteer.query.filter(Volunteer.username == username).first()
        
        aFname = currVol.fname
        aLname = currVol.lname
        
        if request.method == 'POST':
            if request.form['title']:
                if request.form['body']:
                    title = request.form['title']
                    body = request.form['body']
                    author = aFname + ' ' + aLname
                    date_posted = datetime.now()
                    
                    newPress = Press(title, body, author, date_posted)
                    
                    db.session.add(newPress)
                    db.session.flush()
                    db.session.commit()
                    
                    flash('Press release published')
                    return redirect(url_for('press_home'))
                    
                else:
                    flash('You need to add words to the release')
                
            else:
                flash('You must add a title')
                return redirect(request.url)
        
        return render_template('new_press.html')
    except Exception as e:
        return str(e)
    
    
@app.route('/edit/press/<p_id>', methods=['GET', 'POST'])
@login_required
def edit_press(p_id):
    try:
        press = Press.query.get(p_id)
        
        if request.method == 'POST':
            if request.form['title']:
                if request.form['body']:
                    title = request.form['title']
                    body = request.form['body']
                    
                    press.title = title
                    press.body = body
                    db.session.commit()
                    db.session.flush()
                    flash('Changes saved')
                    return redirect(url_for('press_home'))
                else:
                    flash('Your press release must contain words')
                    return redirect(request.url)
            else:
                flash('Title must be added')
                return redirect(request.url)
        
        return render_template('press_edit.html', press=press)
    except Exception as e:
        return str(e)
    
    
@app.route('/delete/press/<p_id>')
@login_required
def delete_press(p_id):
    try:
        press = Press.query.get(p_id)
        
        db.session.delete(press)
        db.session.flush()
        db.session.commit()
        
        flash('Press deleted')
        return redirect(url_for('press_home'))
        
        
    except Exception as e:
        return str(e)
    
    
    
# main site view
# press view

@app.route('/view/press/<press_id>')
def view_press(press_id):
    try:
        press = Press.query.get(press_id)
        return render_template('view_press.html', press=press)
    except Exception as e:
        return str(e)

@app.route('/press/')
@app.route('/press/<int:page>', methods=['GET', 'POST'])
def all_press(page=1):
    try:
        all = Press.query.paginate(page, 3, False)
        return render_template('press_r.html', all=all)
    except Exception as e:
        return str(e)
    
#about page
@app.route('/about/')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        return str(e)
    
#contact
@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            if request.form['name']:
                if request.form['email']:
                    if request.form['phone']:
                        if request.form['message']:
                            name = request.form['name']
                            email = request.form['email']
                            phone = request.form['phone']
                            message = request.form['message']
                            
                            
                            newContact = Contact(name, phone, email, message)
                            db.session.add(newContact)
                            db.session.flush()
                            db.session.commit()
                            
                            flash('Your message was sent!')
                            return redirect(url_for('contact'))
                        else:
                            flash('You must leave a message')
                            return redirect(request.url)
                        
                    else:
                        flash('You must enter your phone number')
                        return redirect(request.url)
                        
                
                    
                else:
                    flash('You must enter your email')
                    return redirect(request.url)
                
            else:
                flash('You must enter your name')
                return redirect(request.url)
        return render_template('contact.html')
    except Exception as e:
        return str(e)
    
    
@app.route('/email/need/')
@login_required
def email_need():
    try:
        all = Contact.query.all()
        return render_template('need_email.html', all=all)
    except Exception as e:
        return str(e)
    
    
@app.route('/email/view/<e_id>')
@login_required
def email_view(e_id):
    try:
        it = Contact.query.get(e_id)
        return render_template('email_view.html', it=it)
    except Exception as e:
        return str(e)

    
# logout
@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        session.clear()
        flash('You have been logged out')
        return redirect(url_for('volunteer_login'))
    except Exception as e:
        return str(e)