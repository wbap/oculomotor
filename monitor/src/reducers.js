import { combineReducers } from 'redux'

const content_id = (state=0, action) => {
  switch (action.type) {
  case 'NEXT_CONTENT':
    return state + 1
  case 'PREV_CONTENT':
    return state - 1
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
  content_id,
  frame,
})
