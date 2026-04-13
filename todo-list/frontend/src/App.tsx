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

    useEffect(() => {
        const fetchTasks = async () => {
            const res = await fetch("http://localhost:8000/tasks");
            const data = await res.json();
            setTasks(data);
        };

        fetchTasks();
    }, []);

    const addTask = async () => {
        await fetch("http://localhost:8000/tasks", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title: input })
        });

        const res = await fetch("http://localhost:8000/tasks");
        const data = await res.json();
        setTasks(data);
    };

    const update_task = async (taskId: number) => {
        const res = await fetch(`http://localhost:8000/tasks/${taskId}`, {
            method: "PUT",
        });

        const updatedTask: Task = await res.json();

        setTasks(prev =>
            prev.map(task =>
            task.id === taskId ? updatedTask : task
            )
        );
    };

    const delete_task = async (taskId: number) => {
        await fetch(`http://localhost:8000/tasks/${taskId}`, {
            method: "DELETE",
        });

        setTasks(prev => prev.filter(task => task.id !== taskId));
    };


    return (
        <div>
            <h1>Todo List</h1>
            <input onChange={(e) => setInput(e.target.value)} />
            <button onClick={addTask}>Add</button>

            {tasks.map(task => (
                <div key={task.id}>
                    <span style={{
                        textDecoration: task.completed ? "line-through" : "none"
                        }}>
                        {task.title}
                    </span>

                    <button onClick={() => update_task(task.id)}>✓</button>
                    <button onClick={() => delete_task(task.id)}>X</button>
                </div>
            ))}
        </div>
    );
}



export default App
