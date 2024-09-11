// Define task array
let tasks = [];

// Load tasks from localStorage
function loadTasks() {
    const savedTasks = localStorage.getItem('tasks');
    if (savedTasks) {
        tasks = JSON.parse(savedTasks);
    }
    renderTasks();
}

// Save tasks to localStorage
function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Render tasks in the table
function renderTasks() {
    const taskList = document.getElementById('task-list');
    taskList.innerHTML = '';
    tasks.forEach((task, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${task.text}</td>
            <td>${task.completed ? 'Completed' : 'Pending'}</td>
            <td>${task.dueDate}</td>
            <td>${task.priority}</td>
            <td>
                <button class="complete" onclick="toggleTask(${index})">${task.completed ? 'Undo' : 'Complete'}</button>
                <button class="delete" onclick="deleteTask(${index})">Delete</button>
            </td>
        `;
        taskList.appendChild(row);
    });
}

// Add a new task
function addTask(event) {
    event.preventDefault();
    const taskInput = document.getElementById('task-input');
    const dueDateInput = document.getElementById('due-date-input');
    const priorityInput = document.getElementById('priority-input');

    if (taskInput.value.trim() === '') return;

    const newTask = {
        text: taskInput.value.trim(),
        dueDate: dueDateInput.value,
        priority: priorityInput.value,
        completed: false,
    };

    tasks.push(newTask);
    saveTasks();
    renderTasks();

    // Clear input fields
    taskInput.value = '';
    dueDateInput.value = '';
    priorityInput.value = 'Medium';
}

// Toggle task completion status
function toggleTask(index) {
    tasks[index].completed = !tasks[index].completed;
    saveTasks();
    renderTasks();
}

// Delete a task
function deleteTask(index) {
    tasks.splice(index, 1);
    saveTasks();
    renderTasks();
}

// Handle navigation
function handleNavigation(event) {
    event.preventDefault();
    const targetId = event.target.id;

    switch (targetId) {
        case 'home-btn':
            window.location.href = '/'; // Home page URL
            break;
        case 'add-task-btn':
            document.querySelector('main').innerHTML = `
                <form id="task-form">
                    <input type="text" id="task-input" placeholder="New Task" required>
                    <input type="date" id="due-date-input" required>
                    <select id="priority-input">
                        <option value="High">High</option>
                        <option value="Medium">Medium</option>
                        <option value="Low">Low</option>
                    </select>
                    <button type="submit">Add Task</button>
                </form>
                <table>
                    <thead>
                        <tr>
                            <th>Tasks</th>
                            <th>Status</th>
                            <th>Due Date</th>
                            <th>Priority</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="task-list">
                        <!-- Task rows will be added here dynamically -->
                    </tbody>
                </table>
            `;
            document.getElementById('task-form').addEventListener('submit', addTask);
            loadTasks();
            break;
        case 'delete-task-btn':
            document.querySelector('main').innerHTML = `
                <h2>Delete Tasks</h2>
                <p>Select a task to delete.</p>
                <!-- Implementation for deleting tasks can be added here -->
            `;
            break;
        case 'completed-task-btn':
            document.querySelector('main').innerHTML = `
                <h2>Completed Tasks</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Tasks</th>
                            <th>Status</th>
                            <th>Due Date</th>
                            <th>Priority</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="completed-task-list">
                        <!-- Completed task rows will be added here dynamically -->
                    </tbody>
                </table>
            `;
            const completedTasks = tasks.filter(task => task.completed);
            const completedTaskList = document.getElementById('completed-task-list');
            completedTasks.forEach((task, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${task.text}</td>
                    <td>${task.completed ? 'Completed' : 'Pending'}</td>
                    <td>${task.dueDate}</td>
                    <td>${task.priority}</td>
                `;
                completedTaskList.appendChild(row);
            });
            break;
        default:
            console.log('Unknown button clicked');
    }
}

// Attach event listeners
document.getElementById('home-btn').addEventListener('click', handleNavigation);
document.getElementById('add-task-btn').addEventListener('click', handleNavigation);
document.getElementById('delete-task-btn').addEventListener('click', handleNavigation);
document.getElementById('completed-task-btn').addEventListener('click', handleNavigation);

document.getElementById('task-form').addEventListener('submit', addTask);
document.addEventListener('DOMContentLoaded', loadTasks);

