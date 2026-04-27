import { useState, useEffect } from 'react'
import './App.css'

type Task = {
  id: number;
  title: string;
  completed: boolean;
};

function App() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [input, setInput] = useState("");
    const [showError, setShowError] = useState(false)

    useEffect(() => {
        const fetchTasks = async () => {
            const res = await fetch("http://localhost:8000/tasks");
            const data = await res.json();
            setTasks(data);
        };

        fetchTasks();
    }, []);

    const addTask = async () => {
        if (!input.trim()) {
            setShowError(true);
            setTimeout(() => setShowError(false), 3000);
            return;
        }

        const res = await fetch("http://localhost:8000/tasks", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title: input })
        });

        const newTask: Task = await res.json();
        setTasks(prev => [...prev, newTask]);
        setInput("")
        console.log(tasks);
    };

    const update_task = async (taskId: number) => {
        const res = await fetch(`http://localhost:8000/tasks/${taskId}`, {
            method: "PUT",
        });

        const updatedTask: Task = await res.json();

        setTasks(prev =>
            prev.map(task => task.id === taskId ? updatedTask : task)
        );
        console.log(tasks);
    };

    const delete_task = async (taskId: number) => {
        await fetch(`http://localhost:8000/tasks/${taskId}`, {
            method: "DELETE",
        });

        setTasks(prev => prev.filter(task => task.id !== taskId));
        console.log(tasks);
    };


    return (
        <div className="app">
            <h1>Todo List</h1>

            <div className="input-row">
                <input
                value={input}
                onChange={(e) => {
                    setInput(e.target.value);
                    if (showError) setShowError(false);
                }}
                placeholder="Add a task..."
                />
                <button onClick={addTask}>Add</button>
            </div>

            {showError && (
                <div className="error-popup">
                    ⚠️ No text added — please enter a task first.
                </div>
            )}

            <div className="task-list">
                {tasks.filter(task => task.id != null).map(task => (
                <div key={task.id} className="task">
                    <span className={task.completed ? "completed" : ""}>
                    {task.title}
                    </span>
 
                    <button onClick={() => update_task(task.id)}>✓</button>
                    <button onClick={() => delete_task(task.id)}>X</button>
                </div>
                ))}
            </div>
        </div>
    );
}



export default App
