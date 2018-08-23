import { combineReducers } from 'redux'

const content = (state=0, action) => {
  switch (action.type) {
  case 'NEXT_CONTENT':
    return state + 1
  case 'PREV_CONTENT':
    return state - 1
  default:
    return state
  }
}

export default combineReducers({
  content,
})
