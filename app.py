import os
import uuid
import json
from datetime import datetime
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, jsonify)
from werkzeug.utils import secure_filename
from database import init_db, get_db

app = Flask(__name__)
app.secret_key = 'civicfix_secret_key_2024'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'civicfix@admin'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Public Routes ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    db = get_db()
    total     = db.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
    resolved  = db.execute("SELECT COUNT(*) FROM reports WHERE status='Resolved'").fetchone()[0]
    progress  = db.execute("SELECT COUNT(*) FROM reports WHERE status='In Progress'").fetchone()[0]
    submitted = db.execute("SELECT COUNT(*) FROM reports WHERE status='Submitted'").fetchone()[0]
    recent    = db.execute(
        'SELECT * FROM reports ORDER BY created_at DESC LIMIT 5'
    ).fetchall()
    return render_template('index.html',
                           total=total, resolved=resolved,
                           progress=progress, submitted=submitted,
                           recent=recent)


@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        category    = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        location    = request.form.get('location', '').strip()
        latitude    = request.form.get('latitude', '')
        longitude   = request.form.get('longitude', '')
        name        = request.form.get('name', '').strip()
        email       = request.form.get('email', '').strip()

        if not category or not description or not location:
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('report'))

        photo_filename = None
        if 'photo' in request.files:
            f = request.files['photo']
            if f and f.filename and allowed_file(f.filename):
                ext = f.filename.rsplit('.', 1)[1].lower()
                photo_filename = secure_filename(f'{uuid.uuid4().hex}.{ext}')
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        report_id = 'CF-' + uuid.uuid4().hex[:8].upper()
        db = get_db()
        db.execute(
            '''INSERT INTO reports
               (report_id, category, description, location, latitude, longitude,
                photo, name, email, status, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            (report_id, category, description, location,
             latitude or None, longitude or None,
             photo_filename, name, email, 'Submitted',
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        db.commit()
        flash(f'Report submitted successfully! Your Report ID is <strong>{report_id}</strong>. Keep it safe to track your complaint.', 'success')
        return redirect(url_for('track', report_id=report_id))
    return render_template('report.html')


@app.route('/track', methods=['GET', 'POST'])
def track():
    result = None
    report_id = request.args.get('report_id', '') or ''
    if request.method == 'POST':
        report_id = request.form.get('report_id', '').strip().upper()
    if report_id:
        db = get_db()
        result = db.execute(
            'SELECT * FROM reports WHERE report_id = ?', (report_id,)
        ).fetchone()
        if not result:
            flash('No report found with that ID. Please check and try again.', 'warning')
    return render_template('track.html', result=result, report_id=report_id)


@app.route('/map')
def map_view():
    return render_template('map.html')


# ─── API Endpoints ────────────────────────────────────────────────────────────

@app.route('/api/reports')
def api_reports():
    db = get_db()
    rows = db.execute(
        '''SELECT report_id, category, description, location,
                  latitude, longitude, status, created_at
           FROM reports
           WHERE latitude IS NOT NULL AND longitude IS NOT NULL'''
    ).fetchall()
    data = [dict(r) for r in rows]
    return jsonify(data)


@app.route('/api/stats')
def api_stats():
    db = get_db()
    total     = db.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
    resolved  = db.execute("SELECT COUNT(*) FROM reports WHERE status='Resolved'").fetchone()[0]
    progress  = db.execute("SELECT COUNT(*) FROM reports WHERE status='In Progress'").fetchone()[0]
    review    = db.execute("SELECT COUNT(*) FROM reports WHERE status='Under Review'").fetchone()[0]
    submitted = db.execute("SELECT COUNT(*) FROM reports WHERE status='Submitted'").fetchone()[0]

    by_category = db.execute(
        "SELECT category, COUNT(*) as cnt FROM reports GROUP BY category"
    ).fetchall()

    return jsonify({
        'total': total, 'resolved': resolved,
        'in_progress': progress, 'under_review': review,
        'submitted': submitted,
        'by_category': [dict(r) for r in by_category]
    })


# ─── Admin Routes ─────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials. Please try again.', 'danger')
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        flash('Please login to access the admin panel.', 'warning')
        return redirect(url_for('admin_login'))

    status_filter   = request.args.get('status', '')
    category_filter = request.args.get('category', '')
    search          = request.args.get('search', '')

    db = get_db()
    query  = 'SELECT * FROM reports WHERE 1=1'
    params = []
    if status_filter:
        query += ' AND status = ?'
        params.append(status_filter)
    if category_filter:
        query += ' AND category = ?'
        params.append(category_filter)
    if search:
        query += ' AND (report_id LIKE ? OR description LIKE ? OR location LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    query += ' ORDER BY created_at DESC'

    reports = db.execute(query, params).fetchall()
    total     = db.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
    resolved  = db.execute("SELECT COUNT(*) FROM reports WHERE status='Resolved'").fetchone()[0]
    progress  = db.execute("SELECT COUNT(*) FROM reports WHERE status='In Progress'").fetchone()[0]
    submitted = db.execute("SELECT COUNT(*) FROM reports WHERE status='Submitted'").fetchone()[0]

    return render_template('admin_dashboard.html',
                           reports=reports, total=total,
                           resolved=resolved, progress=progress,
                           submitted=submitted,
                           status_filter=status_filter,
                           category_filter=category_filter,
                           search=search)


@app.route('/admin/update_status/<int:id>', methods=['POST'])
def update_status(id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    new_status = request.form.get('status')
    valid = ['Submitted', 'Under Review', 'In Progress', 'Resolved']
    if new_status not in valid:
        flash('Invalid status value.', 'danger')
        return redirect(url_for('admin_dashboard'))
    db = get_db()
    db.execute('UPDATE reports SET status = ? WHERE id = ?', (new_status, id))
    db.commit()
    flash('Report status updated successfully.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_report(id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    db = get_db()
    row = db.execute('SELECT photo FROM reports WHERE id = ?', (id,)).fetchone()
    if row and row['photo']:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], row['photo']))
        except OSError:
            pass
    db.execute('DELETE FROM reports WHERE id = ?', (id,))
    db.commit()
    flash('Report deleted.', 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/report/<int:id>')
def admin_view_report(id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    db = get_db()
    report = db.execute('SELECT * FROM reports WHERE id = ?', (id,)).fetchone()
    if not report:
        flash('Report not found.', 'danger')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_report_detail.html', report=report)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
