import { combineReducers } from 'redux'

const content = (state={value: 0, range: 0}, action) => {
  switch(action.type) {
    case 'SET_CONTENT':
      return {
        ...state,
        value: action.value,
      }
    case 'SET_CONTENT_RANGE':
      return {
        ...state,
        range: action.range,
      }
    default:
      return state
  }
}

const difficulty = (state={value: -1, range: 0}, action) => {
  switch(action.type) {
    case 'SET_DIFFICULTY':
      return {
        ...state,
        value: action.value,
      }
    case 'SET_DIFFICULTY_RANGE':
      return {
        ...state,
        range: action.range,
      }
    default:
      return state
  }
}

const frame = (state='', action) => {
  switch(action.type) {
  case 'UPDATE_FRAME':
      return action.image
  default:
    return state
  }
}

export default combineReducers({
  content,
  difficulty,
  frame,
})
