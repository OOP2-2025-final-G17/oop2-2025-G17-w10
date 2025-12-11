from flask import Blueprint, render_template, request, redirect, url_for
from models import Time

# Blueprint を time 用に修正
time_bp = Blueprint('time', __name__, url_prefix='/times')


@time_bp.route('/')
def list():
    times = Time.select()
    return render_template('time_list.html', title='労働時間一覧', items=times)


@time_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        break_start_time = request.form.get('break_start_time')
        break_end_time = request.form.get('break_end_time')

        Time.create(
            name=name,
            start_time=start_time or None,
            end_time=end_time or None,
            break_start_time=break_start_time or None,
            break_end_time=break_end_time or None,
        )
        return redirect(url_for('time.list'))

    return render_template('time_add.html')



@time_bp.route('/edit/<int:time_id>', methods=['GET', 'POST'])
def edit(time_id):
    time = Time.get_or_none(Time.id == time_id)
    if not time:
        return redirect(url_for('time.list'))

    if request.method == 'POST':
        time.name = request.form.get('name')
        time.start_time = request.form.get('start_time') or None
        time.end_time = request.form.get('end_time') or None
        time.break_start_time = request.form.get('break_start_time') or None
        time.break_end_time = request.form.get('break_end_time') or None
        time.save()
        return redirect(url_for('time.list'))

    return render_template('time_edit.html', time=time)
