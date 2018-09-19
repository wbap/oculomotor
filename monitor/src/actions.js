import api from './api'

const wrapDispatch = (f, dispatch) => arg => dispatch(f(arg))

export const init = () => dispatch => api.init().then(wrapDispatch(setInfo, dispatch))
export const info = () => dispatch => api.info().then(wrapDispatch(setInfo, dispatch))

export const setInfo = ({ content_range, content, difficulty_range, difficulty }) => dispatch => {
  dispatch(setContentRange(content_range))
  dispatch(setContent(content))
  dispatch(setDifficultyRange(difficulty_range))
  dispatch(setDifficulty(difficulty))
}

export const setContent = value => ({ type: 'SET_CONTENT', value })
export const setContentRange = range => ({ type: 'SET_CONTENT_RANGE', range })
export const setDifficulty = value => ({ type: 'SET_DIFFICULTY', value })
export const setDifficultyRange = range => ({ type: 'SET_DIFFICULTY_RANGE', range })

export const sendContent = value => dispatch => {
  dispatch(setContent(value))
  api.content(value).then(({ difficulty_range, difficulty }) => {
    dispatch(setDifficultyRange(difficulty_range))
    dispatch(setDifficulty(difficulty))
  })
}

export const sendDifficulty = value => dispatch => {
  dispatch(setDifficulty(value))
  api.difficulty(value)
}

const updateFrame = image => ({ type: 'UPDATE_FRAME', image })
export const stepAgent = () => dispatch => api.step().then(image => dispatch(updateFrame(image)))
