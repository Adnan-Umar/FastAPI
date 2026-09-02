import { useState } from 'react'
import { getHome, getTodos, addTodo } from './api.js'

export default function App() {
  const [home, setHome] = useState(null)
  const [todos, setTodos] = useState([])
  const [newTitle, setNewTitle] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function call(fn, successMsg) {
    setError('')
    setBusy(true)
    try {
      const data = await fn()
      return data
    } catch (e) {
      setError(e.message)
      return null
    } finally {
      setBusy(false)
    }
  }

  const onPing = async () => {
    const data = await call(getHome)
    if (data) setHome(data)
  }

  const onLoadTodos = async () => {
    const data = await call(getTodos)
    if (data) setTodos(data.todos ?? [])
  }

  const onAddTodo = async (e) => {
    e.preventDefault()
    if (!newTitle.trim()) return
    const data = await call(() => addTodo(newTitle.trim()))
    if (data) {
      setNewTitle('')
      await onLoadTodos()
    }
  }

  return (
    <div className="app">
      <h1>🌐 A025 — CORS Demo</h1>
      <p className="subtitle">
        React at <code>localhost:5173</code> talking to FastAPI at{' '}
        <code>127.0.0.1:8000</code>. If CORS works, no errors.
      </p>

      <div className="card">
        <h2>1. Ping the API</h2>
        <button onClick={onPing} disabled={busy}>
          GET /
        </button>
        {home && <pre>{JSON.stringify(home, null, 2)}</pre>}
      </div>

      <div className="card">
        <h2>2. Load todos</h2>
        <button onClick={onLoadTodos} disabled={busy}>
          GET /todos
        </button>
        {todos.length > 0 && (
          <ul className="todos">
            {todos.map((t) => (
              <li key={t.id}>
                {t.done ? '✅' : '⬜'} {t.title}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="card">
        <h2>3. Add a todo</h2>
        <form onSubmit={onAddTodo}>
          <input
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Buy milk"
          />
          <button type="submit" disabled={busy || !newTitle.trim()}>
            POST /todos
          </button>
        </form>
      </div>

      {error && <p className="error">⚠️ {error}</p>}
    </div>
  )
}
