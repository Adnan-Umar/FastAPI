// API base — the FastAPI server. Change this if you deploy elsewhere.
const API_BASE = 'http://127.0.0.1:8000'

export async function getHome() {
  const res = await fetch(`${API_BASE}/`)
  if (!res.ok) throw new Error(`GET / failed: ${res.status}`)
  return res.json()
}

export async function getTodos() {
  const res = await fetch(`${API_BASE}/todos`)
  if (!res.ok) throw new Error(`GET /todos failed: ${res.status}`)
  return res.json()
}

export async function addTodo(title) {
  const res = await fetch(`${API_BASE}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, done: false }),
  })
  if (!res.ok) throw new Error(`POST /todos failed: ${res.status}`)
  return res.json()
}
