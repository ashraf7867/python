from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Initialize Flask app with better configuration
app = Flask(__name__)

# Configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))

app.config.from_object(Config)

# Setup logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/taskmanager.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Task Manager startup')

# In-memory storage for demo (use a database in production)
tasks = []
task_id_counter = 1

@app.route('/')
def home():
    """Home page displaying all tasks"""
    try:
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        app.logger.error(f'Error in home route: {str(e)}')
        flash('An error occurred while loading tasks.', 'error')
        return render_template('index.html', tasks=[])

@app.route('/add_task', methods=['POST'])
def add_task():
    """Add a new task"""
    global task_id_counter
    
    try:
        task_text = request.form.get('task', '').strip()
        if not task_text:
            flash('Please enter a task!', 'error')
            return redirect(url_for('home'))
        
        if len(task_text) > 200:
            flash('Task is too long! Maximum 200 characters.', 'error')
            return redirect(url_for('home'))
        
        new_task = {
            'id': task_id_counter,
            'text': task_text,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        tasks.append(new_task)
        task_id_counter += 1
        
        app.logger.info(f'Task added: {task_text}')
        flash('Task added successfully!', 'success')
        
    except Exception as e:
        app.logger.error(f'Error adding task: {str(e)}')
        flash('An error occurred while adding the task.', 'error')
    
    return redirect(url_for('home'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    """Mark a task as completed"""
    try:
        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = True
                app.logger.info(f'Task completed: {task["text"]}')
                flash('Task completed!', 'success')
                break
        else:
            flash('Task not found!', 'error')
    except Exception as e:
        app.logger.error(f'Error completing task {task_id}: {str(e)}')
        flash('An error occurred while completing the task.', 'error')
    
    return redirect(url_for('home'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    """Delete a task"""
    global tasks
    try:
        original_length = len(tasks)
        tasks = [task for task in tasks if task['id'] != task_id]
        
        if len(tasks) < original_length:
            app.logger.info(f'Task deleted: ID {task_id}')
            flash('Task deleted!', 'info')
        else:
            flash('Task not found!', 'error')
            
    except Exception as e:
        app.logger.error(f'Error deleting task {task_id}: {str(e)}')
        flash('An error occurred while deleting the task.', 'error')
    
    return redirect(url_for('home'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/tasks')
def api_tasks():
    """API endpoint to get tasks as JSON"""
    try:
        return jsonify({
            'tasks': tasks,
            'total': len(tasks),
            'completed': len([t for t in tasks if t['completed']]),
            'pending': len([t for t in tasks if not t['completed']])
        })
    except Exception as e:
        app.logger.error(f'Error in API endpoint: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Run the app
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )