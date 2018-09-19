const json = response => response.json()
const text = response => response.text()

const host = 'http://localhost:5000'
const url = path => `${host}/${path}`

const init = () => fetch(url('init')).then(json)
const info = () => fetch(url('info')).then(json)
const step = () => fetch(url('step')).then(text)
const content = content_id => fetch(url(`content/${content_id}`)).then(json)
const difficulty = difficulty => fetch(url(`difficulty/${difficulty}`))

export default {
  init,
  info,
  step,
  content,
  difficulty,
}
