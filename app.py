from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# In-memory storage for demo (use a database in production)
tasks = []
task_id_counter = 1

@app.route('/')
def home():
    """Home page displaying all tasks"""
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    """Add a new task"""
    global task_id_counter
    
    task_text = request.form.get('task')
    if task_text:
        new_task = {
            'id': task_id_counter,
            'text': task_text,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        tasks.append(new_task)
        task_id_counter += 1
        flash('Task added successfully!', 'success')
    else:
        flash('Please enter a task!', 'error')
    
    return redirect(url_for('home'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    """Mark a task as completed"""
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            flash('Task completed!', 'success')
            break
    return redirect(url_for('home'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    """Delete a task"""
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    flash('Task deleted!', 'info')
    return redirect(url_for('home'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/tasks')
def api_tasks():
    """API endpoint to get tasks as JSON"""
    return {'tasks': tasks, 'total': len(tasks)}

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create static directory for CSS/JS if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Run the app in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)
